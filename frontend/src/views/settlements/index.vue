<template>
  <div class="app-container">
    <div class="filter-container">
      <el-select
        v-model="queryParams.contract_id"
        placeholder="选择合同"
        clearable
        class="filter-item"
        style="width: 200px"
        @change="handleContractChange"
      >
        <el-option
          v-for="item in contracts"
          :key="item.id"
          :label="item.contract_number"
          :value="item.id"
        />
      </el-select>
      
      <el-date-picker
        v-model="queryParams.settlement_date"
        type="date"
        placeholder="结算日期"
        class="filter-item"
        style="width: 200px"
        value-format="YYYY-MM-DD"
      />
      
      <el-button
        class="filter-item"
        type="primary"
        icon="Search"
        @click="handleFilter"
      >
        搜索
      </el-button>
      
      <el-button
        v-if="queryParams.contract_id"
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
      <el-table-column
        prop="remarks"
        label="备注"
        min-width="200"
      />
      <el-table-column
        label="操作"
        width="200"
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
            @click="handleViewDetails(row)"
          >
            查看明细
          </el-button>
          <el-button
            type="danger"
            link
            @click="handleDelete(row)"
          >
            删除
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
    <settlement-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      :form="form"
      :contract-id="queryParams.contract_id"
      @submit="handleSubmit"
    />

    <!-- 结算明细对话框 -->
    <settlement-detail-dialog
      v-model="detailDialogVisible"
      :settlement="currentSettlement"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'
import type { Settlement, Contract } from '@/types/api'
import SettlementDialog from './components/SettlementDialog.vue'
import SettlementDetailDialog from './components/SettlementDetailDialog.vue'

const route = useRoute()
const loading = ref(false)
const list = ref<Settlement[]>([])
const total = ref(0)
const dialogVisible = ref(false)
const detailDialogVisible = ref(false)
const dialogTitle = ref('')
const contracts = ref<Contract[]>([])
const currentSettlement = ref<Settlement>()

const queryParams = reactive({
  page: 1,
  limit: 10,
  contract_id: undefined as number | undefined,
  settlement_date: ''
})

const form = reactive({
  id: undefined as number | undefined,
  contract_id: undefined as number | undefined,
  settlement_date: '',
  settlement_amount: '',
  remarks: '',
  details: []
})

// 获取合同列表
const getContracts = async () => {
  try {
    const response = await request.get('/v1/contracts', { params: { limit: 1000 } })
    contracts.value = response.items
  } catch (error) {
    console.error('Get contracts error:', error)
  }
}

// 获取合同编号
const getContractNumber = (id: number) => {
  const contract = contracts.value.find(item => item.id === id)
  return contract?.contract_number || '-'
}

// 获取结算列表
const getList = async () => {
  try {
    loading.value = true
    const response = await request.get('/v1/settlements', { params: queryParams })
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

const handleContractChange = () => {
  handleFilter()
}

const resetForm = () => {
  form.id = undefined
  form.contract_id = queryParams.contract_id
  form.settlement_date = ''
  form.settlement_amount = ''
  form.remarks = ''
  form.details = []
}

const handleCreate = () => {
  resetForm()
  dialogTitle.value = '新增结算'
  dialogVisible.value = true
}

const handleUpdate = (row: Settlement) => {
  Object.assign(form, row)
  dialogTitle.value = '编辑结算'
  dialogVisible.value = true
}

const handleSubmit = async (formData: typeof form) => {
  try {
    if (formData.id) {
      await request.put(`/v1/settlements/${formData.id}`, formData)
      ElMessage.success('更新成功')
    } else {
      await request.post('/v1/settlements', formData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    getList()
  } catch (error) {
    console.error('Submit error:', error)
  }
}

const handleDelete = async (row: Settlement) => {
  try {
    await ElMessageBox.confirm('确认删除该结算记录吗？', '提示', {
      type: 'warning'
    })
    await request.delete(`/v1/settlements/${row.id}`)
    ElMessage.success('删除成功')
    getList()
  } catch (error) {
    console.error('Delete error:', error)
  }
}

const handleViewDetails = (row: Settlement) => {
  currentSettlement.value = row
  detailDialogVisible.value = true
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
  await getContracts()
  // 如果路由中有合同ID，则设置查询参数
  if (route.query.contract_id) {
    queryParams.contract_id = Number(route.query.contract_id)
  }
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