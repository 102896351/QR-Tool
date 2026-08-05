#!/usr/bin/env node
/**
 * prerender-blog.js
 *
 * Pre-renders one HTML file per route so each URL is a real, crawlable file
 * on disk (no SPA fallback needed). Runs AFTER vite build.
 *
 * For each route below, this script:
 *   1. Reads dist/index.html
 *   2. Rewrites every absolute URL "/..." → relative "../" or "./" so the
 *      file works when opened from its subdirectory
 *   3. Updates <title>, <meta description>, <link rel="canonical">, og:url,
 *      og:title, og:description, og:image, twitter:* to match the route
 *   4. Inserts a BlogPosting JSON-LD for blog posts
 *   5. Writes dist/<route>/index.html
 *
 * Why this works:
 *   - dist/index.html is the Vite SPA shell. The same shell, plus the right
 *     <head> meta, is what crawlers need.
 *   - For blog posts we ALSO patch the meta to match the post (title,
 *     description, canonical, og:image = post.cover).
 *   - The actual Vue app still mounts and hydrates on first visit, so
 *     interactivity is unchanged.
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join, dirname, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const root = join(__dirname, '..');
const distDir = join(root, 'dist');
const SITE = 'https://toolbox168.xyz';

if (!existsSync(join(distDir, 'index.html'))) {
  console.error('❌  dist/index.html not found (run vite build first)');
  process.exit(1);
}

const indexHtml = readFileSync(join(distDir, 'index.html'), 'utf-8');

// --- Routes to prerender (besides /index.html which is already there) ---
// Each: { routePath: '/blog', slug: '', outFile: 'dist/blog/index.html' }
const STATIC_ROUTES = [
  { route: '/blog',    outFile: join(distDir, 'blog', 'index.html') },
  { route: '/privacy', outFile: join(distDir, 'privacy', 'index.html') },
  { route: '/terms',   outFile: join(distDir, 'terms', 'index.html') },
  { route: '/contact', outFile: join(distDir, 'contact', 'index.html') },
  { route: '/about',   outFile: join(distDir, 'about', 'index.html') },
];

// --- Blog posts ---
const posts = JSON.parse(readFileSync(join(root, 'src', 'blog', 'posts.json'), 'utf-8'));

function makeRelative(html, route) {
  // Rewrite src="./assets/..." → "../../assets/..." for blog/<slug>/index.html
  // (depth = number of "/" segments in the route, minus 1 for the leading /)
  if (route === '/' || route === '') return html;
  const depth = route.split('/').filter(Boolean).length;
  const prefix = depth === 1 ? '../' : '../'.repeat(depth);
  return html
    .replace(/(href|src)="\.\/assets\//g, `$1="${prefix}assets/`)
    .replace(/(href|src)="\.\/favicon\.svg/g, `$1="${prefix}favicon.svg`)
    .replace(/(href|src)="\.\/og-image\.png/g, `$1="${prefix}og-image.png`);
}

function makeMeta(html, route, { title, description, image, type, jsonLd } = {}) {
  let out = html;
  if (title) {
    out = out.replace(/<title>[^<]*<\/title>/, `<title>${escapeHtml(title)}</title>`);
  }
  if (description) {
    out = out.replace(/<meta name="description" content="[^"]*"\s*\/?>/,
      `<meta name="description" content="${escapeHtml(description)}" />`);
    out = out.replace(/<meta property="og:description" content="[^"]*"\s*\/?>/,
      `<meta property="og:description" content="${escapeHtml(description)}" />`);
    out = out.replace(/<meta name="twitter:description" content="[^"]*"\s*\/?>/,
      `<meta name="twitter:description" content="${escapeHtml(description)}" />`);
  }
  if (title) {
    out = out.replace(/<meta property="og:title" content="[^"]*"\s*\/?>/,
      `<meta property="og:title" content="${escapeHtml(title)}" />`);
    out = out.replace(/<meta name="twitter:title" content="[^"]*"\s*\/?>/,
      `<meta name="twitter:title" content="${escapeHtml(title)}" />`);
  }
  if (image) {
    out = out.replace(/<meta property="og:image" content="[^"]*"\s*\/?>/,
      `<meta property="og:image" content="${escapeHtml(image)}" />`);
  }
  if (type) {
    out = out.replace(/<meta property="og:type" content="[^"]*"\s*\/?>/,
      `<meta property="og:type" content="${type}" />`);
  }
  // Canonical + og:url
  const canonicalUrl = `${SITE}${route}`;
  if (out.includes('rel="canonical"')) {
    out = out.replace(/<link rel="canonical" href="[^"]*"\s*\/?>/,
      `<link rel="canonical" href="${canonicalUrl}" />`);
  }
  if (out.includes('property="og:url"')) {
    out = out.replace(/<meta property="og:url" content="[^"]*"\s*\/?>/,
      `<meta property="og:url" content="${canonicalUrl}" />`);
  }
  // JSON-LD injection before </head>
  if (jsonLd) {
    const ldScript = `<script type="application/ld+json">${JSON.stringify(jsonLd)}</script>`;
    if (out.includes('</head>')) {
      out = out.replace('</head>', `${ldScript}\n  </head>`);
    }
  }
  return out;
}

function escapeHtml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function writeRoute(route, outFile, meta) {
  let html = makeRelative(indexHtml, route);
  html = makeMeta(html, route, meta);
  mkdirSync(dirname(outFile), { recursive: true });
  writeFileSync(outFile, html, 'utf-8');
  const sizeKB = (html.length / 1024).toFixed(1);
  console.log(`  ✓ ${route.padEnd(30)}  ${relative(distDir, outFile)}  (${sizeKB} KB)`);
}

console.log('Prerendering routes:');

for (const r of STATIC_ROUTES) {
  writeRoute(r.route, r.outFile, {
    title: routeTitle(r.route),
    description: routeDescription(r.route),
    type: 'website',
  });
}

for (const post of posts) {
  const route = `/blog/${post.slug}`;
  const outFile = join(distDir, 'blog', post.slug, 'index.html');
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: post.title,
    description: post.description,
    image: `${SITE}${post.cover}`,
    datePublished: post.date,
    author: { '@type': 'Organization', name: post.author },
    publisher: { '@type': 'Organization', name: 'QR Tool Studio' },
    mainEntityOfPage: { '@type': 'WebPage', '@id': `${SITE}${route}` },
  };
  writeRoute(route, outFile, {
    title: `${post.title} | QR Tool Studio`,
    description: post.description,
    image: `${SITE}${post.cover}`,
    type: 'article',
    jsonLd,
  });
}

console.log(`\n✅ Prerendered ${STATIC_ROUTES.length + posts.length} routes.`);

function routeTitle(route) {
  const map = {
    '/blog': 'Blog — QR Code Guides & Tips | QR Tool Studio',
    '/privacy': 'Privacy Policy | QR Tool Studio',
    '/terms': 'Terms of Service | QR Tool Studio',
    '/contact': 'Contact | QR Tool Studio',
    '/about': 'About | QR Tool Studio',
  };
  return map[route] || null;
}

function routeDescription(route) {
  const map = {
    '/blog': 'Practical, no-fluff guides to help you get the most out of QR codes. From small business use cases to design best practices.',
    '/privacy': 'Privacy policy for QR Tool Studio: what data we collect, how we use it, and how to contact us.',
    '/terms': 'Terms of service for QR Tool Studio.',
    '/contact': 'Contact QR Tool Studio for support, feedback, or partnership inquiries.',
    '/about': 'About QR Tool Studio — the free, privacy-first QR code generator.',
  };
  return map[route] || null;
}