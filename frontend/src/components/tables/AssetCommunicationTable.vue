<template>
  <div class="asset-comm-table">
    <table v-if="rows.length" class="comm-table">
      <thead>
        <tr>
          <th>Asset sorgente</th>
          <th>Interfaccia sorgente</th>
          <th>Asset destinazione</th>
          <th>Interfaccia destinazione</th>
          <th>Pacchetti</th>
          <th>Direzione</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, idx) in rows" :key="idx">
          <td>{{ row.src_asset?.name }}</td>
          <td>
            <div v-if="row.src_interface">
              <div><b>{{ row.src_interface.name }}</b></div>
              <div v-if="row.src_interface.mac_address">MAC: {{ row.src_interface.mac_address }}</div>
              <div v-if="row.src_interface.ip_address">IP: {{ row.src_interface.ip_address }}</div>
            </div>
          </td>
          <td>{{ row.dst_asset?.name }}</td>
          <td>
            <div v-if="row.dst_interface">
              <div><b>{{ row.dst_interface.name }}</b></div>
              <div v-if="row.dst_interface.mac_address">MAC: {{ row.dst_interface.mac_address }}</div>
              <div v-if="row.dst_interface.ip_address">IP: {{ row.dst_interface.ip_address }}</div>
            </div>
          </td>
          <td>{{ row.packet_count }}</td>
          <td>{{ row.direction === 'outgoing' ? t('assetCommunications.outgoing') : t('assetCommunications.incoming') }}</td>
        </tr>
      </tbody>
    </table>
    <div v-else class="placeholder">
      <span>{{ t('assetCommunications.noTableData') }}</span>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import Button from 'primevue/button'
const props = defineProps({
  type: { type: String, default: 'physical' },
  rows: { type: Array, default: () => [] }
})
const { t } = useI18n()
</script>

<style scoped>
.asset-comm-table {
  margin-bottom: 2em;
}
.comm-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
}
.comm-table th, .comm-table td {
  border: 1px solid #e5e7eb;
  padding: 0.5em 0.75em;
  text-align: left;
}
.comm-table th {
  background: #f3f4f6;
}
.placeholder {
  text-align: center;
  color: #888;
  padding: 2em 0;
}
</style> 