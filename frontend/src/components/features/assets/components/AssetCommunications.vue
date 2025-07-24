<!--
  - AssetCommunications.vue
  - Componente per la gestione delle comunicazioni degli asset
  - Utilizza i componenti PrimeVue per la gestione del form
-->
<template>
  <div>
    <h3 class="mb-2 font-semibold">{{ t('assetCommunications.title') }}</h3>

    <DataTable :value="communications">
      <Column :header="t('assetCommunications.connectedAsset')">
        <template #body="{ data }">
          <router-link
            :to="`/assets/${data.linked_asset_id}`"
            class="text-blue-600 hover:underline"
          >
            {{ data.linked_asset_name }}
          </router-link>
        </template>
      </Column>
      <Column field="packet_count" :header="t('assetCommunications.packets')" />
      <Column field="direction" :header="t('assetCommunications.direction')" />
    </DataTable>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import { useToast } from 'primevue/usetoast'
import api from '@/api/api'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const route = useRoute()
const assetId = ref(route.params.id)  // o come lo chiami nel router

const toast = useToast()
const communications = ref([])

const fetchCommunications = async () => {
  try {
    const res = await api.getAssetCommunications(assetId.value)
    communications.value = res.data
  } catch (err) {
    toast.add({ severity: 'error', summary: t('common.error'), detail: t('assetCommunications.fetchError') })
  }
}

onMounted(fetchCommunications)

// 🔁 Ricarica i dati se cambia assetId
watch(() => route.params.id, (newId) => {
  assetId.value = newId
  fetchCommunications()
})
</script>