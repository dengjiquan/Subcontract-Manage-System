<template>
  <el-dialog
    title="结算明细"
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    width="800px"
  >
    <el-descriptions :column="2" border>
      <el-descriptions-item label="合同编号">
        {{ getContractNumber(settlement?.contract_id) }}
      </el-descriptions-item>
      <el-descriptions-item label="结算日期">
        {{ settlement?.settlement_date }}
      </el-descriptions-item>
      <el-descriptions-item label="结算金额">
        {{ settlement?.settlement_amount }}元
      </el-descriptions-item>
      <el-descriptions-item label="备注">
        {{ settlement?.remarks || '-' }}
      </el-descriptions-item>
    </el-descriptions>

    <el-divider>结算明细</el-divider>

    <el-table
      :data="settlement?.details || []"
      border
      style="width: 100%"
    >
      <el-table-column
        label="工程量清单项"
        min-width="200"
      >
        <template #default="{ row }">
          {{ getBOQItemName(row.boq_item_id) }}
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
        prop="completed_quantity"
        label="完成工程量"
        min-width="150"
      />
      <el-table-column
        prop="settlement_amount"
        label="结算金额"
        min-width="150"
      >
        <template #default="{ row }">
          {{ row.settlement_amount }}元
        </template>
      </el-table-column>
    </el-table>

    <template #footer>
      <el-button @click="$emit('update:modelValue', false)">关闭</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Settlement, Contract, BOQItem } from '@/types/api'
import request from '@/utils/request'

const props = defineProps<{
  modelValue: boolean
  settlement?: Settlement
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
}>()

const contracts = ref<Contract[]>([])
const boqItems = ref<BOQItem[]>([])

// 获取合同列表
const getContracts = async () => {
  try {
    const response = await request.get('/v1/contracts', { params: { limit: 1000 } })
    contracts.value = response.items
  } catch (error) {
    console.error('Get contracts error:', error)
  }
}

// 获取工程量清单项
const getBOQItems = async () => {
  if (!props.settlement?.contract_id) return
  try {
    const response = await request.get('/v1/boq-items', {
      params: { contract_id: props.settlement.contract_id, limit: 1000 }
    })
    boqItems.value = response.items
  } catch (error) {
    console.error('Get BOQ items error:', error)
  }
}

// 获取合同编号
const getContractNumber = (id?: number) => {
  if (!id) return '-'
  const contract = contracts.value.find(item => item.id === id)
  return contract?.contract_number || '-'
}

// 获取工程量清单项名称
const getBOQItemName = (id: number) => {
  const item = boqItems.value.find(item => item.id === id)
  return item?.item_name || '-'
}

// 获取工程量清单项单价
const getBOQItemUnitPrice = (id: number) => {
  const item = boqItems.value.find(item => item.id === id)
  return item ? `${item.unit_price}元/${item.unit}` : '-'
}

onMounted(async () => {
  await getContracts()
  await getBOQItems()
})
</script> 