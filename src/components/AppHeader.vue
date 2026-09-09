<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import ThemeToggle from './ThemeToggle.vue'
import LangSwitcher from './LangSwitcher.vue'
import { useI18n, DEFAULT_LOCALE } from '../composables/useI18n'

const { t } = useI18n()
const route = useRoute()
const lang = computed(() => route.meta?.lang || DEFAULT_LOCALE)
function lp(p) {
  if (lang.value === DEFAULT_LOCALE) return p
  return `/${lang.value}${p === '/' ? '/' : p}`
}

const props = defineProps({
  active: { type: String, required: true },
  view:   { type: String, default: 'home' }
})
const emit = defineEmits(['change', 'goto-blog', 'goto-home'])

// Batch 是独立页面（/batch/），Single / History 仍是首页内 Tab
const tabClass = (isActive) =>
  isActive
    ? 'tab-btn tab-btn-active'
    : 'tab-btn'
</script>

<template>
  <header class="w-full max-w-6xl mx-auto px-4 sm:px-6 pt-6 sm:pt-8">
    <div class="flex items-center justify-between gap-3">
      <!-- Logo -->
      <RouterLink :to="lp('/')" class="flex items-center gap-3 group">
        <div class="relative h-11 w-11 rounded-2xl bg-gradient-to-br from-brand-500 to-purple-500 grid place-items-center shadow-lg shadow-brand-500/30 group-hover:scale-105 transition-transform duration-300">
          <svg viewBox="0 0 64 64" width="26" height="26" class="text-white">
            <rect x="6" y="6" width="20" height="20" rx="3" fill="currentColor" opacity="0.95"/>
            <rect x="12" y="12" width="8" height="8" rx="1" fill="#fff"/>
            <rect x="38" y="6" width="20" height="20" rx="3" fill="currentColor" opacity="0.95"/>
            <rect x="44" y="12" width="8" height="8" rx="1" fill="#fff"/>
            <rect x="6" y="38" width="20" height="20" rx="3" fill="currentColor" opacity="0.95"/>
            <rect x="12" y="44" width="8" height="8" rx="1" fill="#fff"/>
            <rect x="36" y="36" width="6" height="6" rx="1" fill="currentColor"/>
            <rect x="46" y="36" width="6" height="6" rx="1" fill="currentColor"/>
            <rect x="36" y="46" width="6" height="6" rx="1" fill="currentColor"/>
            <rect x="46" y="46" width="6" height="6" rx="1" fill="currentColor"/>
          </svg>
        </div>
        <div class="leading-tight">
          <div class="text-base sm:text-lg font-extrabold tracking-tight text-gray-900 dark:text-white">
            {{ t('brand.name') }} <span class="text-brand-600 dark:text-brand-300">Studio</span>
          </div>
          <div class="text-[11px] text-gray-500 dark:text-gray-400 font-medium">
            {{ t('brand.tagline') }}
          </div>
        </div>
      </RouterLink>

      <!-- 主题切换 + 导航 -->
      <div class="flex items-center gap-2 sm:gap-3">
        <nav v-if="view === 'home' || view === 'batch'" class="hidden sm:flex items-center gap-1 p-1 rounded-2xl bg-white/60 dark:bg-white/[0.04] border border-gray-200/60 dark:border-white/10 backdrop-blur">
          <!-- Single：首页内 Tab -->
          <button
            v-if="view === 'home'"
            @click="emit('change', 'single')"
            :class="tabClass(active === 'single')"
          >{{ t('header.nav.single') }}</button>
          <!-- Batch：独立页面入口 -->
          <RouterLink
            :to="lp('/batch/')"
            :class="tabClass(view === 'batch')"
          >{{ t('header.nav.batch') }}</RouterLink>
          <!-- History：首页内 Tab（本地功能，无独立 URL） -->
          <button
            v-if="view === 'home'"
            @click="emit('change', 'history')"
            :class="tabClass(active === 'history')"
          >{{ t('header.nav.history') }}</button>
        </nav>
        <!-- Blog 入口 -->
        <RouterLink
          :to="lp('/blog/')"
          :class="['inline-flex items-center gap-1.5 px-3 py-1.5 sm:px-4 sm:py-2 rounded-xl text-sm font-semibold transition-all border',
                   view === 'blog-list' || view === 'blog-post'
                     ? 'bg-gradient-to-r from-brand-500 to-purple-500 text-white border-transparent shadow-md shadow-brand-500/30'
                     : 'bg-white/60 dark:bg-white/[0.04] text-gray-700 dark:text-gray-200 border-gray-200/60 dark:border-white/10 hover:border-brand-300 dark:hover:border-brand-500/40 hover:text-brand-600 dark:hover:text-brand-300']"
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
          </svg>
          <span>Blog</span>
          <span v-if="view === 'home'" class="hidden sm:inline-block px-1.5 py-0.5 text-[8px] font-bold rounded bg-gradient-to-r from-brand-500 to-purple-500 text-white">NEW</span>
        </RouterLink>
        <ThemeToggle />
        <LangSwitcher />
      </div>
    </div>

    <!-- 移动端导航 -->
    <nav v-if="view === 'home' || view === 'batch'" class="sm:hidden mt-4 flex items-center gap-1 p-1 rounded-2xl bg-white/60 dark:bg-white/[0.04] border border-gray-200/60 dark:border-white/10 backdrop-blur overflow-x-auto no-scrollbar">
      <button
        v-if="view === 'home'"
        @click="emit('change', 'single')"
        :class="['tab-btn whitespace-nowrap flex-1 text-center', active === 'single' && 'tab-btn-active']"
      >{{ t('header.nav.single') }}</button>
      <RouterLink
        :to="lp('/batch/')"
        :class="['tab-btn whitespace-nowrap flex-1 text-center', view === 'batch' && 'tab-btn-active']"
      >{{ t('header.nav.batch') }}</RouterLink>
      <button
        v-if="view === 'home'"
        @click="emit('change', 'history')"
        :class="['tab-btn whitespace-nowrap flex-1 text-center', active === 'history' && 'tab-btn-active']"
      >{{ t('header.nav.history') }}</button>
    </nav>
  </header>
</template>
