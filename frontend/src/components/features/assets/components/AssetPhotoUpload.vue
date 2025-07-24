<!--
  - AssetPhotoUpload.vue
  - Componente per la gestione delle foto degli asset
  - Utilizza i componenti PrimeVue per la gestione del form
-->
<template>
  <Card>
    <template #title>{{ t('assetPhotoUpload.title') }}</template>
    <template #content>
      <div> 
        <FileUpload v-if="!readOnly" name="file" :customUpload="true" :multiple="true" :auto="true" accept="image/*"
          :chooseLabel="t('assetPhotoUpload.chooseLabel')" :uploadLabel="t('assetPhotoUpload.uploadLabel')" @uploader="uploadPhotos" />

        <div class="flex flex-wrap gap-3 mt-4">
          <div v-for="photo in photos" :key="photo.id" class="relative">
            <Image :src="getPhotoUrl(photo)" :alt="t('assetPhotoUpload.photo')" width="150" preview />
            <Button v-if="!readOnly" icon="pi pi-trash" class="p-button-rounded p-button-danger p-button-sm absolute top-0 right-0"
              @click="deletePhoto(photo.id)" />
          </div>
        </div>
      </div>
    </template>
  </Card>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { ref, onMounted } from 'vue'
import Image from 'primevue/image'
import Card from 'primevue/card'
import Button from 'primevue/button'
import api from '@/api/api'
import FileUpload from 'primevue/fileupload';
import { useToast } from 'primevue/usetoast'

const { t } = useI18n()

const props = defineProps({ 
  assetId: String,
  readOnly: { type: Boolean, default: false }
})
const toast = useToast()
const photos = ref([])

const fetchPhotos = async () => {
  try {
    const res = await api.getAsset(props.assetId)
    photos.value = res.data.photos || []
  } catch (err) {
    toast.add({ severity: 'error', summary: t('common.error'), detail: t('assetPhotoUpload.fetchError') })
  }
}

const uploadPhotos = async ({ files }) => {
  try {
    for (const file of files) {
      const formData = new FormData()
      formData.append('file', file)
      await api.uploadAssetPhoto(props.assetId, formData)
    }
    await fetchPhotos()
    toast.add({ severity: 'success', summary: t('assetPhotoUpload.photosUploaded') })
  } catch (err) {
    
    toast.add({ severity: 'error', summary: t('common.error'), detail: t('assetPhotoUpload.uploadError') })
  }
}

const deletePhoto = async (photoId) => {
  try {
    await api.deleteAssetPhoto(props.assetId, photoId)
    toast.add({ severity: 'success', summary: t('assetPhotoUpload.photoDeleted') })
    await fetchPhotos()
  } catch (err) {
    toast.add({ severity: 'error', summary: t('common.error'), detail: t('assetPhotoUpload.deleteError') })
  }
}


const getPhotoUrl = (photo) => {
  return `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/assets/${props.assetId}/photos/${photo.id}`
}

onMounted(fetchPhotos)
</script> 