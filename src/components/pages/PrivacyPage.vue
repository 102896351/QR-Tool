<script setup>
import { useI18n } from '../../composables/useI18n'
const { t } = useI18n()
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="mb-8">
      <span class="inline-block px-3 py-1 text-xs font-semibold rounded-full bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300">
        LEGAL
      </span>
      <h1 class="mt-4 text-4xl font-bold text-slate-900 dark:text-white">
        Privacy Policy
      </h1>
      <p class="mt-2 text-sm text-slate-500 dark:text-slate-400">
        Last updated: July 24, 2026
      </p>
    </div>

    <div class="prose prose-slate dark:prose-invert max-w-none">
      <p class="lead text-lg text-slate-700 dark:text-slate-300">
        QR Tool Studio is built on a privacy-first principle. This page explains in plain language what data we collect, what we don't, and how you stay in control.
      </p>

      <h2>1. Data we do NOT collect</h2>
      <p>QR Tool Studio runs entirely in your browser. When you generate a QR code, the following never leaves your device:</p>
      <ul>
        <li>The text, URL, or contact information you encode</li>
        <li>The logos, colors, or styling you apply</li>
        <li>The QR code image you download</li>
      </ul>
      <p>We have no servers that receive, store, or process your QR code content. We literally cannot see what you generate, because the work happens in JavaScript running on your computer.</p>

      <h2>2. Data we do collect</h2>
      <p>To improve the tool and understand how it's used, we collect the following limited data through third-party services:</p>
      <ul>
        <li><strong>Google Analytics 4</strong> — anonymous usage statistics: which pages you visit, which features you use, your country (derived from IP, then discarded), and your device type. We do not collect your IP address, name, email, or any personally identifiable information.</li>
        <li><strong>Google AdSense</strong> — if you see ads, Google may use cookies to serve personalized ads based on your browsing history on other sites. You can opt out of personalized ads in your Google account settings.</li>
        <li><strong>Cloudflare</strong> — our CDN logs basic request data (IP, user agent, requested URL) for security and performance. These logs are retained for 30 days and are not shared with us beyond what is needed to operate the service.</li>
      </ul>

      <h2>3. Local storage (your device only)</h2>
      <p>QR Tool Studio stores your recent generation history in your browser's <code>localStorage</code>. This data:</p>
      <ul>
        <li>Never leaves your device</li>
        <li>Is limited to your most recent 10 generations</li>
        <li>Can be cleared at any time via your browser settings or the "Clear history" button in the tool</li>
        <li>Is not used for advertising, profiling, or any purpose beyond your own convenience</li>
      </ul>

      <h2>4. Cookies</h2>
      <p>QR Tool Studio itself does not set any cookies. Third-party services we use may set cookies:</p>
      <ul>
        <li>Google Analytics: <code>_ga</code>, <code>_ga_*</code> (analytics, expires after 2 years)</li>
        <li>Google AdSense: <code>_gcl_au</code>, <code>IDE</code> (advertising, varies)</li>
      </ul>
      <p>You can block or delete cookies in your browser settings without affecting the core functionality of QR Tool Studio.</p>

      <h2>5. Children's privacy</h2>
      <p>QR Tool Studio is not directed at children under 13. We do not knowingly collect data from children. The service is general-purpose and safe for all ages.</p>

      <h2>6. Your rights (GDPR & CCPA)</h2>
      <p>If you are in the European Union (GDPR) or California (CCPA), you have the right to:</p>
      <ul>
        <li>Know what data is collected about you (see Section 2 above)</li>
        <li>Request deletion of any data we hold (we hold no personal data, but third-party services may; see their policies)</li>
        <li>Opt out of personalized advertising (Google Ad Settings: <a href="https://adssettings.google.com/" target="_blank" rel="noopener">adssettings.google.com</a>)</li>
        <li>Object to processing (contact us via the <a href="#contact">Contact</a> page)</li>
      </ul>

      <h2>7. Third-party policies</h2>
      <p>The following services have their own privacy policies that apply when they collect data:</p>
      <ul>
        <li><a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google Privacy Policy</a> (covers Analytics and AdSense)</li>
        <li><a href="https://www.cloudflare.com/privacypolicy/" target="_blank" rel="noopener">Cloudflare Privacy Policy</a></li>
      </ul>

      <h2>8. Changes to this policy</h2>
      <p>We may update this policy as the tool evolves. Significant changes will be announced on the homepage. The "Last updated" date at the top of this page reflects the current version.</p>

      <h2>9. Contact</h2>
      <p>For privacy-related questions or data requests, see our <a href="#contact">Contact</a> page.</p>
    </div>
  </div>
</template>
