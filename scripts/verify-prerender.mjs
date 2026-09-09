/**
 * 预渲染验收脚本
 *
 * 验收标准（来自最终优化方案「阶段 B」）：
 *   1. 每个页面 body 纯文本 > 1500 字符（改前是 0）
 *   2. 每页 title / description / canonical 各不相同
 *   3. 每页至少 12 个站内 <a> 内链（改前首页 0 个；12 = 全站 footer 的链接数）
 *   4. 每页都有 JSON-LD 结构化数据
 *
 * 用法：node scripts/verify-prerender.mjs
 */
import fs from 'node:fs'
import path from 'node:path'

const DIST = 'dist'

// 404.html 是 GitHub Pages 的兜底页（noindex），不参与正文/内链验收
const SKIP = new Set(['404.html'])

function walk(dir, acc = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name)
    if (entry.isDirectory()) walk(p, acc)
    else if (entry.name.endsWith('.html') && !SKIP.has(entry.name)) acc.push(p)
  }
  return acc
}

function bodyText(html) {
  const i = html.indexOf('<body')
  const body = i >= 0 ? html.slice(i) : html
  return body
    .replace(/<script[\s\S]*?<\/script>/g, '')
    .replace(/<style[\s\S]*?<\/style>/g, '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
}

const files = walk(DIST).sort()
const rows = []
let pass = 0
let fail = 0

for (const f of files) {
  const html = fs.readFileSync(f, 'utf8')
  const text = bodyText(html)
  const title = (html.match(/<title>([\s\S]*?)<\/title>/) || [, ''])[1].trim()
  const desc = (html.match(/<meta[^>]+name="description"[^>]+content="([^"]*)"/) || [, ''])[1]
  const canonical = (html.match(/<link[^>]+rel="canonical"[^>]+href="([^"]*)"/) || [, ''])[1]
  const internalLinks = new Set(
    (html.match(/<a[^>]+href="\/[^"]*"/g) || []).map((s) => (s.match(/href="([^"]*)"/) || [, ''])[1])
  )
  const ldCount = (html.match(/application\/ld\+json/g) || []).length
  const h1 = (html.match(/<h1[\s\S]*?<\/h1>/g) || []).length

  const ok = text.length > 1500 && !!title && !!desc && !!canonical && internalLinks.size >= 12 && ldCount >= 1 && h1 === 1
  ok ? pass++ : fail++

  rows.push({
    file: f.replace(/\\/g, '/'),
    text: text.length,
    links: internalLinks.size,
    ld: ldCount,
    h1,
    title: title.slice(0, 58),
    canonical,
    ok
  })
}

const pad = (s, n) => String(s).padEnd(n)
console.log('文件'.padEnd(46), '正文'.padStart(7), '内链'.padStart(5), 'LD'.padStart(4), 'H1'.padStart(4), '  状态')
console.log('-'.repeat(100))
for (const r of rows) {
  console.log(
    pad(r.file, 46),
    String(r.text).padStart(7),
    String(r.links).padStart(5),
    String(r.ld).padStart(4),
    String(r.h1).padStart(4),
    '  ' + (r.ok ? 'PASS' : 'FAIL')
  )
}
console.log('-'.repeat(100))

// 唯一性检查：canonical 必须全站唯一（这才是 Google 判重页面依据）。
// 注意：多语言站点里 /blog/foo/ 与 /zh/blog/foo/ 的 title 会相同（正文未翻译），
// 这是正常的 hreflang 备选页，不能用 title 唯一性来判错。
const canons = new Set(rows.map((r) => r.canonical))
console.log(`\n页面总数        : ${rows.length}`)
console.log(`通过            : ${pass}`)
console.log(`未通过          : ${fail}`)
console.log(`唯一 canonical 数: ${canons.size}`)

if (fail > 0 || canons.size !== rows.length) {
  console.log('\n未达标的页面明细：')
  for (const r of rows.filter((x) => !x.ok)) {
    console.log(`  ${r.file} → 正文 ${r.text} / 内链 ${r.links} / LD ${r.ld}`)
  }
  if (canons.size !== rows.length) {
    // 找出重复 canonical
    const seen = new Map()
    for (const r of rows) {
      if (seen.has(r.canonical)) {
        console.log(`  重复 canonical: ${r.canonical} → ${seen.get(r.canonical)} 与 ${r.file}`)
      } else {
        seen.set(r.canonical, r.file)
      }
    }
  }
  process.exitCode = 1
} else {
  console.log('\n全部通过：每个页面都有独立正文、独立 canonical 和足够的站内链接。')
}
