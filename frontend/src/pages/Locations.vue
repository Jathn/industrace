<template>
  <div class="locations-page">
    <div class="page-header">
      <h1>{{ t('locations.title') }}</h1>
      <div class="flex gap-2">
        <Button 
          v-if="!trashMode && canWrite('locations')"
          :label="t('common.new')" 
          icon="pi pi-plus" 
          severity="success"
          @click="openCreateDialog" 
        />

        <div class="w-px h-8 bg-gray-300 mx-2"></div>

        <Button 
          icon="pi pi-trash" 
          :label="trashMode ? t('common.showActive') : t('common.showTrash')" 
          severity="secondary"
          @click="toggleTrashMode"
        />
      </div>
    </div>
    
    <BaseDataTable
      :data="filteredLocations"
      :loading="loading"
      :columns="columnOptions"
      :filters="filters"
      :globalFilterFields="['name','code','description','area','site.name']"
      :selectionMode="!trashMode && canWrite('locations') ? 'multiple' : null"
      :selection="selectedLocations"
      :showExport="false"
      @selection-change="selectedLocations = $event"
      @filter-change="updateFilter"
      @refresh="fetchLocations"
    >
      <template #filters>
        <Dropdown 
          v-model="filters['site_id'].value" 
          :options="siteOptions" 
          optionLabel="name" 
          optionValue="id" 
          :placeholder="t('locations.filterBySite')" 
          showClear 
          style="min-width: 150px" 
        />
        <Dropdown 
          v-model="filters['floorplan_status'].value" 
          :options="floorplanOptions" 
          optionLabel="label" 
          optionValue="value" 
          :placeholder="t('locations.filterByFloorplan')" 
          showClear 
          style="min-width: 150px" 
        />
      </template>

      <template #actions>
        <Button 
          v-if="!trashMode && canWrite('locations')"
          :label="t('common.bulkEdit')" 
          icon="pi pi-pencil" 
          severity="warning"
          :disabled="!selectedLocations.length" 
          @click="openBulkEditDialog" 
        />
      </template>
      
      <template #body-actions="{ data }">
        <div class="flex gap-2">
          <Button 
            v-if="!trashMode"
            icon="pi pi-eye" 
            size="small"
            severity="secondary"
            @click="viewLocation(data.id)" 
          />
          <Button 
            v-if="!trashMode && canWrite('locations')"
            icon="pi pi-pencil" 
            size="small"
            @click="openEditDialog(data)" 
          />
          <Button 
            v-if="!trashMode && canWrite('locations')"
            icon="pi pi-copy" 
            size="small"
            severity="info"
            :loading="duplicating"
            @click="duplicateLocation(data)" 
          />
          <Button 
            v-if="!trashMode && canDelete('locations')"
            icon="pi pi-trash" 
            size="small"
            severity="danger"
            @click="deleteLocation(data.id)" 
          />
          <Button 
            v-if="trashMode && canWrite('locations')"
            icon="pi pi-undo" 
            size="small"
            severity="success"
            @click="restoreLocation(data.id)" 
          />
          <Button 
            v-if="trashMode && canDelete('locations')"
            icon="pi pi-times" 
            size="small"
            severity="danger"
            @click="hardDeleteLocation(data.id)" 
          />
        </div>
      </template>


    </BaseDataTable>
    
    <BaseDialog
      v-model:visible="showDialog"
      :title="editingLocation ? t('common.edit') : t('common.new')"
      :showFooter="false"
      @close="close"
    >
      <LocationForm 
        :location="editingLocation" 
        :sites="sites"
        :areas="areas"
        @submit="saveLocation" 
        @cancel="close"
        @site-changed="handleSiteChanged"
      />
      <FloorplanUploader
        v-if="editingLocation && editingLocation.id"
        :locationId="editingLocation.id"
        :floorplan="editingLocation.floorplan"
        @uploaded="fetchLocations"
      />
    </BaseDialog>

    <BaseDialog
      v-model:visible="showBulkDialog"
      :title="t('common.bulkEdit')"
      :showFooter="false"
      @close="closeBulkDialog"
    >
      <div class="bulk-edit-form">
        <div class="mb-4">
          <p class="text-sm text-gray-600">
            {{ t('common.bulkEditInfo', { count: selectedLocations.length }) }}
          </p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="field">
            <label class="block text-sm font-medium mb-2">{{ t('common.site') }}</label>
            <Dropdown
              v-model="bulkData.site_id"
              :options="siteOptions"
              option-label="name"
              option-value="id"
              :placeholder="t('common.select')"
              class="w-full"
            />
          </div>
          
          <div class="field">
            <label class="block text-sm font-medium mb-2">{{ t('sites.area') }}</label>
            <InputText
              v-model="bulkData.area"
              :placeholder="t('sites.area')"
              class="w-full"
            />
          </div>
        </div>
        
        <div class="flex justify-end gap-2 mt-6">
          <Button 
            :label="t('common.cancel')" 
            severity="secondary"
            @click="closeBulkDialog" 
          />
          <Button 
            :label="t('common.save')" 
            @click="saveBulkEdit" 
          />
        </div>
      </div>
    </BaseDialog>

    <!-- TODO: Implementare LocationImportDialog -->
    <BaseDialog
      v-model:visible="showFloorplanDialog"
      :title="t('common.floorplan')"
      @close="showFloorplanDialog = false"
    >
      <Image 
        v-if="selectedFloorplan" 
        :src="getFloorplanThumbnailUrl(selectedFloorplan)" 
        alt="Planimetria" 
        width="100%" 
        preview 
      />
    </BaseDialog>
    
    <BaseConfirmDialog
      v-model:showConfirmDialog="showConfirmDialog"
      :confirmData="confirmData"
      @execute="executeConfirmedAction"
      @close="closeConfirmDialog"
    />

    <BaseDialog
      v-model:visible="showViewDialog"
      :title="t('locations.title') + ' - ' + (viewingLocation?.name || '')"
      :showFooter="false"
      @close="showViewDialog = false"
    >
      <div v-if="viewingLocation">
        <div class="mb-2"><b>{{ t('common.name') }}:</b> {{ viewingLocation.name }}</div>
        <div class="mb-2"><b>{{ t('common.code') }}:</b> {{ viewingLocation.code }}</div>
        <div class="mb-2"><b>{{ t('common.description') }}:</b> {{ viewingLocation.description }}</div>
        <div class="mb-2"><b>{{ t('locations.area') }}:</b> {{ viewingLocation.area }}</div>
        <div class="mb-2"><b>{{ t('common.site') }}:</b> {{ viewingLocation.site?.name }}</div>
        <div class="mb-2"><b>{{ t('locations.floorplan') }}:</b> {{ viewingLocation.floorplan ? 'Presente' : 'Assente' }}</div>
        <div class="mb-2"><b>{{ t('common.notes') }}:</b> {{ viewingLocation.notes }}</div>
      </div>
    </BaseDialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { usePermissions } from '../composables/usePermissions'
import { useApi } from '../composables/useApi'
import { useFilters } from '../composables/useFilters'
import { useDialog } from '../composables/useDialog'
import { useConfirm } from '../composables/useConfirm'
import { useDuplicate } from '../composables/useDuplicate'
import api from '../api/api'

import BaseDataTable from '../components/base/BaseDataTable.vue'
import BaseDialog from '../components/base/BaseDialog.vue'
import BaseConfirmDialog from '../components/base/BaseConfirmDialog.vue'
import LocationForm from '../components/forms/LocationForm.vue'
import FloorplanUploader from '../components/features/assets/widgets/FloorplanUploader.vue'
import Button from 'primevue/button'
import Dropdown from 'primevue/dropdown'
import InputText from 'primevue/inputtext'
import Image from 'primevue/image'

const { t } = useI18n()
const router = useRouter()
const { canWrite, canDelete } = usePermissions()

// Composables
const { loading, execute } = useApi()
const { filters, globalSearch, selectedColumns, filterData, getApiParams } = useFilters({
  global: { value: null, matchMode: 'contains' },
  site_id: { value: null, matchMode: 'equals' },
  floorplan_status: { value: null, matchMode: 'equals' }
}, 'locations')

const { isVisible: showDialog, data: editingLocation, openCreate, openEdit, close } = useDialog()
const { 
  showConfirmDialog, 
  confirmData, 
  confirmDelete, 
  confirmBulkAction, 
  confirmEmptyTrash,
  executeConfirmedAction,
  closeConfirmDialog 
} = useConfirm()

const { duplicating, duplicateItem, excludeFunctions } = useDuplicate()

const showViewDialog = ref(false)
const viewingLocation = ref(null)


// Data
const locations = ref([])
const sites = ref([])
const areas = ref([])
const selectedLocations = ref([])
const trashMode = ref(false)

// Import/Export

// Bulk edit
const showBulkDialog = ref(false)
const bulkData = ref({
  site_id: null,
  area: ''
})

// Floorplan
const showFloorplanDialog = ref(false)
const selectedFloorplan = ref(null)

const columnOptions = computed(() => {
  const columns = [
    { field: 'name', header: t('common.name'), sortable: true },
    { field: 'code', header: t('common.code'), sortable: true },
    { field: 'description', header: t('common.description'), sortable: false },
    { field: 'area_name', header: t('locations.area'), sortable: false },
    { field: 'site.name', header: t('common.site'), sortable: false },
    { field: 'floorplan_status', header: t('locations.floorplan'), sortable: false }
  ]
  
  // Aggiungi colonna azioni sempre, perché il pulsante "Visualizza" è sempre disponibile
  columns.push({ field: 'actions', header: t('common.actions'), sortable: false })
  
  return columns
})

const siteOptions = computed(() => sites.value)

const floorplanOptions = computed(() => [
  { label: t('locations.floorplanPresent'), value: 'Presente' },
  { label: t('locations.floorplanAbsent'), value: 'Assente' }
])

const filteredLocations = computed(() => {
  let filtered = locations.value
  
  // Aggiungi il campo floorplan_status per la visualizzazione
  filtered = filtered.map(location => ({
    ...location,
    floorplan_status: location.floorplan ? 'Presente' : 'Assente'
  }))
  
  // Filtro per sito
  if (filters.value.site_id && filters.value.site_id.value) {
    filtered = filtered.filter(l => l.site_id === filters.value.site_id.value)
  }
  
  // Filtro per planimetria
  if (filters.value.floorplan_status && filters.value.floorplan_status.value) {
    filtered = filtered.filter(l => l.floorplan_status === filters.value.floorplan_status.value)
  }
  
  // Filtro globale
  if (filters.value.global && filters.value.global.value) {
    const search = filters.value.global.value.toLowerCase()
    filtered = filtered.filter(l =>
      (l.name && l.name.toLowerCase().includes(search)) ||
      (l.code && l.code.toLowerCase().includes(search)) ||
      (l.description && l.description.toLowerCase().includes(search)) ||
      (l.area_name && l.area_name.toLowerCase().includes(search)) ||
      (l.site && l.site.name && l.site.name.toLowerCase().includes(search))
    )
  }
  
  return filtered
})

onMounted(async () => {
  await Promise.all([fetchSites(), fetchAreas(), fetchLocations()])
})

async function fetchSites() {
  await execute(async () => {
    const response = await api.getSites()
    sites.value = response.data
    return response
  }, {
    errorContext: t('common.fetchError'),
    showToast: false
  })
}

async function fetchAreas(siteId = null) {
  await execute(async () => {
    const params = siteId ? { site_id: siteId } : {}
    const response = await api.getAreas(params)
    areas.value = response.data
    return response
  }, {
    errorContext: t('common.fetchError'),
    showToast: false
  })
}

async function handleSiteChanged(siteId) {
  await fetchAreas(siteId)
}

async function fetchLocations() {
  await execute(async () => {
    const params = getApiParams()
    let response
    if (trashMode.value) {
      response = await api.getLocationsTrash(params)
    } else {
      response = await api.getLocations(params)
    }
    locations.value = response.data
    return response
  }, {
    errorContext: t('common.fetchError'),
    showToast: false
  })
}

function openCreateDialog() {
  openCreate(t('common.new'), null)
}

function openEditDialog(location) {
  openEdit(t('common.edit'), location)
}

function openBulkEditDialog() {
  bulkData.value = {
    site_id: null,
    area: ''
  }
  showBulkDialog.value = true
}

function closeBulkDialog() {
  showBulkDialog.value = false
  selectedLocations.value = []
}

async function saveBulkEdit() {
  const updates = {}
  if (bulkData.value.site_id !== null) updates.site_id = bulkData.value.site_id
  if (bulkData.value.area !== '') updates.area = bulkData.value.area
  
  if (Object.keys(updates).length === 0) {
    closeBulkDialog()
    return
  }
  
  await execute(async () => {
    for (const location of selectedLocations.value) {
      await api.updateLocation(location.id, updates)
    }
    closeBulkDialog()
    await fetchLocations()
  }, {
    successMessage: t('common.bulkUpdated'),
    errorContext: t('common.bulkError')
  })
}

async function saveLocation(data) {
  const formData = { ...data }
  
  if (editingLocation.value) {
    // Modalità modifica
    await execute(async () => {
      await api.updateLocation(editingLocation.value.id, formData)
      close()
      await fetchLocations()
    }, {
      successMessage: t('common.updated'),
      errorContext: t('common.updateError')
    })
  } else {
    // Modalità creazione
    await execute(async () => {
      await api.createLocation(formData)
      close()
      await fetchLocations()
    }, {
      successMessage: t('common.created'),
      errorContext: t('common.createError')
    })
  }
}

async function deleteLocation(id) {
  await confirmDelete(
    t('common.confirmDelete'),
    t('common.warningDelete'),
    async () => {
      await execute(async () => {
        await api.deleteLocation(id)
        await fetchLocations()
      }, {
        successMessage: t('common.deleted'),
        errorContext: t('common.deleteError')
      })
    }
  )
}

async function duplicateLocation(location) {
  await duplicateItem(
    location,
    async (data) => {
      const result = await api.createLocation(data)
      await fetchLocations()
      return result
    },
    'location',
    excludeFunctions.location
  )
}

function viewLocation(id) {
  const loc = locations.value.find(l => l.id === id)
  if (loc) {
    viewingLocation.value = loc
    showViewDialog.value = true
  }
}

function openFloorplanDialog(location) {
  selectedFloorplan.value = location.floorplan
  showFloorplanDialog.value = true
}

function getFloorplanThumbnailUrl(floorplan) {
  if (!floorplan || !floorplan.location_id || !floorplan.id) return ''
  const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  return `${baseUrl}/locations/${floorplan.location_id}/floorplan/${floorplan.id}`
}

function toggleTrashMode() {
  trashMode.value = !trashMode.value
  selectedLocations.value = []
  fetchLocations()
}

async function restoreLocation(id) {
  await execute(async () => {
    await api.restoreLocation(id)
    await fetchLocations()
  }, {
    successMessage: t('common.restored'),
    errorContext: t('common.restoreError')
  })
}

async function hardDeleteLocation(id) {
  await execute(async () => {
    await api.hardDeleteLocation(id)
    await fetchLocations()
  }, {
    successMessage: t('common.hardDeleted'),
    errorContext: t('common.hardDeleteError')
  })
}

async function emptyTrash() {
  await execute(async () => {
    for (const loc of locations.value) {
      await api.hardDeleteLocation(loc.id)
    }
    await fetchLocations()
  }, {
    successMessage: t('common.trashEmptied'),
    errorContext: t('common.emptyTrashError')
  })
}

async function handleEmptyTrash() {
  await confirmEmptyTrash(
    t('common.confirmEmptyTrash'),
    t('common.warningEmptyTrash'),
    emptyTrash
  )
}

// Export CSV
async function exportCsv() {
  try {
    const response = await api.exportLocationsCsv();
    const blob = new Blob([response.data], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'locations.csv');
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (e) {
    alert('Errore durante l\'esportazione CSV');
  }
}

// Import
function onLocationImport() {
  showImportDialog.value = false
  fetchLocations()
}

function updateFilter(newFilters) {
  Object.assign(filters, newFilters)
}
</script>

<style scoped>
.locations-page {
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