<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n, DEFAULT_LOCALE } from '../composables/useI18n'
import { openLegal } from '../composables/useLegal'

defineProps({
  isDark: { type: Boolean, default: false }
})

const { t } = useI18n()
const route = useRoute()
const year = computed(() => new Date().getFullYear())

// 当前语言；无前缀为 en
const lang = computed(() => route.meta?.lang || DEFAULT_LOCALE)

/**
 * 语言感知的内链：en 用裸路径，其它语言加 /zh/ 等前缀。
 * 这样在 /zh/ 页面点 footer 链接不会跳回英文页。
 */
function lp(p) {
  if (lang.value === DEFAULT_LOCALE) return p
  return `/${lang.value}${p === '/' ? '/' : p}`
}
</script>

<template>
  <footer class="mt-auto border-t border-gray-200/60 dark:border-white/10 bg-white/40 dark:bg-white/[0.02] backdrop-blur">
    <div class="w-full max-w-6xl mx-auto px-4 sm:px-6 py-10 grid grid-cols-2 sm:grid-cols-6 gap-8 text-sm">
      <!-- 品牌区 -->
      <div class="col-span-2 sm:col-span-2">
        <RouterLink :to="lp('/')" class="flex items-center gap-2 mb-3 group">
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
          <li><RouterLink :to="lp('/#generator')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.link.generator') }}</RouterLink></li>
          <li><RouterLink :to="lp('/batch/')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.link.batch') }}</RouterLink></li>
          <li><RouterLink :to="lp('/#how')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.link.how') }}</RouterLink></li>
          <li><RouterLink :to="lp('/#types')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.link.types') }}</RouterLink></li>
          <li><RouterLink :to="lp('/#use-cases')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.link.usecases') }}</RouterLink></li>
          <li><RouterLink :to="lp('/#faq')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.link.faq') }}</RouterLink></li>
          <li>
            <RouterLink :to="lp('/blog/')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors inline-flex items-center gap-1.5">
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
          <li><RouterLink :to="lp('/privacy/')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.legal.privacy') }}</RouterLink></li>
          <li><RouterLink :to="lp('/terms/')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.legal.terms') }}</RouterLink></li>
          <li><button @click="openLegal()" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors text-left">{{ t('footer.legal.disclaimer') }}</button></li>
          <li><RouterLink :to="lp('/privacy/#cookies')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.legal.cookie') }}</RouterLink></li>
        </ul>
      </div>

      <!-- 关于 -->
      <div>
        <h3 class="text-xs font-bold text-gray-700 dark:text-gray-200 uppercase tracking-wider mb-3">{{ t('footer.col.about') }}</h3>
        <ul class="space-y-2 text-xs text-gray-600 dark:text-gray-400">
          <li><RouterLink :to="lp('/about/')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.about.about') }}</RouterLink></li>
          <li><RouterLink :to="lp('/contact/')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.about.contact') }}</RouterLink></li>
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

      <!-- 相关站点（兄弟站 dofollow 互链） -->
      <div>
        <h3 class="text-xs font-bold text-gray-700 dark:text-gray-200 uppercase tracking-wider mb-3">{{ t('footer.col.sites') }}</h3>
        <ul class="space-y-2 text-xs text-gray-600 dark:text-gray-400">
          <li>
            <a href="https://aiartspell.art/" target="_blank" rel="noopener" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.sites.aiartspell') }}</a>
          </li>
          <li>
            <a href="https://gonglue.xyz/" target="_blank" rel="noopener" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.sites.gonglue') }}</a>
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
            <button @click="openLegal()" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.legal.disclaimer') }}</button>
            <span>·</span>
            <RouterLink :to="lp('/privacy/')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.legal.privacy') }}</RouterLink>
            <span>·</span>
            <RouterLink :to="lp('/terms/')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.legal.terms') }}</RouterLink>
            <span>·</span>
            <RouterLink :to="lp('/about/')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.about.about') }}</RouterLink>
            <span>·</span>
            <RouterLink :to="lp('/contact/')" class="hover:text-brand-600 dark:hover:text-brand-300 transition-colors">{{ t('footer.about.contact') }}</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>