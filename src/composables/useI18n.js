/**
 * i18n 国际化(composable 风格,极简自研)
 * 支持 7 种语言,默认英文,LocalStorage 持久化
 */
import { ref, computed, watch } from 'vue'

export const SUPPORTED = [
  { code: 'en', label: 'English',  flag: '🇺🇸' },
  { code: 'zh', label: '中文',      flag: '🇨🇳' },
  { code: 'ja', label: '日本語',     flag: '🇯🇵' },
  { code: 'ko', label: '한국어',     flag: '🇰🇷' },
  { code: 'fr', label: 'Français', flag: '🇫🇷' },
  { code: 'de', label: 'Deutsch',  flag: '🇩🇪' },
  { code: 'es', label: 'Español',  flag: '🇪🇸' }
]

const KEY = 'qr-lang'

// 全局状态(单例)
const current = ref(typeof localStorage !== 'undefined'
  ? (localStorage.getItem(KEY) || 'en')
  : 'en')

const dicts = {}

async function loadDict(code) {
  if (dicts[code]) return dicts[code]
  try {
    const mod = await import(`./locales/${code}.js`)
    dicts[code] = mod.default
    return mod.default
  } catch (e) {
    console.warn('[i18n] load failed:', code)
    return null
  }
}

// 立即加载当前语言
const messages = ref({})
loadDict(current.value).then(d => { if (d) messages.value = d })

// 监听语言变化
watch(current, async (code) => {
  const d = await loadDict(code)
  if (d) messages.value = d
  try { localStorage.setItem(KEY, code) } catch (e) {}
  // 同步 html lang 属性(SEO)
  if (typeof document !== 'undefined') {
    document.documentElement.lang = code
  }
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
    if (SUPPORTED.some(s => s.code === code)) {
      current.value = code
    }
  }

  const lang = computed(() => current.value)
  const currentMeta = computed(() => SUPPORTED.find(s => s.code === current.value))

  return { t, setLang, lang, currentMeta, SUPPORTED }
}
