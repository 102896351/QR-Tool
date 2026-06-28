# QR Tool Studio · 纯前端在线二维码生成器

一款零广告、零后端、极致隐私的在线二维码工具,核心计算全部在浏览器内完成,可直接托管到 GitHub Pages / Vercel / Cloudflare Pages 等静态平台。

## ✨ 功能特性

- **实时预览** —— 文本、颜色、渐变、Logo 任意调整,二维码毫秒级重绘
- **6 种矩阵样式** —— 方块 / 圆点 / 圆角方块 / 极简曲线 / 圆角曲线 / 极致圆角
- **5 种定位眼样式** —— 同样支持渐变填充
- **颜色与渐变** —— 线性 / 径向渐变,可调旋转角度
- **中心 Logo** —— 支持 PNG / JPG / SVG,可调尺寸,自动建议纠错级别 H
- **背景控制** —— 自定义颜色 + 7 色快速调色板,支持透明
- **多格式导出** —— PNG(1024px) / SVG(矢量) / JPEG
- **复制到剪贴板** —— 一键贴到 IM / 文档
- **批量生成** —— 每行一个内容,自动打包为 ZIP
- **历史记录** —— LocalStorage 保存最近 10 次配置,可一键应用
- **主题切换** —— 亮 / 暗 / 跟随系统,无闪烁过渡
- **完全响应式** —— 桌面 / 平板 / 手机全适配

## 🛠 技术栈

- **Vue 3** (Composition API + `<script setup>`)
- **Vite 6** (极速 HMR + 静态构建)
- **Tailwind CSS 3** (原子化样式 + 玻璃拟态)
- **qr-code-styling 1.6** (核心生码引擎)
- **JSZip** (批量打包)

## 🚀 本地开发

```bash
npm install
npm run dev
# → http://localhost:5173
```

## 📦 生产构建

```bash
npm run build
# 产物在 dist/,纯静态文件,可直接部署
```

## 🌐 部署到静态托管

把 `dist/` 目录内所有文件 Push 到 GitHub Pages / Vercel / Cloudflare Pages 即可,无需任何服务端环境。

## 🎨 设计亮点

- **毛玻璃面板** —— `backdrop-filter: blur(24px) saturate(180%)`
- **Mesh 渐变背景** —— 多层 radial-gradient 营造通透感
- **悬浮动画** —— 预览卡片 6s 缓动浮动
- **范围控件定制** —— 渐变填充轨道 + 缩放 thumb
- **WCAG AA 对比度** —— 暗色模式文字与背景对比度均 ≥ 4.5:1

## 🔒 隐私承诺

所有二维码生成逻辑都在浏览器内本地执行,内容从不上传任何服务器,关闭页面即"销毁"。

---

© QR Tool Studio · 用心做工具
