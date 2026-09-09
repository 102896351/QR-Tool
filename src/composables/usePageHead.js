import { useHead } from '@unhead/vue'
import { SITE } from '../config.js'

/**
 * 静态页面（About / Privacy / Terms / Contact）统一的 head 注入。
 * 之前这 4 个页面没有独立 head，canonical 全部继承首页的 "/"，
 * 会被 Google 判定为首页的重复页而不收录。
 */
export function usePageHead({ title, description, path, extraLd = [] }) {
  const url = `${SITE}${path}`

  useHead(() => ({
    title,
    meta: [
      { name: 'description', content: description },
      { property: 'og:title', content: title },
      { property: 'og:description', content: description },
      { property: 'og:type', content: 'article' },
      { property: 'og:url', content: url },
      { name: 'twitter:title', content: title },
      { name: 'twitter:description', content: description }
    ],
    link: [{ rel: 'canonical', href: url }],
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
