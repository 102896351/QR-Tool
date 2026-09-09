import HomeView from './views/HomeView.vue'
import BlogIndex from './components/blog/BlogIndex.vue'
import BlogPost from './components/blog/BlogPost.vue'
import PrivacyPage from './components/pages/PrivacyPage.vue'
import TermsPage from './components/pages/TermsPage.vue'
import ContactPage from './components/pages/ContactPage.vue'
import AboutPage from './components/pages/AboutPage.vue'
import posts from './blog/posts.json'

/**
 * 路由表
 *
 * 关键设计：
 * 1. history 模式（非 hash）—— Google 只认 path，hash 后面的内容一律忽略
 * 2. 每篇博客生成一条「静态路由记录」而非 `/blog/:slug` 动态段，
 *    这样 vite-ssg 在构建期就能枚举出全部页面并预渲染成真实 HTML
 * 3. sitemap 使用带尾斜杠的地址，vue-router 默认非严格模式可同时匹配
 */

export const scrollBehavior = (to, from, savedPosition) => {
  // 首页锚点（#generator / #how / #faq ...）
  if (to.hash) {
    return { el: to.hash, top: 88, behavior: 'smooth' }
  }
  if (savedPosition) return savedPosition
  return { top: 0, behavior: 'auto' }
}

const staticRoutes = [
  { path: '/', name: 'home', component: HomeView, meta: { view: 'home' } },
  { path: '/blog', name: 'blog', component: BlogIndex, meta: { view: 'blog-list' } },
  { path: '/privacy', name: 'privacy', component: PrivacyPage, meta: { view: 'privacy' } },
  { path: '/terms', name: 'terms', component: TermsPage, meta: { view: 'terms' } },
  { path: '/contact', name: 'contact', component: ContactPage, meta: { view: 'contact' } },
  { path: '/about', name: 'about', component: AboutPage, meta: { view: 'about' } }
]

// 每篇文章一条静态路由 → 预渲染时为每篇生成独立 HTML 文件
const postRoutes = posts.map((p) => ({
  path: `/blog/${p.slug}`,
  name: `post-${p.slug}`,
  component: BlogPost,
  props: { slug: p.slug },
  meta: { view: 'blog-post' }
}))

export const routes = [...staticRoutes, ...postRoutes]
