<template>
  <div class="asset-header-flex-modern">
    <div class="asset-header-main">
      <div class="asset-header-top">
        <Button 
          :label="t('common.back')" 
          icon="pi pi-arrow-left" 
          class="p-button-text p-button-secondary back-btn"
          @click="$emit('back')"
        />
      </div>
      <h1 class="asset-title">{{ asset.name }}</h1>
      <div class="asset-meta">
        <Tag v-if="asset.status?.name" :value="asset.status.name" :style="{ background: asset.status?.color, color: '#fff' }" />
        <span class="type">{{ asset.asset_type?.name || t('common.na') }}</span>
        <span class="site">{{ asset.site?.name || t('common.na') }}</span>
        <span class="area" v-if="asset.area_name">{{ asset.area_name }}</span>
        <Tag
          v-if="asset.business_criticality"
          :value="`${t('assets.businessCriticality')}: ${getCriticalityLabel(asset.business_criticality)}`"
          :style="{ background: getCriticalityColor(asset.business_criticality), color: '#fff', border: 'none' }"
          class="criticality-badge"
        />
        <Tag
          v-if="riskBreakdown && riskBreakdown.final_score !== null"
          :value="`${t('assets.riskScore')}: ${riskBreakdown.final_score} (${riskLevelLabel(riskBreakdown.final_score)})`"
          :severity="riskLevelSeverity(riskBreakdown.final_score)"
          class="risk-badge"
        />
      </div>
    </div>
    <div class="asset-header-actions-modern">
      <Button 
        v-if="canWrite('assets')"
        :label="t('common.edit')" 
        icon="pi pi-pencil" 
        severity="warning"
        @click="$emit('edit')" 
      />
      <Button 
        :label="t('common.print')" 
        icon="pi pi-print" 
        severity="success"
        @click="$emit('print')" 
      />
      <Button 
        :label="t('assets.floorplan')" 
        icon="pi pi-map" 
        severity="info"
        @click="showFloorplanDialog = true" 
        :disabled="!hasFloorplan"
      />
    </div>
  </div>
  
  <!-- Floorplan Dialog -->
  <Dialog v-model:visible="showFloorplanDialog" :header="t('assets.floorplanDialogTitle')" modal style="width: 90vw; max-width: 900px" :closable="true" :dismissableMask="true">
    <AssetDetailFloorplanTab :assetId="asset.id" :readOnly="!canWrite('assets')" @position-saved="onAssetPositionSaved" />
  </Dialog>
</template>

<script setup>
import { toRefs } from 'vue'
import { useI18n } from 'vue-i18n'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import Dialog from 'primevue/dialog'
import AssetDetailFloorplanTab from './tabs/AssetDetailFloorplanTab.vue'

import { computed, ref } from 'vue'

const props = defineProps({
  asset: { type: Object, required: true },
  riskBreakdown: { type: Object, default: null },
  canWrite: { type: Function, required: true },
  getCriticalityLabel: { type: Function, required: true },
  getCriticalityColor: { type: Function, required: true }
})

const { t } = useI18n()
const emit = defineEmits(['back', 'edit', 'print', 'position-saved'])

// State
const showFloorplanDialog = ref(false)

// Computed properties
const hasFloorplan = computed(() => !!(props.asset?.location?.floorplan?.id))

// Risk utility functions
function riskLevelLabel(score) {
  if (score === null || score === undefined) return t('assets.riskLevelUndefined')
  if (score >= 7) return t('assets.riskLevelHigh')
  if (score >= 4) return t('assets.riskLevelMedium')
  return t('assets.riskLevelLow')
}

function riskLevelSeverity(score) {
  if (score === null || score === undefined) return 'info'
  if (score >= 7) return 'danger'
  if (score >= 4) return 'warning'
  return 'success'
}

// Methods
function onAssetPositionSaved({ id, map_x, map_y }) {
  // Emetti un evento per aggiornare l'asset nel componente padre
  emit('position-saved', { id, map_x, map_y })
}
</script>

<style scoped>
.asset-header-flex-modern {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}
.asset-header-main {
  flex: 1;
  min-width: 0;
}
.asset-header-top {
  margin-bottom: 0.5rem;
}
.asset-title {
  margin: 0;
  font-size: 2rem;
  line-height: 1.1;
  word-break: break-word;
}
.asset-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
  margin-top: 0.5rem;
}
.criticality-badge, .risk-badge {
  font-size: 0.9em;
}
.asset-header-actions-modern {
  display: flex;
  flex-direction: row;
  gap: 0.5rem;
  align-items: flex-end;
  flex-wrap: wrap;
}
.back-btn {
  margin-bottom: 0.5rem;
}
@media (max-width: 700px) {
  .asset-header-flex-modern {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  .asset-header-actions-modern {
    justify-content: flex-start;
    align-items: flex-start;
    flex-direction: column;
  }
}
</style> 