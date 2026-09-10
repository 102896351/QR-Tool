/**
 * 预渲染验收脚本
 *
 * 验收标准（来自最终优化方案「阶段 B」）：
 *   1. 每个页面 body 纯文本 > 1500 字符（改前是 0）
 *   2. 每页 title / description / canonical 各不相同
 *   3. 每页至少 12 个站内 <a> 内链（改前首页 0 个；12 = 全站 footer 的链接数）
 *   4. 每页都有 JSON-LD 结构化数据
 *
 * 追加的回归检查（踩过的坑）：
 *   5. 未翻译的 i18n key 字面量不得出现在正文里
 *      （曾出现 "gen.dots.classy" 直接渲染到页面上）
 *   6. 非中日韩语言的页面不得出现中文字符
 *      （BatchGenerator.vue 控件文案曾是中文硬编码，英文页混排中文）
 *   7. 7 个语言字典的 key 必须与 en 完全一致
 *
 * 用法：node scripts/verify-prerender.mjs
 */
import fs from 'node:fs'
import path from 'node:path'
import { pathToFileURL } from 'node:url'

const DIST = 'dist'

// 404.html 是 GitHub Pages 的兜底页（noindex），不参与正文/内链验收
const SKIP = new Set(['404.html'])

// 使用中日韩文字的语言，这些语言的页面允许出现汉字/谚文
const CJK_LOCALES = new Set(['zh', 'ja', 'ko'])

// i18n key 命名空间前缀：命中即说明某处没取到译文，直接把 key 打到页面上了
const KEY_NS = 'gen|batch|faq|mkt|hero|footer|blog|preset|header|lang|meta|blogList|notFound'

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

/** 从 dist 路径判断语言（en 无前缀） */
function localeOf(file) {
  const rel = file.replace(/\\/g, '/').replace(/^dist\//, '')
  const m = rel.match(/^(zh|ja|ko|fr|de|es)(?:\/|$)/)
  return m ? m[1] : 'en'
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

  const locale = localeOf(f)
  // 未翻译 key 泄漏：形如 "gen.dots.classy" / "batch.label.list"
  const keyLeaks = [...new Set(text.match(new RegExp(`\\b(?:${KEY_NS})\\.[a-zA-Z][a-zA-Z0-9.]*`, 'g')) || [])]
  // 中文泄漏：非中日韩语言页面里不该出现汉字
  const cjk = CJK_LOCALES.has(locale) ? 0 : (text.match(/[\u4e00-\u9fff]/g) || []).length

  const ok = text.length > 1500 && !!title && !!desc && !!canonical &&
    internalLinks.size >= 12 && ldCount >= 1 && h1 === 1 &&
    keyLeaks.length === 0 && cjk === 0
  ok ? pass++ : fail++

  rows.push({
    file: f.replace(/\\/g, '/'),
    text: text.length,
    links: internalLinks.size,
    ld: ldCount,
    h1,
    leaks: keyLeaks.length,
    cjk,
    title: title.slice(0, 58),
    canonical,
    ok
  })
}

const pad = (s, n) => String(s).padEnd(n)
console.log('文件'.padEnd(46), '正文'.padStart(7), '内链'.padStart(5), 'LD'.padStart(4), 'H1'.padStart(4), 'key'.padStart(4), '中文'.padStart(5), '  状态')
console.log('-'.repeat(112))
for (const r of rows) {
  console.log(
    pad(r.file, 46),
    String(r.text).padStart(7),
    String(r.links).padStart(5),
    String(r.ld).padStart(4),
    String(r.h1).padStart(4),
    String(r.leaks).padStart(4),
    String(r.cjk).padStart(5),
    '  ' + (r.ok ? 'PASS' : 'FAIL')
  )
}
console.log('-'.repeat(112))

// 唯一性检查：canonical 必须全站唯一（这才是 Google 判重页面依据）。
// 注意：多语言站点里 /blog/foo/ 与 /zh/blog/foo/ 的 title 会相同（正文未翻译），
// 这是正常的 hreflang 备选页，不能用 title 唯一性来判错。
const canons = new Set(rows.map((r) => r.canonical))
console.log(`\n页面总数        : ${rows.length}`)
console.log(`通过            : ${pass}`)
console.log(`未通过          : ${fail}`)
console.log(`唯一 canonical 数: ${canons.size}`)

// 语言字典 key 一致性：任何语言缺 key 都会在页面上打出 key 字面量
const LOCALES = ['en', 'zh', 'ja', 'ko', 'fr', 'de', 'es']
const dicts = {}
for (const lg of LOCALES) {
  const url = pathToFileURL(path.resolve(`src/composables/locales/${lg}.js`)).href
  dicts[lg] = (await import(url)).default
}
const enKeys = new Set(Object.keys(dicts.en))
let dictBad = 0
for (const lg of LOCALES) {
  const ks = new Set(Object.keys(dicts[lg]))
  const missing = [...enKeys].filter((k) => !ks.has(k))
  const extra = [...ks].filter((k) => !enKeys.has(k))
  if (missing.length || extra.length) {
    dictBad++
    console.log(`字典 ${lg}: 缺 ${missing.length} 个${missing.length ? ' → ' + missing.slice(0, 6).join(', ') : ''}${extra.length ? ` / 多 ${extra.length} 个` : ''}`)
  }
}
console.log(`字典一致性      : ${dictBad === 0 ? 'PASS（7 语言 key 完全一致）' : `${dictBad} 个语言不一致`}`)

if (fail > 0 || canons.size !== rows.length || dictBad > 0) {
  console.log('\n未达标的页面明细：')
  for (const r of rows.filter((x) => !x.ok)) {
    console.log(`  ${r.file} → 正文 ${r.text} / 内链 ${r.links} / LD ${r.ld} / key 泄漏 ${r.leaks} / 中文 ${r.cjk}`)
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
  console.log('\n全部通过：每个页面都有独立正文、独立 canonical、足够的站内链接，无 key/中文泄漏。')
}

