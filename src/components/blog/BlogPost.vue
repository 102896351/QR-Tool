<script setup>
import { computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useHead } from '@unhead/vue'
import { useI18n, SUPPORTED, DEFAULT_LOCALE } from '../../composables/useI18n'
import postsData from '../../blog/posts.json'
import { SITE, BRAND } from '../../config.js'

const props = defineProps({
  slug: { type: String, required: true }
})

const { t, isReady, lang } = useI18n()
const router = useRouter()
const route = useRoute()
const posts = postsData

const post = computed(() => posts.find(p => p.slug === props.slug))

/**
  * canonical 与 hreflang 的「去前缀」路径（统一带尾斜杠，与 sitemap 一致）：
  *   /zh/blog/foo/  →  /blog/foo/
  *   /blog/foo/     →  /blog/foo/
  */
const pathNoPrefix = computed(() => {
  let p = route.path.replace(/^\/(en|zh|ja|ko|fr|de|es)(?=\/|$)/, '') || '/'
  if (!p.endsWith('/')) p += '/'
  return p
})

const currentLang = computed(() => route.meta?.lang || DEFAULT_LOCALE)

// 当前语言 + 尾斜杠的完整路径（canonical 自指）
const canonical = computed(() => {
  let p = route.path
  if (!p.endsWith('/')) p += '/'
  return `${SITE}${p}`
})

const hreflangLinks = computed(() => {
  const stripped = pathNoPrefix.value
  const links = []
  for (const s of SUPPORTED) {
    const href = s.code === DEFAULT_LOCALE
      ? `${SITE}${stripped}`
      : `${SITE}/${s.code}${stripped === '/' ? '/' : stripped}`
    links.push({ rel: 'alternate', hreflang: s.code, href })
  }
  // x-default 指向英文版（去前缀）
  links.push({ rel: 'alternate', hreflang: 'x-default', href: `${SITE}${stripped}` })
  return links
})

function formatDate(dateStr) {
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
}

function goBack() {
  // 回列表：保留当前语言
  const target = currentLang.value === DEFAULT_LOCALE ? '/blog/' : `/${currentLang.value}/blog/`
  router.push(target)
}

function goToGenerator() {
  router.push(`/${currentLang.value === DEFAULT_LOCALE ? '' : currentLang.value + '/'}#generator`)
}

/**
 * 相关文章：同分类优先，不足则用最新的补齐，最多 3 篇。
 * 链接保留当前语言前缀，指向同语言的对应文章页。
 */
const related = computed(() => {
  if (!post.value) return []
  const sameCat = posts.filter(p => p.slug !== post.value.slug && p.category === post.value.category)
  const others = posts
    .filter(p => p.slug !== post.value.slug && p.category !== post.value.category)
    .sort((a, b) => new Date(b.date) - new Date(a.date))
  return [...sameCat, ...others].slice(0, 3)
})

function relatedHref(slug) {
  return currentLang.value === DEFAULT_LOCALE ? `/blog/${slug}/` : `/${currentLang.value}/blog/${slug}/`
}

useHead(() => {
  const p = post.value
  if (!p) return { title: `Not found | ${BRAND}` }
  const titleText = currentLang.value === DEFAULT_LOCALE ? p.title : `${p.title} | ${BRAND}`
  return {
    title: `${p.title} | ${BRAND} Blog`,
    meta: [
      { name: 'description', content: p.description },
      { property: 'og:title', content: p.title },
      { property: 'og:description', content: p.description },
      { property: 'og:image', content: `${SITE}${p.cover}` },
      { property: 'og:type', content: 'article' },
      { property: 'og:url', content: canonical.value },
      { property: 'og:locale', content: currentLang.value },
      { property: 'article:published_time', content: p.date },
      { name: 'twitter:title', content: p.title },
      { name: 'twitter:description', content: p.description },
      { name: 'twitter:card', content: 'summary_large_image' }
    ],
    link: [
      { rel: 'canonical', href: canonical.value },
      ...hreflangLinks.value
    ],
    script: [
      {
        type: 'application/ld+json',
        innerHTML: JSON.stringify({
          '@context': 'https://schema.org',
          '@type': 'BlogPosting',
          headline: p.title,
          description: p.description,
          image: `${SITE}${p.cover}`,
          datePublished: p.date,
          dateModified: p.date,
          inLanguage: currentLang.value,
          author: { '@type': 'Organization', name: p.author, url: `${SITE}/about/` },
          publisher: {
            '@type': 'Organization',
            name: BRAND,
            url: `${SITE}/`,
            logo: { '@type': 'ImageObject', url: `${SITE}/favicon.svg` }
          },
          mainEntityOfPage: { '@type': 'WebPage', '@id': canonical.value }
        })
      },
      {
        type: 'application/ld+json',
        innerHTML: JSON.stringify({
          '@context': 'https://schema.org',
          '@type': 'BreadcrumbList',
          itemListElement: [
            { '@type': 'ListItem', position: 1, name: 'Home', item: currentLang.value === DEFAULT_LOCALE ? `${SITE}/` : `${SITE}/${currentLang.value}/` },
            { '@type': 'ListItem', position: 2, name: 'Blog', item: currentLang.value === DEFAULT_LOCALE ? `${SITE}/blog/` : `${SITE}/${currentLang.value}/blog/` },
            { '@type': 'ListItem', position: 3, name: p.title, item: canonical.value }
          ]
        })
      }
    ]
  }
})

// AdSense 文内广告填充（原先是模板内联 <script>，SSR 下不可靠）
onMounted(() => {
  if (typeof window !== 'undefined' && window.adsbygoogle) {
    window.adsbygoogle.push({})
  }
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

    <!-- 非英文页提示：本文为英文原文（按当前 Option A 设计，正文只翻译界面、不翻译文章正文） -->
    <div
      v-if="currentLang !== 'en'"
      class="mb-6 p-4 rounded-xl border border-amber-200/70 dark:border-amber-500/30 bg-amber-50/60 dark:bg-amber-500/[0.08] text-amber-900 dark:text-amber-100 text-sm flex items-start gap-3"
      role="status"
    >
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mt-0.5 flex-none text-amber-500">
        <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
      <div>
        <div class="font-semibold">{{ t('blog.langNotice.title') }}</div>
        <div class="mt-1 text-amber-900/80 dark:text-amber-100/80">
          {{ t('blog.langNotice.desc') }}
          <RouterLink :to="`/blog/${post.slug}/`" class="font-semibold underline underline-offset-2 ml-1">
            {{ t('blog.langNotice.cta') }}
          </RouterLink>
        </div>
      </div>
    </div>

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

    <!-- AdSense: in-article (top) -->
    <!--
      Placeholder slot ID. After AdSense approves toolbox168.xyz:
        1. Create an "In-article ad" unit in AdSense dashboard
        2. Replace data-ad-slot below with the new slot ID
        3. Reload to confirm ad renders

      v-if: ONLY show after post + i18n ready. Hides during loading and
      route transitions to comply with AdSense "no ads on screens
      without publisher content" policy.
    -->
    <aside v-if="post && isReady" class="my-8" aria-label="Sponsored content">
      <div class="text-[10px] uppercase tracking-wider text-gray-400 dark:text-gray-500 mb-1.5 text-center">Advertisement</div>
      <ins
        class="adsbygoogle block w-full"
        style="display:block; text-align:center"
        data-ad-client="ca-pub-1606763409380030"
        data-ad-slot="0000000001"
        data-ad-layout="in-article"
        data-ad-format="fluid"
      ></ins>
      <script>
        (adsbygoogle = window.adsbygoogle || []).push({});
      </script>
    </aside>

    <!-- Article body -->
    <article
      class="blog-content"
      v-html="post.content"
    ></article>

    <!-- AdSense: in-article (bottom, before end CTA) -->
    <aside v-if="post && isReady" class="my-8" aria-label="Sponsored content">
      <div class="text-[10px] uppercase tracking-wider text-gray-400 dark:text-gray-500 mb-1.5 text-center">Advertisement</div>
      <ins
        class="adsbygoogle block w-full"
        style="display:block; text-align:center"
        data-ad-client="ca-pub-1606763409380030"
        data-ad-slot="0000000002"
        data-ad-layout="in-article"
        data-ad-format="fluid"
      ></ins>
      <script>
        (adsbygoogle = window.adsbygoogle || []).push({});
      </script>
    </aside>

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
      <h2 class="text-lg font-extrabold text-gray-900 dark:text-white mb-4">Related guides</h2>
      <ul class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <li v-for="rp in related" :key="rp.slug">
          <RouterLink
            :to="relatedHref(rp.slug)"
            class="block p-4 rounded-xl glass-panel dark:glass-panel-dark hover:shadow-lg transition-shadow"
          >
            <div class="text-[10px] font-bold uppercase tracking-wider text-brand-600 dark:text-brand-300 mb-1.5">
              {{ rp.category }}
            </div>
            <div class="text-sm font-bold text-gray-900 dark:text-white line-clamp-2">{{ rp.title }}</div>
          </RouterLink>
        </li>
      </ul>
    </div>

    <div class="mt-8">
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
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
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
