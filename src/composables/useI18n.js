/**
 * i18n 国际化(composable 风格,极简自研)
 * 支持 7 种语言,默认英文。
 *
 * 关键设计：
 * - 7 个字典全部静态 import → 构建期就能直接渲染对应语言，避免「点 ZH 还是英文」
 * - 路由前缀决定当前语言（meta.lang）→ 切换语言 = 切换 URL，不是仅改 JS state
 * - 提供 langFromPath / pathForLang 给 LangSwitcher 用于跳转
 */
import { ref, computed, watch } from 'vue'
import enMessages from './locales/en.js'
import zhMessages from './locales/zh.js'
import jaMessages from './locales/ja.js'
import koMessages from './locales/ko.js'
import frMessages from './locales/fr.js'
import deMessages from './locales/de.js'
import esMessages from './locales/es.js'

export const SUPPORTED = [
  { code: 'en', label: 'English',  flag: '🇺🇸' },
  { code: 'zh', label: '中文',      flag: '🇨🇳' },
  { code: 'ja', label: '日本語',     flag: '🇯🇵' },
  { code: 'ko', label: '한국어',     flag: '🇰🇷' },
  { code: 'fr', label: 'Français', flag: '🇫🇷' },
  { code: 'de', label: 'Deutsch',  flag: '🇩🇪' },
  { code: 'es', label: 'Español',  flag: '🇪🇸' }
]

export const LOCALE_CODES = SUPPORTED.map((s) => s.code)
export const DEFAULT_LOCALE = 'en'

const dicts = {
  en: enMessages,
  zh: zhMessages,
  ja: jaMessages,
  ko: koMessages,
  fr: frMessages,
  de: deMessages,
  es: esMessages
}

// 单例：当前语言。初始默认 en，由路由 guard 在 App.vue 里覆盖。
const current = ref(DEFAULT_LOCALE)
const messages = ref(enMessages)

export function applyLocale(code) {
  if (!dicts[code]) return false
  current.value = code
  messages.value = dicts[code]
  if (typeof document !== 'undefined') document.documentElement.lang = code
  if (typeof localStorage !== 'undefined') {
    try { localStorage.setItem('qr-lang', code) } catch (e) {}
  }
  return true
}

/** 从路径里抽语言代码；没有前缀则返回默认 en */
export function langFromPath(path) {
  if (!path) return DEFAULT_LOCALE
  const m = path.match(/^\/(en|zh|ja|ko|fr|de|es)(?:\/|$)/)
  return m ? m[1] : DEFAULT_LOCALE
}

/** 把当前路径里的语言前缀替换为目标 code；en 时去掉前缀 */
export function pathForLang(currentPath, targetCode) {
  const stripped = currentPath.replace(/^\/(en|zh|ja|ko|fr|de|es)(?=\/|$)/, '')
  if (targetCode === DEFAULT_LOCALE) return stripped || '/'
  return `/${targetCode}${stripped || '/'}`
}

// 保留 watch 以兼容外部代码
watch(current, (code) => {
  messages.value = dicts[code] || enMessages
})

export function useI18n() {
  function t(key, vars) {
    let v = messages.value[key]
    if (v == null) return key
    if (vars && typeof v === 'string') {
      v = v.replace(/\{(\w+)\}/g, (_, k) => (vars[k] != null ? String(vars[k]) : `{${k}}`))
    }
    return v
  }

  function setLang(code) {
    applyLocale(code)
  }

  const lang = computed(() => current.value)
  const currentMeta = computed(() => SUPPORTED.find(s => s.code === current.value))
  // 现在字典全部同步加载，直接 ready
  const isReady = ref(true)

  return { t, setLang, lang, currentMeta, isReady, SUPPORTED, LOCALE_CODES }
}