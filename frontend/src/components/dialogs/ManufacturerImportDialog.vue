<template>
  <Dialog :visible="visible" @update:visible="$emit('close')" :header="t('manufacturerImport.title')" :modal="true" :style="{ width: '50vw' }">
    <div class="mb-3">
      <a :href="templateUrl" download class="p-button p-button-sm p-button-outlined">
        <i class="pi pi-download mr-2" />{{ t('manufacturerImport.downloadTemplate') }}
      </a>
    </div>
    <div class="mb-3">
      <input type="file" accept=".csv,.xlsx" @change="onFileChange" />
    </div>
    <div v-if="loading" class="mb-3">
      <ProgressSpinner style="width:40px;height:40px" />
    </div>
    <div v-if="error" class="mb-3 text-red-600">
      <pre>{{ error }}</pre>
    </div>
    <div v-if="previewResult">
      <div v-if="previewResult.to_create && previewResult.to_create.length">
        <h4 class="mb-1">{{ t('manufacturerImport.toCreate') }}</h4>
        <DataTable :value="previewResult.to_create" scrollable :scrollHeight="'20vh'">
          <Column v-for="col in columns" :key="col.field" :field="col.field" :header="col.header" />
        </DataTable>
      </div>
      <div v-if="previewResult.to_update && previewResult.to_update.length">
        <h4 class="mt-3 mb-1">{{ t('manufacturerImport.toUpdate') }}</h4>
        <DataTable :value="previewResult.to_update" scrollable :scrollHeight="'20vh'">
          <Column field="name" :header="t('manufacturerForm.name')" />
          <Column field="diff" :header="t('manufacturerImport.differences')">
            <template #body="{ data }">
              <ul>
                <li v-for="(change, field) in data.diff" :key="field">
                  <b>{{ field }}</b>: <span style="color: #888">{{ change.old }}</span> → <span style="color: #059669">{{ change.new }}</span>
                </li>
              </ul>
            </template>
          </Column>
        </DataTable>
      </div>
      <div v-if="previewResult.errors && previewResult.errors.length">
        <h4 class="mt-3 mb-1 text-red-600">{{ t('manufacturerImport.errors') }}</h4>
        <ul>
          <li v-for="err in previewResult.errors" :key="err.row">{{ t('manufacturerImport.row') }} {{ err.row }}: {{ err.error }}</li>
        </ul>
      </div>
    </div>
    <template #footer>
      <Button :label="t('common.cancel')" class="p-button-text" @click="$emit('close')" />
      <Button :label="t('manufacturerImport.confirm')" :disabled="!file || loading || (previewResult && previewResult.errors && previewResult.errors.length)" @click="confirmImport" />
    </template>
  </Dialog>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import ProgressSpinner from 'primevue/progressspinner'
import api from '../../api/api'

const { t } = useI18n()
const props = defineProps({
  visible: Boolean
})
const emit = defineEmits(['close', 'imported'])

const templateUrl = '/template_import_manufacturer.csv'
const file = ref(null)
const columns = [
  { field: 'name', header: t('manufacturerForm.name') },
  { field: 'description', header: t('manufacturerForm.description') },
  { field: 'website', header: t('manufacturerForm.website') },
  { field: 'email', header: t('manufacturerForm.email') },
  { field: 'phone', header: t('manufacturerForm.phone') },
]
const loading = ref(false)
const error = ref('')
const previewResult = ref(null)

async function onFileChange(e) {
  error.value = ''
  previewResult.value = null
  const f = e.target.files[0]
  if (!f) return
  file.value = f
  loading.value = true
  try {
    const { data } = await api.previewManufacturerImportXlsx(f)
    previewResult.value = data
    error.value = (data.errors && data.errors.length) ? data.errors.map(e => `Riga ${e.row}: ${e.error}`).join('\n') : ''
  } catch (e) {
    error.value = t('manufacturerImport.readError')
  }
  loading.value = false
}

async function confirmImport() {
  if (!file.value) return
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.confirmManufacturerImportXlsx(file.value)
    emit('imported', data)
  } catch (e) {
    error.value = t('manufacturerImport.readError')
  }
  loading.value = false
}
</script>

<style scoped>
.text-red-600 {
  color: #dc2626;
}
</style> 