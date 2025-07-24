<template>
  <Dialog :visible="visible" @update:visible="$emit('close')" :header="t('assetImport.title')" :modal="true" :style="{ width: '50vw' }">
    <div class="mb-3">
      <b>{{ t('assetImport.instructionsTitle') }}</b><br><br>
      1. {{ t('assetImport.step1') }}<br>
      2. {{ t('assetImport.step2') }}<br>
      <li>{{ t('assetImport.nameField') }}</li>
      <li>{{ t('assetImport.tagField') }}</li>
      <li>{{ t('assetImport.siteCodeField') }}</li>
      <li>{{ t('assetImport.assetTypeField') }}</li>
      <li>{{ t('assetImport.ipAddressField') }}</li>
      <li>{{ t('assetImport.manufacturerField') }}</li>
      <br>
      3. {{ t('assetImport.step3') }}<br>
      4. {{ t('assetImport.step4') }}<br><br>
      <a :href="templateUrl" download class="p-button p-button-sm p-button-outlined">
        <i class="pi pi-download mr-2" />{{ t('assetImport.downloadTemplate') }}
      </a>
    </div>
    <div class="mb-3">
      <input type="file" accept=".csv,.xlsx" @change="onFileChange" :aria-label="t('assetImport.fileInput')" />
    </div>
    <div v-if="loading" class="mb-3">
      <ProgressSpinner style="width:40px;height:40px" />
    </div>
    <div v-if="error" class="mb-3 text-red-600">
      <pre>{{ error }}</pre>
    </div>
    <div v-if="previewResult">
      <div v-if="previewResult.to_create && previewResult.to_create.length">
        <h4 class="mb-1">{{ t('assetImport.toCreate') }}</h4>
        <DataTable :value="previewResult.to_create" scrollable :scrollHeight="'20vh'">
          <Column v-for="col in columns" :key="col" :field="col" :header="col" v-if="col !== 'interfaces'" />
          <Column v-if="columns.includes('interfaces')" field="interfaces" header="Interfacce">
            <template #body="{ data }">
              <ul v-if="data.interfaces && data.interfaces.length">
                <li v-for="iface in data.interfaces" :key="iface.ip_address">
                  {{ iface.name }} ({{ iface.type }}) - {{ iface.ip_address }}
                </li>
              </ul>
              <span v-else>-</span>
            </template>
          </Column>
        </DataTable>
      </div>
      <div v-if="previewResult.to_update && previewResult.to_update.length">
        <h4 class="mt-3 mb-1">{{ t('assetImport.toUpdate') }}</h4>
        <DataTable :value="previewResult.to_update" scrollable :scrollHeight="'20vh'">
          <Column field="tag" header="Tag" />
          <Column field="diff" header="Differenze">
            <template #body="{ data }">
              <ul>
                <li v-for="(change, field) in data.diff" :key="field">
                  <b>{{ field }}</b>: <span style="color: #888">{{ change.old }}</span> → <span style="color: #059669">{{ change.new }}</span>
                </li>
              </ul>
            </template>
          </Column>
          <Column v-if="data.interfaces && data.interfaces.length" field="interfaces" header="Interfacce">
            <template #body="{ data }">
              <ul v-if="data.interfaces && data.interfaces.length">
                <li v-for="iface in data.interfaces" :key="iface.ip_address">
                  {{ iface.name }} ({{ iface.type }}) - {{ iface.ip_address }}
                </li>
              </ul>
              <span v-else>-</span>
            </template>
          </Column>
        </DataTable>
      </div>
      <div v-if="previewResult.errors && previewResult.errors.length">
        <h4 class="mt-3 mb-1 text-red-600">{{ t('assetImport.errors') }}</h4>
        <ul>
          <li v-for="err in previewResult.errors" :key="err.row">Riga {{ err.row }}: {{ err.error }}</li>
        </ul>
      </div>
    </div>
    <template #footer>
      <Button :label="t('common.cancel')" class="p-button-text" @click="$emit('close')" />
      <Button :label="t('assetImport.confirm')" :disabled="!file || loading || (previewResult && previewResult.errors && previewResult.errors.length)" @click="confirmImport" />
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import ProgressSpinner from 'primevue/progressspinner'
import * as XLSX from 'xlsx'
import api from '../../api/api'

const { t } = useI18n()
const props = defineProps({
  visible: Boolean
})
const emit = defineEmits(['close', 'imported'])

const templateUrl = '/template_import_asset.csv'
const file = ref(null)
const preview = ref([])
const columns = ref([])
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
    // Chiamata preview backend
    const { data } = await api.previewAssetImportXlsx(f)
    previewResult.value = data
    columns.value = ['name', 'tag', 'site_id', 'asset_type_id', 'manufacturer', 'interfaces']
    preview.value = (data.to_create || []).concat((data.to_update || []).map(u => ({ ...u, _update: true })))
    error.value = (data.errors && data.errors.length) ? data.errors.map(e => `Riga ${e.row}: ${e.error}`).join('\n') : ''
  } catch (e) {
    error.value = t('assetImport.readError')
  }
  loading.value = false
}

async function confirmImport() {
  if (!file.value) return
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.confirmAssetImportXlsx(file.value)
    emit('imported', data)
  } catch (e) {
    error.value = t('assetImport.readError')
  }
  loading.value = false
}
</script>

<style scoped>
.text-red-600 {
  color: #dc2626;
}
</style> 