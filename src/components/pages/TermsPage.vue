<script setup>
import { useI18n } from '../../composables/useI18n'
const { t } = useI18n()
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="mb-8">
      <span class="inline-block px-3 py-1 text-xs font-semibold rounded-full bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300">
        LEGAL
      </span>
      <h1 class="mt-4 text-4xl font-bold text-slate-900 dark:text-white">
        Terms of Service
      </h1>
      <p class="mt-2 text-sm text-slate-500 dark:text-slate-400">
        Last updated: July 24, 2026
      </p>
    </div>

    <div class="prose prose-slate dark:prose-invert max-w-none">
      <p class="lead text-lg text-slate-700 dark:text-slate-300">
        By using QR Tool Studio, you agree to these terms. We have tried to keep them short and in plain language.
      </p>

      <h2>1. The service</h2>
      <p>QR Tool Studio is a free, browser-based QR code generator. It runs entirely on your device; we do not run any backend that processes your QR code content. The service is provided free of charge, with no account required and no usage limits.</p>

      <h2>2. Acceptable use</h2>
      <p>You agree to use QR Tool Studio only for lawful purposes. You may not use the service to:</p>
      <ul>
        <li>Generate QR codes that link to content that is illegal in your jurisdiction (malware, child sexual abuse material, fraud, drug trafficking, etc.)</li>
        <li>Impersonate other people, brands, or organizations in a way that causes harm or confusion</li>
        <li>Attempt to disrupt the service, scrape it at high volume, or bypass rate limits</li>
        <li>Generate QR codes that encode personal data about other people without their consent</li>
      </ul>

      <h2>3. Your content stays yours</h2>
      <p>You retain full ownership of any QR code you generate using this tool. The encoded data, the rendered image, and any styling you apply are yours. You may use generated QR codes for any purpose, including commercial use (marketing, packaging, business cards, products, events).</p>
      <p>We make no claim to the QR codes you create. We do not watermark them. We do not track them.</p>

      <h2>4. The service is provided "as is"</h2>
      <p>QR Tool Studio is provided free of charge, without any warranty. We do our best to ensure the tool works correctly and produces QR codes that scan reliably, but we cannot guarantee:</p>
      <ul>
        <li>That the service will be uninterrupted or error-free</li>
        <li>That every generated QR code will scan in every environment</li>
        <li>That the service will continue to be available in the future</li>
      </ul>
      <p>Use the tool at your own discretion. For mission-critical or high-stakes use (medical, legal, financial), test thoroughly before deploying.</p>

      <h2>5. No professional advice</h2>
      <p>The information provided on this site, including all blog content, is for informational purposes only. It does not constitute professional advice of any kind (legal, medical, financial, technical). For decisions that matter, consult a qualified professional.</p>

      <h2>6. Third-party services</h2>
      <p>We use the following third-party services to operate QR Tool Studio:</p>
      <ul>
        <li><strong>Google Analytics</strong> — anonymous usage statistics</li>
        <li><strong>Google AdSense</strong> — advertising</li>
        <li><strong>Cloudflare</strong> — CDN and security</li>
        <li><strong>GitHub Pages</strong> — hosting</li>
      </ul>
      <p>Your use of these services is subject to their own terms. We are not responsible for their availability, accuracy, or behavior.</p>

      <h2>7. Intellectual property</h2>
      <p>The QR Tool Studio website, design, code, and content (excluding user-generated QR codes) are © QR Tool Studio. You may reference, link to, and share our content for non-commercial purposes. For commercial use, please contact us first.</p>
      <p>The QR code technology itself is covered by patents that have expired or are licensed openly; the use of QR codes is not restricted.</p>

      <h2>8. Limitation of liability</h2>
      <p>To the maximum extent permitted by law, QR Tool Studio and its operators are not liable for any direct, indirect, incidental, or consequential damages arising from your use of the service. This includes lost profits, lost data, business interruption, or reputational harm.</p>

      <h2>9. Changes to these terms</h2>
      <p>We may update these terms as the service evolves. The "Last updated" date at the top of this page reflects the current version. Continued use of the service after changes constitutes acceptance of the new terms.</p>

      <h2>10. Governing law</h2>
      <p>These terms are governed by the laws of the jurisdiction in which the operator is based, without regard to conflict of law principles. Disputes will be resolved in the courts of that jurisdiction.</p>

      <h2>11. Contact</h2>
      <p>For questions about these terms, see our <a href="/contact">Contact</a> page.</p>
    </div>
  </div>
</template>
