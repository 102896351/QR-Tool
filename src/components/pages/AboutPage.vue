<script setup>
import { useI18n } from '../../composables/useI18n'
const { t } = useI18n()
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="mb-8">
      <span class="inline-block px-3 py-1 text-xs font-semibold rounded-full bg-violet-100 text-violet-700 dark:bg-violet-900/30 dark:text-violet-300">
        ABOUT
      </span>
      <h1 class="mt-4 text-4xl font-bold text-slate-900 dark:text-white">
        About QR Tool Studio
      </h1>
    </div>

    <div class="prose prose-slate dark:prose-invert max-w-none">
      <p class="lead text-lg text-slate-700 dark:text-slate-300">
        QR Tool Studio is a free, privacy-first QR code generator that runs entirely in your browser. No account, no upload, no tracking of your content. Just a tool that works.
      </p>

      <h2>Our mission</h2>
      <p>Make QR code generation accessible to everyone — small businesses, event organizers, educators, creators, and developers — without compromising on privacy or design quality.</p>

      <h2>What we built</h2>
      <p>QR Tool Studio supports 8 QR code types out of the box:</p>
      <ul>
        <li><strong>URL</strong> — link to any website</li>
        <li><strong>vCard</strong> — share contact info with a single scan</li>
        <li><strong>Text</strong> — encode any plain text</li>
        <li><strong>Email</strong> — pre-fill a mailto link with subject and body</li>
        <li><strong>Phone</strong> — tap-to-call numbers</li>
        <li><strong>SMS</strong> — pre-fill a text message</li>
        <li><strong>WiFi</strong> — share WiFi credentials without typing</li>
        <li><strong>Plain</strong> — any custom string</li>
      </ul>

      <h3>Design features</h3>
      <ul>
        <li>6 module styles (squares, rounded, dots, curves)</li>
        <li>5 finder-pattern styles (the three corner squares)</li>
        <li>Dual-color linear and radial gradients with adjustable rotation</li>
        <li>Center logo support (PNG, JPG, SVG, 10-50% size)</li>
        <li>4 error correction levels (L 7%, M 15%, Q 25%, H 30%)</li>
        <li>Adjustable margin and module size</li>
      </ul>

      <h3>Export &amp; workflow</h3>
      <ul>
        <li>Export to PNG (1024×1024), SVG (vector), JPEG</li>
        <li>Copy to clipboard</li>
        <li>Batch generation with ZIP download</li>
        <li>Recent history (last 10 generations, stored locally)</li>
        <li>Light / dark / system theme</li>
        <li>Responsive: works on desktop, tablet, and mobile</li>
      </ul>

      <h2>How it's different</h2>
      <p>Most free QR generators upload your content to a server. We don't. Our tool uses the same JavaScript library (<a href="https://github.com/nickoala/qr-code-styling" target="_blank" rel="noopener">qr-code-styling</a>) to generate codes in your browser. The entire process — encoding, styling, rendering, downloading — happens locally on your device.</p>

      <h3>The privacy difference</h3>
      <p>This matters when you're generating QR codes that contain sensitive data: WiFi passwords for your office, contact info you don't want indexed, vCard details for an unannounced product launch. With QR Tool Studio, that data never leaves your device.</p>

      <h2>Who builds QR Tool Studio</h2>
      <p>QR Tool Studio is maintained by a small independent team of developers and content contributors. The project started in 2025 with one goal: ship a QR code generator that doesn't require an account, doesn't upload your content to a server, and works the same offline as it does online. Every feature in this tool is the result of that mission.</p>

      <h3>Our team</h3>
      <p>The project is led by an independent developer based in Asia, with rotating contributors handling design, content, and translation. The full list of contributors is publicly visible on the <a href="https://github.com/102896351/QR-Tool/graphs/contributors" target="_blank" rel="noopener">GitHub contributors graph</a>.</p>

      <h3>Editorial standards</h3>
      <p>Every blog post on this site is written or reviewed by a human before publication. We don't publish AI-generated content without human review. We cite the underlying standards (ISO/IEC 18004 for QR codes, the IETF URI specification for URL encoding) wherever they're relevant, and we link to primary sources rather than secondary explainers.</p>

      <h3>Technical credentials</h3>
      <ul>
        <li><strong>Open source:</strong> the entire site is on <a href="https://github.com/102896351/QR-Tool" target="_blank" rel="noopener">GitHub</a> under a permissive license. You can audit every line of the code that runs in your browser.</li>
        <li><strong>Standards-compliant:</strong> we use the <a href="https://github.com/nickoala/qr-code-styling" target="_blank" rel="noopener">qr-code-styling</a> library, an open-source implementation of the ISO/IEC 18004 standard. Generated codes are compatible with every QR scanner built after 2010.</li>
        <li><strong>Privacy by design:</strong> encoding, styling, and download all run locally in your browser. No content is sent to a server, ever. This is verifiable by reading the source code or by using the tool with the network tab open.</li>
        <li><strong>Active maintenance:</strong> check the <a href="https://github.com/102896351/QR-Tool/commits/main" target="_blank" rel="noopener">commit history</a> for proof of ongoing work. Issues and feature requests are tracked publicly on GitHub.</li>
      </ul>

      <h3>How to reach the team</h3>
      <ul>
        <li><strong>Email:</strong> <a href="mailto:andynaonao@gmail.com">andynaonao@gmail.com</a> — direct line to the lead developer. We aim to respond within 48 hours on business days.</li>
        <li><strong>GitHub issues:</strong> the preferred channel for bug reports and feature requests. Open an issue at <a href="https://github.com/102896351/QR-Tool/issues" target="_blank" rel="noopener">github.com/102896351/QR-Tool/issues</a>.</li>
        <li><strong>GitHub discussions:</strong> for general questions, ideas, or to show off what you've built with the tool.</li>
      </ul>

      <h2>Open source</h2>
      <p>The site is open source on <a href="https://github.com/102896351/QR-Tool" target="_blank" rel="noopener">GitHub</a>. The QR code rendering engine we use is the open-source <a href="https://github.com/nickoala/qr-code-styling" target="_blank" rel="noopener">qr-code-styling</a> library. Everything else is plain Vue 3 + Vite.</p>

      <h2>No paywall, no limits</h2>
      <p>QR Tool Studio is free, with no usage limits, no daily caps, no premium tier. The site is supported by unobtrusive advertising. If you find the tool useful, the best way to support us is to share it with someone who'd also find it useful.</p>

      <h2>Get in touch</h2>
      <p>Questions, suggestions, or just want to say hi? See our <a href="/contact">Contact</a> page.</p>
    </div>
  </div>
</template>
