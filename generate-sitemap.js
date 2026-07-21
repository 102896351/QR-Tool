#!/usr/bin/env node
/**
 * generate-sitemap.js
 * Generates 2-file sitemap structure (matches gonglue.xyz convention):
 *   - sitemap.xml      (sitemapindex, points to sitemap-0.xml)
 *   - sitemap-0.xml    (single urlset, all 25 URLs + 7-language hreflang)
 *
 * Why 2 files:
 *   - Avoids "child sitemap 404" failure mode (Google stops processing the
 *     whole index if any child is broken)
 *   - Single urlset file is ~20KB, well under the 50KB per-file limit
 *   - Same naming convention as gonglue.xyz reference
 *
 * Run:  node generate-sitemap.js
 * Output: writes to ./public/ AND mirrors to ./dist/
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const SITE = 'https://toolbox168.xyz';

// 7 languages + x-default (matches the i18n in src/composables/locales/)
const HREFLANGS = ['en', 'zh', 'ja', 'ko', 'fr', 'de', 'es'];

// Priority & changefreq by URL type
const RULES = {
  home:      { priority: '1.0', changefreq: 'weekly'   },
  blogIndex: { priority: '0.9', changefreq: 'daily'    },
  tool:      { priority: '0.9', changefreq: 'monthly'  },
  batch:     { priority: '0.8', changefreq: 'monthly'  },
  faq:       { priority: '0.6', changefreq: 'monthly'  },
  // blog posts - by category
  'How-To':       { priority: '0.9', changefreq: 'monthly' },
  Guide:          { priority: '0.8', changefreq: 'monthly' },
  Comparison:     { priority: '0.8', changefreq: 'monthly' },
  Data:           { priority: '0.7', changefreq: 'monthly' },
  History:        { priority: '0.7', changefreq: 'monthly' },
  Security:       { priority: '0.7', changefreq: 'monthly' },
};

function today() {
  const d = new Date();
  return d.toISOString().slice(0, 10);
}

function urlBlock(loc, lastmod, priority, changefreq) {
  const altLines = HREFLANGS
    .map((hl) => `    <xhtml:link rel="alternate" hreflang="${hl}" href="${loc}"/>`)
    .join('\n');
  return `  <url>
    <loc>${loc}</loc>
    <lastmod>${lastmod}</lastmod>
    <changefreq>${changefreq}</changefreq>
    <priority>${priority}</priority>
    <xhtml:link rel="alternate" hreflang="x-default" href="${loc}"/>
${altLines}
  </url>`;
}

function main() {
  // 1) Read posts.json
  const postsPath = join(__dirname, 'src', 'blog', 'posts.json');
  if (!existsSync(postsPath)) {
    console.error('❌  src/blog/posts.json not found');
    process.exit(1);
  }
  const posts = JSON.parse(readFileSync(postsPath, 'utf-8'));
  const lastmod = today();

  // 2) Build all URL entries
  const blocks = [];

  // Home page
  blocks.push(urlBlock(`${SITE}/`, lastmod, RULES.home.priority, RULES.home.changefreq));

  // Anchor routes (single-page sections)
  blocks.push(urlBlock(`${SITE}/#blog`,     lastmod, RULES.blogIndex.priority, RULES.blogIndex.changefreq));
  blocks.push(urlBlock(`${SITE}/#generator`, lastmod, RULES.tool.priority,     RULES.tool.changefreq));
  blocks.push(urlBlock(`${SITE}/#batch`,     lastmod, RULES.batch.priority,    RULES.batch.changefreq));
  blocks.push(urlBlock(`${SITE}/#faq`,       lastmod, RULES.faq.priority,      RULES.faq.changefreq));

  // Blog posts
  for (const post of posts) {
    const rule = RULES[post.category] || RULES.Guide;
    blocks.push(urlBlock(
      `${SITE}/#blog/${post.slug}`,
      post.date || lastmod,
      rule.priority,
      rule.changefreq,
    ));
  }

  // 3) Compose sitemap-0.xml (single urlset with everything)
  const urlset = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
${blocks.join('\n')}
</urlset>
`;

  // 4) Compose sitemap.xml (sitemapindex, single child)
  const index = `<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>${SITE}/sitemap-0.xml</loc>
    <lastmod>${lastmod}</lastmod>
  </sitemap>
</sitemapindex>
`;

  // 5) Write to both public/ and dist/
  const targets = [
    join(__dirname, 'public'),
    join(__dirname, 'dist'),
  ];

  let totalWritten = 0;
  for (const dir of targets) {
    if (!existsSync(dir)) {
      console.warn(`⚠️   ${dir} not found, skipping`);
      continue;
    }
    writeFileSync(join(dir, 'sitemap-0.xml'), urlset, 'utf-8');
    writeFileSync(join(dir, 'sitemap.xml'), index, 'utf-8');
    totalWritten++;
  }

  // 6) Summary
  const urlCount = blocks.length;
  const sizeKB = (urlset.length / 1024).toFixed(1);
  console.log(`✅  sitemap generated (${totalWritten} location${totalWritten === 1 ? '' : 's'})`);
  console.log(`    ${urlCount} URLs (1 home + 4 anchors + ${posts.length} blog posts)`);
  console.log(`    sitemap-0.xml: ${sizeKB} KB (limit 50 KB)`);
  console.log(`    hreflangs: ${HREFLANGS.length} languages + x-default per URL`);
}

main();
