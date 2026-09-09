<script setup>
import { computed } from 'vue'
import { useI18n } from '../composables/useI18n'
import { openLegal } from '../composables/useLegal'
import { tab } from '../composables/useTab'

defineProps({
  isDark: { type: Boolean, default: false }
})

const { t } = useI18n()
const year = computed(() => new Date().getFullYear())

/**
 * 「批量生成」是首页的一个 Tab，不是独立路由。
 * 在其它页面点击时先回首页再切 Tab，避免为它单独造一个 URL
 * （会造成与首页内容高度重复的 thin page）。
 */
function goBatch() {
  tab.value = 'batch'
}
</script>

<template>
  <footer class="mt-auto border-t border-gray-200/60 dark:border-white/10 bg-white/40 dark:bg-white/[0.02] backdrop-blur">
    <div class="w-full max-w-6xl mx-auto px-4 sm:px-6 py-10 grid grid-cols-2 sm:grid-cols-5 gap-8 text-sm">
      <!-- 品牌区 -->
      <div class="col-span-2 sm:col-span-2">
        <RouterLink to="/" class="flex items-center gap-2 mb-3 group">
          <div class="h-9 w-9 rounded-xl bg-gradient-to-br from-brand-500 to-purple-500 grid place-items-center text-white font-bold shadow-md shadow-brand-500/30">Q</div>
          <div class="leading-tight">
            <div class="font-bold text-gray-900 dark:text-white">QR Tool Studio</div>
            <div class="text-[10px] text-gray-500 dark:text-gray-400">{{ t('footer.brand.sub') }}</div>
          </div>
        </RouterLink>
        <p class="text-xs text-gray-600 dark:text-gray-400 leading-relaxed">
          {{ t('footer.brand.desc') }}
        </p>
      </div>

      <!-- 产品 -->
      <div>
        <h3 class="text-xs font-bold text-gray-700 dark:text-gray-200 uppercase tracking-wider mb-3">{{ t('footer.col.product') }}</h3>
        <ul class="space-y-2 text-xs text-gray-600 dark:text-gray-400">
          <li><RouterLink to="/#generator" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.link.generator') }}</RouterLink></li>
          <li><RouterLink to="/" @click="goBatch" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.link.batch') }}</RouterLink></li>
          <li><RouterLink to="/#how" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.link.how') }}</RouterLink></li>
          <li><RouterLink to="/#types" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.link.types') }}</RouterLink></li>
          <li><RouterLink to="/#use-cases" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.link.usecases') }}</RouterLink></li>
          <li><RouterLink to="/#faq" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.link.faq') }}</RouterLink></li>
          <li>
            <RouterLink to="/blog/" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors inline-flex items-center gap-1.5">
              <span>{{ t('footer.link.blog') || 'Blog' }}</span>
              <span class="inline-block px-1.5 py-0.5 text-[8px] font-bold rounded bg-gradient-to-r from-brand-500 to-purple-500 text-white">NEW</span>
            </RouterLink>
          </li>
        </ul>
      </div>

      <!-- 法律 -->
      <div>
        <h3 class="text-xs font-bold text-gray-700 dark:text-gray-200 uppercase tracking-wider mb-3">{{ t('footer.col.legal') }}</h3>
        <ul class="space-y-2 text-xs text-gray-600 dark:text-gray-400">
          <li><RouterLink to="/privacy/" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.legal.privacy') }}</RouterLink></li>
          <li><RouterLink to="/terms/" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.legal.terms') }}</RouterLink></li>
          <li><button @click="openLegal('disclaimer')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors text-left">{{ t('footer.legal.disclaimer') }}</button></li>
          <li><RouterLink to="/privacy/#cookies" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.legal.cookie') }}</RouterLink></li>
        </ul>
      </div>

      <!-- 关于 -->
      <div>
        <h3 class="text-xs font-bold text-gray-700 dark:text-gray-200 uppercase tracking-wider mb-3">{{ t('footer.col.about') }}</h3>
        <ul class="space-y-2 text-xs text-gray-600 dark:text-gray-400">
          <li><RouterLink to="/about/" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.about.about') }}</RouterLink></li>
          <li><RouterLink to="/contact/" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.about.contact') }}</RouterLink></li>
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

    <!-- 法律信息行 -->
    <div class="border-t border-gray-200/60 dark:border-white/10">
      <div class="w-full max-w-6xl mx-auto px-4 sm:px-6 py-4 flex flex-col gap-3 text-[11px] text-gray-500 dark:text-gray-400">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
          <div class="flex flex-wrap items-center gap-x-3 gap-y-1">
            <span>{{ t('footer.copy', { year }) }}</span>
          </div>
          <div class="flex flex-wrap items-center gap-x-3 gap-y-1">
            <button @click="openLegal('disclaimer')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.legal.disclaimer') }}</button>
            <span>·</span>
            <RouterLink to="/privacy/" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.legal.privacy') }}</RouterLink>
            <span>·</span>
            <RouterLink to="/terms/" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.legal.terms') }}</RouterLink>
            <span>·</span>
            <RouterLink to="/about/" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.about.about') }}</RouterLink>
            <span>·</span>
            <RouterLink to="/contact/" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.about.contact') }}</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>
