<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import AppHeader from './components/AppHeader.vue'
import SingleGenerator from './components/SingleGenerator.vue'
import BatchGenerator from './components/BatchGenerator.vue'
import HistoryView from './components/HistoryView.vue'
import MarketingSections from './components/MarketingSections.vue'
import LegalModal from './components/LegalModal.vue'
import { useTheme } from './composables/useTheme'
import { useI18n } from './composables/useI18n'

const { isDark } = useTheme()
const { t, lang } = useI18n()
const tab = ref('single')

// 法律弹窗
const legalOpen = ref(false)
const legalType = ref('disclaimer') // disclaimer | privacy | about | contact
function openLegal(type) {
  legalType.value = type
  legalOpen.value = true
}
function closeLegal() {
  legalOpen.value = false
}

// 用于在历史记录项点击"应用"后,跳回单个生成并预填值
const seedText = ref('')

function applyHistoryItem(item) {
  seedText.value = item.text || ''
  tab.value = 'single'
  // 平滑滚到生成器
  setTimeout(() => {
    document.getElementById('generator')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }, 100)
}

const year = computed(() => new Date().getFullYear())

// 同步 html lang + 文档标题(SEO)
function syncHeadMeta() {
  if (typeof document === 'undefined') return
  document.documentElement.lang = lang.value
  document.title = t('meta.title')
}

function syncMetaDesc() {
  const desc = t('meta.desc')
  const md = document.querySelector('meta[name="description"]')
  if (md) md.setAttribute('content', desc)
  const og = document.querySelector('meta[property="og:description"]')
  if (og) og.setAttribute('content', desc)
  const tw = document.querySelector('meta[name="twitter:description"]')
  if (tw) tw.setAttribute('content', desc)
}

onMounted(() => {
  syncHeadMeta()
  syncMetaDesc()
  // JSON-LD 国际化
  const ld = document.querySelector('script[type="application/ld+json"][data-i18n]')
  if (ld) {
    try {
      const obj = JSON.parse(ld.textContent)
      obj.description = t('meta.desc')
      ld.textContent = JSON.stringify(obj)
    } catch (e) {}
  }
})

// 切换语言时刷新 head
watch(lang, () => {
  syncHeadMeta()
  syncMetaDesc()
  const ld = document.querySelector('script[type="application/ld+json"][data-i18n]')
  if (ld) {
    try {
      const obj = JSON.parse(ld.textContent)
      obj.description = t('meta.desc')
      ld.textContent = JSON.stringify(obj)
    } catch (e) {}
  }
})

// 滚动到指定锚点
function goAnchor(id) {
  setTimeout(() => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }, 50)
}

const showFeaturesAnchor = ref(false)
function onNavClick(anchor) {
  showFeaturesAnchor.value = false
  goAnchor(anchor)
}
</script>

<template>
  <div class="mesh-bg"></div>

  <div class="min-h-screen flex flex-col">
    <AppHeader :active="tab" @change="(v) => tab = v" />

    <!-- Hero(仅在 single 时显示) -->
    <section v-if="tab === 'single'" class="w-full max-w-6xl mx-auto px-4 sm:px-6 mt-8 sm:mt-10">
      <div class="text-center max-w-3xl mx-auto">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/70 dark:bg-white/[0.04] border border-gray-200/60 dark:border-white/10 text-xs font-medium text-gray-700 dark:text-gray-200 mb-5 backdrop-blur">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          {{ t('hero.badge') }}
        </div>
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
          <span class="inline-flex items-center gap-1.5">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" class="text-emerald-500"><polyline points="20 6 9 17 4 12"/></svg>
            {{ t('hero.trust.free') }}
          </span>
          <span class="inline-flex items-center gap-1.5">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" class="text-emerald-500"><polyline points="20 6 9 17 4 12"/></svg>
            {{ t('hero.trust.noreg') }}
          </span>
          <span class="inline-flex items-center gap-1.5">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" class="text-emerald-500"><polyline points="20 6 9 17 4 12"/></svg>
            {{ t('hero.trust.permanent') }}
          </span>
          <span class="inline-flex items-center gap-1.5">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" class="text-emerald-500"><polyline points="20 6 9 17 4 12"/></svg>
            {{ t('hero.trust.commercial') }}
          </span>
          <span class="inline-flex items-center gap-1.5">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" class="text-emerald-500"><polyline points="20 6 9 17 4 12"/></svg>
            {{ t('hero.trust.hd') }}
          </span>
        </div>
      </div>
    </section>

    <!-- 主内容区 -->
    <main id="generator" class="flex-1 w-full max-w-6xl mx-auto px-4 sm:px-6 pb-12 mt-6 sm:mt-8 scroll-mt-24">
      <SingleGenerator v-if="tab === 'single'" :initial-text="seedText" :key="seedText" />
      <BatchGenerator v-else-if="tab === 'batch'" />
      <HistoryView v-else @apply="applyHistoryItem" />
    </main>

    <!-- SEO 内容板块:How / Types / Use Cases / FAQ -->
    <MarketingSections v-if="tab === 'single'" />

    <!-- Footer -->
    <footer class="mt-auto border-t border-gray-200/60 dark:border-white/10 bg-white/40 dark:bg-white/[0.02] backdrop-blur">
      <div class="w-full max-w-6xl mx-auto px-4 sm:px-6 py-10 grid grid-cols-2 sm:grid-cols-5 gap-8 text-sm">
        <!-- 品牌区 -->
        <div class="col-span-2 sm:col-span-2">
          <div class="flex items-center gap-2 mb-3">
            <div class="h-9 w-9 rounded-xl bg-gradient-to-br from-brand-500 to-purple-500 grid place-items-center text-white font-bold shadow-md shadow-brand-500/30">Q</div>
            <div class="leading-tight">
              <div class="font-bold text-gray-900 dark:text-white">QR Tool Studio</div>
              <div class="text-[10px] text-gray-500 dark:text-gray-400">{{ t('footer.brand.sub') }}</div>
            </div>
          </div>
          <p class="text-xs text-gray-600 dark:text-gray-400 leading-relaxed">
            {{ t('footer.brand.desc') }}
          </p>
        </div>

        <!-- 产品 -->
        <div>
          <h3 class="text-xs font-bold text-gray-700 dark:text-gray-200 uppercase tracking-wider mb-3">{{ t('footer.col.product') }}</h3>
          <ul class="space-y-2 text-xs text-gray-600 dark:text-gray-400">
            <li><a href="#generator" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.link.generator') }}</a></li>
            <li><a href="#batch" @click.prevent="tab='batch'" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.link.batch') }}</a></li>
            <li><a href="#how" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.link.how') }}</a></li>
            <li><a href="#types" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.link.types') }}</a></li>
            <li><a href="#use-cases" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.link.usecases') }}</a></li>
            <li><a href="#faq" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.link.faq') }}</a></li>
          </ul>
        </div>

        <!-- 法律 -->
        <div>
          <h3 class="text-xs font-bold text-gray-700 dark:text-gray-200 uppercase tracking-wider mb-3">{{ t('footer.col.legal') }}</h3>
          <ul class="space-y-2 text-xs text-gray-600 dark:text-gray-400">
            <li><button @click="openLegal('privacy')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors text-left">{{ t('footer.legal.privacy') }}</button></li>
            <li><button @click="openLegal('disclaimer')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors text-left">{{ t('footer.legal.disclaimer') }}</button></li>
            <li><button @click="openLegal('disclaimer')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors text-left">{{ t('footer.legal.terms') }}</button></li>
            <li><button @click="openLegal('privacy')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors text-left">{{ t('footer.legal.cookie') }}</button></li>
          </ul>
        </div>

        <!-- 关于 -->
        <div>
          <h3 class="text-xs font-bold text-gray-700 dark:text-gray-200 uppercase tracking-wider mb-3">{{ t('footer.col.about') }}</h3>
          <ul class="space-y-2 text-xs text-gray-600 dark:text-gray-400">
            <li><button @click="openLegal('about')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors text-left">{{ t('footer.about.about') }}</button></li>
            <li><button @click="openLegal('contact')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors text-left">{{ t('footer.about.contact') }}</button></li>
            <li>
              <a href="mailto:andynaonao@gmail.com" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">
                {{ t('footer.about.biz') }}
              </a>
            </li>
            <li>
              <span class="inline-flex items-center gap-1.5 text-gray-500 dark:text-gray-400">
                {{ t('footer.about.theme') }}:
                <strong class="text-gray-700 dark:text-gray-200">{{ isDark ? t('theme.dark') : t('theme.light') }}</strong>
              </span>
            </li>
          </ul>
        </div>
      </div>

      <!-- 法律信息行(广而全) -->
      <div class="border-t border-gray-200/60 dark:border-white/10">
        <div class="w-full max-w-6xl mx-auto px-4 sm:px-6 py-4 flex flex-col gap-3 text-[11px] text-gray-500 dark:text-gray-400">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
            <div class="flex flex-wrap items-center gap-x-3 gap-y-1">
              <span>{{ t('footer.copy', { year }) }}</span>
            </div>
            <div class="flex flex-wrap items-center gap-x-3 gap-y-1">
              <button @click="openLegal('disclaimer')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.legal.disclaimer') }}</button>
              <span>·</span>
              <button @click="openLegal('privacy')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.legal.privacy') }}</button>
              <span>·</span>
              <button @click="openLegal('about')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.about.about') }}</button>
              <span>·</span>
              <button @click="openLegal('contact')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.about.contact') }}</button>
            </div>
          </div>
        </div>
      </div>
    </footer>

    <!-- 法律弹窗 -->
    <LegalModal :open="legalOpen" :type="legalType" @close="closeLegal" />
  </div>
</template>
