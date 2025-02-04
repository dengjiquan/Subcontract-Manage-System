import { App } from 'vue'
import { ElMessage } from 'element-plus'

export function setupErrorHandler(app: App) {
  app.config.errorHandler = (err, instance, info) => {
    console.error('Global error:', err)
    console.error('Error instance:', instance)
    console.error('Error info:', info)

    ElMessage.error('系统错误，请稍后重试')
  }

  window.onerror = (message, source, lineno, colno, error) => {
    console.error('Window error:', {
      message,
      source,
      lineno,
      colno,
      error
    })
  }

  window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason)
  })
} 