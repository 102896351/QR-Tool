<script setup>
import { ref } from 'vue'
import { useI18n } from '../composables/useI18n'

defineProps({
  onGoBlog: { type: Function, default: null }
})

const { t } = useI18n()

// 8 种类型(只保留 id + icon,文案走 i18n)
const types = [
  { id: 'url',      icon: 'M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71 M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71' },
  { id: 'vcard',    icon: 'M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2 M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z' },
  { id: 'text',     icon: 'M4 6h16 M4 12h16 M4 18h7' },
  { id: 'email',    icon: 'M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z M22 6l-10 7L2 6' },
  { id: 'tel',      icon: 'M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z' },
  { id: 'sms',      icon: 'M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z' },
  { id: 'wifi',     icon: 'M5 12.55a11 11 0 0 1 14.08 0 M1.42 9a16 16 0 0 1 21.16 0 M8.53 16.11a6 6 0 0 1 6.95 0 M12 20h.01' },
  { id: 'location', icon: 'M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z M12 13a3 3 0 1 0 0-6 3 3 0 0 0 0 6z' }
]

// FAQ 展开/收起
const openIdx = ref(-1)
function toggleFaq(i) {
  openIdx.value = openIdx.value === i ? -1 : i
}

// How 3 步
const steps = [
  { n: '1', key: 'how' },
  { n: '2', key: 'how' },
  { n: '3', key: 'how' }
]

// 6 个功能图标(纯 SVG 路径,无文字)
const featureIcons = [
  'M4 4h6v6H4z M14 4h6v6h-6z M4 14h6v6H4z M14 14h2v2h-2z M18 14h2v2h-2z M14 18h2v2h-2z M18 18h2v2h-2z',
  'M12 2v20 M2 12h20',
  'M12 2L2 7l10 5 10-5-10-5z M2 17l10 5 10-5 M2 12l10 5 10-5',
  'M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4 M7 10l5 5 5-5 M12 15V3',
  'M16 3h5v5 M14 10L21 3 M21 14v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5 M3 21l7-7',
  'M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8 M3 3v5h5 M12 7v5l4 2'
]
</script>

<template>
  <div class="w-full max-w-6xl mx-auto px-4 sm:px-6 space-y-16 sm:space-y-24 pb-12">

    <!-- 1. How to Use: 3 步 -->
    <section id="how" class="scroll-mt-24">
      <div class="text-center mb-10">
        <div class="section-label">{{ t('mkt.how.label') }}</div>
        <h2 class="text-3xl sm:text-4xl font-extrabold mt-2 text-gray-900 dark:text-white">
          {{ t('mkt.how.title') }}
        </h2>
        <p class="mt-3 text-gray-600 dark:text-gray-300">{{ t('mkt.how.sub') }}</p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div v-for="(s, i) in steps" :key="i"
        class="relative glass-panel dark:glass-panel-dark p-6 noise-bg">
          <div class="absolute -top-3 -left-3 h-9 w-9 rounded-2xl bg-gradient-to-br from-brand-500 to-purple-500 text-white font-bold grid place-items-center shadow-lg shadow-brand-500/30">
            {{ s.n }}
          </div>
          <h3 class="text-lg font-bold mt-2 text-gray-900 dark:text-white">{{ t(`mkt.how.s${i + 1}.t`) }}</h3>
          <p class="mt-2 text-sm text-gray-600 dark:text-gray-300 leading-relaxed">{{ t(`mkt.how.s${i + 1}.d`) }}</p>
        </div>
      </div>
    </section>

    <!-- 2. Types: 8 种类型 -->
    <section id="types" class="scroll-mt-24">
      <div class="text-center mb-10">
        <div class="section-label">{{ t('mkt.types.label') }}</div>
        <h2 class="text-3xl sm:text-4xl font-extrabold mt-2 text-gray-900 dark:text-white">
          {{ t('mkt.types.title') }}
        </h2>
        <p class="mt-3 text-gray-600 dark:text-gray-300">{{ t('mkt.types.sub') }}</p>
      </div>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div v-for="tp in types" :key="tp.id"
             class="group glass-panel dark:glass-panel-dark p-4 sm:p-5 noise-bg hover:scale-[1.03] hover:shadow-xl transition-all duration-300">
          <div class="h-10 w-10 rounded-xl bg-gradient-to-br from-brand-500/15 to-purple-500/15 text-brand-600 dark:text-brand-300 grid place-items-center mb-3 group-hover:scale-110 transition-transform">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path :d="tp.icon"/>
            </svg>
          </div>
          <h3 class="text-sm font-bold text-gray-900 dark:text-white">{{ t(`mkt.types.${tp.id}.name`) }}</h3>
          <p class="mt-1.5 text-xs text-gray-500 dark:text-gray-400 leading-relaxed">{{ t(`mkt.types.${tp.id}.desc`) }}</p>
        </div>
      </div>
    </section>

    <!-- 3. Use Cases -->
    <section id="use-cases" class="scroll-mt-24">
      <div class="text-center mb-10">
        <div class="section-label">{{ t('mkt.useCases.label') }}</div>
        <h2 class="text-3xl sm:text-4xl font-extrabold mt-2 text-gray-900 dark:text-white">
          {{ t('mkt.useCases.title') }}
        </h2>
        <p class="mt-3 text-gray-600 dark:text-gray-300">{{ t('mkt.useCases.sub') }}</p>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        <div v-for="i in 6" :key="i"
             class="group relative overflow-hidden glass-panel dark:glass-panel-dark p-6 noise-bg hover:border-brand-300 dark:hover:border-brand-500/40 transition-colors">
          <div class="text-[10px] font-bold tracking-wider uppercase text-brand-600 dark:text-brand-300 mb-2">{{ t(`mkt.useCases.${i}.tag`) }}</div>
          <h3 class="text-lg font-bold text-gray-900 dark:text-white group-hover:text-brand-600 dark:group-hover:text-brand-300 transition-colors">{{ t(`mkt.useCases.${i}.t`) }}</h3>
          <p class="mt-2 text-sm text-gray-600 dark:text-gray-300 leading-relaxed">{{ t(`mkt.useCases.${i}.d`) }}</p>
          <div class="absolute -bottom-12 -right-12 h-32 w-32 rounded-full bg-gradient-to-br from-brand-500/10 to-purple-500/10 blur-2xl group-hover:scale-150 transition-transform duration-500"></div>
        </div>
      </div>
    </section>

    <!-- 4. Features Grid -->
    <section id="features" class="scroll-mt-24">
      <div class="text-center mb-10">
        <div class="section-label">{{ t('mkt.features.label') }}</div>
        <h2 class="text-3xl sm:text-4xl font-extrabold mt-2 text-gray-900 dark:text-white">
          {{ t('mkt.features.title') }}
        </h2>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="i in 6" :key="i"
        class="group glass-panel dark:glass-panel-dark p-5 noise-bg hover:shadow-lg transition-shadow">
          <div class="h-10 w-10 rounded-xl bg-gradient-to-br from-brand-500 to-purple-500 text-white grid place-items-center mb-3 shadow-md shadow-brand-500/30">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path :d="featureIcons[i - 1]"/>
            </svg>
          </div>
          <h3 class="text-base font-bold text-gray-900 dark:text-white">{{ t(`mkt.features.${i}.t`) }}</h3>
          <p class="mt-1.5 text-sm text-gray-600 dark:text-gray-300 leading-relaxed">{{ t(`mkt.features.${i}.d`) }}</p>
        </div>
      </div>
    </section>

    <!-- 5. FAQ -->
    <section id="faq" class="scroll-mt-24">
      <div class="text-center mb-10">
        <div class="section-label">{{ t('mkt.faq.label') }}</div>
        <h2 class="text-3xl sm:text-4xl font-extrabold mt-2 text-gray-900 dark:text-white">
          {{ t('mkt.faq.title') }}
        </h2>
        <p class="mt-3 text-gray-600 dark:text-gray-300">
          <span>{{ t('mkt.faq.sub') }}</span>
          <a href="#" class="text-brand-600 dark:text-brand-300 hover:underline">{{ t('legal.contact.title') }}</a>
        </p>
      </div>
      <div class="max-w-3xl mx-auto glass-panel dark:glass-panel-dark p-2 sm:p-3 noise-bg">
        <div v-for="i in 8" :key="i"
             class="border-b border-gray-200/60 dark:border-white/5 last:border-b-0">
          <button
            @click="toggleFaq(i - 1)"
            class="w-full flex items-center justify-between gap-4 p-4 sm:p-5 text-left rounded-xl hover:bg-gray-50 dark:hover:bg-white/[0.03] transition-colors"
            :aria-expanded="openIdx === i - 1"
          >
            <span class="text-sm sm:text-base font-semibold text-gray-900 dark:text-white">{{ t(`faq.q${i}`) }}</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"
                 class="text-gray-400 transition-transform shrink-0" :class="openIdx === i - 1 && 'rotate-45 text-brand-500'">
              <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
          </button>
          <transition
            enter-active-class="transition duration-300 ease-out"
            enter-from-class="opacity-0 max-h-0"
            enter-to-class="opacity-100 max-h-96"
            leave-active-class="transition duration-200 ease-in"
            leave-from-class="opacity-100 max-h-96"
            leave-to-class="opacity-0 max-h-0"
          >
            <div v-show="openIdx === i - 1" class="overflow-hidden">
              <p class="px-4 sm:px-5 pb-4 sm:pb-5 text-sm text-gray-600 dark:text-gray-300 leading-relaxed">{{ t(`faq.a${i}`) }}</p>
            </div>
          </transition>
        </div>
      </div>
    </section>

    <!-- 6. Why QR Tool Studio -->
    <section id="why" class="scroll-mt-24">
      <div class="relative overflow-hidden glass-panel dark:glass-panel-dark p-8 sm:p-10 noise-bg">
        <div class="absolute -top-20 -right-20 h-60 w-60 rounded-full bg-gradient-to-br from-brand-500/20 to-purple-500/20 blur-3xl pointer-events-none"></div>
        <div class="relative grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
          <div>
            <div class="section-label">{{ t('mkt.why.label') }}</div>
            <h2 class="text-2xl sm:text-3xl font-extrabold mt-2 text-gray-900 dark:text-white leading-tight" v-html="t('mkt.why.title').replace('\n', '<br>')"></h2>
            <p class="mt-4 text-sm sm:text-base text-gray-600 dark:text-gray-300 leading-relaxed">
              {{ t('mkt.why.desc') }}
            </p>
            <a
              v-if="onGoBlog"
              href="#blog"
              @click.prevent="onGoBlog"
              class="mt-5 inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-brand-500 to-purple-500 text-white text-sm font-bold shadow-md shadow-brand-500/30 hover:shadow-lg transition-shadow"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
              </svg>
              Read our guides
              <span class="px-1.5 py-0.5 text-[8px] font-bold rounded bg-white/20">NEW</span>
            </a>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div v-for="i in 4" :key="i"
            class="p-4 rounded-2xl bg-white/60 dark:bg-white/[0.04] border border-gray-200/60 dark:border-white/10">
              <div class="text-sm font-bold text-gray-900 dark:text-white">{{ t(`mkt.why.${i}.t`) }}</div>
              <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">{{ t(`mkt.why.${i}.d`) }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 7. CTA -->
    <section class="text-center pb-4">
      <h2 class="text-2xl sm:text-3xl font-extrabold text-gray-900 dark:text-white">
        {{ t('mkt.cta.title') }}
      </h2>
      <a href="#generator" class="btn-brand mt-6 inline-flex">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        {{ t('mkt.cta.button') }}
      </a>
    </section>
  </div>
</template>
