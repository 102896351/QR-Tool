<script setup>
import { computed } from 'vue'
import { useTheme } from '../composables/useTheme'
import { useI18n } from '../composables/useI18n'

const { theme, isDark, cycleTheme } = useTheme()
const { t } = useI18n()

// 主题按钮的 tooltip / 无障碍文案走字典，避免非中文页面出现中文字符
const label = computed(() => {
  if (theme.value === 'light') return t('theme.current', { mode: t('theme.light') })
  if (theme.value === 'dark') return t('theme.current', { mode: t('theme.dark') })
  return t('theme.current', { mode: t('theme.system') })
})
</script>

<template>
  <button
    @click="cycleTheme"
    :title="label"
    :aria-label="t('theme.aria')"
    class="theme-toggle-btn"
  >
    <!-- 太阳 -->
    <svg v-if="isDark" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="4"/>
      <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>
    </svg>
    <!-- 月亮 -->
    <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
    </svg>
    <span class="sr-only">{{ label }}</span>
  </button>
</template>
