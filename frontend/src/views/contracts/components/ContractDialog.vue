<template>
  <el-dialog
    :title="title"
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    width="600px"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-width="100px"
    >
      <el-form-item label="分包商" prop="subcontractor_id">
        <el-select
          v-model="formData.subcontractor_id"
          placeholder="请选择分包商"
          style="width: 100%"
        >
          <el-option
            v-for="item in subcontractors"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="合同编号" prop="contract_number">
        <el-input v-model="formData.contract_number" />
      </el-form-item>

      <el-form-item label="开始日期" prop="start_date">
        <el-date-picker
          v-model="formData.start_date"
          type="date"
          placeholder="选择开始日期"
          style="width: 100%"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>

      <el-form-item label="结束日期" prop="end_date">
        <el-date-picker
          v-model="formData.end_date"
          type="date"
          placeholder="选择结束日期"
          style="width: 100%"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>

      <el-form-item label="合同金额" prop="contract_amount">
        <el-input
          v-model="formData.contract_amount"
          type="number"
          placeholder="请输入合同金额"
        >
          <template #append>元</template>
        </el-input>
      </el-form-item>

      <el-form-item label="状态" prop="status">
        <el-select
          v-model="formData.status"
          placeholder="请选择状态"
          style="width: 100%"
        >
          <el-option label="草稿" value="draft" />
          <el-option label="生效" value="active" />
          <el-option label="完成" value="completed" />
          <el-option label="终止" value="terminated" />
        </el-select>
      </el-form-item>

      <el-form-item label="备注" prop="remarks">
        <el-input
          v-model="formData.remarks"
          type="textarea"
          :rows="3"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="$emit('update:modelValue', false)">取消</el-button>
      <el-button type="primary" @click="handleSubmit">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import type { FormInstance } from 'element-plus'
import type { Contract, Subcontractor } from '@/types/api'

const props = defineProps<{
  modelValue: boolean
  title: string
  form: Partial<Contract>
  subcontractors: Subcontractor[]
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'submit', form: Partial<Contract>): void
}>()

const formRef = ref<FormInstance>()
const formData = reactive<Partial<Contract>>({})

const rules = {
  subcontractor_id: [{ required: true, message: '请选择分包商', trigger: 'change' }],
  contract_number: [{ required: true, message: '请输入合同编号', trigger: 'blur' }],
  start_date: [{ required: true, message: '请选择开始日期', trigger: 'change' }],
  end_date: [{ required: true, message: '请选择结束日期', trigger: 'change' }],
  contract_amount: [{ required: true, message: '请输入合同金额', trigger: 'blur' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

watch(
  () => props.form,
  (newVal) => {
    Object.assign(formData, newVal)
  },
  { immediate: true, deep: true }
)

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate()
  emit('submit', formData)
}
</script> 