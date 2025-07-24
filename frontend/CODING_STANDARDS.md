# Standard di Coding Frontend

## 📋 Overview

This document definisce gli standard di coding per il frontend Vue.js del CMDB, garantendo coerenza, manutenibilità e qualità del codice.

##  Architecture

### Standard Composables 

#### `useApi()`
Gestisce le chiamate API con loading, errori e toast automatici.

```javascript
import { useApi } from '../composables/useApi'

const { loading, error, data, execute } = useApi()

// Uso
await execute(async () => {
  const response = await api.getAssets()
  return response
}, {
  successMessage: t('assets.fetched'),
  errorContext: t('assets.fetchError')
})
```

#### `useForm()`
Gestisce form con validazione e gestione errori.

```javascript
import { useForm } from '../composables/useForm'

const { form, errors, isSubmitting, isValid, submit } = useForm(initialData)

// Uso
await submit(async (formData) => {
  await api.createAsset(formData)
}, {
  successMessage: t('assets.created'),
  errorContext: t('assets.createError')
})
```

#### `useFilters()`
Gestisce filtri, ricerca e ordinamento con persistenza.

```javascript
import { useFilters } from '../composables/useFilters'

const { filters, globalSearch, filterData, getApiParams } = useFilters(
  initialFilters, 
  'storageKey'
)
```

#### `useDialog()`
Gestisce dialog e modali con modalità create/edit/view.

```javascript
import { useDialog } from '../composables/useDialog'

const { isVisible, data, openCreate, openEdit, close } = useDialog()

// Uso
openCreate(t('assets.new'))
openEdit(t('assets.edit'), assetData)
```

#### `useConfirm()`
Gestisce conferme per azioni distruttive.

```javascript
import { useConfirm } from '../composables/useConfirm'

const { confirmDelete, confirmBulkAction } = useConfirm()

// Uso
confirmDelete(asset, asset.name, deleteAsset)
confirmBulkAction(selectedAssets, 'delete', bulkDelete)
```

### Componenti Base

#### `BaseDataTable.vue`
Tabella standardizzata con filtri, ordinamento, esportazione.

```vue
<BaseDataTable
  :data="assets"
  :loading="loading"
  :columns="columns"
  :filters="filters"
  :global-filter-fields="['name', 'ip_address']"
  storage-key="assets"
  @selection-change="onSelectionChange"
>
  <template #actions>
    <Button label="Nuovo" @click="openCreate" />
  </template>
</BaseDataTable>
```

#### `BaseForm.vue`
Form standardizzato con validazione e gestione errori.

```vue
<BaseForm
  :is-submitting="isSubmitting"
  :is-valid="isValid"
  :errors="errors"
  @submit="handleSubmit"
  @cancel="handleCancel"
>
  <!-- Campi del form -->
</BaseForm>
```

#### `BaseDialog.vue`
Dialog standardizzato con modalità create/edit/view.

```vue
<BaseDialog
  v-model:is-visible="showDialog"
  :title="title"
  :mode="mode"
  :is-submitting="isSubmitting"
  :is-valid="isValid"
  @submit="handleSubmit"
  @cancel="handleCancel"
>
  <!-- Contenuto del dialog -->
</BaseDialog>
```

#### `BaseConfirmDialog.vue`
Dialog di conferma standardizzato.

```vue
<BaseConfirmDialog
  :show-confirm-dialog="showConfirmDialog"
  :confirm-data="confirmData"
  :is-executing="isExecuting"
  @execute="executeConfirmedAction"
  @close="closeConfirmDialog"
/>
```

## 📝 Convenzioni di Naming

### File e Cartelle
- **Componenti**: PascalCase (`AssetForm.vue`)
- **Composables**: camelCase (`useApi.js`)
- **Utility**: camelCase (`validation.js`)
- **Costanti**: UPPER_SNAKE_CASE (`API_ENDPOINTS.js`)

### Variabili e Funzioni
- **Variabili**: camelCase (`assetData`, `isLoading`)
- **Funzioni**: camelCase (`fetchAssets`, `handleSubmit`)
- **Costanti**: UPPER_SNAKE_CASE (`DEFAULT_PAGE_SIZE`)
- **Props**: kebab-case (`:is-visible`, `:asset-data`)

### Eventi
- **Emit**: camelCase (`@submit`, `@selection-change`)
- **Handler**: camelCase con prefisso (`handleSubmit`, `onSelectionChange`)

## 🎯 Pattern Standardizzati

### Gestione API
```javascript
// ✅ Corretto
const { loading, execute } = useApi()

await execute(async () => {
  const response = await api.getAssets(params)
  assets.value = response.data
  return response
}, {
  successMessage: t('assets.fetched'),
  errorContext: t('assets.fetchError'),
  showToast: true
})

// ❌ Sbagliato
const loading = ref(false)
try {
  loading.value = true
  const response = await api.getAssets()
  assets.value = response.data
} catch (error) {
  toast.add({ severity: 'error', detail: 'Errore' })
} finally {
  loading.value = false
}
```

### Gestione Form
```javascript
// ✅ Corretto
const { form, errors, isSubmitting, submit } = useForm(initialData)

await submit(async (formData) => {
  await api.createAsset(formData)
}, {
  successMessage: t('assets.created'),
  errorContext: t('assets.createError')
})

// ❌ Sbagliato
const form = ref({})
const errors = ref({})
const isSubmitting = ref(false)

async function handleSubmit() {
  isSubmitting.value = true
  try {
    await api.createAsset(form.value)
    toast.add({ severity: 'success', detail: 'Creato' })
  } catch (error) {
    errors.value = error.response?.data?.errors || {}
  } finally {
    isSubmitting.value = false
  }
}
```

### Gestione Filtri
```javascript
// ✅ Corretto
const { filters, filterData, getApiParams } = useFilters(initialFilters, 'assets')

const filteredAssets = computed(() => 
  filterData(assets.value, ['name', 'ip_address', 'site.name'])
)

// ❌ Sbagliato
const filters = ref({})
const globalSearch = ref('')

const filteredAssets = computed(() => {
  let filtered = assets.value
  if (globalSearch.value) {
    filtered = filtered.filter(asset => 
      asset.name.includes(globalSearch.value)
    )
  }
  return filtered
})
```

## 🎨 Styling

### CSS Classes
- **Utility**: Tailwind-like (`flex`, `gap-2`, `mb-3`)
- **Componenti**: BEM-like (`.base-form`, `.base-form__field`)
- **Stati**: Modificatori (`.p-invalid`, `.p-disabled`)

### CSS Variables
```css
:root {
  --primary-color: #1976d2;
  --surface-border: #dee2e6;
  --surface-hover: #f8f9fa;
  --red-500: #dc3545;
  --green-500: #28a745;
}
```

## 🔧 Configurazione

### Vite
```javascript
// vite.config.js
export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5173,
  },
  optimizeDeps: {
    include: ['vis-network']
  }
})
```

### ESLint (se aggiunto)
```javascript
// .eslintrc.js
module.exports = {
  extends: [
    '@vue/eslint-config-typescript',
    'plugin:vue/vue3-essential'
  ],
  rules: {
    'vue/multi-word-component-names': 'off',
    'vue/no-unused-vars': 'error'
  }
}
```

## 📚 Struttura Progetto

```
frontend/
├── src/
│   ├── components/
│   │   ├── base/           # Componenti base standardizzati
│   │   │   ├── BaseDataTable.vue
│   │   │   ├── BaseForm.vue
│   │   │   ├── BaseDialog.vue
│   │   │   └── BaseConfirmDialog.vue
│   │   └── ...             # Componenti specifici
│   ├── composables/        # Composables standardizzati
│   │   ├── useApi.js
│   │   ├── useForm.js
│   │   ├── useFilters.js
│   │   ├── useDialog.js
│   │   └── useConfirm.js
│   ├── pages/              # Pagine dell'applicazione
│   ├── api/                # Layer API
│   ├── store/              # State management (Pinia)
│   ├── locales/            # Internazionalizzazione
│   └── assets/             # Risorse statiche
├── package.json
├── vite.config.js
└── CODING_STANDARDS.md
```

## 🚀 Best Practices

### Performance
- Usa `computed` per calcoli derivati
- Usa `v-memo` per componenti pesanti
- Lazy loading per componenti non critici
- Debounce per ricerche e filtri

### Accessibilità
- Usa `aria-label` per elementi senza testo
- Usa `role` appropriati per elementi interattivi
- Supporta navigazione da tastiera
- Contrasto colori adeguato

### Sicurezza
- Sanitizza input utente
- Valida dati lato client e server
- Usa HTTPS in produzione
- Non esporre informazioni sensibili

### Testing (se implementato)
```javascript
// Esempio test componente
import { mount } from '@vue/test-utils'
import AssetForm from '../components/AssetForm.vue'

describe('AssetForm', () => {
  it('emits submit with form data', async () => {
    const wrapper = mount(AssetForm)
    await wrapper.find('form').trigger('submit')
    expect(wrapper.emitted('submit')).toBeTruthy()
  })
})
```

## 🔄 Processo di Refactoring

1. **Identifica** componenti non standardizzati
2. **Crea** composables per logica comune
3. **Refactor** componenti per usare composables
4. **Testa** funzionalità dopo refactoring
5. **Documenta** cambiamenti

## 📖 Risorse

- [Vue 3 Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)
- [PrimeVue Documentation](https://primevue.org/)
- [Vite Documentation](https://vitejs.dev/)
- [Pinia Documentation](https://pinia.vuejs.org/)

---

**Nota**: Questo documento è in evoluzione. Aggiorna quando aggiungi nuovi pattern o standard. 