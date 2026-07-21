<script setup>
import { ref, computed } from 'vue'
import { useI18n } from '../../composables/useI18n'
import postsData from '../../blog/posts.json'

const { t } = useI18n()
const posts = ref(postsData)

const sortedPosts = computed(() => {
  return [...posts.value].sort((a, b) => new Date(b.date) - new Date(a.date))
})

function goToPost(slug) {
  window.location.hash = `blog/${slug}`
  window.scrollTo({ top: 0, behavior: 'instant' })
}

function formatDate(dateStr) {
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}
</script>

<template>
  <div class="w-full max-w-6xl mx-auto px-4 sm:px-6 mt-8 sm:mt-10 pb-16">
    <!-- Hero -->
    <div class="text-center max-w-3xl mx-auto mb-12">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/70 dark:bg-white/[0.04] border border-gray-200/60 dark:border-white/10 text-xs font-medium text-gray-700 dark:text-gray-200 mb-5 backdrop-blur">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-brand-500">
          <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
        </svg>
        {{ t('blog.badge') }}
      </div>
      <h1 class="text-4xl sm:text-5xl font-extrabold tracking-tight text-gray-900 dark:text-white">
        {{ t('blog.hero.title.l1') }} <span class="text-transparent bg-clip-text bg-gradient-to-r from-brand-600 via-purple-500 to-pink-500">{{ t('blog.hero.title.l2') }}</span>
      </h1>
      <p class="mt-4 text-base sm:text-lg text-gray-600 dark:text-gray-300 leading-relaxed">
        {{ t('blog.hero.desc') }}
      </p>
    </div>

    <!-- Posts grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <article
        v-for="post in sortedPosts"
        :key="post.slug"
        @click="goToPost(post.slug)"
        class="group cursor-pointer glass-panel dark:glass-panel-dark overflow-hidden noise-bg hover:shadow-xl hover:-translate-y-1 transition-all duration-300"
      >
        <!-- Cover image -->
        <div class="relative aspect-[1200/630] overflow-hidden bg-gradient-to-br from-brand-500/10 to-purple-500/10">
          <img
            :src="post.cover"
            :alt="post.title"
            loading="lazy"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            @error="(e) => { e.target.style.display='none' }"
          />
          <div class="absolute top-3 left-3">
            <span class="inline-flex items-center px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider bg-white/90 dark:bg-gray-900/90 text-brand-600 dark:text-brand-300 backdrop-blur">
              {{ post.category }}
            </span>
          </div>
        </div>

        <!-- Content -->
        <div class="p-5">
          <div class="flex items-center gap-2 text-[11px] text-gray-500 dark:text-gray-400 mb-2">
            <time :datetime="post.date">{{ formatDate(post.date) }}</time>
            <span>·</span>
            <span>{{ post.readTime }} {{ t('blog.minRead') }}</span>
          </div>
          <h2 class="text-lg font-bold text-gray-900 dark:text-white group-hover:text-brand-600 dark:group-hover:text-brand-300 transition-colors line-clamp-2">
            {{ post.title }}
          </h2>
          <p class="mt-2 text-sm text-gray-600 dark:text-gray-300 leading-relaxed line-clamp-3">
            {{ post.description }}
          </p>
          <div class="mt-4 flex items-center gap-1.5 text-xs font-semibold text-brand-600 dark:text-brand-300">
            {{ t('blog.readArticle') }}
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="group-hover:translate-x-1 transition-transform">
              <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
            </svg>
          </div>
        </div>
      </article>
    </div>

    <!-- Empty state -->
    <div v-if="sortedPosts.length === 0" class="text-center py-16">
      <p class="text-gray-500 dark:text-gray-400">{{ t('blog.empty') }}</p>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
