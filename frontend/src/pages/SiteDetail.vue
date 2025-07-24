<template>
  <div class="site-detail-page">
    <Button icon="pi pi-arrow-left" :label="t('common.back')" class="mb-3" @click="goBack" />

    <h2>{{ t('common.site') }}</h2>

    <Card v-if="site" class="mb-4">
      <template #title>{{ site.name }}</template>
      <template #content>
        <p><strong>{{ t('common.code') }}:</strong> {{ site.code }}</p>
        <p><strong>{{ t('common.address') }}:</strong> {{ site.address || 'N/A' }}</p>
        <p><strong>{{ t('common.description') }}:</strong> {{ site.description || 'N/A' }}</p>
      </template>
    </Card>

    <h3>{{ t('locations.title') }}</h3>
    <div class="flex justify-content-between align-items-center mb-2">
  <Button 
    :label="t('common.new')" 
    icon="pi pi-plus" 
    class="p-button-sm" 
    @click="createNewLocation" 
  />
</div>
    <DataTable :value="locations" :loading="loadingLocations" emptyMessage="No locations found">
      <Column field="name" :header="t('common.name')" sortable />
      <Column field="description" :header="t('common.description')" />
      <Column field="area" :header="t('sites.area')" />
<Column header="Planimetria">
  <template #body="{ data }">
    <div v-if="data.floorplan">
      <Image
        :src="getFloorplanThumbnailUrl(data.floorplan)"
        alt="Planimetria"
        width="150"
        preview
      />
    </div>
    <div v-else>-</div>
  </template>
</Column>
      <Column :header="t('common.actions')">
        <template #body="{ data }">
          <Button icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-info" @click="editLocation(data)" />
        </template>
      </Column>
    </DataTable>

<Dialog 
  v-model:visible="editLocationDialog" 
  :header="editingLocation ? t('common.edit') : t('common.new')" 
  :modal="true" 
  :style="{ width: '40vw' }"
>
  <LocationForm 
    :location="editingLocation" 
    :sites="[site]"
    @submit="saveLocation" 
    @cancel="editLocationDialog = false" 
  />
  <template v-if="editingLocation?.id">
<FloorplanUploader 
  v-if="editingLocation?.id"
  :locationId="editingLocation.id"
  :floorplan="editingLocation.floorplan"
  @uploaded="fetchLocations"
/>
</template>
</Dialog>

    <h3>{{ t('contacts.contacts') }}</h3>
    <div class="flex align-items-center gap-2 mb-2">
      <MultiSelect v-model="selectedContactIds" :options="allContacts" optionLabel="fullName" optionValue="id" :placeholder="t('contacts.addContacts')" display="chip" class="mr-2" style="min-width:250px" />
      <Button :label="t('common.save')" icon="pi pi-check" class="p-button-sm" @click="updateSiteContacts" />
      <Button :label="t('common.new')" icon="pi pi-plus" class="p-button-sm" @click="showContactDialog = true" />
    </div>
            <DataTable :value="siteContacts" :loading="loadingContacts" emptyMessage="No associated contacts">
      <Column field="fullName" :header="t('common.fullName')" />
      <Column field="email" :header="t('common.email')" />
      <Column field="phone1" :header="t('common.phone')" />
      <Column field="type" :header="t('common.type')" />
      <Column :header="t('common.actions')">
        <template #body="{ data }">
          <Button icon="pi pi-trash" class="p-button-rounded p-button-text p-button-danger" @click="removeContact(data.id)" :title="t('common.delete')" />
        </template>
      </Column>
    </DataTable>
    <Dialog v-model:visible="showContactDialog" :header="t('common.new')" :modal="true" :style="{ width: '30vw' }">
      <ContactForm @submit="createContact" @cancel="showContactDialog = false" />
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import api from '../api/api'
import LocationForm from '../components/forms/LocationForm.vue'
import FloorplanUploader from '../components/features/assets/widgets/FloorplanUploader.vue'
import { useI18n } from 'vue-i18n'

import Button from 'primevue/button'
import Card from 'primevue/card'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Dialog from 'primevue/dialog'
import Image from 'primevue/image'
import MultiSelect from 'primevue/multiselect'
import ContactForm from '../components/forms/ContactForm.vue'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const { t } = useI18n()

const site = ref(null)
const locations = ref([])
const loadingLocations = ref(false)
const editLocationDialog = ref(false)
const editingLocation = ref(null)

const siteContacts = ref([])
const allContacts = ref([])
const selectedContactIds = ref([])
const loadingContacts = ref(false)
const showContactDialog = ref(false)

const siteId = route.params.id

onMounted(async () => {
  await fetchSite()
  await fetchLocations()
  await fetchAllContacts()
  await fetchSiteContacts()
})

async function fetchSite() {
  try {
    const response = await api.getSite(siteId)
    site.value = response.data
    // console.log('Fetched site:', site.value)
  } catch (error) {
    toast.add({ severity: 'error', summary: t('common.error'), detail: t('siteDetail.fetchError'), life: 3000 })
  }
}

async function fetchLocations() {
  loadingLocations.value = true
  try {
    const response = await api.getLocations({ site_id: siteId })
    locations.value = response.data
          // console.log('Locations fetched:', response.data)
  } catch (error) {
    toast.add({ severity: 'error', summary: t('common.error'), detail: t('siteDetail.fetchLocationsError'), life: 3000 })
  } finally {
    loadingLocations.value = false
  }
}

async function fetchAllContacts() {
  const response = await api.getContacts()
  allContacts.value = response.data.map(mapContact)
}

async function fetchSiteContacts() {
  loadingContacts.value = true
  const response = await api.getSiteContacts(siteId)
  siteContacts.value = response.data.map(mapContact)
  selectedContactIds.value = siteContacts.value.map(c => c.id)
  loadingContacts.value = false
}

async function updateSiteContacts() {
  await api.updateSiteContacts(siteId, selectedContactIds.value)
  await fetchSiteContacts()
}

async function removeContact(contactId) {
  await api.deleteSiteContact(siteId, contactId)
  await fetchSiteContacts()
  selectedContactIds.value = siteContacts.value.map(c => c.id)
}

async function createContact(contactData) {
  // Assumendo che esista api.createContact()
  await api.createContact(contactData)
  showContactDialog.value = false
  await fetchAllContacts()
  await fetchSiteContacts()
}

function mapContact(contact) {
  return { ...contact, fullName: `${contact.first_name} ${contact.last_name}` }
}

async function saveLocation(data) {
  const formData = { ...data, site_id: site.value.id } 

  const request = editingLocation.value?.id
    ? api.updateLocation(editingLocation.value.id, formData)
    : api.createLocation(formData)

  request
    .then(() => {
      toast.add({
        severity: 'success',
        summary: t('common.success'),
        detail: editingLocation.value ? t('siteDetail.locationUpdated') : t('siteDetail.locationCreated'),
        life: 3000
      })
      editLocationDialog.value = false
      editingLocation.value = null
      return fetchLocations()
    })
    .catch(() => {
      toast.add({
        severity: 'error',
        summary: t('common.error'),
        detail: t('siteDetail.saveLocationError'),
        life: 3000
      })
    })
}

const getFloorplanThumbnailUrl = (floorplan) => {
  const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  return `${baseUrl}/locations/${floorplan.location_id}/floorplan/${floorplan.id}`
}

function createNewLocation() {
  editingLocation.value = null
  editLocationDialog.value = true
}

function editLocation(location) {
  editingLocation.value = { ...location }
  editLocationDialog.value = true
}

function goBack() {
  router.back()
}
</script>

<style scoped>
.site-detail-page {
  background: var(--background-color);
  color: var(--text-color);
  padding: 1rem;
}
:deep(.p-card) {
  background: var(--card-bg) !important;
  color: var(--text-color) !important;
  border: 1px solid var(--border-color) !important;
}
</style>
