<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import postsData from '../blog/posts.json'
import { useI18n } from '../composables/useI18n'

const { t } = useI18n()

/**
 * 首页「最新指南」区块。
 *
 * 存在的唯一理由是 SEO：首页是全站权重最高的页面，
 * 之前它对博客文章零内链，Google 只能靠 sitemap 发现文章。
 * 现在每篇被推荐的文章都会从首页获得一条 dofollow 内链。
 */
const featured = computed(() =>
  [...postsData]
    .sort((a, b) => new Date(b.date) - new Date(a.date))
    .slice(0, 6)
)

function formatDate(d) {
  try {
    return new Date(d).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
  } catch {
    return d
  }
}
</script>

<template>
  <section id="guides" class="w-full max-w-6xl mx-auto px-4 sm:px-6 py-14 scroll-mt-24">
    <div class="flex items-end justify-between gap-4 mb-7">
      <div>
        <h2 class="text-2xl sm:text-3xl font-extrabold tracking-tight text-gray-900 dark:text-white">
          Latest QR code guides
        </h2>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Practical walkthroughs, size rules and troubleshooting — written for people who just need the code to scan.
        </p>
      </div>
      <RouterLink
        to="/blog/"
        class="hidden sm:inline-flex shrink-0 items-center gap-1.5 text-sm font-semibold text-brand-600 dark:text-brand-300 hover:underline"
      >
        {{ t('blog.browseAll') }}
        <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
      </RouterLink>
    </div>

    <ul class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3 list-none p-0 m-0">
      <li v-for="post in featured" :key="post.slug">
        <RouterLink
          :to="`/blog/${post.slug}/`"
          class="group flex h-full flex-col rounded-2xl border border-gray-200/60 dark:border-white/10 bg-white/70 dark:bg-white/[0.03] p-5 backdrop-blur transition-all duration-300 hover:-translate-y-1 hover:shadow-xl hover:border-brand-400/50"
        >
          <div class="flex items-center gap-2 text-[11px] text-gray-500 dark:text-gray-400 mb-2">
            <span class="inline-flex items-center rounded-md bg-brand-500/10 px-2 py-0.5 font-semibold text-brand-600 dark:text-brand-300">
              {{ post.category }}
            </span>
            <time :datetime="post.date">{{ formatDate(post.date) }}</time>
          </div>

          <h3 class="text-base font-bold leading-snug text-gray-900 dark:text-white group-hover:text-brand-600 dark:group-hover:text-brand-300 transition-colors">
            {{ post.title }}
          </h3>

          <p class="mt-2 text-sm leading-relaxed text-gray-600 dark:text-gray-400 line-clamp-3">
            {{ post.description }}
          </p>

          <span class="mt-4 inline-flex items-center gap-1 text-xs font-semibold text-brand-600 dark:text-brand-300">
            {{ post.readTime }} min read
            <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" class="transition-transform group-hover:translate-x-0.5"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </span>
        </RouterLink>
      </li>
    </ul>

    <div class="mt-7 text-center sm:hidden">
      <RouterLink to="/blog/" class="btn-ghost">
        {{ t('blog.browseAll') }}
      </RouterLink>
    </div>
  </section>
</template>
