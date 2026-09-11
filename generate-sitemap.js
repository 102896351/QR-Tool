#!/usr/bin/env node
/**
 * generate-sitemap.js
 * 双层 sitemap（与 gonglue.xyz / aiartspell.art 同款结构）：
 *   - sitemap-index.xml  (sitemapindex，极小，约 150 字节 —— GSC 提交这个)
 *   - sitemap-0.xml      (urlset，7 语言 × 全部路由，每条 URL 带 hreflang 备用链接)
 *
 * 为什么用 index 层（而不是单文件 sitemap.xml 直接提交）：
 *   GSC 实际读取的是 sitemap-index.xml（~150 字节），Cloudflare/Fastly 代理链
 *   对极小文件稳定返回 Transfer-Encoding: chunked（无 Content-Length 冲突），
 *   再由 GSC 二级拉取 sitemap-0.xml（266 条，271KB）。这样避免了「直接提交大单
 *   文件时偶发响应头错配 → GSC 判无法读取」的情况。两个参考站点（同在
 *   Cloudflare + GitHub Pages 下）均验证此结构可正常被 GSC 收录。
 *
 * 多语言 URL 规则：
 *   en 用裸路径（/、/blog/、/blog/<slug>/）
 *   其它语言加 /zh/、/ja/、/ko/、/fr/、/de/、/es/ 前缀
 *
 * Run:  node generate-sitemap.js
 * Output: 写 ./public/ 并镜像到 ./dist/
 */

import { readFileSync, writeFileSync, existsSync } from 'node:fs';
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
  batch:     { priority: '0.8', changefreq: 'monthly'  },
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

  // 1) 收集全部路由（去语言前缀的 stripped path + 元信息）
  const routes = [];
  routes.push({ path: '/', lastmod, ...RULES.home });
  routes.push({ path: '/batch/', lastmod, ...RULES.batch });
  routes.push({ path: '/blog/', lastmod, ...RULES.blogIndex });
  for (const p of ['privacy', 'terms', 'contact', 'about']) {
    routes.push({ path: `/${p}/`, lastmod, ...RULES.static });
  }
  for (const post of posts) {
    const rule = RULES[post.category] || RULES.Guide;
    routes.push({
      path: `/blog/${post.slug}/`,
      lastmod: post.date || lastmod,
      priority: rule.priority,
      changefreq: rule.changefreq,
    });
  }

  // 2) 展开成 7 语言 × 路由 的全部 URL，每个 URL 带完整 hreflang 备用链接
  const urlBlocks = [];
  for (const r of routes) {
    const altLines = LOCALES
      .map((hl) => `    <xhtml:link rel="alternate" hreflang="${hl}" href="${localeUrl(r.path, hl)}"/>`)
      .join('\n');
    for (const lang of LOCALES) {
      const loc = localeUrl(r.path, lang);
      urlBlocks.push(`  <url>
    <loc>${loc}</loc>
    <lastmod>${r.lastmod}</lastmod>
    <changefreq>${r.changefreq}</changefreq>
    <priority>${r.priority}</priority>
    <xhtml:link rel="alternate" hreflang="x-default" href="${localeUrl(r.path, DEFAULT_LOCALE)}"/>
${altLines}
  </url>`);
    }
  }

  // 3) urlset 本体 → sitemap-0.xml
  const urlset = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
${urlBlocks.join('\n')}
</urlset>
`;

  // 4) 极小的索引文件 → sitemap-index.xml（GSC 提交这个）
  const index = `<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>${SITE}/sitemap-0.xml</loc>
    <lastmod>${lastmod}</lastmod>
  </sitemap>
</sitemapindex>
`;

  const targets = [join(__dirname, 'public'), join(__dirname, 'dist')];
  let written = 0;
  for (const dir of targets) {
    if (!existsSync(dir)) {
      console.warn(`⚠️   ${dir} not found, skipping`);
      continue;
    }
    writeFileSync(join(dir, 'sitemap-0.xml'), urlset, 'utf-8');
    writeFileSync(join(dir, 'sitemap-index.xml'), index, 'utf-8');
    written++;
  }

  console.log(`✅  双层 sitemap 生成完成（写入 ${written} 个目录）`);
  console.log(`    ${urlBlocks.length} 条 URL = ${routes.length} 路由 × ${LOCALES.length} 语言`);
  console.log(`    sitemap-0.xml   : ${urlset.length} 字节（urlset 本体）`);
  console.log(`    sitemap-index.xml: ${index.length} 字节（索引，提交给 GSC）`);
  console.log(`    robots.txt 的 Sitemap: 改为指向 /sitemap-index.xml`);
}

main();
