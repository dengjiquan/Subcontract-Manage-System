<template>
  <el-switch
    v-model="isDark"
    inline-prompt
    :active-icon="Moon"
    :inactive-icon="Sunny"
    @change="handleChange"
  />
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Moon, Sunny } from '@element-plus/icons-vue'
import { currentTheme, setTheme } from '@/styles/theme'

const isDark = computed({
  get: () => currentTheme.value === 'dark',
  set: (value) => setTheme(value ? 'dark' : 'light')
})

const handleChange = (value: boolean) => {
  // 这里可以添加其他主题切换相关的逻辑
  console.log('Theme changed:', value ? 'dark' : 'light')
}
</script> 