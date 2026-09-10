<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useHead } from '@unhead/vue'
import { useRoute, useRouter } from 'vue-router'
import SingleGenerator from '../components/SingleGenerator.vue'
import HistoryView from '../components/HistoryView.vue'
import MarketingSections from '../components/MarketingSections.vue'
import BlogTeaser from '../components/BlogTeaser.vue'
import { useI18n, SUPPORTED, DEFAULT_LOCALE } from '../composables/useI18n'
import { useHreflang } from '../composables/usePageHead'
import { tab } from '../composables/useTab'
import { SITE, BRAND } from '../config.js'

const { t } = useI18n()
const router = useRouter()
const route = useRoute()

const seedText = ref('')

function applyHistoryItem(item) {
  seedText.value = item.text || ''
  tab.value = 'single'
  setTimeout(() => {
    document.getElementById('generator')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }, 100)
}

function goAnchor(id) {
  setTimeout(() => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }, 50)
}

const currentLang = computed(() => route.meta?.lang || DEFAULT_LOCALE)
const homeUrl = computed(() => currentLang.value === DEFAULT_LOCALE ? `${SITE}/` : `${SITE}/${currentLang.value}/`)
const blogUrl = computed(() => currentLang.value === DEFAULT_LOCALE ? `${SITE}/blog/` : `${SITE}/${currentLang.value}/blog/`)

function goBlog() {
  router.push(currentLang.value === DEFAULT_LOCALE ? '/blog/' : `/${currentLang.value}/blog/`)
}

// 各语言 hreflang（首屏 + 所有视图共享）
useHreflang(() => route.path)

// 处理来自其它页面（如 batch）带 ?tab=history 的跳转：
// 1) 切到 history tab
// 2) 清理 query（避免 SEO 收录带参数的 URL 与重复内容）
watch(
  () => route.query.tab,
  (v) => {
    if (v === 'history') {
      tab.value = 'history'
      router.replace({ query: {} })
    }
  },
  { immediate: true }
)

// ---------- 结构化数据 ----------
function stripHtml(s = '') {
  return String(s).replace(/<[^>]*>/g, '')
}

const faqLd = computed(() => ({
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: Array.from({ length: 8 }, (_, i) => ({
    '@type': 'Question',
    name: stripHtml(t(`faq.q${i + 1}`)),
    acceptedAnswer: { '@type': 'Answer', text: stripHtml(t(`faq.a${i + 1}`)) }
  }))
}))

const webAppLd = {
  '@context': 'https://schema.org',
  '@type': 'WebApplication',
  name: BRAND,
  url: homeUrl.value,
  applicationCategory: 'UtilitiesApplication',
  operatingSystem: 'Any (Browser)',
  browserRequirements: 'Requires JavaScript. Requires HTML5.',
  isAccessibleForFree: true,
  offers: { '@type': 'Offer', price: '0', priceCurrency: 'USD' },
  inLanguage: currentLang.value,
  featureList: [
    '8 QR code types: URL / vCard / text / email / phone / SMS / WiFi / location',
    '6 matrix styles and 5 eye styles',
    'Linear and radial gradients with adjustable rotation',
    'Center logo (PNG / JPG / SVG)',
    'Export PNG (1024px) / SVG / JPEG',
    'Batch generation with ZIP packaging',
    'Everything runs in your browser — nothing is uploaded'
  ]
}

const howToLd = {
  '@context': 'https://schema.org',
  '@type': 'HowTo',
  name: 'How to create a QR code',
  description: 'Create a custom QR code in three steps.',
  totalTime: 'PT1M',
  inLanguage: currentLang.value,
  estimatedCost: { '@type': 'MonetaryAmount', currency: 'USD', value: '0' },
  step: [
    { '@type': 'HowToStep', position: 1, name: 'Pick a type and enter your content', text: 'Paste a URL, fill in vCard or WiFi details, or type plain text.' },
    { '@type': 'HowToStep', position: 2, name: 'Customize the design', text: 'Choose a matrix style, set a gradient, upload a center logo and pick an error correction level.' },
    { '@type': 'HowToStep', position: 3, name: 'Download or copy', text: 'Export PNG, SVG or JPEG, or copy the code straight to your clipboard.' }
  ]
}

const breadcrumbLd = {
  '@context': 'https://schema.org',
  '@type': 'BreadcrumbList',
  itemListElement: [
    { '@type': 'ListItem', position: 1, name: 'Home', item: homeUrl.value },
    { '@type': 'ListItem', position: 2, name: 'QR Code Generator', item: `${homeUrl.value}#generator` }
  ]
}

useHead(() => ({
  title: t('meta.title'),
  meta: [
    { name: 'description', content: t('meta.desc') },
    { property: 'og:title', content: t('meta.title') },
    { property: 'og:description', content: t('meta.desc') },
    { property: 'og:type', content: 'website' },
    { property: 'og:url', content: homeUrl.value },
    { property: 'og:locale', content: currentLang.value },
    { name: 'twitter:title', content: t('meta.title') },
    { name: 'twitter:description', content: t('meta.desc') }
  ],
  link: [{ rel: 'canonical', href: homeUrl.value }],
  script: [
    { type: 'application/ld+json', innerHTML: JSON.stringify(webAppLd) },
    { type: 'application/ld+json', innerHTML: JSON.stringify(howToLd) },
    { type: 'application/ld+json', innerHTML: JSON.stringify(faqLd.value) },
    { type: 'application/ld+json', innerHTML: JSON.stringify(breadcrumbLd) }
  ]
}))
</script>

<template>
  <!-- Hero -->
  <section class="w-full max-w-6xl mx-auto px-4 sm:px-6 mt-8 sm:mt-10">
    <div class="text-center max-w-3xl mx-auto">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/70 dark:bg-white/[0.04] border border-gray-200/60 dark:border-white/10 text-xs font-medium text-gray-700 dark:text-gray-200 mb-5 backdrop-blur">
        <span class="relative flex h-2 w-2">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
        </span>
        {{ t('hero.badge') }}
      </div>

      <!-- 全站唯一的 H1 -->
      <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-[1.05]">
        <span class="text-transparent bg-clip-text bg-gradient-to-r from-brand-600 via-purple-500 to-pink-500">{{ t('hero.title.line1') }}</span>
        <span class="text-gray-900 dark:text-white">{{ t('hero.title.line2') }}</span>
      </h1>

      <p class="mt-4 sm:mt-5 text-base sm:text-lg text-gray-600 dark:text-gray-300 leading-relaxed" v-html="t('hero.desc')"></p>

      <div class="mt-6 flex flex-wrap items-center justify-center gap-3 text-sm">
        <button @click="goAnchor('generator')" class="btn-brand">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          {{ t('hero.cta.primary') }}
        </button>
        <button @click="goAnchor('how')" class="btn-ghost">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          {{ t('hero.cta.secondary') }}
        </button>
      </div>

      <!-- 信任标识 -->
      <div class="mt-7 flex flex-wrap items-center justify-center gap-x-5 gap-y-2 text-xs text-gray-500 dark:text-gray-400">
        <span v-for="key in ['free', 'noreg', 'permanent', 'commercial', 'hd']" :key="key" class="inline-flex items-center gap-1.5">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" class="text-emerald-500"><polyline points="20 6 9 17 4 12"/></svg>
          {{ t(`hero.trust.${key}`) }}
        </span>
      </div>
    </div>
  </section>

  <!-- 主内容区 -->
  <main id="generator" class="flex-1 w-full max-w-6xl mx-auto px-4 sm:px-6 pb-12 mt-6 sm:mt-8 scroll-mt-24">
    <SingleGenerator v-if="tab === 'single'" :initial-text="seedText" :key="seedText" @saved="() => {}" />
    <HistoryView v-else @apply="applyHistoryItem" />
  </main>

  <!-- AdSense: display ad（首页内容最丰富，仅此处展示） -->
  <aside
    v-if="tab === 'single'"
    class="w-full max-w-6xl mx-auto px-4 sm:px-6 mt-2 mb-8" aria-label="Sponsored content"
  >
    <div class="text-[10px] uppercase tracking-wider text-gray-400 dark:text-gray-500 mb-1.5 text-center">Advertisement</div>
    <ins
      class="adsbygoogle block w-full min-h-[120px]"
      style="display:block; min-height:120px"
      data-ad-client="ca-pub-1606763409380030"
      data-ad-slot="0000000000"
      data-ad-format="auto"
      data-full-width-responsive="true"
    ></ins>
  </aside>

  <!-- 首页直达 6 篇最新文章的内链（Google 发现文章的主通道） -->
  <BlogTeaser />

  <!-- SEO 内容板块:How / Types / Use Cases / Features / FAQ / Why / CTA -->
  <MarketingSections :on-go-blog="goBlog" />
</template>
