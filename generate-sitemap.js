#!/usr/bin/env node
/**
 * generate-sitemap.js
 * 生成 2 文件 sitemap 结构：
 *   - sitemap.xml     (sitemapindex → sitemap-0.xml)
 *   - sitemap-0.xml   (urlset，包含 7 语言 × 全部路由 + 逐 URL 的 hreflang)
 *
 * 多语言 URL 规则：
 *   en 用裸路径（/、/blog/、/blog/<slug>/）
 *   其它语言加 /zh/、/ja/、/ko/、/fr/、/de/、/es/ 前缀
 *
 * Run:  node generate-sitemap.js
 * Output: 写 ./public/ 并镜像到 ./dist/
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const SITE = 'https://toolbox168.xyz';

// 与 src/composables/useI18n.js 保持一致
const LOCALES = ['en', 'zh', 'ja', 'ko', 'fr', 'de', 'es'];
const DEFAULT_LOCALE = 'en';

// Priority & changefreq by URL type
const RULES = {
  home:      { priority: '1.0', changefreq: 'weekly'   },
  blogIndex: { priority: '0.9', changefreq: 'daily'    },
  tool:      { priority: '0.9', changefreq: 'monthly'  },
  batch:     { priority: '0.8', changefreq: 'monthly'  },
  faq:       { priority: '0.6', changefreq: 'monthly'  },
  static:    { priority: '0.5', changefreq: 'yearly'   },
  // blog posts - by category
  'How-To':       { priority: '0.9', changefreq: 'monthly' },
  Guide:          { priority: '0.8', changefreq: 'monthly' },
  Comparison:     { priority: '0.8', changefreq: 'monthly' },
  Data:           { priority: '0.7', changefreq: 'monthly' },
  History:        { priority: '0.7', changefreq: 'monthly' },
  Security:       { priority: '0.7', changefreq: 'monthly' },
};

function today() {
  return new Date().toISOString().slice(0, 10);
}

// 去前缀路径 → 某语言的完整 URL
function localeUrl(strippedPath, lang) {
  if (lang === DEFAULT_LOCALE) return `${SITE}${strippedPath}`;
  return `${SITE}/${lang}${strippedPath}`;
}

function main() {
  const postsPath = join(__dirname, 'src', 'blog', 'posts.json');
  if (!existsSync(postsPath)) {
    console.error('❌  src/blog/posts.json not found');
    process.exit(1);
  }
  const posts = JSON.parse(readFileSync(postsPath, 'utf-8'));
  const lastmod = today();

  // 3) 按语言拆成 7 个 urlset 文件（每个 < 50KB，规避 sitemap 单文件体积限制）
  const langFiles = {};
  for (const lang of LOCALES) {
    langFiles[lang] = [];
  }

  const pushUrl = (lang, strippedPath, lastmodVal, prio, freq) => {
    const loc = localeUrl(strippedPath, lang);
    const altLines = LOCALES
      .map((hl) => `    <xhtml:link rel="alternate" hreflang="${hl}" href="${localeUrl(strippedPath, hl)}"/>`)
      .join('\n');
    langFiles[lang].push(`  <url>
    <loc>${loc}</loc>
    <lastmod>${lastmodVal}</lastmod>
    <changefreq>${freq}</changefreq>
    <priority>${prio}</priority>
    <xhtml:link rel="alternate" hreflang="x-default" href="${localeUrl(strippedPath, DEFAULT_LOCALE)}"/>
${altLines}
  </url>`);
  };

  // 首页
  for (const lang of LOCALES) pushUrl(lang, '/', lastmod, RULES.home.priority, RULES.home.changefreq);
  // 批量生成独立页（/batch/）
  for (const lang of LOCALES) pushUrl(lang, '/batch/', lastmod, RULES.batch.priority, RULES.batch.changefreq);
  // 博客索引 + 静态页
  for (const lang of LOCALES) pushUrl(lang, '/blog/', lastmod, RULES.blogIndex.priority, RULES.blogIndex.changefreq);
  for (const p of ['privacy', 'terms', 'contact', 'about']) {
    for (const lang of LOCALES) pushUrl(lang, `/${p}/`, lastmod, RULES.static.priority, RULES.static.changefreq);
  }
  // 博客文章
  for (const post of posts) {
    const rule = RULES[post.category] || RULES.Guide;
    for (const lang of LOCALES) pushUrl(lang, `/blog/${post.slug}/`, post.date || lastmod, rule.priority, rule.changefreq);
  }

  // 4) 写 7 个 sitemap-<lang>.xml + sitemap.xml 索引
  const targets = [join(__dirname, 'public'), join(__dirname, 'dist')];
  const indexItems = [];
  const fileSizes = [];
  for (const lang of LOCALES) {
    const urlset = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
${langFiles[lang].join('\n')}
</urlset>
`;
    const fname = `sitemap-${lang}.xml`;
    for (const dir of targets) {
      if (existsSync(dir)) writeFileSync(join(dir, fname), urlset, 'utf-8');
    }
    indexItems.push(`  <sitemap>
    <loc>${SITE}/${fname}</loc>
    <lastmod>${lastmod}</lastmod>
  </sitemap>`);
    fileSizes.push(`${fname}: ${(urlset.length / 1024).toFixed(1)} KB`);
  }

  const index = `<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${indexItems.join('\n')}
</sitemapindex>
`;

  let totalWritten = 0;
  for (const dir of targets) {
    if (!existsSync(dir)) {
      console.warn(`⚠️   ${dir} not found, skipping`);
      continue;
    }
    writeFileSync(join(dir, 'sitemap.xml'), index, 'utf-8');
    totalWritten++;
  }

  const urlCount = langFiles[LOCALES[0]].length * LOCALES.length;
  console.log(`✅  sitemap generated (${totalWritten} location${totalWritten === 1 ? '' : 's'})`);
  console.log(`    ${urlCount} URLs = 38 路由 × ${LOCALES.length} 语言`);
  console.log(`    ${fileSizes.length} 个分文件，每个 < 50 KB`);
  for (const s of fileSizes) console.log(`      ${s}`);
}

main();