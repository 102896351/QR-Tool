<script setup>
import { ref } from 'vue'
import { useI18n } from '../../composables/useI18n'
const { t } = useI18n()

const form = ref({ name: '', email: '', subject: 'general', message: '' })
const submitted = ref(false)

function submit() {
  // Since we don't have a backend, this opens the user's mail client
  // with the form data pre-filled. Real form submission would need a backend.
  const subjectMap = {
    general: 'General inquiry',
    bug: 'Bug report',
    feature: 'Feature request',
    privacy: 'Privacy concern',
    partnership: 'Partnership',
  }
  const subject = subjectMap[form.value.subject] || 'Contact'
  const body = `Name: ${form.value.name}%0D%0AEmail: ${form.value.email}%0D%0A%0D%0A${encodeURIComponent(form.value.message)}`
  // Build mailto link (user can change email if needed)
  const mailto = `mailto:contact@toolbox168.xyz?subject=${encodeURIComponent(subject)}&body=${body}`
  window.location.href = mailto
  submitted.value = true
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="mb-8">
      <span class="inline-block px-3 py-1 text-xs font-semibold rounded-full bg-indigo-100 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-300">
        CONTACT
      </span>
      <h1 class="mt-4 text-4xl font-bold text-slate-900 dark:text-white">
        Get in touch
      </h1>
      <p class="mt-2 text-slate-600 dark:text-slate-400">
        Bug reports, feature requests, partnership inquiries, or just a friendly hello — we read everything.
      </p>
    </div>

    <div class="grid md:grid-cols-2 gap-8">
      <!-- Direct contact -->
      <div>
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white mb-4">
          Direct channels
        </h2>

        <div class="space-y-4">
          <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700">
            <div class="text-sm text-slate-500 dark:text-slate-400">Email</div>
            <a href="mailto:contact@toolbox168.xyz" class="text-indigo-600 dark:text-indigo-400 font-medium hover:underline">
              contact@toolbox168.xyz
            </a>
            <div class="text-xs text-slate-500 dark:text-slate-400 mt-1">
              For general inquiries, bug reports, and feature requests
            </div>
          </div>

          <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700">
            <div class="text-sm text-slate-500 dark:text-slate-400">GitHub</div>
            <a href="https://github.com/102896351/QR-Tool" target="_blank" rel="noopener" class="text-indigo-600 dark:text-indigo-400 font-medium hover:underline">
              github.com/102896351/QR-Tool
            </a>
            <div class="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Source code, issues, and feature requests
            </div>
          </div>

          <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700">
            <div class="text-sm text-slate-500 dark:text-slate-400">Response time</div>
            <div class="text-slate-900 dark:text-white font-medium">
              1-3 business days
            </div>
            <div class="text-xs text-slate-500 dark:text-slate-400 mt-1">
              We are a small team; please be patient with replies
            </div>
          </div>
        </div>
      </div>

      <!-- Contact form -->
      <div>
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white mb-4">
          Send a message
        </h2>

        <form @submit.prevent="submit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Your name</label>
            <input
              v-model="form.name"
              type="text"
              required
              class="w-full px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white"
              placeholder="Jane Cooper"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Your email</label>
            <input
              v-model="form.email"
              type="email"
              required
              class="w-full px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white"
              placeholder="jane@example.com"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Subject</label>
            <select
              v-model="form.subject"
              class="w-full px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white"
            >
              <option value="general">General inquiry</option>
              <option value="bug">Bug report</option>
              <option value="feature">Feature request</option>
              <option value="privacy">Privacy concern</option>
              <option value="partnership">Partnership / business</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Message</label>
            <textarea
              v-model="form.message"
              required
              rows="5"
              class="w-full px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white"
              placeholder="Tell us what's on your mind..."
            ></textarea>
          </div>

          <button
            type="submit"
            class="w-full px-4 py-2 rounded-lg bg-indigo-600 text-white font-medium hover:bg-indigo-700 transition"
          >
            Open email client to send
          </button>

          <p v-if="submitted" class="text-xs text-emerald-600 dark:text-emerald-400">
            Your email client should have opened. If not, send directly to contact@toolbox168.xyz.
          </p>

          <p class="text-xs text-slate-500 dark:text-slate-400">
            Note: This form opens your default email client. We don't run a form backend to keep the service 100% free and private.
          </p>
        </form>
      </div>
    </div>
  </div>
</template>
