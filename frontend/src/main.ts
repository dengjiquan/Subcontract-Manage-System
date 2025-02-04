import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { i18n } from './i18n'
import App from './App.vue'
import router from './router'
import { setupRouterGuard } from './router/guard'
import { setupErrorHandler } from './utils/error-handler'
import { setTheme, currentTheme } from './styles/theme'

import 'element-plus/dist/index.css'
import './styles/index.scss'

const app = createApp(App)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 设置主题
setTheme(currentTheme.value as 'light' | 'dark')

// 设置路由守卫
setupRouterGuard(router)

// 设置错误处理
setupErrorHandler(app)

app.use(createPinia())
app.use(router)
app.use(ElementPlus)
app.use(i18n)

app.mount('#app') 