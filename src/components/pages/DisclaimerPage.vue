<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n, DEFAULT_LOCALE } from '../../composables/useI18n'
import { usePageHead } from '../../composables/usePageHead'
import { pickDisclaimer, DISCLAIMER_UPDATED } from '../../legal/disclaimer'

const { t } = useI18n()
const route = useRoute()
const lang = computed(() => route.meta?.lang || DEFAULT_LOCALE)

// 长文只维护 en / zh，其余语言由 pickDisclaimer 回退英文（与博客策略一致）
const doc = computed(() => pickDisclaimer(lang.value))
const title = computed(() => doc.value.title)
const disclaimerPath = computed(() => lang.value === DEFAULT_LOCALE ? '/disclaimer/' : `/${lang.value}/disclaimer/`)

usePageHead({
  title: `${title.value} — QR Tool Studio`,
  description:
    'The QR Tool Studio disclaimer: the service is provided "as is" for technical and informational use, it is an independent third-party project, and it accepts no liability for third-party links or services.',
  path: disclaimerPath.value
})
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="mb-8">
      <span class="inline-block px-3 py-1 text-xs font-semibold rounded-full bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300">
        LEGAL
      </span>
      <h1 class="mt-4 text-4xl font-bold text-slate-900 dark:text-white">
        {{ title }}
      </h1>
      <p class="mt-2 text-sm text-slate-500 dark:text-slate-400">
        Last updated: {{ DISCLAIMER_UPDATED }}
      </p>
    </div>

    <div class="prose prose-slate dark:prose-invert max-w-none">
      <p class="lead text-lg text-slate-700 dark:text-slate-300" v-html="doc.tldr"></p>

      <template v-for="s in doc.sections" :key="s.h">
        <h2>{{ s.h }}</h2>
        <!-- eslint-disable-next-line vue/no-v-html -->
        <div v-html="s.body"></div>
      </template>

      <h2>Related policies</h2>
      <p>
        This disclaimer is one part of our legal documentation. See also the
        <RouterLink :to="disclaimerPath.replace('/disclaimer/', '/privacy/')">Privacy Policy</RouterLink>,
        the <RouterLink :to="disclaimerPath.replace('/disclaimer/', '/terms/')">Terms of Service</RouterLink>
        and our <RouterLink :to="disclaimerPath.replace('/disclaimer/', '/contact/')">Contact</RouterLink> page.
      </p>
      <p>QR Tool Studio is provided free of charge and is supported by privacy-respecting, non-intrusive advertising. This disclaimer is provided for information only and does not limit any rights you may have under applicable law.</p>
    </div>
  </div>
</template>
