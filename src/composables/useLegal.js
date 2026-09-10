import { ref } from 'vue'

/**
 * 免责声明弹窗的共享状态。
 * Footer 在布局层，弹窗也在布局层，但触发点分散（页脚两处 + 移动端），故提升为单例。
 *
 * 注：早先还支持 privacy / about / contact 三种 type，但它们从未被触发，
 * 且内容是中文硬编码，会让英文页面弹出中文；现已删除，只保留 disclaimer。
 * 隐私政策 / 服务条款都有独立的本地化页面（/privacy/、/terms/）。
 */
export const legalOpen = ref(false)

export function openLegal() {
  legalOpen.value = true
}

export function closeLegal() {
  legalOpen.value = false
}
