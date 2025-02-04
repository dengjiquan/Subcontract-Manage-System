<template>
  <div class="app-container">
    <div class="filter-container">
      <el-select
        v-model="queryParams.subcontractor_id"
        placeholder="选择分包商"
        clearable
        class="filter-item"
        style="width: 200px"
      >
        <el-option
          v-for="item in subcontractors"
          :key="item.id"
          :label="item.name"
          :value="item.id"
        />
      </el-select>
      
      <el-input
        v-model="queryParams.contract_number"
        placeholder="合同编号"
        style="width: 200px"
        class="filter-item"
        @keyup.enter="handleFilter"
      />
      
      <el-select
        v-model="queryParams.status"
        placeholder="合同状态"
        clearable
        class="filter-item"
        style="width: 150px"
      >
        <el-option label="草稿" value="draft" />
        <el-option label="生效" value="active" />
        <el-option label="完成" value="completed" />
        <el-option label="终止" value="terminated" />
      </el-select>
      
      <el-button
        class="filter-item"
        type="primary"
        icon="Search"
        @click="handleFilter"
      >
        搜索
      </el-button>
      
      <el-button
        class="filter-item"
        type="primary"
        icon="Plus"
        @click="handleCreate"
      >
        新增
      </el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="list"
      border
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
        prop="start_date"
        label="开始日期"
        min-width="120"
      />
      <el-table-column
        prop="end_date"
        label="结束日期"
        min-width="120"
      />
      <el-table-column
        prop="contract_amount"
        label="合同金额"
        min-width="120"
      />
      <el-table-column
        prop="status"
        label="状态"
        min-width="100"
      >
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        width="250"
        fixed="right"
      >
        <template #default="{ row }">
          <el-button
            type="primary"
            link
            @click="handleUpdate(row)"
          >
            编辑
          </el-button>
          <el-button
            type="primary"
            link
            @click="handleViewBOQ(row)"
          >
            工程量清单
          </el-button>
          <el-button
            type="primary"
            link
            @click="handleViewSettlements(row)"
          >
            结算记录
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-model:current-page="queryParams.page"
      v-model:page-size="queryParams.limit"
      :total="total"
      :page-sizes="[10, 20, 30, 50]"
      layout="total, sizes, prev, pager, next"
      class="pagination-container"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />

    <!-- 新增/编辑对话框 -->
    <contract-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      :form="form"
      :subcontractors="subcontractors"
      @submit="handleSubmit"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'
import type { Contract, Subcontractor } from '@/types/api'
import ContractDialog from './components/ContractDialog.vue'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const list = ref<Contract[]>([])
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const subcontractors = ref<Subcontractor[]>([])

const queryParams = reactive({
  page: 1,
  limit: 10,
  subcontractor_id: undefined as number | undefined,
  contract_number: '',
  status: ''
})

const form = reactive({
  id: undefined as number | undefined,
  subcontractor_id: undefined as number | undefined,
  contract_number: '',
  start_date: '',
  end_date: '',
  contract_amount: '',
  status: 'draft',
  remarks: ''
})

// 获取分包商列表
const getSubcontractors = async () => {
  try {
    const response = await request.get('/v1/subcontractors', { params: { limit: 1000 } })
    subcontractors.value = response.items
  } catch (error) {
    console.error('Get subcontractors error:', error)
  }
}

// 获取分包商名称
const getSubcontractorName = (id: number) => {
  const subcontractor = subcontractors.value.find(item => item.id === id)
  return subcontractor?.name || '-'
}

// 获取状态类型
const getStatusType = (status: string) => {
  const statusMap: Record<string, string> = {
    draft: 'info',
    active: 'success',
    completed: '',
    terminated: 'danger'
  }
  return statusMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    draft: '草稿',
    active: '生效',
    completed: '完成',
    terminated: '终止'
  }
  return statusMap[status] || status
}

// 获取合同列表
const getList = async () => {
  try {
    loading.value = true
    const response = await request.get('/v1/contracts', { params: queryParams })
    list.value = response.items
    total.value = response.total
  } finally {
    loading.value = false
  }
}

const handleFilter = () => {
  queryParams.page = 1
  getList()
}

const resetForm = () => {
  form.id = undefined
  form.subcontractor_id = undefined
  form.contract_number = ''
  form.start_date = ''
  form.end_date = ''
  form.contract_amount = ''
  form.status = 'draft'
  form.remarks = ''
}

const handleCreate = () => {
  resetForm()
  dialogTitle.value = '新增合同'
  dialogVisible.value = true
}

const handleUpdate = (row: Contract) => {
  Object.assign(form, row)
  dialogTitle.value = '编辑合同'
  dialogVisible.value = true
}

const handleSubmit = async (formData: typeof form) => {
  try {
    if (formData.id) {
      await request.put(`/v1/contracts/${formData.id}`, formData)
      ElMessage.success('更新成功')
    } else {
      await request.post('/v1/contracts', formData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    getList()
  } catch (error) {
    console.error('Submit error:', error)
  }
}

const handleViewBOQ = (row: Contract) => {
  router.push({
    path: '/boq-items',
    query: { contract_id: row.id }
  })
}

const handleViewSettlements = (row: Contract) => {
  router.push({
    path: '/settlements',
    query: { contract_id: row.id }
  })
}

const handleSizeChange = (val: number) => {
  queryParams.limit = val
  getList()
}

const handleCurrentChange = (val: number) => {
  queryParams.page = val
  getList()
}

onMounted(async () => {
  // 如果路由中有分包商ID，则设置查询参数
  if (route.query.subcontractor_id) {
    queryParams.subcontractor_id = Number(route.query.subcontractor_id)
  }
  await getSubcontractors()
  getList()
})
</script>

<style lang="scss" scoped>
.app-container {
  padding: 20px;
}

.filter-container {
  padding-bottom: 10px;
  .filter-item {
    margin-right: 10px;
  }
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style> 