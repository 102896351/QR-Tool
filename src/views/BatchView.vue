<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import BatchGenerator from '../components/BatchGenerator.vue'
import { useI18n, DEFAULT_LOCALE } from '../composables/useI18n'
import { usePageHead } from '../composables/usePageHead'
import { SITE } from '../config.js'

const route = useRoute()
const lang = computed(() => route.meta?.lang || DEFAULT_LOCALE)
const batchPath = computed(() => (lang.value === DEFAULT_LOCALE ? '/batch/' : `/${lang.value}/batch/`))

function lp(p) {
  if (lang.value === DEFAULT_LOCALE) return p
  return `/${lang.value}${p === '/' ? '/' : p}`
}

// 批量工具结构化数据
const webAppLd = {
  '@context': 'https://schema.org',
  '@type': 'WebApplication',
  name: 'Bulk QR Code Generator',
  url: `${SITE}${batchPath.value}`,
  applicationCategory: 'UtilitiesApplication',
  operatingSystem: 'Any (Browser)',
  browserRequirements: 'Requires JavaScript. Requires HTML5.',
  isAccessibleForFree: true,
  offers: { '@type': 'Offer', price: '0', priceCurrency: 'USD' },
  featureList: [
    'Paste one URL or text per line to generate hundreds of QR codes at once',
    'Uniform design: one color, one logo and one error-correction level for the whole batch',
    'Download all QR codes as a single ZIP archive',
    'Every QR code is generated locally — nothing is uploaded'
  ]
}

const faqLd = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: 'How many QR codes can I generate in one batch?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'You can paste any number of lines, but we recommend keeping a single batch under 200 codes so the browser stays fast. There is no hard limit and no account required.'
      }
    },
    {
      '@type': 'Question',
      name: 'What format are the bulk QR codes downloaded in?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'All QR codes are generated as 600×600 PNG images and packed into one ZIP file. You can unzip and use them directly in print, email or documents.'
      }
    },
    {
      '@type': 'Question',
      name: 'Can I add a logo to every QR code in the batch?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Yes. Upload one logo and it is applied uniformly to every QR code in the batch, with an adjustable size so it stays scannable.'
      }
    },
    {
      '@type': 'Question',
      name: 'Is the bulk QR code generator free?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Yes, it is completely free for personal and commercial use. Everything runs in your browser, so your data never leaves your device.'
      }
    }
  ]
}

usePageHead({
  title: 'Bulk QR Code Generator — Create 100+ QR Codes & Download ZIP',
  description:
    'Generate hundreds of QR codes at once. Paste one link or text per line, apply a uniform color and logo, then download every QR code as a single ZIP. Free, private, no sign-up.',
  path: batchPath.value,
  extraLd: [webAppLd, faqLd]
})
</script>

<template>
  <!-- Hero -->
  <section class="w-full max-w-6xl mx-auto px-4 sm:px-6 mt-8 sm:mt-10">
    <div class="text-center max-w-3xl mx-auto">
      <span class="inline-block px-3 py-1 rounded-full bg-white/70 dark:bg-white/[0.04] border border-gray-200/60 dark:border-white/10 text-xs font-semibold text-gray-700 dark:text-gray-200 mb-5 backdrop-blur">
        BULK MODE
      </span>
      <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight leading-[1.1] text-gray-900 dark:text-white">
        Bulk QR Code <span class="text-transparent bg-clip-text bg-gradient-to-r from-brand-600 via-purple-500 to-pink-500">Generator</span>
      </h1>
      <p class="mt-4 sm:mt-5 text-base sm:text-lg text-gray-600 dark:text-gray-300 leading-relaxed">
        Create hundreds of QR codes in one go. Paste one link, phone number or text per line, pick a single style, and download the whole batch as a ZIP file — no sign-up, no upload, no cost.
      </p>
      <div class="mt-6 flex flex-wrap items-center justify-center gap-x-5 gap-y-2 text-xs text-gray-500 dark:text-gray-400">
        <span v-for="k in ['100+ codes at once', 'One ZIP download', 'Uniform logo', 'Runs in your browser']" :key="k" class="inline-flex items-center gap-1.5">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" class="text-emerald-500"><polyline points="20 6 9 17 4 12"/></svg>
          {{ k }}
        </span>
      </div>
    </div>
  </section>

  <!-- 生成器主体 -->
  <main id="batch-generator" class="flex-1 w-full max-w-6xl mx-auto px-4 sm:px-6 pb-8 mt-8 scroll-mt-24">
    <BatchGenerator />
  </main>

  <!-- 差异化 SEO 正文：批量场景（与首页区分，避免 thin page） -->
  <section class="w-full max-w-4xl mx-auto px-4 sm:px-6 pb-10">
    <h2 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white mb-5">
      When to use a bulk QR code generator
    </h2>
    <p class="text-gray-600 dark:text-gray-300 leading-relaxed mb-4">
      A single QR code is enough when you have one link. But the moment you need the same design applied to dozens or hundreds of items, generating them one by one is a waste of time. A bulk generator lets you paste a plain list and turn it into ready-to-print codes in seconds.
    </p>
    <ul class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm text-gray-600 dark:text-gray-300">
      <li class="flex items-start gap-2.5 p-3 rounded-xl border border-gray-200/60 dark:border-white/10 bg-white/60 dark:bg-white/[0.03]">
        <span class="mt-0.5 text-brand-600 dark:text-brand-300">▸</span>
        <span><strong class="text-gray-800 dark:text-gray-100">E-commerce &amp; SKUs</strong> — give every product listing or package its own scannable URL.</span>
      </li>
      <li class="flex items-start gap-2.5 p-3 rounded-xl border border-gray-200/60 dark:border-white/10 bg-white/60 dark:bg-white/[0.03]">
        <span class="mt-0.5 text-brand-600 dark:text-brand-300">▸</span>
        <span><strong class="text-gray-800 dark:text-gray-100">Events &amp; badges</strong> — print attendee badges, tickets and check-in codes in bulk.</span>
      </li>
      <li class="flex items-start gap-2.5 p-3 rounded-xl border border-gray-200/60 dark:border-white/10 bg-white/60 dark:bg-white/[0.03]">
        <span class="mt-0.5 text-brand-600 dark:text-brand-300">▸</span>
        <span><strong class="text-gray-800 dark:text-gray-100">Restaurants &amp; menus</strong> — one QR per table or per menu page.</span>
      </li>
      <li class="flex items-start gap-2.5 p-3 rounded-xl border border-gray-200/60 dark:border-white/10 bg-white/60 dark:bg-white/[0.03]">
        <span class="mt-0.5 text-brand-600 dark:text-brand-300">▸</span>
        <span><strong class="text-gray-800 dark:text-gray-100">Business cards &amp; vCards</strong> — generate a batch of contact codes for a whole team.</span>
      </li>
      <li class="flex items-start gap-2.5 p-3 rounded-xl border border-gray-200/60 dark:border-white/10 bg-white/60 dark:bg-white/[0.03]">
        <span class="mt-0.5 text-brand-600 dark:text-brand-300">▸</span>
        <span><strong class="text-gray-800 dark:text-gray-100">Asset &amp; inventory tracking</strong> — label equipment, shelves and boxes with scannable IDs.</span>
      </li>
      <li class="flex items-start gap-2.5 p-3 rounded-xl border border-gray-200/60 dark:border-white/10 bg-white/60 dark:bg-white/[0.03]">
        <span class="mt-0.5 text-brand-600 dark:text-brand-300">▸</span>
        <span><strong class="text-gray-800 dark:text-gray-100">Marketing campaigns</strong> — roll out a different landing URL to every channel or region.</span>
      </li>
    </ul>

    <div class="mt-8 p-4 rounded-2xl border border-brand-200/60 dark:border-brand-500/20 bg-brand-50/60 dark:bg-brand-500/10 text-sm text-gray-700 dark:text-gray-200">
      <span class="font-semibold">Prefer a single code?</span>
      Use the
      <RouterLink :to="lp('/')" class="font-semibold text-brand-600 dark:text-brand-300 hover:underline">single QR code generator</RouterLink>
      for one link with full style controls, gradients and a live preview.
    </div>
  </section>
</template>
