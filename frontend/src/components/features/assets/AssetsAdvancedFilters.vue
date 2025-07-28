<template>
  <Dialog :visible="visible" @update:visible="$emit('update:visible', $event)" :header="t('assets.advancedFilters') || 'Filtri avanzati'" :modal="true" :style="{ width: '400px' }">
    <div class="p-fluid">
      <div class="p-field">
        <label for="advanced_business_criticality">{{ t('assetForm.businessCriticality') }}</label>
        <Dropdown
          id="advanced_business_criticality"
          v-model="localFilters.business_criticality"
          :options="businessCriticalityOptions"
          optionLabel="label"
          optionValue="value"
          :placeholder="t('assetForm.businessCriticality')"
          showClear
        />
      </div>
      <div class="p-field">
        <label for="advanced_risk_score_min">{{ t('assets.riskScore') }}</label>
        <div class="flex align-items-center gap-2">
          <InputNumber id="advanced_risk_score_min" v-model="localFilters.risk_score_min" :placeholder="t('assets.riskScoreMin')" :min="0" :max="10" mode="decimal" style="width: 80px" />
          <span>-</span>
          <InputNumber id="advanced_risk_score_max" v-model="localFilters.risk_score_max" :placeholder="t('assets.riskScoreMax')" :min="0" :max="10" mode="decimal" style="width: 80px" />
        </div>
      </div>
      <div class="p-field flex gap-2 mt-3">
        <Button :label="t('common.confirm')" icon="pi pi-check" class="p-button-success" @click="applyFilters" />
        <Button :label="t('common.clear')" icon="pi pi-times" class="p-button-text" @click="clearFilters" />
      </div>
    </div>
  </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import Dropdown from 'primevue/dropdown'
import InputNumber from 'primevue/inputnumber'

const props = defineProps({
  visible: { type: Boolean, default: false },
  filters: { type: Object, required: true }
})

const emit = defineEmits(['update:visible', 'apply', 'clear'])

const { t } = useI18n()

const businessCriticalityOptions = [
  { label: t('assetForm.businessCriticalityLow'), value: 'low' },
  { label: t('assetForm.businessCriticalityMedium'), value: 'medium' },
  { label: t('assetForm.businessCriticalityHigh'), value: 'high' },
  { label: t('assetForm.businessCriticalityCritical'), value: 'critical' }
]

const localFilters = ref({
  business_criticality: null,
  risk_score_min: null,
  risk_score_max: null
})

// Sincronizza i filtri locali con quelli esterni
watch(() => props.filters, (newFilters) => {
  if (newFilters) {
    localFilters.value.business_criticality = newFilters.business_criticality?.value || null
    localFilters.value.risk_score_min = newFilters.risk_score_min?.value || null
    localFilters.value.risk_score_max = newFilters.risk_score_max?.value || null
  }
}, { immediate: true })

function applyFilters() {
  emit('apply', localFilters.value)
  emit('update:visible', false)
}

function clearFilters() {
  localFilters.value = {
    business_criticality: null,
    risk_score_min: null,
    risk_score_max: null
  }
  emit('clear')
  emit('update:visible', false)
}
</script> 