import HomeView from './views/HomeView.vue'
import BatchView from './views/BatchView.vue'
import BlogIndex from './components/blog/BlogIndex.vue'
import BlogPost from './components/blog/BlogPost.vue'
import PrivacyPage from './components/pages/PrivacyPage.vue'
import TermsPage from './components/pages/TermsPage.vue'
import ContactPage from './components/pages/ContactPage.vue'
import AboutPage from './components/pages/AboutPage.vue'
import posts from './blog/posts.json'
import { LOCALE_CODES, DEFAULT_LOCALE } from './composables/useI18n'

/**
 * 路由表 —— 每个基础路由 × 7 语言派生
 *
 * 设计：
 * 1. history 模式（非 hash）—— Google 只认 path
 * 2. 每篇博客一条「静态路由记录」而非动态段，vite-ssg 构建期枚举预渲染
 * 3. 7 语言独立 URL：en 用裸路径（/、/about/），其它语言加 /zh/、/ja/... 前缀
 * 4. 每条路由 meta.lang 标记当前语言，App.vue 据此切换 i18n 状态
 * 5. sitemap 用带尾斜杠的地址
 */

export const scrollBehavior = (to, from, savedPosition) => {
  if (to.hash) return { el: to.hash, top: 88, behavior: 'smooth' }
  if (savedPosition) return savedPosition
  return { top: 0, behavior: 'auto' }
}

const baseStaticRoutes = [
  { path: '/',        name: 'home',    component: HomeView,    meta: { view: 'home' } },
  { path: '/batch',   name: 'batch',   component: BatchView,   meta: { view: 'batch' } },
  { path: '/blog',    name: 'blog',    component: BlogIndex,   meta: { view: 'blog-list' } },
  { path: '/privacy', name: 'privacy', component: PrivacyPage, meta: { view: 'privacy' } },
  { path: '/terms',   name: 'terms',   component: TermsPage,   meta: { view: 'terms' } },
  { path: '/contact', name: 'contact', component: ContactPage, meta: { view: 'contact' } },
  { path: '/about',   name: 'about',   component: AboutPage,   meta: { view: 'about' } }
]

// 每篇文章一条静态路由
const basePostRoutes = posts.map((p) => ({
  path: `/blog/${p.slug}`,
  name: `post-${p.slug}`,
  component: BlogPost,
  props: { slug: p.slug },
  meta: { view: 'blog-post', slug: p.slug }
}))

const allBase = [...baseStaticRoutes, ...basePostRoutes]

// 为每种语言派生一组路由。en 不加前缀（/、/about/），其它语言加 /zh/ 等前缀。
export const routes = LOCALE_CODES.flatMap((lang) => {
  const prefix = lang === DEFAULT_LOCALE ? '' : `/${lang}`
  return allBase.map((r) => ({
    path: prefix + r.path,
    name: `${lang}-${r.name}`,
    component: r.component,
    props: r.props,
    meta: { ...r.meta, lang }
  }))
})