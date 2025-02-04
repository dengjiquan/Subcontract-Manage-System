import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/layouts/index.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/login/index.vue'),
      meta: { title: '登录' }
    },
    {
      path: '/',
      component: Layout,
      redirect: '/dashboard',
      children: [
        {
          path: 'dashboard',
          name: 'Dashboard',
          component: () => import('@/views/dashboard/index.vue'),
          meta: { title: '首页', icon: 'dashboard' }
        },
        {
          path: 'subcontractors',
          name: 'Subcontractors',
          component: () => import('@/views/subcontractors/index.vue'),
          meta: { title: '分包商管理', icon: 'users' }
        },
        {
          path: 'contracts',
          name: 'Contracts',
          component: () => import('@/views/contracts/index.vue'),
          meta: { title: '合同管理', icon: 'document' }
        },
        {
          path: 'boq-items',
          name: 'BOQItems',
          component: () => import('@/views/boq-items/index.vue'),
          meta: { title: '工程量清单', icon: 'list' }
        },
        {
          path: 'settlements',
          name: 'Settlements',
          component: () => import('@/views/settlements/index.vue'),
          meta: { title: '结算管理', icon: 'money' }
        }
      ]
    }
  ]
})

export default router 