<template>
  <div class="areas-page">
    <div class="page-header">
      <div class="header-content">
        <h1>{{ t('areas.title') }}</h1>
        <p class="page-description">{{ t('areas.description') }}</p>
      </div>
      <div class="header-actions">
        <Button 
          :label="t('areas.create')" 
          icon="pi pi-plus" 
          @click="openCreateDialog"
          class="p-button-primary"
        />
      </div>
    </div>

    <!-- Filtri -->
    <div class="filters-section">
      <div class="filters-row">
        <div class="filter-group">
          <label>{{ t('common.site') }}</label>
          <Dropdown
            v-model="filters.site_id.value"
            :options="sites"
            optionLabel="name"
            optionValue="id"
            :placeholder="t('common.selectSite')"
            class="w-full"
            @change="loadAreas"
          />
        </div>
      </div>
    </div>

    <!-- Tabella Aree -->
    <div class="table-section">
      <BaseDataTable
        :data="areas"
        :loading="loading"
        :columns="columns"
        :filters="filters"
        :selected-columns="selectedColumns"
        :show-column-selector="true"
        @row-select="onRowSelect"
        @filter-change="updateFilter"
      >
        <template #body-actions="{ data }">
          <div class="action-buttons">
            <Button
              icon="pi pi-pencil"
              class="p-button-text p-button-sm"
              @click="editArea(data)"
              :title="t('common.edit')"
            />
            <Button
              icon="pi pi-trash"
              class="p-button-text p-button-danger p-button-sm"
              @click="confirmDelete(data)"
              :title="t('common.delete')"
            />
          </div>
        </template>
      </BaseDataTable>
    </div>

    <!-- Dialog Creazione/Modifica -->
    <BaseDialog
      v-model:visible="dialogVisible"
      :title="dialogTitle"
      :showFooter="false"
      @close="closeDialog"
    >
      <AreaForm
        v-if="dialogVisible"
        :area="editingArea"
        :sites="sites"
        @submit="handleFormSubmit"
        @cancel="closeDialog"
      />
    </BaseDialog>

    <!-- Dialog Conferma Eliminazione -->
    <BaseConfirmDialog
      v-model:showConfirmDialog="deleteDialogVisible"
      :confirm-data="{
        type: 'delete',
        title: t('areas.deleteTitle'),
        message: t('areas.deleteMessage', { name: areaToDelete?.name })
      }"
      @confirm="deleteArea"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToast } from 'primevue/usetoast'
import { useApi } from '@/composables/useApi'
import { useConfirm } from '@/composables/useConfirm'
import { usePermissions } from '@/composables/usePermissions'
import { useFilters } from '@/composables/useFilters'
import api from '@/api/api'

import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Dropdown from 'primevue/dropdown'
import BaseDataTable from '@/components/base/BaseDataTable.vue'
import BaseDialog from '@/components/base/BaseDialog.vue'
import BaseConfirmDialog from '@/components/base/BaseConfirmDialog.vue'
import AreaForm from '@/components/forms/AreaForm.vue'

const { t } = useI18n()


const toast = useToast()
const { loading, execute } = useApi()
const { canRead, canWrite, canDelete } = usePermissions()

// Data
const areas = ref([])
const sites = ref([])
const selectedArea = ref(null)

// Filters
const { filters, globalSearch, selectedColumns, filterData, getApiParams } = useFilters({
  site_id: { value: null, matchMode: 'equals' },
  global: { value: '', matchMode: 'contains' }
}, 'areas', ['name', 'code', 'typology', 'site_name', 'created_at', 'actions'])

// Dialog states
const dialogVisible = ref(false)
const deleteDialogVisible = ref(false)
const submitting = ref(false)
const editingArea = ref(null)
const areaToDelete = ref(null)

// Computed
const dialogTitle = computed(() => {
  return editingArea.value ? t('areas.edit') : t('areas.create')
})

const columns = computed(() => [
  { field: 'name', header: t('common.name') },
  { field: 'code', header: t('areas.code') },
  { field: 'typology', header: t('areas.typology') },
  { field: 'site_name', header: t('common.site') },
  { field: 'created_at', header: t('common.createdAt') },
  { field: 'actions', header: t('common.actions') }
])

// selectedColumns è già definito dal composable useFilters

// Methods
async function loadAreas() {
  const params = getApiParams()
  if (filters.value.site_id && filters.value.site_id.value) {
    params.site_id = filters.value.site_id.value
  }
  
  const response = await execute(() => api.getAreas(params))
  if (response) {
    areas.value = response.data
  }
}

async function loadSites() {
  const response = await execute(() => api.getSites())
  if (response) {
    sites.value = response.data
  }
}

function openCreateDialog() {
  if (!canWrite('areas')) {
    toast.add({
      severity: 'error',
      summary: t('common.error'),
      detail: t('common.noPermission'),
      life: 3000
    })
    return
  }
  
  editingArea.value = null
  dialogVisible.value = true
}

function editArea(area) {
  if (!canWrite('areas')) {
    toast.add({
      severity: 'error',
      summary: t('common.error'),
      detail: t('common.noPermission'),
      life: 3000
    })
    return
  }
  
  editingArea.value = { ...area }
  dialogVisible.value = true
}

function confirmDelete(area) {
  if (!canDelete('areas')) {
    toast.add({
      severity: 'error',
      summary: t('common.error'),
      detail: t('common.noPermission'),
      life: 3000
    })
    return
  }
  
  areaToDelete.value = area
  deleteDialogVisible.value = true
}

async function handleFormSubmit(formData) {
  submitting.value = true
  
  try {
    if (editingArea.value) {
      // Update
      const response = await execute(() => api.updateArea(editingArea.value.id, formData))
      if (response) {
        toast.add({
          severity: 'success',
          summary: t('common.success'),
          detail: t('areas.updated'),
          life: 3000
        })
        await loadAreas()
        closeDialog()
      }
    } else {
      // Create
      const response = await execute(() => api.createArea(formData))
      if (response) {
        toast.add({
          severity: 'success',
          summary: t('common.success'),
          detail: t('areas.created'),
          life: 3000
        })
        await loadAreas()
        closeDialog()
      }
    }
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: t('common.error'),
      detail: t('areas.saveError'),
      life: 5000
    })
  } finally {
    submitting.value = false
  }
}

async function deleteArea() {
  if (!areaToDelete.value) return
  
  const response = await execute(() => api.deleteArea(areaToDelete.value.id))
  if (response) {
    toast.add({
      severity: 'success',
      summary: t('common.success'),
      detail: t('areas.deleted'),
      life: 3000
    })
    await loadAreas()
  }
  
  areaToDelete.value = null
  deleteDialogVisible.value = false
}

function closeDialog() {
  dialogVisible.value = false
  editingArea.value = null
}

function updateFilter(newFilters) {
  Object.assign(filters.value, newFilters)
  loadAreas()
}

function onRowSelect(event) {
  selectedArea.value = event.data
}

// La ricerca globale è gestita dal composable useFilters

// Lifecycle
onMounted(async () => {
  await Promise.all([loadSites(), loadAreas()])
})
</script>

<style scoped>
.areas-page {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  gap: 2rem;
}

.header-content h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
  font-weight: 600;
  color: var(--text-color);
}

.page-description {
  margin: 0;
  color: var(--text-color-secondary);
  font-size: 1rem;
}

.filters-section {
  background: var(--surface-card);
  border: 1px solid var(--surface-border);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.filters-row {
  display: flex;
  gap: 1rem;
  align-items: end;
}

.filter-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 500;
  color: var(--text-color);
}

.table-section {
  background: var(--surface-card);
  border: 1px solid var(--surface-border);
  border-radius: 8px;
  overflow: hidden;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

@media (max-width: 768px) {
  .areas-page {
    padding: 1rem;
  }
  
  .page-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .filters-row {
    flex-direction: column;
  }
}
</style> 