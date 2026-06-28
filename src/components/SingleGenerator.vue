<script setup>
import { ref, reactive, watch, onMounted, onBeforeUnmount, computed, nextTick } from 'vue'
import QRCodeStyling from 'qr-code-styling'
import { useI18n } from '../composables/useI18n'

const { t } = useI18n()
import { qrInstanceToBlob, fileToDataURL, downloadBlob, detectContentType } from '../utils/qr.js'
import { saveHistoryItem } from '../utils/history.js'

const props = defineProps({
  initialText: { type: String, default: '' }
})
const emit = defineEmits(['saved'])

// ====== 配置状态 ======
const cfg = reactive({
  text: props.initialText,
  size: 320,                // 预览尺寸
  margin: 4,
  errorLevel: 'M',          // L/M/Q/H
  dotsType: 'square',       // 默认:经典方块
  dotsColor: '#000000',     // 默认:纯黑
  dotsGradient: false,
  dotsGradientType: 'linear', // linear | radial
  dotsColor2: '#a855f7',
  dotsGradientRotate: 45,
  cornersType: 'square',    // 默认:方框定位眼
  cornersColor: '#000000',
  cornersGradient: false,
  cornersColor2: '#a855f7',
  bgColor: '#ffffff',
  bgTransparent: false,
  logoDataUrl: '',
  logoSize: 0.3,            // 0.1 - 0.5
  logoMargin: 6
})

const qrContainer = ref(null)
const qrCode = ref(null)
const detected = computed(() => detectContentType(cfg.text))
const canExport = computed(() => cfg.text.trim().length > 0)
const detectedLabel = computed(() => {
  const map = {
    empty: t('gen.preview.empty'),
    url: t('gen.preview.url'),
    text: t('gen.preview.text'),
    email: t('gen.preview.email'),
    tel: t('gen.preview.phone'),
    sms: t('gen.preview.sms'),
    wifi: t('gen.preview.wifi'),
    vcard: t('gen.preview.vcard')
  }
  return map[detected.value.type] || detected.value.label
})

// 实时状态(节流)
let updateTimer = null
function scheduleUpdate() {
  if (updateTimer) clearTimeout(updateTimer)
  updateTimer = setTimeout(() => doUpdate(), 60)
}

function buildOptions() {
  const o = {
    width: cfg.size,
    height: cfg.size,
    type: 'canvas',
    data: cfg.text || ' ',
    margin: cfg.margin,
    qrOptions: { errorCorrectionLevel: cfg.errorLevel },
    dotsOptions: {
      type: cfg.dotsType,
      ...(cfg.dotsGradient
        ? {
            gradient: {
              type: cfg.dotsGradientType,
              rotation: (cfg.dotsGradientRotate * Math.PI) / 180,
              colorStops: [
                { offset: 0, color: cfg.dotsColor },
                { offset: 1, color: cfg.dotsColor2 }
              ]
            }
          }
        : { color: cfg.dotsColor })
    },
    cornersSquareOptions: {
      type: cfg.cornersType,
      ...(cfg.cornersGradient
        ? {
            gradient: {
              type: cfg.dotsGradientType,
              rotation: (cfg.dotsGradientRotate * Math.PI) / 180,
              colorStops: [
                { offset: 0, color: cfg.cornersColor },
                { offset: 1, color: cfg.cornersColor2 }
              ]
            }
          }
        : { color: cfg.cornersColor })
    },
    cornersDotOptions: {
      ...(cfg.cornersGradient
        ? {
            gradient: {
              type: cfg.dotsGradientType,
              rotation: (cfg.dotsGradientRotate * Math.PI) / 180,
              colorStops: [
                { offset: 0, color: cfg.cornersColor },
                { offset: 1, color: cfg.cornersColor2 }
              ]
            }
          }
        : { color: cfg.cornersColor })
    },
    backgroundOptions: { color: cfg.bgTransparent ? '#ffffff00' : cfg.bgColor },
    image: cfg.logoDataUrl || undefined,
    imageOptions: {
      crossOrigin: 'anonymous',
      margin: cfg.logoMargin,
      imageSize: cfg.logoSize,
      hideBackgroundDots: true
    }
  }
  return o
}

function doUpdate() {
  if (!qrCode.value) return
  try {
    qrCode.value.update(buildOptions())
  } catch (e) {
    console.warn('[qr update]', e)
  }
}

// 监听所有字段
watch(cfg, () => scheduleUpdate(), { deep: true })

// 监听外部清空
function resetAll() {
  cfg.text = ''
  cfg.dotsType = 'square'
  cfg.dotsColor = '#000000'
  cfg.dotsGradient = false
  cfg.cornersType = 'square'
  cfg.bgColor = '#ffffff'
  cfg.bgTransparent = false
  cfg.logoDataUrl = ''
  cfg.size = 320
  cfg.margin = 4
  cfg.errorLevel = 'M'
}

async function onPickLogo(e) {
  const f = e.target.files?.[0]
  if (!f) return
  if (f.size > 2 * 1024 * 1024) {
    alert('Logo file must be smaller than 2MB')
    return
  }
  cfg.logoDataUrl = await fileToDataURL(f)
}

function removeLogo() { cfg.logoDataUrl = '' }

// 模板预设
const presets = [
  { name: '品牌渐变', dotsColor: '#4f46e5', color2: '#a855f7', gradient: true, type: 'rounded', corners: 'extra-rounded' },
  { name: '纯净黑白', dotsColor: '#111827', color2: '#111827', gradient: false, type: 'square', corners: 'square' },
  { name: '夏日阳光', dotsColor: '#f59e0b', color2: '#ef4444', gradient: true, type: 'rounded', corners: 'extra-rounded' },
  { name: '森林清新', dotsColor: '#10b981', color2: '#0ea5e9', gradient: true, type: 'classy-rounded', corners: 'classy-rounded' },
  { name: '樱花粉',   dotsColor: '#ec4899', color2: '#f43f5e', gradient: true, type: 'dots', corners: 'dot' },
  { name: '深海蓝',   dotsColor: '#1e3a8a', color2: '#0ea5e9', gradient: true, type: 'classy', corners: 'extra-rounded' }
]

// 预设名 i18n key 映射
const presetKeyMap = {
  '品牌渐变': 'preset.brand',
  '纯净黑白': 'preset.mono',
  '夏日阳光': 'preset.sunshine',
  '森林清新': 'preset.forest',
  '樱花粉': 'preset.cherry',
  '深海蓝': 'preset.deepsea'
}
const tPreset = (name) => t(presetKeyMap[name] || name)
function applyPreset(p) {
  cfg.dotsColor = p.dotsColor
  cfg.dotsColor2 = p.color2
  cfg.dotsGradient = p.gradient
  cfg.dotsType = p.type
  cfg.cornersType = p.corners
  cfg.cornersColor = p.dotsColor
  cfg.cornersColor2 = p.color2
  cfg.cornersGradient = p.gradient
}

// 下载
const exporting = ref({ png: false, svg: false, jpeg: false })

async function exportAs(format) {
  if (!canExport.value) return
  exporting.value[format] = true
  try {
    // 用高分辨率实例导出
    const HiQR = new QRCodeStyling({
      ...buildOptions(),
      width: 1024,
      height: 1024
    })
    const blob = await HiQR.getRawData(format === 'jpeg' ? 'jpeg' : format)
    if (!blob) throw new Error('导出失败')
    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19)
    const safeName = (cfg.text.trim() || 'qrcode').replace(/[\\/:*?"<>|\s]/g, '_').slice(0, 24)
    downloadBlob(blob, `qr-${safeName}-${ts}.${format}`)

    // 保存到历史
    const list = saveHistoryItem({
      id: Date.now() + '-' + Math.random().toString(36).slice(2, 6),
      text: cfg.text,
      size: cfg.size,
      dotsType: cfg.dotsType,
      dotsColor: cfg.dotsColor,
      errorLevel: cfg.errorLevel,
      hasLogo: !!cfg.logoDataUrl
    })
    emit('saved', list)
  } catch (e) {
    console.error(e)
    alert('Export failed: ' + (e.message || e))
  } finally {
    exporting.value[format] = false
  }
}

// 复制到剪贴板
const copyState = ref('idle') // idle | ok | err
async function copyImage() {
  if (!canExport.value) return
  try {
    const HiQR = new QRCodeStyling({
      ...buildOptions(),
      width: 1024,
      height: 1024
    })
    const blob = await HiQR.getRawData('png')
    if (!navigator.clipboard || !window.ClipboardItem) throw new Error('浏览器不支持剪贴板图片')
    await navigator.clipboard.write([new ClipboardItem({ 'image/png': blob })])
    copyState.value = 'ok'
    setTimeout(() => (copyState.value = 'idle'), 1500)
  } catch (e) {
    console.warn(e)
    copyState.value = 'err'
    setTimeout(() => (copyState.value = 'idle'), 1800)
  }
}

// 模板:Wi-Fi / 邮箱 / 电话 - 默认展开
const showTemplates = ref(true)
function fillTemplate(kind) {
  if (kind === 'url') cfg.text = 'https://example.com'
  if (kind === 'email') cfg.text = 'mailto:hello@example.com?subject=Hello'
  if (kind === 'tel') cfg.text = 'tel:+8613800000000'
  if (kind === 'sms') cfg.text = 'sms:+8613800000000?body=Hello'
  if (kind === 'wifi') cfg.text = 'WIFI:T:WPA;S:YourWiFi;P:password;;'
  if (kind === 'vcard') cfg.text = 'BEGIN:VCARD\nVERSION:3.0\nFN:张三\nTEL:+8613800000000\nEMAIL:zhangsan@example.com\nORG:Example Co.\nEND:VCARD'
  if (kind === 'text') cfg.text = 'Hello, 这是一段纯文本内容。'
  // 模板面板常驻展开,不再自动收起
}

// 尺寸范围滑块的 CSS 变量
function syncRange(el) {
  const min = Number(el.min || 0), max = Number(el.max || 100), val = Number(el.value)
  const pct = ((val - min) / (max - min)) * 100
  el.style.setProperty('--val', pct + '%')
}
function bindRanges(root) {
  if (!root) return
  root.querySelectorAll('input[type=range]').forEach(syncRange)
}

onMounted(async () => {
  await nextTick()
  qrCode.value = new QRCodeStyling({
    ...buildOptions(),
    width: cfg.size,
    height: cfg.size
  })
  qrCode.value.append(qrContainer.value)
  bindRanges(document)
})

onBeforeUnmount(() => {
  if (updateTimer) clearTimeout(updateTimer)
})
</script>

<template>
  <div class="grid grid-cols-1 lg:grid-cols-5 gap-6 animate-slide-up">
    <!-- 左侧:配置面板 -->
    <section class="lg:col-span-3 glass-panel dark:glass-panel-dark p-6 sm:p-8 noise-bg relative">
      <h2 class="text-xl sm:text-2xl font-bold mb-1 text-gray-900 dark:text-white flex items-center gap-2">
        <span class="inline-block h-5 w-1.5 rounded-full bg-gradient-to-b from-brand-500 to-purple-500"></span>
        {{ t('gen.section.config') }}
      </h2>
      <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">
        {{ t('gen.section.config.sub') }}
      </p>

      <!-- 内容输入 -->
      <div class="mb-5">
        <div class="flex items-center justify-between mb-2">
          <label class="text-sm font-semibold text-gray-700 dark:text-gray-200">{{ t('gen.label.content') }}</label>
          <div class="flex items-center gap-2">
            <span v-if="cfg.text.trim()" class="text-[11px] px-2 py-0.5 rounded-full font-medium bg-brand-50 text-brand-700 dark:bg-brand-500/15 dark:text-brand-200">
              {{ detectedLabel }}
            </span>
          </div>
        </div>
        <textarea
          v-model="cfg.text"
          rows="3"
          class="input-field resize-y"
          :placeholder="t('gen.placeholder')"
        ></textarea>

        <!-- 模板下拉 -->
        <transition
          enter-active-class="transition duration-200 ease-out"
          enter-from-class="opacity-0 -translate-y-1"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition duration-150 ease-in"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
        >
          <div v-if="showTemplates" class="mt-2 p-2 rounded-xl bg-gray-50 dark:bg-white/[0.04] border border-gray-200/70 dark:border-white/10 grid grid-cols-2 sm:grid-cols-4 gap-1.5">
            <button v-for="k in ['url','email','tel','sms','wifi','vcard','text']" :key="k"
                    @click="fillTemplate(k)"
                    class="text-xs px-2 py-1.5 rounded-lg bg-white dark:bg-white/[0.04] border border-gray-200 dark:border-white/10 hover:border-brand-400 hover:text-brand-600 dark:hover:text-brand-300 transition">
              {{ t('tmpl.' + k) }}
            </button>
          </div>
        </transition>
      </div>

      <!-- 风格预设 -->
      <div class="mb-6">
        <label class="section-label">{{ t('gen.label.preset') }}</label>
        <div class="mt-2 flex flex-wrap gap-2">
          <button
            v-for="p in presets" :key="p.name"
            @click="applyPreset(p)"
            class="group flex items-center gap-2 pl-2 pr-3 py-1.5 rounded-full bg-white dark:bg-white/[0.04] border border-gray-200 dark:border-white/10 hover:border-brand-400 transition text-xs"
          >
            <span class="inline-block w-4 h-4 rounded-md border border-black/5"
                  :style="{ background: p.gradient ? `linear-gradient(135deg, ${p.dotsColor}, ${p.color2})` : p.dotsColor }"></span>
            <span class="font-medium text-gray-700 dark:text-gray-200 group-hover:text-brand-600 dark:group-hover:text-brand-300">{{ tPreset(p.name) }}</span>
          </button>
        </div>
      </div>

      <!-- 矩阵点样式 -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-5">
        <div>
          <label class="text-sm font-semibold text-gray-700 dark:text-gray-200 mb-2 block">{{ t('gen.label.dotsType') }}</label>
          <select v-model="cfg.dotsType" class="select-field">
            <option value="square">{{ t('gen.dots.square') }}</option>
            <option value="dots">{{ t('gen.dots.dots') }}</option>
            <option value="rounded">{{ t('gen.dots.rounded') }}</option>
            <option value="classy">{{ t('gen.dots.classy') }}</option>
            <option value="classy-rounded">{{ t('gen.dots.classyRounded') }}</option>
            <option value="extra-rounded">{{ t('gen.dots.extraRounded') }}</option>
          </select>
        </div>
        <div>
          <label class="text-sm font-semibold text-gray-700 dark:text-gray-200 mb-2 block">{{ t('gen.label.cornersType') }}</label>
          <select v-model="cfg.cornersType" class="select-field">
            <option value="square">{{ t('gen.corners.square') }}</option>
            <option value="dot">{{ t('gen.corners.dot') }}</option>
            <option value="extra-rounded">{{ t('gen.corners.extraRounded') }}</option>
            <option value="classy">{{ t('gen.corners.classy') }}</option>
            <option value="classy-rounded">{{ t('gen.corners.classyRounded') }}</option>
          </select>
        </div>
      </div>

      <!-- 颜色 -->
      <div class="mb-5 p-4 rounded-2xl bg-gray-50/70 dark:bg-white/[0.03] border border-gray-200/60 dark:border-white/10">
        <div class="flex items-center justify-between mb-3">
          <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">{{ t('gen.label.color') }}</span>
          <label class="flex items-center gap-2 text-xs cursor-pointer">
            <input type="checkbox" v-model="cfg.dotsGradient" class="accent-brand-500">
            <span class="text-gray-600 dark:text-gray-300">{{ t('gen.label.useGradient') }}</span>
          </label>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="text-[11px] text-gray-500 dark:text-gray-400 mb-1 block">{{ t('gen.label.primary') }}</label>
            <div class="h-11 rounded-xl overflow-hidden border border-gray-200 dark:border-white/10 bg-white dark:bg-white/[0.04] relative">
              <input type="color" v-model="cfg.dotsColor" class="absolute -top-2 left-0 w-full h-16 cursor-pointer">
              <div class="absolute inset-0 pointer-events-none flex items-center pl-3 text-xs text-gray-500 font-mono">
                {{ cfg.dotsColor }}
              </div>
            </div>
          </div>
          <div v-if="cfg.dotsGradient">
            <label class="text-[11px] text-gray-500 dark:text-gray-400 mb-1 block">{{ t('gen.label.secondary') }}</label>
            <div class="h-11 rounded-xl overflow-hidden border border-gray-200 dark:border-white/10 bg-white dark:bg-white/[0.04] relative">
              <input type="color" v-model="cfg.dotsColor2" class="absolute -top-2 left-0 w-full h-16 cursor-pointer">
              <div class="absolute inset-0 pointer-events-none flex items-center pl-3 text-xs text-gray-500 font-mono">
                {{ cfg.dotsColor2 }}
              </div>
            </div>
          </div>
          <div v-if="cfg.dotsGradient">
            <label class="text-[11px] text-gray-500 dark:text-gray-400 mb-1 block">{{ t('gen.label.gradientType') }}</label>
            <select v-model="cfg.dotsGradientType" class="select-field h-11">
              <option value="linear">{{ t('gen.label.gradientLinear') }}</option>
              <option value="radial">{{ t('gen.label.gradientRadial') }}</option>
            </select>
          </div>
          <div v-if="cfg.dotsGradient">
            <label class="text-[11px] text-gray-500 dark:text-gray-400 mb-1 block">{{ t('gen.label.rotate') }} {{ cfg.dotsGradientRotate }}°</label>
            <input type="range" v-model.number="cfg.dotsGradientRotate" min="0" max="360" step="5" @input="syncRange($event.target)">
          </div>
        </div>
      </div>

      <!-- 背景色 -->
      <div class="mb-5 p-4 rounded-2xl bg-gray-50/70 dark:bg-white/[0.03] border border-gray-200/60 dark:border-white/10">
        <div class="flex items-center justify-between mb-3">
          <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">{{ t('gen.label.bg') }}</span>
          <label class="flex items-center gap-2 text-xs cursor-pointer">
            <input type="checkbox" v-model="cfg.bgTransparent" class="accent-brand-500">
            <span class="text-gray-600 dark:text-gray-300">{{ t('gen.label.transparent') }}</span>
          </label>
        </div>
        <div v-if="!cfg.bgTransparent" class="flex items-center gap-3">
          <div class="h-11 w-20 rounded-xl overflow-hidden border border-gray-200 dark:border-white/10 bg-white relative">
            <input type="color" v-model="cfg.bgColor" class="absolute -top-2 left-0 w-full h-16 cursor-pointer">
          </div>
          <div class="flex flex-wrap gap-1.5">
            <button v-for="c in ['#ffffff','#f3f4f6','#fef3c7','#dbeafe','#dcfce7','#fce7f3','#111827']"
                    :key="c"
                    @click="cfg.bgColor = c"
                    class="w-7 h-7 rounded-lg border border-gray-200 dark:border-white/10 transition hover:scale-110"
                    :style="{ background: c }"></button>
          </div>
        </div>
      </div>

      <!-- 尺寸 / 边距 / 纠错 -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-5">
        <div>
          <label class="text-sm font-semibold text-gray-700 dark:text-gray-200 mb-2 flex items-center justify-between">
            <span>{{ t('gen.label.size') }}</span>
            <span class="text-xs text-gray-500 font-mono">{{ cfg.size }}px</span>
          </label>
          <input type="range" v-model.number="cfg.size" min="160" max="600" step="10" @input="syncRange($event.target)">
        </div>
        <div>
          <label class="text-sm font-semibold text-gray-700 dark:text-gray-200 mb-2 flex items-center justify-between">
            <span>{{ t('gen.label.margin') }}</span>
            <span class="text-xs text-gray-500 font-mono">{{ cfg.margin }}</span>
          </label>
          <input type="range" v-model.number="cfg.margin" min="0" max="10" step="1" @input="syncRange($event.target)">
        </div>
        <div>
          <label class="text-sm font-semibold text-gray-700 dark:text-gray-200 mb-2 block">{{ t('gen.label.errorLevel') }}</label>
          <select v-model="cfg.errorLevel" class="select-field h-[26px]">
            <option value="L">L · 7%</option>
            <option value="M">M · 15%</option>
            <option value="Q">Q · 25%</option>
            <option value="H">H · 30%</option>
          </select>
        </div>
      </div>

      <!-- Logo 上传 -->
      <div class="p-4 rounded-2xl bg-gray-50/70 dark:bg-white/[0.03] border border-gray-200/60 dark:border-white/10">
        <div class="flex items-center justify-between mb-3">
          <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">{{ t('gen.label.logo') }}</span>
          <span v-if="cfg.logoDataUrl" class="text-xs text-gray-500">{{ t('gen.action.upload') }}ed</span>
        </div>
        <div v-if="!cfg.logoDataUrl" class="flex items-center gap-3">
          <label class="btn-ghost cursor-pointer text-sm">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
            {{ t('gen.action.upload') }}
            <input type="file" accept="image/*" class="hidden" @change="onPickLogo">
          </label>
          <span class="text-xs text-gray-500">PNG / JPG / SVG · ≤ 2MB</span>
        </div>
        <div v-else class="flex items-center gap-4">
          <img :src="cfg.logoDataUrl" class="h-14 w-14 rounded-xl object-contain bg-white border border-gray-200 dark:border-white/10" alt="logo">
          <div class="flex-1">
            <label class="text-[11px] text-gray-500 dark:text-gray-400 mb-1 block">Logo 大小 {{ Math.round(cfg.logoSize * 100) }}%</label>
            <input type="range" v-model.number="cfg.logoSize" min="0.1" max="0.5" step="0.05" @input="syncRange($event.target)">
          </div>
          <button @click="removeLogo" class="btn-ghost text-rose-500 hover:!text-rose-500 hover:!border-rose-300">移除</button>
        </div>
      </div>
    </section>

    <!-- 右侧:实时预览 -->
    <section class="lg:col-span-2 flex flex-col gap-4">
      <div class="qr-preview-card animate-float">
        <div class="flex items-center justify-between mb-4">
          <div>
            <div class="section-label">{{ t('gen.preview.title') }}</div>
            <div class="text-sm text-gray-500 dark:text-gray-400 mt-1 font-medium">{{ t('gen.preview.sub') }}</div>
          </div>
          <button @click="resetAll" class="btn-ghost text-xs" :title="t('gen.action.reset')">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg>
            {{ t('gen.action.reset') }}
          </button>
        </div>
        <div
          id="qr-preview"
          ref="qrContainer"
          class="rounded-2xl flex items-center justify-center transition-all duration-300"
          :class="cfg.bgTransparent ? 'bg-[conic-gradient(at_50%_50%,#eef2ff_0deg,#fdf4ff_90deg,#ecfeff_180deg,#fef9c3_270deg,#eef2ff_360deg)] dark:bg-[conic-gradient(at_50%_50%,#1e1b4b_0deg,#4c1d95_90deg,#0c4a6e_180deg,#0f172a_270deg,#1e1b4b_360deg)]' : 'bg-white'"
          :style="{ minHeight: (cfg.size + 32) + 'px' }"
        ></div>
      </div>

      <!-- 操作按钮 -->
      <div class="grid grid-cols-2 gap-3">
        <button @click="exportAs('png')" :disabled="!canExport" class="btn-brand" :class="{ 'opacity-50 cursor-not-allowed': !canExport }">
          <svg v-if="!exporting.png" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          <svg v-else class="animate-spin" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
          {{ t('gen.btn.png') }}
        </button>
        <button @click="exportAs('svg')" :disabled="!canExport" class="btn-ghost" :class="{ 'opacity-50 cursor-not-allowed': !canExport }">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
          {{ t('gen.btn.svg') }}
        </button>
        <button @click="exportAs('jpeg')" :disabled="!canExport" class="btn-ghost" :class="{ 'opacity-50 cursor-not-allowed': !canExport }">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
          {{ t('gen.btn.jpeg') }}
        </button>
        <button @click="copyImage" :disabled="!canExport" class="btn-ghost" :class="{ 'opacity-50 cursor-not-allowed': !canExport, '!text-emerald-600 !border-emerald-300 dark:!text-emerald-300 dark:!border-emerald-500/40': copyState === 'ok', '!text-rose-500 !border-rose-300 dark:!text-rose-300': copyState === 'err' }">
          <svg v-if="copyState === 'idle'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
          <svg v-else-if="copyState === 'ok'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
          {{ copyState === 'ok' ? t('gen.btn.copied') : copyState === 'err' ? t('gen.btn.copyFailed') : t('gen.btn.copy') }}
        </button>
      </div>

      <!-- 提示卡 -->
      <div class="glass-panel dark:glass-panel-dark p-4 text-xs text-gray-600 dark:text-gray-300 leading-relaxed">
        <div class="flex items-start gap-2">
          <span class="mt-0.5 inline-grid place-items-center h-5 w-5 rounded-md bg-emerald-100 dark:bg-emerald-500/15 text-emerald-600 dark:text-emerald-300">
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
          </span>
          <div>
            <strong class="text-gray-800 dark:text-gray-100">Tip</strong> · {{ t('gen.tip') }} <code class="px-1 py-0.5 rounded bg-gray-100 dark:bg-white/5">{{ t('gen.tip.h') }}</code> {{ t('gen.tip.after') }}
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
