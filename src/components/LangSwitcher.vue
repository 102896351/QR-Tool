<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useI18n, SUPPORTED } from '../composables/useI18n'

const { lang, currentMeta, setLang } = useI18n()
const open = ref(false)
const root = ref(null)

const list = SUPPORTED

function pick(code) {
  setLang(code)
  open.value = false
}

function onDocClick(e) {
  if (!root.value) return
  if (!root.value.contains(e.target)) open.value = false
}

onMounted(() => document.addEventListener('click', onDocClick))
onBeforeUnmount(() => document.removeEventListener('click', onDocClick))
</script>

<template>
  <div ref="root" class="relative">
    <button
      @click="open = !open"
      class="theme-toggle-btn gap-2 !w-auto px-3"
      :aria-label="currentMeta.label"
      aria-haspopup="listbox"
      :aria-expanded="open"
    >
      <span class="text-base leading-none">{{ currentMeta.flag }}</span>
      <span class="text-xs font-semibold uppercase tracking-wider hidden sm:inline">{{ currentMeta.code }}</span>
      <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" class="text-gray-400 transition-transform" :class="open && 'rotate-180'">
        <polyline points="6 9 12 15 18 9"/>
      </svg>
    </button>

    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 -translate-y-1 scale-95"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0 -translate-y-1"
    >
      <div
        v-if="open"
        role="listbox"
        class="absolute right-0 mt-2 w-48 rounded-2xl glass-panel dark:glass-panel-dark p-1.5 z-50 origin-top-right"
      >
        <button
          v-for="s in list"
          :key="s.code"
          @click="pick(s.code)"
          role="option"
          :aria-selected="lang === s.code"
          :class="['w-full flex items-center gap-3 px-3 py-2 rounded-xl text-sm transition-colors',
                   lang === s.code
                     ? 'bg-brand-50 dark:bg-brand-500/15 text-brand-700 dark:text-brand-200'
                     : 'text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-white/[0.04]']"
        >
          <span class="text-base leading-none">{{ s.flag }}</span>
          <span class="font-medium">{{ s.label }}</span>
          <svg v-if="lang === s.code" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" class="ml-auto text-brand-600 dark:text-brand-300"><polyline points="20 6 9 17 4 12"/></svg>
        </button>
      </div>
    </transition>
  </div>
</template>
