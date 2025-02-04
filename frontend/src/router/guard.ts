import { Router } from 'vue-router'
import { useUserStore } from '@/stores/user'

const whiteList = ['/login']

export function setupRouterGuard(router: Router) {
  router.beforeEach(async (to, from, next) => {
    const userStore = useUserStore()
    const hasToken = userStore.token

    if (hasToken) {
      if (to.path === '/login') {
        next({ path: '/' })
      } else {
        // 这里可以添加获取用户信息的逻辑
        next()
      }
    } else {
      if (whiteList.includes(to.path)) {
        next()
      } else {
        next(`/login?redirect=${to.path}`)
      }
    }
  })
} 