import { useHead } from '@unhead/vue'
import { SITE } from '../config.js'
import { SUPPORTED, DEFAULT_LOCALE } from './useI18n'

/**
 * 静态页面（About / Privacy / Terms / Contact）统一的 head 注入。
 *
 * 关键设计：
 * - canonical 自指当前语言 URL，避免重复页收录
 * - hreflang 列出 7 语言 + x-default，让 Google 正确关联多语言版本
 */
export function usePageHead({ title, description, path, extraLd = [] }) {
  // path 是带语言前缀的当前路径，如 /zh/about/
  const url = `${SITE}${path}`

  // 去掉语言前缀，得到去前缀路径（用于 en 备选）
  const stripped = path.replace(/^\/(en|zh|ja|ko|fr|de|es)(?=\/|$)/, '') || '/'

  const hreflangs = SUPPORTED.map((s) => ({
    rel: 'alternate',
    hreflang: s.code,
    href: s.code === DEFAULT_LOCALE
      ? `${SITE}${stripped}`
      : `${SITE}/${s.code}${stripped === '/' ? '/' : stripped}`
  }))
  hreflangs.push({ rel: 'alternate', hreflang: 'x-default', href: `${SITE}${stripped}` })

  useHead(() => ({
    title,
    meta: [
      { name: 'description', content: description },
      { property: 'og:title', content: title },
      { property: 'og:description', content: description },
      { property: 'og:type', content: 'article' },
      { property: 'og:url', content: url }
    ],
    link: [{ rel: 'canonical', href: url }, ...hreflangs],
    script: [
      {
        type: 'application/ld+json',
        innerHTML: JSON.stringify({
          '@context': 'https://schema.org',
          '@type': 'BreadcrumbList',
          itemListElement: [
            { '@type': 'ListItem', position: 1, name: 'Home', item: `${SITE}/` },
            { '@type': 'ListItem', position: 2, name: title, item: url }
          ]
        })
      },
      ...extraLd.map((o) => ({ type: 'application/ld+json', innerHTML: JSON.stringify(o) }))
    ]
  }))
}

/** 直接根据当前路径注入 hreflang（首页、博客列表等非 usePageHead 场景使用）。
 *  接受字符串或 getter 函数（后者随路由变化而响应式更新）。 */
export function useHreflang(pathOrGetter) {
  const getPath = typeof pathOrGetter === 'function' ? pathOrGetter : () => pathOrGetter
  useHead(() => {
    const path = getPath() || '/'
    // 去语言前缀，并统一补尾斜杠（与 sitemap 一致，避免 Google 视为两个 URL）
    let stripped = path.replace(/^\/(en|zh|ja|ko|fr|de|es)(?=\/|$)/, '') || '/'
    if (!stripped.endsWith('/')) stripped += '/'
    const links = SUPPORTED.map((s) => ({
      rel: 'alternate',
      hreflang: s.code,
      href: s.code === DEFAULT_LOCALE
        ? `${SITE}${stripped}`
        : `${SITE}/${s.code}${stripped === '/' ? '/' : stripped}`
    }))
    links.push({ rel: 'alternate', hreflang: 'x-default', href: `${SITE}${stripped}` })
    return { link: links }
  })
}