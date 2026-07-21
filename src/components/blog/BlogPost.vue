<script setup>
import { computed, onMounted, watch, nextTick } from 'vue'
import { useI18n } from '../../composables/useI18n'
import postsData from '../../blog/posts.json'

const props = defineProps({
  slug: { type: String, required: true }
})

const { t, isReady } = useI18n()
const posts = postsData

const post = computed(() => posts.find(p => p.slug === props.slug))

function goBack() {
  window.location.hash = 'blog'
  window.scrollTo({ top: 0, behavior: 'instant' })
}

function goToGenerator() {
  window.location.hash = ''
  setTimeout(() => {
    document.getElementById('generator')?.scrollIntoView({ behavior: 'smooth' })
  }, 100)
}

function formatDate(dateStr) {
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
}

// 同步 head meta（SEO 友好）
function syncHead() {
  if (typeof document === 'undefined' || !post.value) return
  const p = post.value
  document.title = `${p.title} | QR Tool Studio Blog`

  function setMeta(selector, attr, value) {
    let el = document.querySelector(selector)
    if (!el) {
      el = document.createElement('meta')
      const [k, v] = attr
      el.setAttribute(k, v)
      document.head.appendChild(el)
    }
    el.setAttribute('content', value)
  }

  setMeta('meta[name="description"]', ['name', 'description'], p.description)
  setMeta('meta[property="og:title"]', ['property', 'og:title'], p.title)
  setMeta('meta[property="og:description"]', ['property', 'og:description'], p.description)
  setMeta('meta[property="og:image"]', ['property', 'og:image'], `https://toolbox168.xyz${p.cover}`)
  setMeta('meta[property="og:type"]', ['property', 'og:type'], 'article')
  setMeta('meta[name="twitter:title"]', ['name', 'twitter:title'], p.title)
  setMeta('meta[name="twitter:description"]', ['name', 'twitter:description'], p.description)

  // JSON-LD Article schema
  let ld = document.querySelector('script[type="application/ld+json"][data-blog]')
  if (!ld) {
    ld = document.createElement('script')
    ld.type = 'application/ld+json'
    ld.setAttribute('data-blog', 'true')
    document.head.appendChild(ld)
  }
  ld.textContent = JSON.stringify({
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: p.title,
    description: p.description,
    image: `https://toolbox168.xyz${p.cover}`,
    datePublished: p.date,
    author: { '@type': 'Organization', name: p.author },
    publisher: {
      '@type': 'Organization',
      name: 'QR Tool Studio',
      logo: { '@type': 'ImageObject', url: 'https://toolbox168.xyz/favicon.svg' }
    }
  })
}

function cleanupHead() {
  if (typeof document === 'undefined') return
  // 恢复默认 meta
  document.title = t('meta.title') || 'QR Tool Studio'
  const ld = document.querySelector('script[type="application/ld+json"][data-blog]')
  if (ld) ld.remove()
}

onMounted(() => {
  if (isReady.value) syncHead()
  window.scrollTo({ top: 0, behavior: 'instant' })
})

watch([() => props.slug, isReady], () => {
  syncHead()
  window.scrollTo({ top: 0, behavior: 'instant' })
})
</script>

<template>
  <div v-if="post" class="w-full max-w-4xl mx-auto px-4 sm:px-6 mt-6 sm:mt-8 pb-16">
    <!-- Back nav -->
    <button
      @click="goBack"
      class="inline-flex items-center gap-1.5 text-sm text-gray-600 dark:text-gray-300 hover:text-brand-600 dark:hover:text-brand-300 transition-colors mb-6"
    >
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/>
      </svg>
      {{ t('blog.backToList') }}
    </button>

    <!-- Article header -->
    <header class="mb-8">
      <div class="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400 mb-3">
        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider bg-brand-50 dark:bg-brand-500/10 text-brand-600 dark:text-brand-300">
          {{ post.category }}
        </span>
        <span>·</span>
        <time :datetime="post.date">{{ formatDate(post.date) }}</time>
        <span>·</span>
        <span>{{ post.readTime }} {{ t('blog.minRead') }}</span>
      </div>
      <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-gray-900 dark:text-white leading-tight">
        {{ post.title }}
      </h1>
      <p class="mt-4 text-base sm:text-lg text-gray-600 dark:text-gray-300 leading-relaxed">
        {{ post.description }}
      </p>
      <div class="mt-5 flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
        <div class="h-8 w-8 rounded-full bg-gradient-to-br from-brand-500 to-purple-500 grid place-items-center text-white text-xs font-bold">
          {{ post.author.charAt(0) }}
        </div>
        <span>{{ post.author }}</span>
      </div>
    </header>

    <!-- Cover image -->
    <figure class="mb-10 rounded-2xl overflow-hidden glass-panel dark:glass-panel-dark">
      <img
        :src="post.cover"
        :alt="post.title"
        class="w-full h-auto"
      />
    </figure>

    <!-- Article body -->
    <article
      class="blog-content"
      v-html="post.content"
    ></article>

    <!-- Inline CTA at end -->
    <div class="mt-12 p-6 sm:p-8 rounded-2xl bg-gradient-to-br from-brand-500 to-purple-500 text-white text-center">
      <h3 class="text-xl sm:text-2xl font-extrabold">{{ t('blog.endCta.title') }}</h3>
      <p class="mt-2 text-sm sm:text-base text-white/90">
        {{ t('blog.endCta.desc') }}
      </p>
      <button
        @click="goToGenerator"
        class="mt-5 inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-white text-brand-600 font-bold text-sm hover:shadow-lg transition-shadow"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        {{ t('blog.endCta.button') }}
      </button>
    </div>

    <!-- Related -->
    <div class="mt-12 pt-8 border-t border-gray-200/60 dark:border-white/10">
      <button
        @click="goBack"
        class="inline-flex items-center gap-1.5 text-sm font-semibold text-brand-600 dark:text-brand-300 hover:underline"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/>
        </svg>
        {{ t('blog.browseAll') }}
      </button>
    </div>
  </div>

  <!-- 404 fallback -->
  <div v-else class="w-full max-w-3xl mx-auto px-4 sm:px-6 py-20 text-center">
    <h1 class="text-3xl font-extrabold text-gray-900 dark:text-white">{{ t('blog.notFoundTitle') }}</h1>
    <p class="mt-3 text-gray-600 dark:text-gray-300">{{ t('blog.notFoundDesc') }}</p>
    <button @click="goBack" class="mt-6 btn-brand">{{ t('blog.backToBlog') }}</button>
  </div>
</template>

<style scoped>
.blog-content :deep(p) {
  margin-top: 1.25rem;
  margin-bottom: 1.25rem;
  line-height: 1.8;
  color: rgb(55 65 81);
}
.dark .blog-content :deep(p) {
  color: rgb(209 213 219);
}
.blog-content :deep(.lead) {
  font-size: 1.15rem;
  color: rgb(75 85 99);
  font-weight: 500;
  line-height: 1.7;
}
.dark .blog-content :deep(.lead) {
  color: rgb(229 231 235);
}
.blog-content :deep(h2) {
  margin-top: 3rem;
  margin-bottom: 1rem;
  font-size: 1.875rem;
  font-weight: 800;
  color: rgb(17 24 39);
  line-height: 1.3;
  letter-spacing: -0.02em;
}
.dark .blog-content :deep(h2) {
  color: rgb(255 255 255);
}
.blog-content :deep(h2#conclusion) {
  background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
.blog-content :deep(h3) {
  margin-top: 2rem;
  margin-bottom: 0.75rem;
  font-size: 1.375rem;
  font-weight: 700;
  color: rgb(17 24 39);
  line-height: 1.4;
}
.dark .blog-content :deep(h3) {
  color: rgb(255 255 255);
}
.blog-content :deep(ul),
.blog-content :deep(ol) {
  margin-top: 1rem;
  margin-bottom: 1rem;
  padding-left: 1.5rem;
  color: rgb(55 65 81);
  line-height: 1.8;
}
.dark .blog-content :deep(ul),
.dark .blog-content :deep(ol) {
  color: rgb(209 213 219);
}
.blog-content :deep(li) {
  margin-top: 0.4rem;
  margin-bottom: 0.4rem;
}
.blog-content :deep(ul) li {
  list-style-type: disc;
}
.blog-content :deep(ol) li {
  list-style-type: decimal;
}
.blog-content :deep(strong) {
  color: rgb(17 24 39);
  font-weight: 700;
}
.dark .blog-content :deep(strong) {
  color: rgb(255 255 255);
}
.blog-content :deep(a) {
  color: rgb(99 102 241);
  text-decoration: underline;
  text-underline-offset: 2px;
  font-weight: 500;
}
.blog-content :deep(a:hover) {
  color: rgb(168 85 247);
}
.blog-content :deep(code) {
  font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace;
  font-size: 0.875em;
  padding: 0.125rem 0.375rem;
  background: rgb(243 244 246);
  color: rgb(99 102 241);
  border-radius: 0.375rem;
  font-weight: 500;
}
.dark .blog-content :deep(code) {
  background: rgb(31 41 55);
  color: rgb(196 181 253);
}
.blog-content :deep(pre) {
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
  padding: 1rem 1.25rem;
  background: rgb(17 24 39);
  color: rgb(229 231 235);
  border-radius: 0.75rem;
  overflow-x: auto;
  font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace;
  font-size: 0.875rem;
  line-height: 1.6;
}
.blog-content :deep(pre code) {
  background: transparent;
  color: inherit;
  padding: 0;
  font-size: inherit;
}
.blog-content :deep(figure) {
  margin: 2.5rem 0;
  text-align: center;
}
.blog-content :deep(figure img) {
  width: 100%;
  height: auto;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
}
.dark .blog-content :deep(figure img) {
  border-color: rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}
.blog-content :deep(figcaption) {
  margin-top: 0.75rem;
  font-size: 0.875rem;
  color: rgb(107 114 128);
  font-style: italic;
  line-height: 1.5;
}
.dark .blog-content :deep(figcaption) {
  color: rgb(156 163 175);
}
.blog-content :deep(.cta-link) {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1.5rem;
  padding: 0.875rem 1.5rem;
  background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
  color: white;
  border-radius: 0.75rem;
  text-decoration: none;
  font-weight: 700;
  font-size: 1rem;
  transition: all 0.2s;
  box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
}
.blog-content :deep(.cta-link:hover) {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
  color: white;
}
</style>
