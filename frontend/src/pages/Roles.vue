<template>
  <div class="roles-page">
    <div class="page-header">
      <h1>{{ t('roles.title') }}</h1>
      <div class="flex gap-2">
        <!-- Azioni principali -->
        <Button 
          v-if="canWrite('roles')"
          :label="t('roles.new')" 
          icon="pi pi-plus" 
          severity="success"
          @click="openCreateDialog" 
        />
        <!-- Separatore visivo -->
        <div v-if="canWrite('roles')" class="w-px h-8 bg-gray-300 mx-2"></div>
        <!-- Test Permissions -->
        <Button 
          v-if="canWrite('roles')"
          icon="pi pi-key" 
          :label="t('roles.testPermissions')" 
          severity="info"
          @click="testPermissions" 
        />
      </div>
    </div>

    <BaseDataTable
      :data="filteredRoles"
      :loading="loading"
      :columns="columnOptions"
      :filters="filters"
      :globalFilterFields="['name']"
      :selectionMode="canWrite('roles') ? 'multiple' : null"
      :selection="selectedRoles"
      :showExport="false"
      @selection-change="selectedRoles = $event"
      @filter-change="updateFilter"
      @refresh="fetchRoles"
    >
      <template #body-permissions_count="{ data }">
        <Tag :value="getPermissionsCount(data)" :severity="getPermissionsSeverity(data)" />
      </template>

      <template #body-actions="{ data }">
        <div class="flex gap-2">
          <Button 
            icon="pi pi-eye" 
            size="small"
            severity="secondary"
            @click="goToDetail(data.id)" 
          />
          <Button 
            v-if="canWrite('roles')"
            icon="pi pi-pencil" 
            size="small"
            @click="openEditDialog(data)" 
          />
          <Button 
            v-if="canDelete('roles')"
            icon="pi pi-trash" 
            size="small"
            severity="danger"
            @click="deleteRole(data.id)" 
          />
        </div>
      </template>
    </BaseDataTable>

    <BaseDialog
      v-model:visible="showDialog"
      :title="dialogTitle"
      :showFooter="false"
      @close="close"
    >
      <RoleForm 
        :role="editingRole" 
        @submit="saveRole" 
        @cancel="close" 
      />
    </BaseDialog>

    <BaseConfirmDialog
      v-model:showConfirmDialog="showConfirmDialog"
      :confirmData="confirmData"
      @execute="executeConfirmedAction"
      @close="closeConfirmDialog"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { i18n } from '../locales/loader.js'
import { useToast } from 'primevue/usetoast'
import { usePermissions } from '../composables/usePermissions'
import { useApi } from '../composables/useApi'
import { useFilters } from '../composables/useFilters'
import { useDialog } from '../composables/useDialog'
import { useConfirm } from '../composables/useConfirm'
import api from '../api/api'

import BaseDataTable from '../components/base/BaseDataTable.vue'
import BaseDialog from '../components/base/BaseDialog.vue'
import BaseConfirmDialog from '../components/base/BaseConfirmDialog.vue'
import RoleForm from '../components/forms/RoleForm.vue'
import Button from 'primevue/button'
import Tag from 'primevue/tag'

const { t } = useI18n()
const router = useRouter()
const { canWrite, canDelete } = usePermissions()
const toast = useToast()

// Composables
const { loading, execute } = useApi()
const { filters, globalSearch, selectedColumns, filterData, getApiParams } = useFilters({
  global: { value: null, matchMode: 'contains' }
}, 'roles')

const { isVisible: showDialog, data: editingRole, openCreate, openEdit, close } = useDialog()
const { 
  showConfirmDialog, 
  confirmData, 
  confirmDelete, 
  executeConfirmedAction,
  closeConfirmDialog 
} = useConfirm()

// Data
const roles = ref([])
const selectedRoles = ref([])

const columnOptions = computed(() => [
  { field: 'name', header: t('roles.name'), sortable: true },
  { field: 'permissions_count', header: t('roles.permissions'), sortable: false },
  { field: 'created_at_formatted', header: t('roles.createdAt'), sortable: true },
  { field: 'actions', header: t('common.actions'), sortable: false }
])

const filteredRoles = computed(() => {
  let filtered = roles.value
  
  // Aggiungi il campo permissions_count e formatta le date per la visualizzazione
  filtered = filtered.map(role => ({
    ...role,
    permissions_count: getPermissionsCount(role),
    created_at_formatted: formatDate(role.created_at),
    updated_at_formatted: formatDate(role.updated_at)
  }))
  
  // Filtro globale
  if (filters.value.global && filters.value.global.value) {
    const search = filters.value.global.value.toLowerCase()
    filtered = filtered.filter(r =>
      (r.name && r.name.toLowerCase().includes(search))
    )
  }
  
  return filtered
})

const dialogTitle = computed(() => 
  editingRole.value ? t('roles.edit') : t('roles.new')
)

onMounted(async () => {
  await fetchRoles()
})

async function fetchRoles() {
  await execute(async () => {
    const response = await api.getRoles()
    roles.value = response.data
    return response
  }, {
    errorContext: t('roles.fetchError'),
    showToast: false
  })
}

function openCreateDialog() {
  openCreate(t('roles.new'), null)
}

function openEditDialog(role) {
  openEdit(t('roles.edit'), role)
}

function goToDetail(id) {
  router.push({ name: 'RoleDetails', params: { id } })
}

function deleteRole(id) {
  confirmDelete(
    t('roles.deleteConfirm'),
    t('roles.deleteWarning'),
    async () => {
      await execute(async () => {
        await api.deleteRole(id)
        await fetchRoles()
      }, {
        successMessage: t('roles.deleted'),
        errorContext: t('roles.deleteError')
      })
    }
  )
}

async function saveRole(data) {
  if (editingRole.value) {
    // Modalità modifica
    await execute(async () => {
      await api.updateRole(editingRole.value.id, data)
      close()
      await fetchRoles()
    }, {
      successMessage: t('roles.updated'),
      errorContext: t('roles.updateError')
    })
  } else {
    // Modalità creazione
    await execute(async () => {
      await api.createRole(data)
      close()
      await fetchRoles()
    }, {
      successMessage: t('roles.created'),
      errorContext: t('roles.createError')
    })
  }
}

function getPermissionsCount(role) {
  if (!role.permissions) return '0'
  const count = Object.values(role.permissions).filter(p => p > 0).length
  return count.toString()
}

function getPermissionsSeverity(role) {
  if (!role.permissions) return 'secondary'
  const count = Object.values(role.permissions).filter(p => p > 0).length
  if (count === 0) return 'secondary'
  if (count <= 5) return 'info'
  if (count <= 10) return 'warning'
  return 'success'
}

async function testPermissions() {
  await execute(async () => {
    const response = await api.testUserPermissions()
          // console.log('Permessi utente:', response.data)
    
    // Mostra toast personalizzato con i dati
    toast.add({
      severity: 'info',
      summary: 'Test Permessi',
      detail: `Ruolo: ${response.data.role_name}, Permessi: ${JSON.stringify(response.data.effective_permissions)}`,
      life: 8000
    })
    
    return response
  }, {
    showToast: false, // Disabilitiamo il toast automatico
    errorContext: t('roles.testPermissionsError')
  })
}

function updateFilter(filterName, value) {
  if (filters.value[filterName]) {
    filters.value[filterName].value = value
  }
}

function formatDate(dateString) {
  if (!dateString) return '-'
  
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) return '-'
    
    const locale = i18n.global.locale.value;
    const dateLocale = locale === 'it' ? 'it-IT' : 'en-US';
    return date.toLocaleDateString(dateLocale, {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (error) {
    return '-'
  }
}
</script>

<style scoped>
.roles-page {
  padding: 1rem;
}
</style>