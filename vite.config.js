import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// Vite 配置:开启相对路径基础,以便直接部署到任意子路径(静态托管)
export default defineConfig({
  base: './',
  plugins: [vue()],
  server: {
    host: true,
    port: 5173
  },
  build: {
    outDir: 'dist',
    assetsInlineLimit: 0,
    target: 'es2020'
  }
})
