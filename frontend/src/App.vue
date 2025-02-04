<template>
  <el-config-provider :locale="locale">
    <router-view />
  </el-config-provider>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import en from 'element-plus/dist/locale/en.mjs'

const { locale: currentLocale } = useI18n()

const locale = computed(() => {
  return currentLocale.value === 'zh-CN' ? zhCn : en
})
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  background-color: var(--el-bg-color);
  color: var(--el-text-color-primary);
}

#app {
  height: 100%;
}
</style> 