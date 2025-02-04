<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="queryParams.name"
        placeholder="分包商名称"
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
        prop="name"
        label="分包商名称"
        min-width="200"
      />
      <el-table-column
        prop="contact_name"
        label="联系人"
        min-width="120"
      />
      <el-table-column
        prop="contact_phone"
        label="联系电话"
        min-width="120"
      />
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
            @click="handleViewContracts(row)"
          >
            查看合同
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
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="分包商名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="联系人" prop="contact_name">
          <el-input v-model="form.contact_name" />
        </el-form-item>
        <el-form-item label="联系电话" prop="contact_phone">
          <el-input v-model="form.contact_phone" />
        </el-form-item>
        <el-form-item label="备注" prop="remarks">
          <el-input
            v-model="form.remarks"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'
import request from '@/utils/request'
import type { Subcontractor } from '@/types/api'

const router = useRouter()
const loading = ref(false)
const list = ref<Subcontractor[]>([])
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref<FormInstance>()

const queryParams = reactive({
  page: 1,
  limit: 10,
  name: ''
})

const form = reactive({
  id: undefined,
  name: '',
  contact_name: '',
  contact_phone: '',
  remarks: ''
})

const rules = {
  name: [{ required: true, message: '请输入分包商名称', trigger: 'blur' }],
  contact_name: [{ required: true, message: '请输入联系人', trigger: 'blur' }],
  contact_phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }]
}

const getList = async () => {
  try {
    loading.value = true
    const response = await request.get('/v1/subcontractors', { params: queryParams })
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
  form.name = ''
  form.contact_name = ''
  form.contact_phone = ''
  form.remarks = ''
}

const handleCreate = () => {
  resetForm()
  dialogTitle.value = '新增分包商'
  dialogVisible.value = true
}

const handleUpdate = (row: Subcontractor) => {
  Object.assign(form, row)
  dialogTitle.value = '编辑分包商'
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate()
  
  try {
    if (form.id) {
      await request.put(`/v1/subcontractors/${form.id}`, form)
      ElMessage.success('更新成功')
    } else {
      await request.post('/v1/subcontractors', form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    getList()
  } catch (error) {
    console.error('Submit error:', error)
  }
}

const handleDelete = async (row: Subcontractor) => {
  try {
    await ElMessageBox.confirm('确认删除该分包商吗？', '提示', {
      type: 'warning'
    })
    await request.delete(`/v1/subcontractors/${row.id}`)
    ElMessage.success('删除成功')
    getList()
  } catch (error) {
    console.error('Delete error:', error)
  }
}

const handleViewContracts = (row: Subcontractor) => {
  router.push({
    path: '/contracts',
    query: { subcontractor_id: row.id }
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

onMounted(() => {
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