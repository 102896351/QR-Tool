<script setup>
import { computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
import LegalModal from './components/LegalModal.vue'
import { useTheme } from './composables/useTheme'
import { useI18n, applyLocale, langFromPath } from './composables/useI18n'
import { tab } from './composables/useTab'
import { legalOpen, closeLegal } from './composables/useLegal'

const route = useRoute()
const { isDark } = useTheme()
const { lang, isReady } = useI18n()

/** 当前视图标识（供 Header 决定高亮 / 是否显示生成器 Tab） */
const view = computed(() => route.meta?.view || 'home')

// 从其它页面回到首页时，重置为单张生成 Tab（与原 hash 路由行为一致）。
// 例外：?tab=history 表示用户明确想看历史记录，保留 HomeView 的处理结果。
watch(
  () => route.name,
  (name) => {
    if (name && name.endsWith('-home') && route.query.tab !== 'history') {
      tab.value = 'single'
    }
  }
)

/**
 * 路由语言 ↔ i18n 状态双向同步：
 * - 进入新页面时按 URL 前缀 / meta.lang 强制设定当前语言（覆盖 localStorage）
 * - 第一次 setup 也跑一次 immediate=true，确保 SSR/prebuild 阶段就用正确的字典
 */
function syncLangFromRoute() {
  const code = route.meta?.lang || langFromPath(route.path)
  if (code && code !== lang.value) applyLocale(code)
}

syncLangFromRoute()
watch(() => route.fullPath, syncLangFromRoute)

/** 同步 <html lang>，便于 Google 判断页面语言 */
function applyI18nToHead() {
  if (typeof document === 'undefined') return
  document.documentElement.lang = lang.value
}

onMounted(() => {
  if (isReady.value) applyI18nToHead()
})

watch([lang, isReady], () => applyI18nToHead())
</script>

<template>
  <div class="mesh-bg"></div>

  <div class="min-h-screen flex flex-col">
    <AppHeader :active="tab" :view="view" @change="(v) => tab = v" />

    <!-- 路由视图：每个 URL 渲染不同的组件，构建期各自预渲染成独立 HTML -->
    <RouterView />

    <!-- Footer 全站常驻：为 Google 提供稳定的站内链接发现路径 -->
    <AppFooter :is-dark="isDark" />

    <LegalModal :open="legalOpen" @close="closeLegal" />
  </div>
</template>