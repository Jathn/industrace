<!--
  - Assets.vue
  - Componente per la gestione degli asset
  - Utilizza i componenti PrimeVue per la gestione del form
-->
<template>
  <div class="assets-page">
    <AssetsHeader 
      :trashMode="trashMode"
      @create="openCreate(t('assets.create'))"
      @import="showImportDialog = true"
      @toggleTrash="toggleTrashMode"
    />

    <AssetsFilters 
      :filters="filters"
      :assetStatusOptions="assetStatusOptions"
      :sites="sites"
      :areas="allAreas"
      @showAdvancedFilters="showAdvancedFilters = true"
    />

    <BaseDataTable
      :data="assetsWithIP"
      :loading="loading"
      :columns="allColumns"
      :filters="filters"
      :globalFilterFields="['name','site.name','location.name','status.name','manufacturer.name','asset_type.name']"
      :selectionMode="canWrite('assets') ? 'multiple' : null"
      :storageKey="'assets'"
      :showExport="false"
      @selection-change="selectedAssets = $event"
      @sort="onSort"
    >


      <template #actions>
        <Button 
          v-if="!trashMode && canWrite('assets')"
          :label="t('common.bulkEdit')" 
          icon="pi pi-pencil" 
          severity="warning"
          :disabled="!selectedAssets.length" 
          @click="showBulkDialog = true" 
        />
        <Button 
          v-if="!trashMode && canDelete('assets')"
          :label="t('common.moveToTrash')" 
          icon="pi pi-trash" 
          severity="danger"
          :disabled="!selectedAssets.length" 
          @click="confirmBulkSoftDelete" 
        />
      </template>

      <template #body-status.name="{ data }">
        <span v-if="data.status">
          <span :style="{ background: data.status.color, color: '#fff', padding: '0.2rem 0.5rem', borderRadius: '4px' }">
            {{ data.status.name }}
          </span>
        </span>
        <span v-else>-</span>
      </template>

      <template #body-business_criticality="{ data }">
        <span v-if="data.business_criticality">
          {{ getBusinessCriticalityLabel(data.business_criticality) }}
        </span>
        <span v-else>-</span>
      </template>

      <template #body-risk_score="{ data }">
        <span v-if="data.risk_score !== null && data.risk_score !== undefined">
          <Tag :value="data.risk_score.toFixed(2)" :severity="riskLevelSeverity(data.risk_score)" />
        </span>
        <span v-else>-</span>
      </template>

      <template #body-actions="{ data }">
        <div class="flex gap-2">
          <Button 
            v-if="!trashMode"
            icon="pi pi-eye" 
            size="small"
            @click="viewAsset(data.id)" 
          />
          <Button
            v-if="!trashMode && canWrite('assets')"
            icon="pi pi-pencil"
            size="small"
            @click="openEdit(t('assets.edit'), data)"
          />
          <Button 
            v-if="!trashMode && canWrite('assets')"
            icon="pi pi-copy" 
            size="small"
            severity="info"
            :loading="duplicating"
            @click="duplicateAsset(data)" 
          />
          <Button 
            v-if="!trashMode && canDelete('assets')"
            icon="pi pi-trash" 
            size="small"
            severity="danger"
            @click="deleteAsset(data.id)" 
          />
          <Button 
            v-if="trashMode && canWrite('assets')" 
            icon="pi pi-undo" 
            size="small"
            severity="success"
            @click="restoreAsset(data.id)" 
          />
          <Button 
            v-if="trashMode && canDelete('assets')" 
            icon="pi pi-times" 
            size="small"
            severity="danger"
            @click="hardDeleteAsset(data.id)" 
          />
        </div>
      </template>
    </BaseDataTable>

    <BaseDialog
      v-model:isVisible="showDialog"
      :title="dialogTitle"
      :mode="dialogMode"
      :data="editingAsset"
      :showFooter="false"
      @cancel="close"
    >
      <template #default="{ data }">
        <AssetForm 
          :asset="data" 
          :sites="sites" 
          :allLocations="locations"
          :allAreas="allAreas"
          :assetTypes="assetTypes" 
          :manufacturers="manufacturers"
          :assetStatusOptions="assetStatusOptions"
          @submit="handleSubmit" 
          @cancel="close" 
        />
      </template>
    </BaseDialog>

    <AssetImportDialog :visible="showImportDialog" @close="showImportDialog = false" @imported="onAssetImport" />
    
    <BaseConfirmDialog
      v-model:showConfirmDialog="showConfirmDialog"
      :confirmData="confirmData"
      @execute="executeConfirmedAction"
      @close="closeConfirmDialog"
    />
    
    <AssetsAdvancedFilters 
      v-model:visible="showAdvancedFilters"
      :filters="filters"
      @apply="applyAdvancedFilters"
      @clear="clearAdvancedFilters"
    />

    <AssetsBulkActions 
      v-model:visible="showBulkDialog"
      :assetStatusOptions="assetStatusOptions"
      :sites="sites"
      :assetTypes="assetTypes"
      :locations="locations"
      :manufacturers="manufacturers"
      @bulkUpdate="onBulkUpdate"
    />

    <AssetsTrashActions 
      :trashMode="trashMode"
      @emptyTrash="confirmEmptyTrash"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch, computed, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useToast } from 'primevue/usetoast'
import { useApi } from '../composables/useApi'
import { useFilters } from '../composables/useFilters'
import { useDialog } from '../composables/useDialog'
import { useConfirm } from '../composables/useConfirm'
import { useDuplicate } from '../composables/useDuplicate'
import { usePermissions } from '../composables/usePermissions'
import { useStatus } from '../composables/useStatus'
import api from '../api/api'

import Tag from 'primevue/tag'
import AssetForm from '../components/forms/AssetForm.vue'
import BaseDataTable from '../components/base/BaseDataTable.vue'
import BaseDialog from '../components/base/BaseDialog.vue'
import BaseConfirmDialog from '../components/base/BaseConfirmDialog.vue'
import AssetImportDialog from '../components/dialogs/AssetImportDialog.vue'
import AssetsHeader from '../components/features/assets/AssetsHeader.vue'
import AssetsFilters from '../components/features/assets/AssetsFilters.vue'
import AssetsAdvancedFilters from '../components/features/assets/AssetsAdvancedFilters.vue'
import AssetsBulkActions from '../components/features/assets/AssetsBulkActions.vue'
import AssetsTrashActions from '../components/features/assets/AssetsTrashActions.vue'

const router = useRouter()
const { t } = useI18n()
const toast = useToast()

// Definizione delle colonne PRIMA di useFilters
const allColumns = [
  { field: 'name', header: t('common.name') },
  { field: 'ip_address', header: t('assets.ipAddress') },
  { field: 'vlan', header: t('assets.vlan') },
  { field: 'logical_port', header: t('assets.logicalPort') },
  { field: 'site.name', header: t('common.site') },
  { field: 'area_name', header: t('common.area') },
  { field: 'location.name', header: t('assets.location') },
  { field: 'status.name', header: t('common.status') },
  { field: 'manufacturer.name', header: t('assets.manufacturer') },
  { field: 'asset_type.name', header: t('common.type') },
  { field: 'business_criticality', header: t('assets.businessCriticality'), sortable: true },
  { field: 'risk_score', header: t('assets.riskScore'), sortable: true },
  { field: 'actions', header: t('common.actions') }
]

// Composables
const { loading, execute } = useApi()
const { filters, globalSearch, selectedColumns, filterData, getApiParams } = useFilters({
  global: { value: null, matchMode: 'contains' },
  status_id: { value: null, matchMode: 'equals' },
  site_id: { value: null, matchMode: 'equals' },
  area_id: { value: null, matchMode: 'equals' },
  business_criticality: { value: null, matchMode: 'equals' },
  risk_score_min: { value: null, matchMode: 'gte' },
  risk_score_max: { value: null, matchMode: 'lte' }
}, 'assets')

const { isVisible: showDialog, data: editingAsset, openCreate, openEdit, close } = useDialog()
// Importa il composable useConfirm e rinomina la funzione per evitare conflitti
const { 
  showConfirmDialog, 
  confirmData, 
  confirmDelete, 
  confirmBulkAction, 
  confirmEmptyTrash: confirmEmptyTrashFn, // rinominato
  executeConfirmedAction,
  closeConfirmDialog 
} = useConfirm()

const { duplicating, duplicateItem, excludeFunctions } = useDuplicate()
const { canRead, canWrite, canDelete } = usePermissions()
const { getStatusSeverity } = useStatus()

// Computed properties per il dialog
const dialogTitle = computed(() => {
  return editingAsset.value ? t('assets.edit') : t('assets.create')
})

const dialogMode = computed(() => {
  return editingAsset.value ? 'edit' : 'create'
})

// Data
const assets = ref([])
const sites = ref([])
const manufacturers = ref([])
const assetTypes = ref([])
const locations = ref([])
const allAreas = ref([])
const assetStatusOptions = ref([])
const showImportDialog = ref(false)
const selectedAssets = ref([])
const showBulkDialog = ref(false)
const trashMode = ref(false)



const showAdvancedFilters = ref(false)
function applyAdvancedFilters(advancedFiltersData) {
  filters.value.business_criticality.value = advancedFiltersData.business_criticality
  filters.value.risk_score_min.value = advancedFiltersData.risk_score_min
  filters.value.risk_score_max.value = advancedFiltersData.risk_score_max
}
function clearAdvancedFilters() {
  advancedFilters.business_criticality = null
  advancedFilters.risk_score_min = null
  advancedFilters.risk_score_max = null
  filters.value.business_criticality.value = null
  filters.value.risk_score_min.value = null
  filters.value.risk_score_max.value = null
}

function onEditCancel() {
  close()
}

function onSort(event) {
  // Gestione ordinamento se necessario
}


function cleanAssetData(assetData) {
  const cleaned = { ...assetData }
  
  const optionalFieldsToClean = ['ip_address', 'vlan', 'logical_port', 'physical_plug_label', 'firmware_version', 'serial_number', 'tag', 'model', 'description']
  optionalFieldsToClean.forEach(field => {
    if (cleaned[field] === '') {
      cleaned[field] = null
    }
  })
  
  return cleaned
}

// Funzione unificata per gestire submit (creazione e modifica)
async function handleSubmit(assetData) {
  
  const cleanedData = cleanAssetData(assetData)
  
  if (editingAsset.value) {
    // Modalità modifica
    await updateAsset(cleanedData)
  } else {
    // Modalità creazione
    await createAsset(cleanedData)
  }
}

// Debug per verificare i dati
watch(() => editingAsset.value, (newAsset) => {
})

onMounted(async () => {
  await Promise.all([
    fetchAssets(), 
    fetchSites(), 
    fetchAssetTypes(), 
    fetchLocations(),
    fetchAreas(),
    fetchManufactures(),
    fetchAssetStatuses()
  ])
})

async function fetchAssets() {
  await execute(async () => {
    const params = getApiParams()
    let response
    if (trashMode.value) {
      response = await api.getAssetsTrash(params)
    } else {
      response = await api.getAssets(params)
    }
    assets.value = response.data
    return response
  }, {
    errorContext: t('assets.fetchError'),
    showToast: false
  })
}

async function fetchSites() {
  await execute(async () => {
    const response = await api.getSites()
    sites.value = response.data
    return response
  }, {
    errorContext: t('assets.fetchSitesError'),
    showToast: false
  })
}

async function fetchLocations() {
  try {
    const response = await api.getLocations()
    locations.value = response.data
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: t('common.error'),
      detail: t('assets.fetchLocationsError'),
      life: 3000
    })
  }
}

async function fetchAreas() {
  try {
    const response = await api.getAreas()
    allAreas.value = response.data
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: t('common.error'),
      detail: t('assets.fetchAreasError'),
      life: 3000
    })
  }
}

async function fetchManufactures() {
  try {
    const response = await api.getManufacturers()
    manufacturers.value = response.data
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: t('common.error'),
      detail: t('assets.fetchManufacturersError'),
      life: 3000
    })
  }
}

async function fetchAssetTypes() {
  try {
    const response = await api.getAssetTypes()
    assetTypes.value = response.data
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: t('common.error'),
      detail: t('assets.fetchAssetTypesError'),
      life: 3000
    })
  }
}

async function fetchAssetStatuses() {
  try {
    const res = await api.getAssetStatuses()
    assetStatusOptions.value = res.data.filter(s => s.active)
  } catch (e) {
    assetStatusOptions.value = []
  }
}



function viewAsset(id) {
  router.push(`/assets/${id}`)
}

async function createAsset(assetData) {
  try {
    const result = await api.createAsset(assetData)
    close()
    await fetchAssets()
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: t('common.error'),
      detail: t('assets.createError'),
      life: 3000
    })
  }
}

async function updateAsset(assetData) {
  try {
    await api.updateAsset(editingAsset.value.id, assetData)
    close()
    await fetchAssets()
  } catch (error) {
    toast.add({ severity: 'error', summary: t('common.error'), detail: t('assets.updateError'), life: 3000 })
  }
}

async function deleteAsset(id) {
  const asset = assets.value.find(a => a.id === id)
  const assetName = asset ? asset.name : 'Asset'
  
  confirmDelete(asset, assetName, async () => {
    await api.deleteAsset(id)
    await fetchAssets()
  }, {
    successMessage: t('assets.deleteSuccess'),
    errorContext: t('assets.deleteError')
  })
}

async function duplicateAsset(asset) {
  await duplicateItem(
    asset,
    async (data) => {
      const result = await api.createAsset(data)
      await fetchAssets()
      return result
    },
    'asset',
    excludeFunctions.asset
  )
}

const filteredAssets = computed(() => {
  let filtered = assets.value
  if (filters.value.status_id.value) {
    filtered = filtered.filter(a => a.status_id === filters.value.status_id.value)
  }
  if (filters.value.site_id.value) {
    filtered = filtered.filter(a => a.site_id === filters.value.site_id.value)
  }
  if (filters.value.area_id.value) {
    filtered = filtered.filter(a => a.area_id === filters.value.area_id.value)
  }
  if (filters.value.business_criticality.value) {
    filtered = filtered.filter(a => (a.business_criticality || '').toLowerCase() === filters.value.business_criticality.value)
  }
  if (filters.value.risk_score_min.value !== null) {
    filtered = filtered.filter(a => (a.risk_score ?? 0) >= filters.value.risk_score_min.value)
  }
  if (filters.value.risk_score_max.value !== null) {
    filtered = filtered.filter(a => (a.risk_score ?? 0) <= filters.value.risk_score_max.value)
  }
  if (filters.value.global.value) {
    const search = filters.value.global.value.toLowerCase()
    filtered = filtered.filter(a =>
      (a.name && a.name.toLowerCase().includes(search)) ||
      (a.interfaces && a.interfaces.some(i => i.ip_address && i.ip_address.toLowerCase().includes(search))) ||
      (a.site && a.site.name && a.site.name.toLowerCase().includes(search)) ||
      (a.area_name && a.area_name.toLowerCase().includes(search)) ||
      (a.location && a.location.name && a.location.name.toLowerCase().includes(search)) ||
      (a.status && a.status.name && a.status.name.toLowerCase().includes(search)) ||
      (a.manufacturer && a.manufacturer.name && a.manufacturer.name.toLowerCase().includes(search)) ||
      (a.asset_type && a.asset_type.name && a.asset_type.name.toLowerCase().includes(search))
    )
  }
  return filtered
})

const assetsWithIP = computed(() =>
  filteredAssets.value.map(asset => ({
    ...asset,
    ip_address: asset.interfaces && asset.interfaces.length
      ? asset.interfaces.map(i => i.ip_address).filter(Boolean).join(', ')
      : '-'
  }))
)

function onAssetImport(result) {
  showImportDialog.value = false
  if (result && (result.created || result.updated)) {
    toast.add({
      severity: 'success',
      summary: t('common.success'),
      detail: `${(result.created?.length || 0)} asset creati, ${(result.updated?.length || 0)} asset aggiornati` + (result.errors?.length ? `, ${result.errors.length} errori` : ''),
      life: 4000
    })
    fetchAssets()
  } else if (result && result.errors && result.errors.length) {
    toast.add({
      severity: 'warn',
      summary: t('common.warning'),
      detail: `${result.errors.length} errori durante l'import`,
      life: 4000
    })
  } else {
    toast.add({
      severity: 'info',
      summary: t('assets.import'),
      detail: t('assets.importedInfo'),
      life: 4000
    })
  }
}

async function onBulkUpdate(bulkData) {
  try {
    const assetIds = selectedAssets.value.map(asset => asset.id)
    await api.bulkUpdateAssets(assetIds, { [bulkData.field]: bulkData.value })
    toast.add({ severity: 'success', summary: t('common.success'), detail: t('assets.bulkUpdated'), life: 3000 })
    selectedAssets.value = []
    await fetchAssets()
  } catch (error) {
    toast.add({ severity: 'error', summary: t('common.error'), detail: t('assets.bulkUpdateError'), life: 4000 })
  }
}

function confirmBulkSoftDelete() {
  const assetNames = selectedAssets.value.map(asset => asset.name).join(', ')
  confirmBulkAction(
    selectedAssets.value,
    'soft_delete',
    () => bulkSoftDelete(selectedAssets.value), // Passa i parametri correttamente
    t('assets.confirmBulkSoftDelete'),
    t('assets.confirmBulkSoftDeleteMessage', { count: selectedAssets.value.length, names: assetNames })
  )
}

async function bulkSoftDelete(assets) {
  try {
    const assetIds = assets.map(asset => asset.id)
    // console.log('Bulk soft delete - Asset IDs:', assetIds)
    
    const response = await api.bulkSoftDeleteAssets(assetIds)
          // console.log('Bulk soft delete - Response:', response.data)
    
    const deletedCount = response.data.deleted ? response.data.deleted.length : 0
    const errorCount = response.data.errors ? response.data.errors.length : 0
    
          // console.log('Bulk soft delete - Deleted count:', deletedCount, 'Error count:', errorCount)
    
    // Mostra toast di successo solo se ci sono asset eliminati
    if (deletedCount > 0) {
      toast.add({ 
        severity: 'success', 
        summary: t('common.success'), 
        detail: t('assets.bulkSoftDeleted', { count: deletedCount }), 
        life: 3000 
      })
    }
    
    // Mostra toast di warning solo se ci sono errori
    if (errorCount > 0) {
      toast.add({ 
        severity: 'warn', 
        summary: t('common.warning'), 
        detail: t('assets.bulkSoftDeleteErrors', { count: errorCount }), 
        life: 4000 
      })
    }
    
    // Mostra toast di errore se non è stato eliminato nessun asset
    if (deletedCount === 0 && errorCount === 0) {
      toast.add({ 
        severity: 'error', 
        summary: t('common.error'), 
        detail: t('assets.bulkSoftDeleteError'), 
        life: 4000 
      })
    }
    
    selectedAssets.value = []
    await fetchAssets()
  } catch (error) {
    console.error('Bulk soft delete error:', error)
    toast.add({ 
      severity: 'error', 
      summary: t('common.error'), 
      detail: t('assets.bulkSoftDeleteError'), 
      life: 4000 
    })
  }
}

function toggleTrashMode() {
  trashMode.value = !trashMode.value
  fetchAssets()
}

async function restoreAsset(id) {
  try {
    await api.restoreAsset(id)
    toast.add({ severity: 'success', summary: t('common.success'), detail: t('assets.restored'), life: 3000 })
    fetchAssets()
  } catch {
    toast.add({ severity: 'error', summary: t('common.error'), detail: t('assets.restoreError'), life: 3000 })
  }
}

async function hardDeleteAsset(id) {
  try {
    await api.hardDeleteAsset(id)
    toast.add({ severity: 'success', summary: t('common.success'), detail: t('assets.hardDeleted'), life: 3000 })
    fetchAssets()
  } catch {
    toast.add({ severity: 'error', summary: t('common.error'), detail: t('assets.hardDeleteError'), life: 3000 })
  }
}

async function emptyTrash() {
  try {
    await api.emptyAssetsTrash()
    toast.add({ severity: 'success', summary: t('common.success'), detail: t('assets.trashEmptied'), life: 3000 })
    fetchAssets()
  } catch (err) {
    // console.log(err)
    toast.add({ severity: 'error', summary: t('common.error'), detail: t('assets.trashEmptyError'), life: 3000 })
  }
}

function riskLevelSeverity(score) {
  if (score === null || score === undefined) return 'info'
  if (score >= 7) return 'danger'
  if (score >= 4) return 'warning'
  return 'success'
}

function getBusinessCriticalityLabel(value) {
  switch ((value || '').toLowerCase()) {
    case 'low': return t('assets.businessCriticalityLow')
    case 'medium': return t('assets.businessCriticalityMedium')
    case 'high': return t('assets.businessCriticalityHigh')
    case 'critical': return t('assets.businessCriticalityCritical')
    default: return t('common.na')
  }
}

// Funzione locale per mostrare il dialog di conferma svuota cestino
function confirmEmptyTrash() {
  confirmEmptyTrashFn(emptyTrash)
}

</script>

<style scoped>
.assets-page {
  padding: 1rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}
</style>
