#!/usr/bin/env node
/**
 * copy-404-fallback.js
 * Copies dist/index.html → dist/404.html so GitHub Pages serves the SPA
 * for any unmatched path (history-mode routing fallback).
 *
 * How it works:
 *   - GitHub Pages returns 404.html (when present) for any URL that doesn't
 *     match a physical file. Since 404.html is identical to index.html,
 *     the browser loads the SPA, which then parses window.location.pathname
 *     and routes to the correct view.
 *   - Note: this works for custom-domain sites (cname). For default
 *     102896351.github.io/QR-Tool/ URLs, GitHub Pages may show its own
 *     404 page; the real solution is real per-URL HTML files.
 *
 * If you'd rather generate real per-URL files, swap this for a prerender
 * step that emits dist/blog/<slug>/index.html for each post.
 */
import { copyFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// repo root = parent of scripts/
const root = join(__dirname, '..');
const indexHtml = join(root, 'dist', 'index.html');
const fallbackHtml = join(root, 'dist', '404.html');

if (!existsSync(indexHtml)) {
  console.error('❌  dist/index.html not found (run vite build first)');
  process.exit(1);
}

copyFileSync(indexHtml, fallbackHtml);
console.log(`✅  Copied index.html → 404.html (SPA fallback for history routing)`);