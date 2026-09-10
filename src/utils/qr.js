import JSZip from 'jszip'

/**
 * 触发浏览器下载 Blob
 */
export function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  setTimeout(() => URL.revokeObjectURL(url), 1500)
}

/**
 * 把 qr-code-styling 实例的画布转成 Blob
 */
export async function qrInstanceToBlob(qrCode, format = 'png') {
  // qr-code-styling 1.6+ 提供 getRawData
  if (typeof qrCode.getRawData === 'function') {
    const ext = format === 'jpeg' ? 'jpeg' : format
    const blob = await qrCode.getRawData(ext)
    return blob
  }
  // 兜底:从 DOM 抓 canvas
  const canvas = document.querySelector('#qr-preview canvas, #qr-preview svg')
  if (canvas && canvas.tagName === 'CANVAS') {
    return new Promise((resolve) => {
      canvas.toBlob((b) => resolve(b), format === 'jpeg' ? 'image/jpeg' : 'image/png', 0.95)
    })
  }
  return null
}

/**
 * 读取 file -> dataURL
 */
export function fileToDataURL(file) {
  return new Promise((resolve, reject) => {
    const r = new FileReader()
    r.onload = () => resolve(r.result)
    r.onerror = reject
    r.readAsDataURL(file)
  })
}

/**
 * 批量生成:每行文本生成一个二维码,打包成 ZIP
 */
export async function batchGenerate(opts) {
  const { default: QRCodeStyling } = await import('qr-code-styling')
  const lines = opts.lines.map(l => l.trim()).filter(Boolean)
  if (!lines.length) return null
  const zip = new JSZip()
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    const instance = new QRCodeStyling({
      width: 600,
      height: 600,
      type: 'canvas',
      data: line,
      margin: opts.margin ?? 4,
      qrOptions: { errorCorrectionLevel: opts.errorCorrectionLevel || 'M' },
      dotsOptions: {
        color: opts.dotsColor,
        type: opts.dotsType
      },
      backgroundOptions: { color: opts.backgroundColor },
      image: opts.logoDataUrl || undefined,
      imageOptions: {
        crossOrigin: 'anonymous',
        margin: 6,
        imageSize: opts.logoSize ?? 0.3,
        hideBackgroundDots: true
      }
    })
    const blob = await instance.getRawData('png')
    const safeName = line.replace(/[\\/:*?"<>|]/g, '_').slice(0, 32) || `qr-${i + 1}`
    zip.file(`${String(i + 1).padStart(2, '0')}-${safeName}.png`, blob)
  }
  return await zip.generateAsync({ type: 'blob' })
}

/**
 * 推断内容类型。
 * 只返回 type，不返回文案 —— 文案由调用方走 i18n（gen.preview.*）。
 * type 的取值必须与 SingleGenerator 的 detectedLabel 映射表一致，
 * 否则会回退成 type 字面量（早期这里返回过中文 label，导致所有语言都显示中文）。
 */
export function detectContentType(text) {
  if (!text) return { type: 'empty' }
  const v = text.trim()
  if (/^https?:\/\//i.test(v)) return { type: 'url' }
  if (/^mailto:/i.test(v)) return { type: 'email' }
  if (/^sms:/i.test(v)) return { type: 'sms' }
  if (/^tel:/i.test(v)) return { type: 'tel' }
  if (/^wifi:/i.test(v)) return { type: 'wifi' }
  if (/^BEGIN:VCARD/i.test(v)) return { type: 'vcard' }
  if (/^[0-9+\-\s()]{6,}$/.test(v)) return { type: 'tel' }
  return { type: 'text' }
}
