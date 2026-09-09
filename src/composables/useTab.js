import { ref } from 'vue'

/**
 * 首页生成器 Tab 的共享状态。
 * Header（布局层）与 HomeView（视图层）都需要读写，
 * 因此提升为模块级单例（SSR 下默认 'single'，保证预渲染输出稳定）。
 */
export const tab = ref('single')
