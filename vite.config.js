import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

/**
 * Vite 配置
 *
 * 重要：base 必须是绝对路径 '/'。
 * 之前是 './'（相对路径）+ hash 路由，两者叠加导致
 * 所有子页面在 Google 眼里都是同一个空壳首页。
 * 现在改为 history 路由 + vite-ssg 预渲染，相对路径会让 /blog/xxx/ 下的资源 404。
 */
export default defineConfig({
  base: '/',
  plugins: [vue()],
  server: {
    host: true,
    port: 5173
  },
  build: {
    outDir: 'dist',
    assetsInlineLimit: 0,
    target: 'es2020'
  },
  ssgOptions: {
    // 每篇文章都会生成 dist/blog/<slug>/index.html
    dirStyle: 'nested',
    formatting: 'none'
  }
})
