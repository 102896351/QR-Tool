import { ViteSSG } from 'vite-ssg'
import App from './App.vue'
import { routes, scrollBehavior } from './router.js'
import './style.css'

/**
 * ViteSSG 入口
 * - 构建期：把每条路由渲染成带完整正文的静态 HTML（Google 可读）
 * - 运行期：退化为普通 Vue SPA（交互、i18n、生成器全部照常）
 */
export const createApp = ViteSSG(
  App,
  {
    routes,
    scrollBehavior,
    base: import.meta.env.BASE_URL
  },
  ({ app, router, isClient }) => {
    if (isClient) {
      // 拦截站内 <a> 点击，走前端路由而不做整页刷新
      // （博客正文里的 CTA 链接是 v-html 注入的原生 <a>，拿不到 RouterLink）
      document.addEventListener('click', (e) => {
        if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return
        const a = e.target && e.target.closest ? e.target.closest('a') : null
        if (!a) return
        if (a.target === '_blank' || a.hasAttribute('download')) return

        const href = a.getAttribute('href')
        if (!href || href.startsWith('mailto:') || href.startsWith('tel:')) return

        // 纯锚点：当前页内滚动
        if (href.startsWith('#')) {
          const el = document.querySelector(href)
          if (el) {
            e.preventDefault()
            el.scrollIntoView({ behavior: 'smooth', block: 'start' })
          }
          return
        }

        // 外链
        if (/^[a-z][a-z0-9+.-]*:/i.test(href) && !href.startsWith('/')) return

        // 站内路径
        if (href.startsWith('/')) {
          e.preventDefault()
          const [path, hash] = href.split('#')
          router.push(hash ? { path, hash: `#${hash}` } : path)
        }
      })
    }
  }
)
