<!--
  - UserDetail.vue
  - Componente per la visualizzazione dei dettagli di un utente
  - Utilizza i componenti PrimeVue per la gestione del form
-->
<template>
  <div class="user-detail-page">
    <div class="page-header">
      <Button icon="pi pi-arrow-left" :label="t('common.back')" class="mb-3" @click="goBack" />
      <h1>{{ t('users.title') }}</h1>
    </div>

    <Card v-if="user" class="mb-4">
      <template #title>{{ user.name }}</template>
      <template #content>
        <div class="grid">
          <div class="col-12 md:col-6">
            <p><strong>{{ t('common.name') }}:</strong> {{ user.name }}</p>
            <p><strong>{{ t('common.email') }}:</strong> {{ user.email }}</p>
            <p><strong>{{ t('users.role') }}:</strong> {{ user.role?.name || t('common.na') }}</p>
            <p><strong>{{ t('common.status') }}:</strong> 
              <Tag :value="user.is_active ? t('common.active') : t('common.inactive')" 
                   :severity="user.is_active ? 'success' : 'danger'" />
            </p>
            <p><strong>{{ t('common.createdAt') }}:</strong> {{ formatDate(user.created_at) }}</p>
            <p><strong>{{ t('users.lastLogin') }}:</strong> {{ user.last_login ? formatDate(user.last_login) : t('common.na') }}</p>
          </div>
        </div>
      </template>
    </Card>

    <div v-if="!user && !loading" class="text-center">
      <p>{{ t('users.userNotFound') }}</p>
    </div>

    <div v-if="loading" class="text-center">
      <ProgressSpinner />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useI18n } from 'vue-i18n'
import api from '../api/api'

import Button from 'primevue/button'
import Card from 'primevue/card'
import Tag from 'primevue/tag'
import ProgressSpinner from 'primevue/progressspinner'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const toast = useToast()

const user = ref(null)
const loading = ref(false)
const userId = route.params.id

function goBack() {
  router.push({ name: 'Users' })
}

function formatDate(dateString) {
  if (!dateString) return t('common.na')
  return new Date(dateString).toLocaleDateString('it-IT', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

async function fetchUser() {
  loading.value = true
  try {
    const response = await api.getUser(userId)
    user.value = response.data
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: t('common.error'),
      detail: t('users.fetchError'),
      life: 3000
    })
    user.value = null
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUser()
})
</script>

<style scoped>
.user-detail-page {
  padding: 1rem;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.page-header h1 {
  margin: 0;
}
</style> 