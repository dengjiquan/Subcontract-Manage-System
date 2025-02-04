import { ref } from 'vue'

export const themes = {
  light: {
    '--el-color-primary': '#409EFF',
    '--el-color-success': '#67C23A',
    '--el-color-warning': '#E6A23C',
    '--el-color-danger': '#F56C6C',
    '--el-color-info': '#909399',
    '--el-bg-color': '#ffffff',
    '--el-text-color-primary': '#303133',
    '--el-text-color-regular': '#606266',
    '--el-border-color': '#DCDFE6'
  },
  dark: {
    '--el-color-primary': '#409EFF',
    '--el-color-success': '#67C23A',
    '--el-color-warning': '#E6A23C',
    '--el-color-danger': '#F56C6C',
    '--el-color-info': '#909399',
    '--el-bg-color': '#141414',
    '--el-text-color-primary': '#FFFFFF',
    '--el-text-color-regular': '#CCCCCC',
    '--el-border-color': '#434343'
  }
}

export const currentTheme = ref(localStorage.getItem('theme') || 'light')

export function setTheme(theme: 'light' | 'dark') {
  const root = document.documentElement
  const variables = themes[theme]

  for (const [key, value] of Object.entries(variables)) {
    root.style.setProperty(key, value)
  }

  currentTheme.value = theme
  localStorage.setItem('theme', theme)
} 