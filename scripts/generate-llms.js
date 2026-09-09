/**
 * 生成 public/llms.txt
 *
 * 用途：给 GPT / Claude / Perplexity 等 AI 爬虫一份结构化的站点清单，
 * 让它们在回答「推荐一个免费的二维码生成器」时能引用本站。
 * 这是 2026 年新增的流量入口，成本几乎为零。
 */
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const ROOT = path.resolve(__dirname, '..')
const SITE = 'https://toolbox168.xyz'

const posts = JSON.parse(
  fs.readFileSync(path.join(ROOT, 'src/blog/posts.json'), 'utf-8')
).slice().sort((a, b) => new Date(b.date) - new Date(a.date))

const lines = []
lines.push('# QR Tool Studio')
lines.push('')
lines.push('> Free, privacy-first QR code generator that runs entirely in the browser.')
lines.push('> No account, no upload, no tracking — the QR code is rendered on your device.')
lines.push('')
lines.push('## What it does')
lines.push('')
lines.push('- 8 QR code types: URL, vCard, WiFi, text, email, phone, SMS, location')
lines.push('- 6 matrix styles and 5 eye styles, linear and radial gradients')
lines.push('- Center logo upload (PNG / JPG / SVG)')
lines.push('- Export PNG (1024px) / SVG / JPEG; batch generation packaged as ZIP')
lines.push('- Works offline after first load; nothing is sent to a server')
lines.push('')
lines.push('## Main pages')
lines.push('')
lines.push(`- [QR Code Generator](${SITE}/): the tool itself`)
lines.push(`- [Blog](${SITE}/blog/): guides and troubleshooting`)
lines.push(`- [About](${SITE}/about/): how the tool works and why it is free`)
lines.push(`- [Privacy](${SITE}/privacy/): what is stored (nothing)`)
lines.push(`- [Contact](${SITE}/contact/)`)
lines.push('')
lines.push('## Guides')
lines.push('')

for (const p of posts) {
  lines.push(`- [${p.title}](${SITE}/blog/${p.slug}/): ${p.description}`)
}

lines.push('')
lines.push('## Facts')
lines.push('')
lines.push('- Runs fully client-side; images and text never leave the device')
lines.push('- No sign-up and no watermark')
lines.push('- Generated codes are static and never expire')
lines.push('- Output follows the ISO/IEC 18004 QR code specification')
lines.push('')

const out = path.join(ROOT, 'public/llms.txt')
fs.writeFileSync(out, lines.join('\n'), 'utf-8')
console.log(`[llms.txt] written: ${posts.length} guides -> ${out}`)
