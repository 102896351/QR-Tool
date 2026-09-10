/**
 * 免责声明弹窗内容（页脚 → Disclaimer）
 *
 * 为什么单独放这里，而不是塞进 locales/*.js：
 * 这是一段长文法务文案，不属于「界面文案」。整站的语言策略是
 * 「界面全翻译、长文只保留 en/zh」——和博客正文保持一致。
 * 因此这里只维护 en / zh 两份，其余语言回退英文（见 pickContent）。
 *
 * 正文是 HTML 片段，由 LegalModal 用 v-html 渲染，允许的标签：
 * <p> <strong> <code> <ul> <li> <a>
 */

export const DISCLAIMER_UPDATED = '2026-06-28'

export const DISCLAIMER = {
  en: {
    title: 'Disclaimer',
    badge: 'Legal',
    sections: [
      {
        h: '1. Technical and informational use only',
        body: `<p><strong>QR Tool Studio</strong> is an independently maintained online QR code generator for developers and everyday users. All content on this site (including but not limited to copy, examples, links, screenshots and comments) is provided <strong>for technical learning and informational reference only</strong>, and does not constitute investment, legal, tax, medical or other professional advice.</p>`
      },
      {
        h: '2. Independent third party, no endorsement',
        body: `<p>This site is an <strong>independent third-party project</strong> with no affiliation, endorsement, sponsorship or partnership with any commercial entity, platform operator or investor. All product names, trademarks, logos and brand assets belong to their respective owners and are used here for identification and reference only.</p>`
      },
      {
        h: '3. Provided "as is", without warranty',
        body: `<p>The QR code generation feature is built on a mature open-source library (<code>qr-code-styling</code>). We make every effort to ensure the output conforms to the QR Code ISO/IEC 18004 standard, but it is still provided on an <strong>"AS IS"</strong> basis, <strong>without any warranty of absolute accuracy, completeness, timeliness or fitness for a particular purpose</strong>. Before commercial use, please test thoroughly in your target environment (scanning devices, printing process, paper stock).</p>`
      },
      {
        h: '4. Third-party links and services',
        body: `<p>This site may contain links to third-party websites (GitHub, social platforms, official QR scanner sites, etc.) and advertising slots provided by third parties. The content, policies, availability and security of those services are the responsibility of their respective operators, and <strong>this site accepts no liability for their actions</strong>. When you leave this site, please read and comply with the third party's terms and privacy policy.</p>`
      },
      {
        h: '5. Limitation of liability',
        body: `<p>To the maximum extent permitted by applicable law, the authors, contributors and hosting providers of this site <strong>shall not be liable for any direct, indirect, incidental, special or consequential damages</strong> arising from the use of, or inability to use, the content of this site (including but not limited to loss of data, business interruption, loss of opportunity or loss of profit).</p><p>Please use this site <strong>only to the extent permitted by applicable law</strong>. This tool must not be used for activities that violate local laws and regulations, nor as a tool or teaching material for unlawful acts.</p>`
      },
      {
        h: '6. Changes and termination',
        body: `<p>We may <strong>modify, suspend or take down</strong> any page, feature, layout or this disclaimer at any time without prior notice. Significant changes are recorded in the <code>CHANGELOG</code> of the GitHub repository — PRs and issues are welcome.</p>`
      }
    ],
    tldr: '<strong>For technical exchange and informational reference only · Use within the limits of the law · Rely on official sources for commercial or legal decisions.</strong>'
  },

  zh: {
    title: '免责声明 (Disclaimer)',
    badge: '法律声明',
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
        h: '4. 第三方链接与服务',
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
  }
}

/** 取对应语言的内容；没有译文时回退英文（长文只维护 en / zh） */
export function pickDisclaimer(lang) {
  return DISCLAIMER[lang] || DISCLAIMER.en
}
