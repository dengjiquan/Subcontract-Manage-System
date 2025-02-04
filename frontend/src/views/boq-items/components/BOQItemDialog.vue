<template>
  <el-dialog
    :title="title"
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    width="500px"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-width="100px"
    >
      <el-form-item label="项目名称" prop="item_name">
        <el-input v-model="formData.item_name" />
      </el-form-item>

      <el-form-item label="单位" prop="unit">
        <el-input v-model="formData.unit" />
      </el-form-item>

      <el-form-item label="单价" prop="unit_price">
        <el-input
          v-model="formData.unit_price"
          type="number"
          @input="calculateTotalPrice"
        >
          <template #append>元</template>
        </el-input>
      </el-form-item>

      <el-form-item label="总工程量" prop="total_quantity">
        <el-input
          v-model="formData.total_quantity"
          type="number"
          @input="calculateTotalPrice"
        />
      </el-form-item>

      <el-form-item label="总价" prop="total_price">
        <el-input
          v-model="formData.total_price"
          type="number"
          disabled
        >
          <template #append>元</template>
        </el-input>
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
import type { BOQItem } from '@/types/api'

const props = defineProps<{
  modelValue: boolean
  title: string
  form: Partial<BOQItem>
  contractId: number | undefined
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'submit', form: Partial<BOQItem>): void
}>()

const formRef = ref<FormInstance>()
const formData = reactive<Partial<BOQItem>>({})

const rules = {
  item_name: [{ required: true, message: '请输入项目名称', trigger: 'blur' }],
  unit: [{ required: true, message: '请输入单位', trigger: 'blur' }],
  unit_price: [{ required: true, message: '请输入单价', trigger: 'blur' }],
  total_quantity: [{ required: true, message: '请输入总工程量', trigger: 'blur' }]
}

watch(
  () => props.form,
  (newVal) => {
    Object.assign(formData, newVal)
    formData.contract_id = props.contractId
  },
  { immediate: true, deep: true }
)

const calculateTotalPrice = () => {
  if (formData.unit_price && formData.total_quantity) {
    formData.total_price = String(
      Number(formData.unit_price) * Number(formData.total_quantity)
    )
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate()
  emit('submit', formData)
}
</script> 