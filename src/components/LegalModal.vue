<script setup>
import { computed } from 'vue'

const props = defineProps({
  open: { type: Boolean, required: true },
  type: { type: String, default: 'disclaimer' } // disclaimer | privacy | about | contact
})
const emit = defineEmits(['close'])

const config = {
  disclaimer: {
    title: '免责声明 (Disclaimer)',
    badge: '法律声明',
    updated: '2026-06-28',
    sections: [
      {
        h: '1. 仅供技术与信息参考',
        body: `<p><strong>QR Tool Studio</strong> 是一款独立维护的在线二维码生成工具,面向开发者与普通用户使用。本站所有内容(包括但不限于文案、案例、链接、截图、评论)均<strong>仅供技术学习与信息参考之用</strong>,不构成投资、法律、税务、医疗或其他专业建议。</p>`
      },
      {
        h: '2. 独立第三方,非代言',
        body: `<p>本站为<strong>独立第三方项目</strong>,与任何商业实体、平台运营商或投资方均无关联、代言、赞助或合作关系。所有产品名称、商标、Logo 与品牌资产归各自所有者所有,在本站仅用于识别与参考。</p>`
      },
      {
        h: '3. "按现状"提供,无担保',
        body: `<p>本站二维码生成功能基于成熟的开源库(<code>qr-code-styling</code>),我们已尽力保证输出符合 QR Code ISO/IEC 18004 标准,但仍按<strong>"AS IS"(按现状)</strong>原则提供,<strong>不对绝对准确性、完整性、时效性或特定用途的适用性作任何担保</strong>。商业使用前请先在目标环境(扫描设备、印刷工艺、纸张介质)进行充分测试。</p>`
      },
      {
        h: '2. 第三方链接与服务',
        body: `<p>本站可能包含指向第三方网站(GitHub、社交平台、二维码扫描器官网等)的链接,以及第三方提供的广告位。这些第三方服务的内容、政策、可用性与安全由其各自运营方负责,<strong>本站不对其行为承担任何责任</strong>。离开本站时,请阅读并遵守第三方的条款与隐私政策。</p>`
      },
      {
        h: '5. 责任限制',
        body: `<p>在适用法律允许的最大范围内,本站作者、贡献者与托管方<strong>不对因使用或无法使用本站内容而产生的任何直接、间接、偶发、特殊或衍生损害</strong>(包括但不限于数据丢失、业务中断、机会丧失或利润损失)承担责任。</p><p>请仅在<strong>适用法律允许的范围内</strong>使用本站。不得将本工具用于违反当地法律法规的活动,亦不得用作违法行为的工具或教学材料。</p>`
      },
      {
        h: '6. 修改与终止',
        body: `<p>我们可能<strong>随时修改、暂停或下线</strong>本站的页面、功能、布局或本免责声明,无需事先通知。重大变更将在 GitHub 仓库的 <code>CHANGELOG</code> 中记录,欢迎通过 PR 或 Issue 跟进。</p>`
      }
    ],
    tldr: '<strong>仅供技术交流与信息参考 · 在法律允许范围内使用 · 商业或法律决策请以官方信息源为准。</strong>'
  },
  privacy: {
    title: '隐私政策 (Privacy Policy)',
    badge: '隐私保护',
    updated: '2026-06-28',
    sections: [
      {
        h: '1. 我们收集什么',
        body: `<p><strong>QR Tool Studio 是一个纯静态站点</strong>(可部署于 GitHub Pages / Vercel / Cloudflare Pages 等平台)。它不运行后端,不提供用户账号,自身不维护任何数据库。默认情况下,我们<strong>不主动收集您的姓名、邮箱、电话、身份证号或任何其他可识别个人身份的信息</strong>。</p><p>您访问过程中可能产生的技术日志仅包括:</p><ul class="list-disc pl-5 space-y-1"><li>请求时间、请求 URL、HTTP 状态、User-Agent 与 Referer —— 由托管平台(GitHub Pages / CDN 边缘节点)出于安全与运维目的生成;</li><li>启用 Cloudflare 时的反爬虫与缓存日志 —— 用于站点加速与基础防护。</li></ul>`
      },
      {
        h: '2. Cookie 与本地存储',
        body: `<p>本站<strong>不使用任何追踪 Cookie</strong>,也未集成 Google Analytics、Meta Pixel、TikTok Pixel 等第三方追踪脚本。</p><p>写入您浏览器 <code>localStorage</code> 的内容仅有:</p><ul class="list-disc pl-5 space-y-1"><li><strong>主题偏好</strong>(亮 / 暗 / 跟随系统)—— 仅用于下次访问时恢复显示选择;</li><li><strong>历史记录</strong>(最多 10 条最近生成的二维码配置)—— 仅保存在您的设备本地。</li></ul><p>这些数据<strong>保留在您的设备上</strong>,绝不上传至任何服务器。</p>`
      },
      {
        h: '3. 第三方链接',
        body: `<p>本站可能包含指向第三方网站的链接(例如 GitHub 仓库、应用商店、二维码扫描器官网等)。一旦您点击并离开本站,<strong>我们无法控制这些第三方的数据收集行为</strong>。访问前请阅读各第三方的隐私政策。</p>`
      },
      {
        h: '4. 嵌入式资源',
        body: `<p>为提升体验,部分页面可能嵌入来自 <strong>YouTube、Bilibili 或 X (Twitter)</strong> 的视频或推文。这些嵌入由对应平台加载,可能根据其自身隐私政策设置 Cookie 或收集 IP。若您不希望被这些平台追踪,请在浏览器中开启"屏蔽第三方 Cookie"或使用 <code>uBlock Origin</code> 等隐私扩展。</p>`
      },
      {
        h: '5. 您的权利',
        body: `<p>由于本站不维护任何个人数据,我们通常<strong>无法提供</strong>数据访问、更正、删除或导出等服务。如果您发现本站上有关于您的不准确信息(例如误署名),可通过<strong>联系页面</strong>告知我们,我们核实后将尽快修正。</p>`
      },
      {
        h: '6. 未成年人',
        body: `<p>本站面向具备完全民事行为能力的开发者与普通用户,不专为 14 岁以下儿童设计。如未成年人通过监护人访问本站,同样适用本政策。</p>`
      },
      {
        h: '7. 政策更新',
        body: `<p>本政策可能随产品演进而修订(例如新增订阅功能、嵌入新平台)。修订后,本页顶部的"最后更新"时间戳将同步更新,不再单独通知。持续使用本站即视为接受当前版本。</p>`
      }
    ],
    tldr: '<strong>本站不收集可识别个人身份的信息 · 您浏览器中仅有的存储是主题偏好与历史记录。</strong>'
  },
  about: {
    title: '关于 QR Tool Studio',
    badge: '关于我们',
    updated: '2026-06-28',
    sections: [
      {
        h: '为什么做这个',
        body: `<p>市面上的二维码生成器工具众多,QR Tool Studio 想做那个<strong>轻量、专业、够用</strong>的选项:</p><ul class="list-disc pl-5 space-y-1"><li>浏览器内即时生成,毫秒级响应;</li><li>无需注册,打开网页即用;</li><li>功能专业:支持渐变、Logo、批量、6 种矩阵样式、PNG/SVG/JPEG 多格式导出。</li></ul>`
      },
      {
        h: '产品原则',
        body: `<ul class="list-disc pl-5 space-y-1"><li><strong>纯前端架构</strong> —— 无后端、无数据库,可托管在任意静态平台;</li><li><strong>本地历史</strong> —— 历史记录只存您的浏览器,不上传;</li><li><strong>开源引擎</strong> —— 基于 <code>qr-code-styling</code> 与 <code>qrcode-generator</code> 等成熟开源库;</li><li><strong>免费到底</strong> —— 所有功能永久免费,商用授权,无功能阉割。</li></ul>`
      },
      {
        h: '技术栈',
        body: `<p>Vue 3 (Composition API) · Vite 6 · Tailwind CSS 3 · qr-code-styling 1.6 · JSZip</p>`
      },
      {
        h: '独立声明',
        body: `<p>QR Tool Studio 是<strong>独立项目</strong>,不接受任何形式的付费排序、软文或品牌合作。如未来有任何商业合作,会在相关位置清晰披露。</p>`
      },
      {
        h: '建议与反馈',
        body: `<p>看到功能 bug?想要新功能?欢迎通过下方<strong>联系页面</strong>告诉我们,或在 GitHub 仓库提 Issue / PR。</p>`
      }
    ],
    tldr: '<strong>独立、轻量、专业 —— 让二维码工具回归工具本身。</strong>'
  },
  contact: {
    title: '联系我们 (Contact)',
    badge: '联系',
    updated: '2026-06-28',
    sections: [
      {
        h: '邮箱',
        body: `<p>想提需求、报 bug、谈合作或只是想打个招呼 —— 给我们发邮件即可:</p><p class="text-2xl font-bold tracking-tight"><a href="mailto:andynaonao@gmail.com" class="text-brand-600 dark:text-brand-300 hover:underline">andynaonao@gmail.com</a></p>`
      },
      {
        h: '何时联系我们',
        body: `<ul class="list-disc pl-5 space-y-2"><li><strong>功能建议</strong> —— 想要新的矩阵样式、新的导出格式、新的二维码类型?</li><li><strong>Bug 反馈</strong> —— 某个功能表现异常,带上浏览器版本和复现步骤能帮我们快速定位;</li><li><strong>商业 / 合作</strong> —— 品牌合作、内容分发、API 数据合作等;</li><li><strong>误用 / 侵权</strong> —— 发现站点内容侵犯了您的权益;</li><li><strong>随便聊聊</strong> —— 任何关于二维码、关于工具、关于独立开发的思考都欢迎。</li></ul>`
      },
      {
        h: '提交新功能建议(清单)',
        body: `<p>为提高沟通效率,功能建议邮件请包含以下信息:</p><ul class="list-disc pl-5 space-y-1"><li>想解决的具体场景或痛点;</li><li>期望的交互方式(可选,附草图更佳);</li><li>对哪类用户最有价值。</li></ul><p>信息越完整,评估越快。优质建议通常在 1-3 个工作日内回复。</p>`
      },
      {
        h: '通常不回复的类型',
        body: `<p>为保持收件箱的可读性,我们通常不回复以下内容:</p><ul class="list-disc pl-5 space-y-1"><li>SEO 友链交换 / 批量外链请求;</li><li>与二维码主题无关的"独家专访"或嘉宾邀请;</li><li>与本站产品无关的推广信息。</li></ul><p>若您的请求属于上述类型,提前致歉,也感谢您的理解。</p>`
      },
      {
        h: '隐私',
        body: `<p>您的邮箱仅用于本次沟通,我们不会将您加入任何邮件列表,也不会与第三方分享。如需删除历史往来邮件,直接回复"please delete my email"即可。详细说明见<strong>隐私政策</strong>。</p>`
      }
    ],
    tldr: '<strong>andynaonao@gmail.com</strong>'
  }
}

const current = computed(() => config[props.type] || config.disclaimer)
</script>

<template>
  <transition
    enter-active-class="transition duration-200 ease-out"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition duration-150 ease-in"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div v-if="open" class="fixed inset-0 z-50 grid place-items-center p-4 bg-black/40 backdrop-blur-sm" @click.self="emit('close')">
      <transition
        enter-active-class="transition duration-300 ease-out"
        enter-from-class="opacity-0 scale-95 translate-y-2"
        enter-to-class="opacity-100 scale-100 translate-y-0"
        leave-active-class="transition duration-200 ease-in"
        leave-from-class="opacity-100 scale-100"
        leave-to-class="opacity-0 scale-95"
        appear
      >
        <div class="w-full max-w-2xl max-h-[85vh] flex flex-col glass-panel dark:glass-panel-dark noise-bg overflow-hidden">
          <!-- 头部 -->
          <div class="px-6 sm:px-8 py-5 border-b border-gray-200/60 dark:border-white/10 flex items-start justify-between gap-4">
            <div>
              <div class="text-[10px] font-bold tracking-[0.2em] uppercase text-brand-600 dark:text-brand-300 mb-1.5">{{ current.badge }}</div>
              <h2 class="text-xl sm:text-2xl font-extrabold text-gray-900 dark:text-white">{{ current.title }}</h2>
              <div class="text-xs text-gray-500 dark:text-gray-400 mt-1.5">最后更新:{{ current.updated }}</div>
            </div>
            <button @click="emit('close')" class="theme-toggle-btn !h-9 !w-9 shrink-0" aria-label="关闭">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>

          <!-- 内容 -->
          <div class="flex-1 overflow-y-auto px-6 sm:px-8 py-6 space-y-5 prose-content">
            <section v-for="(s, i) in current.sections" :key="i">
              <h3 class="text-sm sm:text-base font-bold text-gray-900 dark:text-white mb-2">{{ s.h }}</h3>
              <div class="text-sm text-gray-700 dark:text-gray-300 leading-relaxed space-y-2" v-html="s.body"></div>
            </section>
            <div v-if="current.tldr" class="mt-6 p-4 rounded-2xl bg-brand-50/80 dark:bg-brand-500/10 border border-brand-200/60 dark:border-brand-500/20 text-sm text-gray-800 dark:text-gray-200" v-html="current.tldr"></div>
          </div>

          <!-- 底部 -->
          <div class="px-6 sm:px-8 py-4 border-t border-gray-200/60 dark:border-white/10 flex items-center justify-between gap-3 bg-white/40 dark:bg-white/[0.02]">
            <span class="text-xs text-gray-500 dark:text-gray-400">继续浏览即表示您同意本站条款</span>
            <button @click="emit('close')" class="btn-brand text-sm !py-2 !px-4">我知道了</button>
          </div>
        </div>
      </transition>
    </div>
  </transition>
</template>

<style scoped>
.prose-content :deep(code) {
  @apply px-1.5 py-0.5 rounded bg-gray-100 dark:bg-white/5 text-[12px] font-mono text-brand-700 dark:text-brand-300;
}
.prose-content :deep(ul) {
  margin-top: 0.25rem;
}
.prose-content :deep(li) {
  font-size: 0.875rem;
  line-height: 1.6;
}
.prose-content :deep(strong) {
  @apply text-gray-900 dark:text-white;
}
</style>
