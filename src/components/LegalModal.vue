<script setup>
import { computed } from 'vue'
import { useI18n } from '../composables/useI18n'
import { pickDisclaimer, DISCLAIMER_UPDATED } from '../legal/disclaimer.js'

defineProps({
  open: { type: Boolean, required: true }
})
const emit = defineEmits(['close'])

const { t, lang } = useI18n()

// 免责声明是唯一会被打开的弹窗（页脚 → Disclaimer）。
// 正文是长文法务文案，只维护 en / zh，其余语言回退英文。
const content = computed(() => pickDisclaimer(lang.value))
</script>

<template>
  <transition
    enter-active-class="transition duration-200 ease-out"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition duration-150 ease-in"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div v-if="open" class="fixed inset-0 z-50 grid place-items-center p-4 bg-black/40 backdrop-blur-sm" @click.self="emit('close')">
      <transition
        enter-active-class="transition duration-300 ease-out"
        enter-from-class="opacity-0 scale-95 translate-y-2"
        enter-to-class="opacity-100 scale-100 translate-y-0"
        leave-active-class="transition duration-200 ease-in"
        leave-from-class="opacity-100 scale-100"
        leave-to-class="opacity-0 scale-95"
        appear
      >
        <div class="w-full max-w-2xl max-h-[85vh] flex flex-col glass-panel dark:glass-panel-dark noise-bg overflow-hidden">
          <!-- 头部 -->
          <div class="px-6 sm:px-8 py-5 border-b border-gray-200/60 dark:border-white/10 flex items-start justify-between gap-4">
            <div>
              <div class="text-[10px] font-bold tracking-[0.2em] uppercase text-brand-600 dark:text-brand-300 mb-1.5">{{ content.badge }}</div>
              <h2 class="text-xl sm:text-2xl font-extrabold text-gray-900 dark:text-white">{{ content.title }}</h2>
              <div class="text-xs text-gray-500 dark:text-gray-400 mt-1.5">{{ t('legal.updated', { date: DISCLAIMER_UPDATED }) }}</div>
            </div>
            <button @click="emit('close')" class="theme-toggle-btn !h-9 !w-9 shrink-0" :aria-label="t('legal.closeAria')">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>

          <!-- 内容 -->
          <div class="flex-1 overflow-y-auto px-6 sm:px-8 py-6 space-y-5 prose-content">
            <section v-for="(s, i) in content.sections" :key="i">
              <h3 class="text-sm sm:text-base font-bold text-gray-900 dark:text-white mb-2">{{ s.h }}</h3>
              <div class="text-sm text-gray-700 dark:text-gray-300 leading-relaxed space-y-2" v-html="s.body"></div>
            </section>
            <div v-if="content.tldr" class="mt-6 p-4 rounded-2xl bg-brand-50/80 dark:bg-brand-500/10 border border-brand-200/60 dark:border-brand-500/20 text-sm text-gray-800 dark:text-gray-200" v-html="content.tldr"></div>
          </div>

          <!-- 底部 -->
          <div class="px-6 sm:px-8 py-4 border-t border-gray-200/60 dark:border-white/10 flex items-center justify-between gap-3 bg-white/40 dark:bg-white/[0.02]">
            <span class="text-xs text-gray-500 dark:text-gray-400">{{ t('legal.agree') }}</span>
            <button @click="emit('close')" class="btn-brand text-sm !py-2 !px-4">{{ t('legal.close') }}</button>
          </div>
        </div>
      </transition>
    </div>
  </transition>
</template>

<style scoped>
.prose-content :deep(code) {
  @apply px-1.5 py-0.5 rounded bg-gray-100 dark:bg-white/5 text-[12px] font-mono text-brand-700 dark:text-brand-300;
}
.prose-content :deep(ul) {
  margin-top: 0.25rem;
}
.prose-content :deep(li) {
  font-size: 0.875rem;
  line-height: 1.6;
}
.prose-content :deep(strong) {
  @apply text-gray-900 dark:text-white;
}
</style>
