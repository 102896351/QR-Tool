import { ref, watch, onMounted, onBeforeUnmount } from 'vue'

/**
 * 主题切换:light / dark / system
 * 自动同步 html.dark 类与 system 偏好变化
 */
const STORAGE_KEY = 'qr-theme'
const themeRef = ref('system')
const isDarkRef = ref(false)
let mediaQuery = null

function applyTheme(t) {
  themeRef.value = t
  let dark = false
  if (t === 'dark') dark = true
  else if (t === 'light') dark = false
  else dark = mediaQuery ? mediaQuery.matches : false
  isDarkRef.value = dark
  document.documentElement.classList.toggle('dark', dark)
}

export function useTheme() {
  onMounted(() => {
    let initial = 'system'
    try { initial = localStorage.getItem(STORAGE_KEY) || 'system' } catch (e) {}
    if (!['light', 'dark', 'system'].includes(initial)) initial = 'system'
    mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    applyTheme(initial)
    const onSys = () => { if (themeRef.value === 'system') applyTheme('system') }
    mediaQuery.addEventListener('change', onSys)
    onBeforeUnmount(() => {
      if (mediaQuery) mediaQuery.removeEventListener('change', onSys)
    })
  })

  function setTheme(t) {
    applyTheme(t)
    try { localStorage.setItem(STORAGE_KEY, t) } catch (e) {}
  }

  function cycleTheme() {
    const order = ['light', 'dark', 'system']
    const idx = order.indexOf(themeRef.value)
    setTheme(order[(idx + 1) % order.length])
  }

  return { theme: themeRef, isDark: isDarkRef, setTheme, cycleTheme }
}
