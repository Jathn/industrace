<template>
  <Dialog :visible="visible" @update:visible="$emit('update:visible', $event)" :header="t('assets.bulkUpdate')" :modal="true" :style="{ width: '40vw' }">
    <div class="p-fluid">
      <div class="p-field">
        <label for="field">{{ t('assets.chooseField') }}</label>
        <Dropdown v-model="bulkField" :options="bulkFieldOptions" optionLabel="label" optionValue="value" :placeholder="t('assets.chooseField')" />
      </div>
      
      <!-- Status -->
      <div class="p-field" v-if="bulkField === 'status_id'">
        <label>{{ t('assets.status') }}</label>
        <Dropdown v-model="bulkValue" :options="assetStatusOptions" optionLabel="name" optionValue="id" :placeholder="t('assets.status')" />
      </div>
      
      <!-- Site -->
      <div class="p-field" v-if="bulkField === 'site_id'">
        <label>{{ t('assets.site') }}</label>
        <Dropdown v-model="bulkValue" :options="sites" optionLabel="name" optionValue="id" :placeholder="t('assets.site')" />
      </div>
      
      <!-- Asset Type -->
      <div class="p-field" v-if="bulkField === 'asset_type_id'">
        <label>{{ t('assets.type') }}</label>
        <Dropdown v-model="bulkValue" :options="assetTypes" optionLabel="name" optionValue="id" :placeholder="t('assets.type')" />
      </div>
      
      <!-- Area -->
      <div class="p-field" v-if="bulkField === 'area_id'">
        <label>{{ t('assets.area') }}</label>
        <Dropdown v-model="bulkValue" :options="areas" optionLabel="name" optionValue="id" :placeholder="t('assets.area')" showClear />
      </div>
      
      <!-- Location -->
      <div class="p-field" v-if="bulkField === 'location_id'">
        <label>{{ t('assets.location') }}</label>
        <Dropdown v-model="bulkValue" :options="locations" optionLabel="name" optionValue="id" :placeholder="t('assets.location')" showClear />
      </div>
      
      <!-- Manufacturer -->
      <div class="p-field" v-if="bulkField === 'manufacturer_id'">
        <label>{{ t('assets.manufacturer') }}</label>
        <Dropdown v-model="bulkValue" :options="manufacturers" optionLabel="name" optionValue="id" :placeholder="t('assets.manufacturer')" />
      </div>
      
      <!-- VLAN -->
      <div class="p-field" v-if="bulkField === 'vlan'">
        <label for="bulk_vlan">{{ t('assets.vlan') }}</label>
        <InputText id="bulk_vlan" v-model="bulkValue" />
      </div>
      
      <!-- Business Criticality -->
      <div class="p-field" v-if="bulkField === 'business_criticality'">
        <label>{{ t('assetForm.businessCriticality') }}</label>
        <Dropdown
          v-model="bulkValue"
          :options="businessCriticalityOptions"
          optionLabel="label"
          optionValue="value"
          :placeholder="t('assetForm.businessCriticality')"
          showClear
        />
      </div>
      
      <!-- Altri campi generici -->
      <div class="p-field" v-if="bulkField && !['status_id','site_id','area_id','asset_type_id','location_id','manufacturer_id','vlan','business_criticality'].includes(bulkField)">
        <label for="bulk_generic">{{ t('assets.value') }}</label>
        <InputText id="bulk_generic" v-model="bulkValue" />
      </div>
      
      <div class="p-field">
        <Button :label="t('common.confirm')" icon="pi pi-check" class="p-button-success" :disabled="!bulkField || bulkValue === null || bulkValue === ''" @click="onBulkUpdate" />
        <Button :label="t('common.cancel')" icon="pi pi-times" class="p-button-text" @click="close" />
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
import InputText from 'primevue/inputtext'

const props = defineProps({
  visible: { type: Boolean, default: false },
  assetStatusOptions: { type: Array, default: () => [] },
  sites: { type: Array, default: () => [] },
  assetTypes: { type: Array, default: () => [] },
  areas: { type: Array, default: () => [] },
  locations: { type: Array, default: () => [] },
  manufacturers: { type: Array, default: () => [] }
})

const emit = defineEmits(['update:visible', 'bulkUpdate'])

const { t } = useI18n()

const bulkField = ref(null)
const bulkValue = ref(null)

const bulkFieldOptions = [
  { label: t('assets.status'), value: 'status_id' },
  { label: t('assets.site'), value: 'site_id' },
  { label: t('assets.area'), value: 'area_id' },
  { label: t('assets.location'), value: 'location_id' },
  { label: t('assets.type'), value: 'asset_type_id' },
  { label: t('assets.manufacturer'), value: 'manufacturer_id' },
  { label: t('assets.vlan'), value: 'vlan' },
  { label: t('assetForm.businessCriticality'), value: 'business_criticality' }
]

const businessCriticalityOptions = [
  { label: t('assetForm.businessCriticalityLow'), value: 'low' },
  { label: t('assetForm.businessCriticalityMedium'), value: 'medium' },
  { label: t('assetForm.businessCriticalityHigh'), value: 'high' },
  { label: t('assetForm.businessCriticalityCritical'), value: 'critical' }
]

// Reset form quando si apre/chiude il dialog
watch(() => props.visible, (newVisible) => {
  if (!newVisible) {
    bulkField.value = null
    bulkValue.value = null
  }
})

function onBulkUpdate() {
  if (!bulkField.value || bulkValue.value === null || bulkValue.value === '') return
  
  emit('bulkUpdate', {
    field: bulkField.value,
    value: bulkValue.value
  })
  
  close()
}

function close() {
  emit('update:visible', false)
}
</script> 