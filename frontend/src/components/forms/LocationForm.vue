<template>
  <form @submit.prevent="handleSubmit">
    <div class="p-fluid">
      <div class="p-field">
        <label for="name">{{ t('common.name') }}</label>
        <InputText id="name" v-model="form.name" required />
      </div>
      <div class="p-field">
        <label for="code">{{ t('common.code') }}</label>
        <InputText id="code" v-model="form.code" />
      </div>
      <div class="p-field">
        <label for="description">{{ t('common.description') }}</label>
        <Textarea id="description" v-model="form.description" rows="3" />
      </div>
      <div class="p-field">
        <label for="site_id">{{ t('common.site') }}</label>
        <Dropdown
          id="site_id"
          v-model="form.site_id"
          :options="sites"
          optionLabel="name"
          optionValue="id"
          :placeholder="t('common.selectSite')"
          class="w-full"
          :showClear="true"
          @change="onSiteChange"
        />
      </div>
      <div class="p-field">
        <label for="area_id">{{ t('common.area') }}</label>
        <Dropdown
          id="area_id"
          v-model="form.area_id"
          :options="areas"
          optionLabel="name"
          optionValue="id"
          :placeholder="t('common.selectArea')"
          class="w-full"
          :showClear="true"
          :disabled="!form.site_id"
        />
      </div>
      <div class="p-field">
        <label for="notes">{{ t('common.notes') }}</label>
        <Textarea id="notes" v-model="form.notes" rows="4" />
      </div>
      
      <div class="flex justify-content-end gap-2 mt-4">
        <Button :label="t('common.cancel')" class="p-button-text" @click="emit('cancel')" />
        <Button :label="t('common.save')" type="submit" />
      </div>
    </div>
  </form>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Button from 'primevue/button'
import Dropdown from 'primevue/dropdown'

const { t } = useI18n()

const props = defineProps({
  location: {
    type: Object,
    default: null,
  },
  sites: {
    type: Array,
    default: () => []
  },
  areas: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['submit', 'cancel', 'site-changed'])

const form = ref({
  name: '',
  code: '',
  description: '',
  area_id: null,
  notes: '',
  site_id: null
})

watch(
  () => props.location,
  (loc) => {
    if (loc) {
      form.value = {
        name: loc.name || '',
        code: loc.code || '',
        description: loc.description || '',
        notes: loc.notes || '',
        area_id: loc.area_id || null,
        site_id: loc.site_id || null
      }
    } else {
      form.value = {
        name: '',
        code: '',
        description: '',
        notes: '',
        area_id: null,
        site_id: null
      }
    }
  },
  { immediate: true }
)

function onSiteChange() {
  if (form.value.site_id) {
    emit('site-changed', form.value.site_id)
  } else {
    form.value.area_id = null
  }
}

function handleSubmit() {
  emit('submit', { ...form.value })
}
</script>

<style scoped>
.p-field {
  margin-bottom: 1.5rem;
}

.p-dropdown {
  min-height: 2.5rem;
}

.p-dropdown .p-dropdown-label {
  font-size: 1rem;
  padding: 0.75rem 1rem;
}

.p-dropdown .p-dropdown-trigger {
  width: 2.5rem;
}
</style>
