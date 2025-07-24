<template>
  <div>
    <div class="section-title">{{ t('assets.mainInfo') }}</div>
    <div class="info-list">
      <div><span class="label">{{ t('assets.serialNumber') }}:</span> <span class="value">{{ asset.serial_number || t('common.na') }}</span></div>
      <div><span class="label">{{ t('assets.model') }}:</span> <span class="value">{{ asset.model || t('common.na') }}</span></div>
      <div><span class="label">{{ t('assets.manufacturer') }}:</span> <span class="value">{{ asset.manufacturer?.name || t('common.na') }}</span></div>
      <div><span class="label">{{ t('common.status') }}:</span> <span class="value">{{ asset.status?.name || t('common.na') }}</span></div>
    </div>
    <div class="section-title">{{ t('assets.networkInterfaces') }}</div>
    <div v-if="asset.interfaces && asset.interfaces.length">
      <div class="flex align-items-center mb-2">
        <span>{{ t('interfaces.summary', { count: asset.interfaces.length }) }}</span>
        <Button class="ml-2 p-button-text p-button-sm" :label="interfacesExpanded ? t('interfaces.hide') : t('interfaces.show')" icon="pi pi-chevron-down" @click="interfacesExpanded = !interfacesExpanded" />
      </div>
      <transition name="fade">
        <div v-if="interfacesExpanded">
          <template v-if="asset.interfaces.length > 4">
            <DataTable :value="asset.interfaces" class="p-datatable-sm" :paginator="false" :rows="50" :filterDisplay="'row'">
              <Column field="name" :header="t('interfaces.name')" :filter="true" :filterPlaceholder="t('interfaces.searchName')" />
              <Column field="type" :header="t('interfaces.type')" />
              <Column field="ip_address" :header="t('interfaces.ipAddress')" />
              <Column field="mac_address" :header="t('interfaces.macAddress')" />
              <Column field="vlan" :header="t('interfaces.vlan')" :filter="true" :filterPlaceholder="t('interfaces.searchVlan')" />
              <Column field="status" :header="t('interfaces.status')" />
            </DataTable>
          </template>
          <template v-else>
            <div
              v-for="(iface, idx) in asset.interfaces"
              :key="iface.id || idx"
              class="interface-info-list mb-3 p-2"
              style="border:1px solid #eee; border-radius:6px;"
            >
              <div class="mb-1">
                <Tag :value="iface.type" severity="info" class="mr-2" />
                <b>{{ iface.name }}</b>
              </div>
              <div class="info-list">
                <div><span class="label">{{ t('interfaces.ipAddress') }}:</span> <span class="value">{{ iface.ip_address || t('common.na') }}</span></div>
                <div><span class="label">{{ t('interfaces.macAddress') }}:</span> <span class="value">{{ iface.mac_address || t('common.na') }}</span></div>
                <div><span class="label">{{ t('interfaces.vlan') }}:</span> <span class="value">{{ iface.vlan || t('common.na') }}</span></div>
                <div><span class="label">{{ t('interfaces.gateway') }}:</span> <span class="value">{{ iface.default_gateway || t('common.na') }}</span></div>
                <div><span class="label">{{ t('interfaces.subnet') }}:</span> <span class="value">{{ iface.subnet_mask || t('common.na') }}</span></div>
                <div><span class="label">{{ t('interfaces.logicalPort') }}:</span> <span class="value">{{ iface.logical_port || t('common.na') }}</span></div>
                <div><span class="label">{{ t('interfaces.plugLabel') }}:</span> <span class="value">{{ iface.physical_plug_label || t('common.na') }}</span></div>
                <div><span class="label">{{ t('interfaces.other') }}:</span> <span class="value">{{ iface.other || t('common.na') }}</span></div>
                <div v-if="iface.details && Object.keys(iface.details).length">
                  <span class="label">{{ t('interfaces.details') }}:</span>
                  <span class="value">
                    <Button icon="pi pi-info-circle" class="p-button-text p-button-info p-button-sm"
                      v-tooltip="JSON.stringify(iface.details, null, 2)" />
                  </span>
                </div>
              </div>
            </div>
          </template>
        </div>
      </transition>
    </div>
    <div v-else class="text-muted p-2">{{ t('assetDetail.noInterfaces') }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

const props = defineProps({
  asset: { type: Object, required: true }
})
const { t } = useI18n()
const interfacesExpanded = ref(false)
</script>

<style scoped>
.section-title { font-weight: bold; margin-top: 1.5rem; margin-bottom: 0.5rem; }
.info-list { margin-bottom: 1rem; }
.label { font-weight: 500; color: #555; }
.value { color: #222; }
.interface-info-list { background: #fafbfc; }
.text-muted { color: #888; }
</style> 