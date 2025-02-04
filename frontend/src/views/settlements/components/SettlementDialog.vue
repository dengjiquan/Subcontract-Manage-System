<template>
  <el-dialog
    :title="title"
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    width="800px"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-width="100px"
    >
      <el-form-item label="结算日期" prop="settlement_date">
        <el-date-picker
          v-model="formData.settlement_date"
          type="date"
          placeholder="选择结算日期"
          style="width: 100%"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>

      <el-form-item label="备注" prop="remarks">
        <el-input
          v-model="formData.remarks"
          type="textarea"
          :rows="3"
        />
      </el-form-item>

      <el-divider>结算明细</el-divider>

      <el-table
        :data="formData.details"
        border
        style="width: 100%"
      >
        <el-table-column
          label="工程量清单项"
          min-width="200"
        >
          <template #default="{ row }">
            <el-select
              v-model="row.boq_item_id"
              placeholder="选择工程量清单项"
              style="width: 100%"
              @change="handleBOQItemChange($event, row)"
            >
              <el-option
                v-for="item in boqItems"
                :key="item.id"
                :label="item.item_name"
                :value="item.id"
              />
            </el-select>
          </template>
        </el-table-column>
        <el-table-column
          label="单价"
          min-width="120"
        >
          <template #default="{ row }">
            {{ getBOQItemUnitPrice(row.boq_item_id) }}
          </template>
        </el-table-column>
        <el-table-column
          label="完成工程量"
          min-width="150"
        >
          <template #default="{ row }">
            <el-input
              v-model="row.completed_quantity"
              type="number"
              @input="calculateSettlementAmount(row)"
            />
          </template>
        </el-table-column>
        <el-table-column
          label="结算金额"
          min-width="150"
        >
          <template #default="{ row }">
            <el-input
              v-model="row.settlement_amount"
              type="number"
              disabled
            >
              <template #append>元</template>
            </el-input>
          </template>
        </el-table-column>
        <el-table-column
          label="操作"
          width="100"
        >
          <template #default="{ $index }">
            <el-button
              type="danger"
              link
              @click="removeDetail($index)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="detail-actions">
        <el-button
          type="primary"
          plain
          @click="addDetail"
        >
          添加明细
        </el-button>
      </div>

      <el-form-item label="结算总额">
        <el-input
          v-model="formData.settlement_amount"
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
import { ref, reactive, watch, onMounted } from 'vue'
import type { FormInstance } from 'element-plus'
import type { Settlement, BOQItem } from '@/types/api'
import request from '@/utils/request'

const props = defineProps<{
  modelValue: boolean
  title: string
  form: Partial<Settlement>
  contractId: number | undefined
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'submit', form: Partial<Settlement>): void
}>()

const formRef = ref<FormInstance>()
const formData = reactive<Partial<Settlement>>({
  details: []
})
const boqItems = ref<BOQItem[]>([])

const rules = {
  settlement_date: [{ required: true, message: '请选择结算日期', trigger: 'change' }],
  details: [{ required: true, message: '请添加结算明细', trigger: 'change' }]
}

// 获取工程量清单项
const getBOQItems = async () => {
  if (!props.contractId) return
  try {
    const response = await request.get('/v1/boq-items', {
      params: { contract_id: props.contractId, limit: 1000 }
    })
    boqItems.value = response.items
  } catch (error) {
    console.error('Get BOQ items error:', error)
  }
}

// 获取工程量清单项单价
const getBOQItemUnitPrice = (id: number) => {
  const item = boqItems.value.find(item => item.id === id)
  return item ? `${item.unit_price}元/${item.unit}` : '-'
}

// 计算结算金额
const calculateSettlementAmount = (detail: any) => {
  const boqItem = boqItems.value.find(item => item.id === detail.boq_item_id)
  if (boqItem && detail.completed_quantity) {
    detail.settlement_amount = String(
      Number(boqItem.unit_price) * Number(detail.completed_quantity)
    )
    // 计算总金额
    formData.settlement_amount = String(
      formData.details?.reduce(
        (sum, detail) => sum + Number(detail.settlement_amount || 0),
        0
      )
    )
  }
}

const handleBOQItemChange = (value: number, detail: any) => {
  detail.completed_quantity = ''
  detail.settlement_amount = ''
}

const addDetail = () => {
  if (!formData.details) {
    formData.details = []
  }
  formData.details.push({
    boq_item_id: undefined,
    completed_quantity: '',
    settlement_amount: ''
  })
}

const removeDetail = (index: number) => {
  formData.details?.splice(index, 1)
  // 重新计算总金额
  formData.settlement_amount = String(
    formData.details?.reduce(
      (sum, detail) => sum + Number(detail.settlement_amount || 0),
      0
    )
  )
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate()
  emit('submit', formData)
}

watch(
  () => props.form,
  (newVal) => {
    Object.assign(formData, newVal)
    formData.contract_id = props.contractId
  },
  { immediate: true, deep: true }
)

onMounted(() => {
  getBOQItems()
})
</script>

<style lang="scss" scoped>
.detail-actions {
  margin: 16px 0;
  text-align: center;
}
</style> 