# QR Tool Studio · 文案与 SEO 落地指南

> 本文档梳理了网站所有页面文案 + 针对 Google 的 SEO 优化策略,供运营与内容更新参考。

---

## 1. 参考调研:qr-code-generator.com 核心要素

| 维度 | 对方做法 | 我们的策略 |
|------|---------|-----------|
| 主标题 | "Create your QR Code for Free" | "免费在线二维码生成器" + 卖点副标题 |
| 信任标识 | SOC 2 Type II、Bitly 平台背书 | "100% 本地计算 / 完全免费 / 无需注册 / 永久有效 / 商用授权" 5 条 |
| 类型矩阵 | 8 种静态 + 动态 + 商业版 | 8 种 + 4 步说明 + 6 大行业场景 |
| FAQ | 25+ 条,分三类(Basics/Creating/Scanning) | 12 条,精简但覆盖全部核心长尾词 |
| 卖点强调 | "instantly access scan data" | "数据不出浏览器" (差异化隐私卖点) |
| 语气 | 国际化、偏商务 | 简洁、可信、技术感 |

---

## 2. 文案语料库 (可直接复用)

### 2.1 标题/描述层级
- **H1 (页面主标题):** 免费在线二维码生成器
- **H2 (区段):** 三步创建你的专属二维码 / 支持 8 种常见二维码类型 / 6 大行业场景 / 核心功能 / 常见问题 / 隐私承诺
- **Tagline:** "一款纯前端的二维码工具,支持网址、名片、WiFi、文本、邮箱、电话等 8 种类型,自定义渐变颜色、中心 Logo、多种矩阵样式,一键导出 PNG / SVG / JPEG。"

### 2.2 信任标签 (5 条)
1. 完全免费
2. 无需注册
3. 永久有效
4. 商用授权
5. 高清导出

### 2.3 三大核心卖点
- **隐私:** 100% 在浏览器内运行,数据从未离开你的设备
- **专业:** 6 种矩阵样式 + 5 种定位眼 + 双色渐变 + 中心 Logo
- **通用:** 8 种类型覆盖 90% 日常场景

### 2.4 CTA (Call to Action)
- 主 CTA: 「立即生成」「立即开始」
- 次 CTA: 「使用指南」「查看 3 步教程」

---

## 3. Google SEO 优化清单

### 3.1 技术 SEO ✅ 已落地

| 项目 | 状态 | 说明 |
|------|------|------|
| HTTPS | ⚠️ 部署时配置 | 静态托管平台默认支持 |
| Canonical | ✅ | `<link rel="canonical">` 已设置 |
| hreflang | ✅ | zh-CN / x-default |
| robots.txt | ✅ | `public/robots.txt` 已生成 |
| sitemap.xml | ✅ | `public/sitemap.xml` 已生成 |
| 结构化数据 | ✅ | WebApplication / FAQPage / HowTo / BreadcrumbList / Organization |
| Open Graph | ✅ | og:title / description / image / url / locale |
| Twitter Card | ✅ | summary_large_image |
| 移动端响应式 | ✅ | viewport meta + sm/md/lg 断点 |
| 主题色 | ✅ | 双 theme-color(亮/暗) |
| LCP 优化 | ✅ | 主题预应用 + 内联关键 CSS |
| 字体加载 | ⚠️ 后续 | 建议使用 `font-display: swap` |

### 3.2 On-Page SEO ✅ 已落地

| 元素 | 内容 |
|------|------|
| **Title** | 免费在线二维码生成器 - 自定义 Logo / 渐变 / 批量生成 \| QR Tool Studio |
| **Meta Description** | 158 字,包含核心关键词 + 8 种类型 + 隐私卖点 + CTA |
| **H1** | 1 个 / 页面,出现核心词"二维码" |
| **H2** | 6 个,匹配长尾搜索意图(类型/步骤/场景/功能/FAQ/隐私) |
| **正文关键词** | 二维码生成器、免费、自定义、Logo、渐变、批量、WiFi、vCard、纯前端、隐私、PNG、SVG |
| **图片 Alt** | og-image 已有 alt 文字,后续增加内文图标描述 |
| **内链** | 顶部导航 + 页脚导航 + FAQ 内部跳转 |
| **锚文本** | "立即生成""使用指南""立即开始"多样化 |

### 3.3 关键词策略

#### 核心词 (Head Keywords)
- 二维码生成器
- 在线二维码
- 免费二维码
- QR Code 生成器

#### 长尾词 (Long-tail,布局在 H2/FAQ)
- 自定义二维码
- 带 Logo 的二维码
- 渐变色二维码
- 批量生成二维码
- WiFi 二维码
- 电子名片二维码
- vCard 二维码
- 二维码无法扫描怎么办
- 二维码纠错级别

#### LSI 词 (Latent Semantic Indexing,自然嵌入)
- 静态二维码、动态二维码、容错率、矩阵样式、定位眼、PNG、SVG、JPEG、ZIP、剪贴板、扫码、扫描率、印刷、海报、名片、签到、溯源

### 3.4 E-E-A-T 信号建设

| 维度 | 落地措施 |
|------|---------|
| **Experience (经验)** | "测试"区:扫描每个预设二维码作为示例图 |
| **Expertise (专业)** | 详细的 FAQ + 纠错级别解释 + 印刷注意事项 |
| **Authoritativeness (权威)** | 完整的产品描述 + 12 条 FAQ + 8 种类型 + 6 大场景 |
| **Trustworthiness (可信)** | 隐私承诺版块 + 5 条信任标识 + 无 Cookie / 无广告 / 无注册 |

### 3.5 Core Web Vitals 目标

| 指标 | 目标 | 当前措施 |
|------|------|---------|
| **LCP** (Largest Contentful Paint) | < 2.5s | 主题预应用 + 无外链字体阻塞 + 懒加载图片 |
| **FID / INP** (Interaction to Next Paint) | < 200ms | 纯客户端、零网络等待、watch 节流 60ms |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 固定布局尺寸、字体 fallback、aspect-ratio |
| **TTFB** (Time to First Byte) | < 600ms | 静态托管(Vercel/Cloudflare Pages ≈ 50ms) |

### 3.6 索引与发现

```bash
# 部署后必做
1. Google Search Console 添加站点
2. 提交 sitemap.xml
3. 使用 "网址检查" 工具请求索引首页
4. Bing Webmaster Tools 同样提交
5. Google Analytics 4 (可选)
```

### 3.7 后续可拓展的内容矩阵 (Pillar + Cluster)

以"二维码生成器"为 Pillar Page,围绕以下 Cluster 内容扩展,可显著提升长尾覆盖:

| 集群 | 文章标题(示例) |
|------|---------------|
| 类型 | "WiFi 二维码怎么生成?客人扫码自动连网" |
| 场景 | "餐厅点餐二维码怎么做?完整教程" |
| 营销 | "海报二维码放在哪个位置转化率最高?" |
| 技术 | "二维码纠错级别怎么选?L/M/Q/H 详解" |
| 印刷 | "印刷二维码最容易被忽略的 5 个细节" |
| 安全 | "二维码会被植入病毒吗?如何识别风险" |

每个 Cluster 文章内部互相链接回 Pillar + 工具页,形成 Topic Cluster 结构。

---

## 4. 部署清单 (Deployment Checklist)

```bash
# 1. 构建生产包
npm run build

# 2. 把 dist/ 拖到任意静态托管平台
#    - Cloudflare Pages (推荐,全球 CDN + 零成本)
#    - Vercel (一键 GitHub 集成)
#    - GitHub Pages (gh-pages 分支)
#    - Netlify

# 3. 配置自定义域名 + HTTPS

# 4. 上线后 24h 内
#    - Google Search Console 提交 sitemap
#    - Bing Webmaster Tools 提交 sitemap
#    - 用 "site:your-domain.com" 验证收录
```

---

## 5. 内容更新节奏

| 频率 | 内容 |
|------|------|
| 每周 | 检查 404、补充新 FAQ 答案 |
| 每月 | 写 1-2 篇 Cluster 博客文章 |
| 每季 | 更新 schema.org 的 aggregateRating、screenshot |
| 半年 | 重新审计 Core Web Vitals、关键词排名 |

---

## 6. 关键文件位置

```
qr-tool/
├── index.html              # Meta / JSON-LD / 主题预应用
├── public/
│   ├── robots.txt          # 爬虫协议
│   ├── sitemap.xml         # 站点地图
│   └── BingSiteAuth.xml    # Bing 站长认证占位
└── src/
    ├── App.vue             # 主壳 + 顶部 Hero + 底部 Footer
    └── components/
        ├── AppHeader.vue   # 导航
        └── MarketingSections.vue  # ⭐ How / Types / UseCases / Features / FAQ / Privacy
```

---

## 7. 立即可优化项 (Quick Wins)

1. ⭐ 添加 Google Analytics / Plausible 统计流量来源
2. ⭐ 制作一张 1200×630 的 `og-image.png` 分享卡
3. ⭐ 添加 manifest.json 支持 "添加到主屏幕"
4. ⭐ 接入 Cloudflare Analytics(隐私友好)
5. ⭐ 在 FAQ 里加入更多真实用户问题
6. ⭐ 增加 sitemap 中 Hreflang 各语言版本(后续多语言时)
7. ⭐ 部署后用 [PageSpeed Insights](https://pagespeed.web.dev/) 实测打分

---

*文档版本: 2026-06-28 · QR Tool Studio*
