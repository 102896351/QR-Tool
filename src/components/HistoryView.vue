<script setup>
import { ref, onMounted } from 'vue'
import { loadHistory, clearHistory, removeHistoryItem } from '../utils/history.js'

const emit = defineEmits(['apply', 'rebuild'])
const list = ref([])

function refresh() {
  list.value = loadHistory()
}

onMounted(refresh)

function fmtTime(t) {
  const d = new Date(t)
  const now = new Date()
  const diff = (now - d) / 1000
  if (diff < 60) return '刚刚'
  if (diff < 3600) return Math.floor(diff / 60) + ' 分钟前'
  if (diff < 86400) return Math.floor(diff / 3600) + ' 小时前'
  if (diff < 604800) return Math.floor(diff / 86400) + ' 天前'
  return d.toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

function applyItem(item) {
  emit('apply', item)
}

function del(id) {
  list.value = removeHistoryItem(id)
}

function clear() {
  if (confirm('确认清空所有历史记录?')) {
    clearHistory()
    list.value = []
  }
}

const dotsTypeMap = {
  square: '方块', dots: '圆点', rounded: '圆角',
  classy: '极简', 'classy-rounded': '圆角曲线', 'extra-rounded': '极致圆角'
}
</script>

<template>
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-slide-up">
    <section class="lg:col-span-2 glass-panel dark:glass-panel-dark p-6 sm:p-8 noise-bg relative">
      <div class="flex items-start justify-between gap-3">
        <div>
          <h2 class="text-xl sm:text-2xl font-bold mb-1 text-gray-900 dark:text-white flex items-center gap-2">
            <span class="inline-block h-5 w-1.5 rounded-full bg-gradient-to-b from-brand-500 to-purple-500"></span>
            历史记录
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-400">最近 10 次配置,仅存储在你的浏览器中</p>
        </div>
        <button v-if="list.length" @click="clear" class="btn-ghost text-xs text-rose-500 hover:!text-rose-500 hover:!border-rose-300">清空全部</button>
      </div>

      <div class="mt-6 space-y-2.5">
        <transition-group
          enter-active-class="transition duration-300"
          enter-from-class="opacity-0 -translate-y-1"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition duration-200 absolute"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
        >
          <div
            v-for="item in list"
            :key="item.id"
            class="group relative flex items-center gap-4 p-4 rounded-2xl bg-white/70 dark:bg-white/[0.04] border border-gray-200/60 dark:border-white/10 hover:border-brand-300 dark:hover:border-brand-500/40 hover:shadow-md transition-all"
          >
            <!-- 色块标识 -->
            <div class="shrink-0 h-12 w-12 rounded-xl grid place-items-center"
                 :style="{ background: item.dotsColor }">
              <svg width="20" height="20" viewBox="0 0 24 24" class="text-white">
                <rect x="2" y="2" width="8" height="8" rx="1" fill="currentColor"/>
                <rect x="14" y="2" width="8" height="8" rx="1" fill="currentColor"/>
                <rect x="2" y="14" width="8" height="8" rx="1" fill="currentColor"/>
                <rect x="14" y="14" width="4" height="4" fill="currentColor"/>
                <rect x="20" y="14" width="2" height="2" fill="currentColor"/>
                <rect x="14" y="20" width="2" height="2" fill="currentColor"/>
              </svg>
            </div>

            <div class="flex-1 min-w-0">
              <div class="text-sm font-medium text-gray-900 dark:text-white truncate" :title="item.text">
                {{ item.text }}
              </div>
              <div class="text-xs text-gray-500 dark:text-gray-400 mt-0.5 flex flex-wrap items-center gap-x-3">
                <span>{{ fmtTime(item.at) }}</span>
                <span>·</span>
                <span>{{ dotsTypeMap[item.dotsType] || item.dotsType }}</span>
                <span>·</span>
                <span>纠错 {{ item.errorLevel }}</span>
                <span v-if="item.hasLogo">· 含 Logo</span>
              </div>
            </div>

            <div class="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
              <button @click="applyItem(item)" class="btn-ghost text-xs !py-1.5 !px-3">应用</button>
              <button @click="del(item.id)" class="btn-ghost text-xs !py-1.5 !px-3 !text-rose-500 hover:!text-rose-500 hover:!border-rose-300">删除</button>
            </div>
          </div>
        </transition-group>

        <div v-if="!list.length" class="py-16 text-center text-sm text-gray-500 dark:text-gray-400">
          <div class="inline-grid place-items-center h-14 w-14 rounded-2xl bg-gray-100 dark:bg-white/5 mb-3 text-gray-400">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          </div>
          暂无历史记录
          <div class="text-xs text-gray-400 mt-1">生成二维码后会自动保存到这里</div>
        </div>
      </div>
    </section>

    <section class="lg:col-span-1 flex flex-col gap-4">
      <div class="glass-panel dark:glass-panel-dark p-6">
        <div class="section-label">使用提示</div>
        <ul class="mt-3 space-y-2.5 text-sm text-gray-700 dark:text-gray-300">
          <li class="flex items-start gap-2">
            <span class="mt-1.5 h-1.5 w-1.5 rounded-full bg-brand-500 shrink-0"></span>
            点击 <strong>应用</strong> 可将该配置快速载入生成器
          </li>
          <li class="flex items-start gap-2">
            <span class="mt-1.5 h-1.5 w-1.5 rounded-full bg-brand-500 shrink-0"></span>
            历史仅保存在本地,可随时一键清空
          </li>
          <li class="flex items-start gap-2">
            <span class="mt-1.5 h-1.5 w-1.5 rounded-full bg-brand-500 shrink-0"></span>
            最多保存最近 10 条记录,按时间倒序
          </li>
        </ul>
      </div>
    </section>
  </div>
</template>
