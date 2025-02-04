<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>分包商数量</span>
            </div>
          </template>
          <div class="card-body">
            <h2>{{ stats.subcontractor_count }}</h2>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>合同总数</span>
            </div>
          </template>
          <div class="card-body">
            <h2>{{ stats.contract_count }}</h2>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>合同总金额</span>
            </div>
          </template>
          <div class="card-body">
            <h2>{{ stats.total_contract_amount }}元</h2>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>已结算金额</span>
            </div>
          </template>
          <div class="card-body">
            <h2>{{ stats.total_settlement_amount }}元</h2>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-4">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>最近的结算记录</span>
            </div>
          </template>
          <el-table
            :data="recentSettlements"
            style="width: 100%"
          >
            <el-table-column
              label="合同编号"
              min-width="150"
            >
              <template #default="{ row }">
                {{ getContractNumber(row.contract_id) }}
              </template>
            </el-table-column>
            <el-table-column
              prop="settlement_date"
              label="结算日期"
              min-width="120"
            />
            <el-table-column
              prop="settlement_amount"
              label="结算金额"
              min-width="120"
            >
              <template #default="{ row }">
                {{ row.settlement_amount }}元
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>即将到期的合同</span>
            </div>
          </template>
          <el-table
            :data="expiringContracts"
            style="width: 100%"
          >
            <el-table-column
              prop="contract_number"
              label="合同编号"
              min-width="150"
            />
            <el-table-column
              label="分包商"
              min-width="200"
            >
              <template #default="{ row }">
                {{ getSubcontractorName(row.subcontractor_id) }}
              </template>
            </el-table-column>
            <el-table-column
              prop="end_date"
              label="到期日期"
              min-width="120"
            />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Contract, Settlement, Subcontractor } from '@/types/api'
import request from '@/utils/request'

interface Stats {
  subcontractor_count: number
  contract_count: number
  total_contract_amount: string
  total_settlement_amount: string
}

const stats = ref<Stats>({
  subcontractor_count: 0,
  contract_count: 0,
  total_contract_amount: '0',
  total_settlement_amount: '0'
})

const recentSettlements = ref<Settlement[]>([])
const expiringContracts = ref<Contract[]>([])
const contracts = ref<Contract[]>([])
const subcontractors = ref<Subcontractor[]>([])

// 获取统计数据
const getStats = async () => {
  try {
    const response = await request.get('/v1/stats')
    stats.value = response
  } catch (error) {
    console.error('Get stats error:', error)
  }
}

// 获取最近的结算记录
const getRecentSettlements = async () => {
  try {
    const response = await request.get('/v1/settlements', {
      params: { limit: 5, sort: '-settlement_date' }
    })
    recentSettlements.value = response.items
  } catch (error) {
    console.error('Get recent settlements error:', error)
  }
}

// 获取即将到期的合同
const getExpiringContracts = async () => {
  try {
    const response = await request.get('/v1/contracts', {
      params: { limit: 5, status: 'active', sort: 'end_date' }
    })
    expiringContracts.value = response.items
  } catch (error) {
    console.error('Get expiring contracts error:', error)
  }
}

// 获取合同列表
const getContracts = async () => {
  try {
    const response = await request.get('/v1/contracts', { params: { limit: 1000 } })
    contracts.value = response.items
  } catch (error) {
    console.error('Get contracts error:', error)
  }
}

// 获取分包商列表
const getSubcontractors = async () => {
  try {
    const response = await request.get('/v1/subcontractors', { params: { limit: 1000 } })
    subcontractors.value = response.items
  } catch (error) {
    console.error('Get subcontractors error:', error)
  }
}

// 获取合同编号
const getContractNumber = (id: number) => {
  const contract = contracts.value.find(item => item.id === id)
  return contract?.contract_number || '-'
}

// 获取分包商名称
const getSubcontractorName = (id: number) => {
  const subcontractor = subcontractors.value.find(item => item.id === id)
  return subcontractor?.name || '-'
}

onMounted(async () => {
  await Promise.all([
    getStats(),
    getRecentSettlements(),
    getExpiringContracts(),
    getContracts(),
    getSubcontractors()
  ])
})
</script>

<style lang="scss" scoped>
.app-container {
  padding: 20px;
}

.mt-4 {
  margin-top: 1rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-body {
  text-align: center;
  h2 {
    margin: 0;
    font-size: 24px;
    color: #409EFF;
  }
}
</style> 