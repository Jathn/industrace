import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/store/auth'
import api from '@/api/api'

export function useGlobalSearch() {
  const router = useRouter()
  const toast = useToast()
  const auth = useAuthStore()
  
  const searchQuery = ref('')
  const searchResults = ref([])
  const isLoading = ref(false)
  const isVisible = ref(false)
  
  const hasResults = computed(() => searchResults.value.length > 0)
  
  const search = async (query) => {
    if (!query || query.trim().length < 2) {
      searchResults.value = []
      return
    }
    
    // Verifica che l'utente sia autenticato
    if (!auth.isAuthenticated) {
      toast.add({
        severity: 'warn',
        summary: 'Attenzione',
        detail: 'Devi essere autenticato per utilizzare la ricerca',
        life: 3000
      })
      return
    }
    
    isLoading.value = true
    
    try {
      const response = await api.globalSearch(query.trim(), 5)
      searchResults.value = response.data.results || []
    } catch (error) {
      console.error('Errore durante la ricerca:', error)
      toast.add({
        severity: 'error',
        summary: 'Errore',
        detail: 'Errore durante la ricerca',
        life: 3000
      })
      searchResults.value = []
    } finally {
      isLoading.value = false
    }
  }
  
  const handleSearch = async () => {
    if (searchQuery.value.trim()) {
      await search(searchQuery.value)
    }
  }
  
  const handleResultClick = (result) => {
    router.push(result.url)
    isVisible.value = false
    searchQuery.value = ''
    searchResults.value = []
  }
  
  const handleKeydown = (event) => {
    if (event.key === 'Enter' && searchQuery.value.trim()) {
      handleSearch()
    } else if (event.key === 'Escape') {
      isVisible.value = false
      searchQuery.value = ''
      searchResults.value = []
    }
  }
  
  const openSearch = () => {
    isVisible.value = true
    // Focus sull'input dopo che il dialog è aperto
    setTimeout(() => {
      const input = document.querySelector('.global-search-input')
      if (input) {
        input.focus()
      }
    }, 100)
  }
  
  const closeSearch = () => {
    isVisible.value = false
    searchQuery.value = ''
    searchResults.value = []
  }
  
  return {
    searchQuery,
    searchResults,
    isLoading,
    isVisible,
    hasResults,
    search,
    handleSearch,
    handleResultClick,
    handleKeydown,
    openSearch,
    closeSearch
  }
} 