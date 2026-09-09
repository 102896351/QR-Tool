import { ref } from 'vue'

/**
 * 法律弹窗（免责声明 / Cookie 说明）的共享状态。
 * Footer 在布局层，弹窗也在布局层，但触发点分散，故提升为单例。
 */
export const legalOpen = ref(false)
export const legalType = ref('disclaimer') // disclaimer | privacy | about | contact

export function openLegal(type) {
  legalType.value = type
  legalOpen.value = true
}

export function closeLegal() {
  legalOpen.value = false
}
