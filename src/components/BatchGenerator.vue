<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { batchGenerate, fileToDataURL, downloadBlob } from '../utils/qr.js'

const cfg = reactive({
  text: '',
  margin: 4,
  errorLevel: 'M',
  dotsType: 'rounded',
  dotsColor: '#4f46e5',
  backgroundColor: '#ffffff',
  logoDataUrl: '',
  logoSize: 0.3
})

const busy = ref(false)
const progress = ref(0)
const total = computed(() => cfg.text.split('\n').map(l => l.trim()).filter(Boolean).length)

const onPickLogo = async (e) => {
  const f = e.target.files?.[0]
  if (!f) return
  if (f.size > 2 * 1024 * 1024) { alert('Logo ≤ 2MB'); return }
  cfg.logoDataUrl = await fileToDataURL(f)
}
const removeLogo = () => { cfg.logoDataUrl = '' }

async function generate() {
  if (!total.value) return
  busy.value = true
  progress.value = 0
  try {
    const lines = cfg.text.split('\n').map(l => l.trim()).filter(Boolean)
    const opts = {
      lines,
      margin: cfg.margin,
      errorCorrectionLevel: cfg.errorLevel,
      dotsType: cfg.dotsType,
      dotsColor: cfg.dotsColor,
      backgroundColor: cfg.backgroundColor,
      logoDataUrl: cfg.logoDataUrl,
      logoSize: cfg.logoSize
    }
    const blob = await batchGenerate(opts)
    if (blob) {
      const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19)
      downloadBlob(blob, `qr-batch-${ts}.zip`)
    }
  } catch (e) {
    console.error(e)
    alert('生成失败: ' + (e.message || e))
  } finally {
    busy.value = false
    progress.value = 0
  }
}

const sampleBatch = () => {
  cfg.text = [
    'https://github.com',
    'https://vuejs.org',
    'https://vitejs.dev',
    'https://tailwindcss.com',
    'mailto:hello@example.com?subject=Hi',
    'tel:+8613800000000',
    'WIFI:T:WPA;S:OfficeWiFi;P:Welcome2024;;',
    'BEGIN:VCARD\nVERSION:3.0\nFN:Customer Support\nTEL:+86-400-000-0000\nEND:VCARD'
  ].join('\n')
}

onMounted(() => {
  sampleBatch()
})
</script>

<template>
  <div class="grid grid-cols-1 lg:grid-cols-5 gap-6 animate-slide-up">
    <section class="lg:col-span-3 glass-panel dark:glass-panel-dark p-6 sm:p-8 noise-bg relative">
      <h2 class="text-xl sm:text-2xl font-bold mb-1 text-gray-900 dark:text-white flex items-center gap-2">
        <span class="inline-block h-5 w-1.5 rounded-full bg-gradient-to-b from-brand-500 to-purple-500"></span>
        批量生成
      </h2>
      <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">
        每行一个内容,一次性生成多个二维码并打包为 ZIP
      </p>

      <div class="mb-4">
        <div class="flex items-center justify-between mb-2">
          <label class="text-sm font-semibold text-gray-700 dark:text-gray-200">内容列表</label>
          <span class="text-xs text-gray-500">
            共 <span class="font-bold text-brand-600 dark:text-brand-300">{{ total }}</span> 个待生成
          </span>
        </div>
        <textarea
          v-model="cfg.text"
          rows="9"
          class="input-field resize-y font-mono text-sm"
          placeholder="每行一条内容,例如:&#10;https://example.com&#10;tel:+8613800000000"
        ></textarea>
        <div class="mt-2 flex items-center gap-2 text-xs text-gray-500">
          <button @click="sampleBatch" class="text-brand-600 dark:text-brand-300 hover:underline">填入示例</button>
          <span>·</span>
          <button @click="cfg.text = ''" class="text-rose-500 hover:underline">清空</button>
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-4">
        <div>
          <label class="text-sm font-semibold text-gray-700 dark:text-gray-200 mb-2 block">矩阵样式</label>
          <select v-model="cfg.dotsType" class="select-field">
            <option value="square">方块</option>
            <option value="dots">圆点</option>
            <option value="rounded">圆角</option>
            <option value="classy">极简</option>
            <option value="classy-rounded">圆角曲线</option>
            <option value="extra-rounded">极致圆角</option>
          </select>
        </div>
        <div>
          <label class="text-sm font-semibold text-gray-700 dark:text-gray-200 mb-2 block">主色</label>
          <div class="h-11 rounded-xl overflow-hidden border border-gray-200 dark:border-white/10 bg-white dark:bg-white/[0.04] relative">
            <input type="color" v-model="cfg.dotsColor" class="absolute -top-2 left-0 w-full h-16 cursor-pointer">
            <div class="absolute inset-0 pointer-events-none flex items-center pl-3 text-xs text-gray-500 font-mono">{{ cfg.dotsColor }}</div>
          </div>
        </div>
        <div>
          <label class="text-sm font-semibold text-gray-700 dark:text-gray-200 mb-2 block">纠错</label>
          <select v-model="cfg.errorLevel" class="select-field h-[44px]">
            <option value="L">L · 7%</option>
            <option value="M">M · 15%</option>
            <option value="Q">Q · 25%</option>
            <option value="H">H · 30%</option>
          </select>
        </div>
      </div>

      <div class="p-4 rounded-2xl bg-gray-50/70 dark:bg-white/[0.03] border border-gray-200/60 dark:border-white/10">
        <div class="flex items-center justify-between mb-3">
          <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">统一 Logo (可选)</span>
        </div>
        <div v-if="!cfg.logoDataUrl" class="flex items-center gap-3">
          <label class="btn-ghost cursor-pointer text-sm">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
            选择图片
            <input type="file" accept="image/*" class="hidden" @change="onPickLogo">
          </label>
          <span class="text-xs text-gray-500">所有二维码将使用同一个 Logo</span>
        </div>
        <div v-else class="flex items-center gap-4">
          <img :src="cfg.logoDataUrl" class="h-12 w-12 rounded-xl object-contain bg-white border border-gray-200 dark:border-white/10">
          <div class="flex-1">
            <label class="text-[11px] text-gray-500 dark:text-gray-400 mb-1 block">Logo 大小 {{ Math.round(cfg.logoSize * 100) }}%</label>
            <input type="range" v-model.number="cfg.logoSize" min="0.1" max="0.5" step="0.05">
          </div>
          <button @click="removeLogo" class="btn-ghost text-rose-500 hover:!text-rose-500 hover:!border-rose-300">移除</button>
        </div>
      </div>
    </section>

    <section class="lg:col-span-2 flex flex-col gap-4">
      <div class="qr-preview-card">
        <div class="section-label">摘要</div>
        <div class="mt-3 space-y-2.5 text-sm">
          <div class="flex items-center justify-between">
            <span class="text-gray-500 dark:text-gray-400">总条数</span>
            <span class="font-bold text-gray-900 dark:text-white">{{ total }}</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-gray-500 dark:text-gray-400">单图分辨率</span>
            <span class="font-bold text-gray-900 dark:text-white">600 × 600</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-gray-500 dark:text-gray-400">输出格式</span>
            <span class="font-bold text-gray-900 dark:text-white">ZIP / PNG</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-gray-500 dark:text-gray-400">含 Logo</span>
            <span class="font-bold text-gray-900 dark:text-white">{{ cfg.logoDataUrl ? '是' : '否' }}</span>
          </div>
        </div>
      </div>

      <button
        @click="generate"
        :disabled="busy || total === 0"
        class="btn-brand w-full text-base py-4"
        :class="{ 'opacity-50 cursor-not-allowed': busy || total === 0 }"
      >
        <svg v-if="!busy" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>
        <svg v-else class="animate-spin" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
        {{ busy ? '正在打包...' : '生成并下载 ZIP' }}
      </button>

      <div class="glass-panel dark:glass-panel-dark p-4 text-xs text-gray-600 dark:text-gray-300 leading-relaxed">
        <div class="flex items-start gap-2">
          <span class="mt-0.5 inline-grid place-items-center h-5 w-5 rounded-md bg-amber-100 dark:bg-amber-500/15 text-amber-600 dark:text-amber-300">
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          </span>
          <div>
            建议单个批次不超过 <strong class="text-gray-800 dark:text-gray-100">200 条</strong>,以免浏览器卡顿。所有内容仅在本地生成。
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
