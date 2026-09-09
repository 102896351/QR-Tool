<script setup>
import { computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
import LegalModal from './components/LegalModal.vue'
import { useTheme } from './composables/useTheme'
import { useI18n } from './composables/useI18n'
import { tab } from './composables/useTab'
import { legalOpen, legalType, closeLegal } from './composables/useLegal'

const route = useRoute()
const { isDark } = useTheme()
const { lang, isReady } = useI18n()

/** 当前视图标识（供 Header 决定高亮 / 是否显示生成器 Tab） */
const view = computed(() => route.meta?.view || 'home')

// 从其它页面回到首页时，重置为单张生成 Tab（与原 hash 路由行为一致）
watch(
  () => route.name,
  (name) => {
    if (name === 'home') tab.value = 'single'
  }
)

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

    <LegalModal :open="legalOpen" :type="legalType" @close="closeLegal" />
  </div>
</template>
