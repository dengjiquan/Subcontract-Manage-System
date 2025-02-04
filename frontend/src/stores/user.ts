import { defineStore } from 'pinia'
import { ref } from 'vue'
import request from '@/utils/request'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref<any>(null)

  const login = async (username: string, password: string) => {
    try {
      const response = await request.post('/v1/auth/login', {
        username,
        password
      })
      token.value = response.token
      localStorage.setItem('token', response.token)
      return response
    } catch (error) {
      console.error('Login error:', error)
      throw error
    }
  }

  const logout = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
  }

  const getUserInfo = async () => {
    try {
      const response = await request.get('/v1/auth/user-info')
      userInfo.value = response
      return response
    } catch (error) {
      console.error('Get user info error:', error)
      throw error
    }
  }

  return {
    token,
    userInfo,
    login,
    logout,
    getUserInfo
  }
}) 