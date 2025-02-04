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
      
      <el-input
        v-model="queryParams.item_name"
        placeholder="项目名称"
        style="width: 200px"
        class="filter-item"
        @keyup.enter="handleFilter"
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
        prop="item_name"
        label="项目名称"
        min-width="200"
      />
      <el-table-column
        prop="unit"
        label="单位"
        min-width="100"
      />
      <el-table-column
        prop="unit_price"
        label="单价"
        min-width="120"
      />
      <el-table-column
        prop="total_quantity"
        label="总工程量"
        min-width="120"
      />
      <el-table-column
        prop="total_price"
        label="总价"
        min-width="120"
      />
      <el-table-column
        label="操作"
        width="150"
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
    <boq-item-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      :form="form"
      :contract-id="queryParams.contract_id"
      @submit="handleSubmit"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'
import type { BOQItem, Contract } from '@/types/api'
import BOQItemDialog from './components/BOQItemDialog.vue'

const route = useRoute()
const loading = ref(false)
const list = ref<BOQItem[]>([])
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const contracts = ref<Contract[]>([])

const queryParams = reactive({
  page: 1,
  limit: 10,
  contract_id: undefined as number | undefined,
  item_name: ''
})

const form = reactive({
  id: undefined as number | undefined,
  contract_id: undefined as number | undefined,
  item_name: '',
  unit: '',
  unit_price: '',
  total_quantity: '',
  total_price: ''
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

// 获取工程量清单列表
const getList = async () => {
  try {
    loading.value = true
    const response = await request.get('/v1/boq-items', { params: queryParams })
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
  form.item_name = ''
  form.unit = ''
  form.unit_price = ''
  form.total_quantity = ''
  form.total_price = ''
}

const handleCreate = () => {
  resetForm()
  dialogTitle.value = '新增工程量清单项'
  dialogVisible.value = true
}

const handleUpdate = (row: BOQItem) => {
  Object.assign(form, row)
  dialogTitle.value = '编辑工程量清单项'
  dialogVisible.value = true
}

const handleSubmit = async (formData: typeof form) => {
  try {
    if (formData.id) {
      await request.put(`/v1/boq-items/${formData.id}`, formData)
      ElMessage.success('更新成功')
    } else {
      await request.post('/v1/boq-items', formData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    getList()
  } catch (error) {
    console.error('Submit error:', error)
  }
}

const handleDelete = async (row: BOQItem) => {
  try {
    await ElMessageBox.confirm('确认删除该工程量清单项吗？', '提示', {
      type: 'warning'
    })
    await request.delete(`/v1/boq-items/${row.id}`)
    ElMessage.success('删除成功')
    getList()
  } catch (error) {
    console.error('Delete error:', error)
  }
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