<!--
  - SidebarMenu.vue
  - Componente per la sidebar del menu
  - Utilizza PanelMenu per la gestione del menu
  - Utilizza router per la navigazione tra le pagine
  - Utilizza i18n per la gestione delle lingue
-->
<template>
  <nav :class="['modern-sidebar', { collapsed }]">
    <div class="sidebar-header">
      <img src="/src/assets/industrace_square.png" alt="Industrace" class="logo" v-if="!collapsed" />
      <button class="collapse-btn" @click="collapsed = !collapsed">
        <i :class="collapsed ? 'pi pi-angle-right' : 'pi pi-angle-left'"></i>
      </button>
    </div>
    <div class="sidebar-sections">
      <div v-for="section in menuSections" :key="section.label" class="sidebar-section">
        <div class="section-title" v-if="!collapsed">{{ section.label }}</div>
        <router-link v-for="item in section.items" :key="item.label" :to="item.to" class="sidebar-link" :title="item.label">
          <i :class="['pi', item.icon, 'sidebar-icon']"></i>
          <span v-if="!collapsed">{{ item.label }}</span>
        </router-link>
      </div>
    </div>
    <div class="sidebar-lang" v-if="!collapsed">
      <span class="lang-flag" v-if="locale === 'it'">🇮🇹</span>
      <span class="lang-flag" v-else>🇬🇧</span>
      <select v-model="locale" @change="changeLocale" class="lang-select">
        <option value="it">Italiano</option>
        <option value="en">English</option>
      </select>
    </div>
    <div class="sidebar-logout">
      <router-link to="/logout" class="sidebar-link logout-link" :title="t('menu.logout')">
        <i class="pi pi-sign-out sidebar-icon"></i>
        <span v-if="!collapsed">{{ t('menu.logout') }}</span>
      </router-link>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { usePermissions } from '@/composables/usePermissions'
import { useAuthStore } from '@/store/auth'

const { t, locale } = useI18n()
const router = useRouter()
const collapsed = ref(false)
const { canRead, userPermissions, accessibleSections, refreshUserPermissions } = usePermissions()
const authStore = useAuthStore()

const menuSections = computed(() => {
  const sections = []

  // Sezione Management
  const managementItems = []
  if (canRead('assets')) managementItems.push({ label: t('menu.assets'), icon: 'pi-server', to: '/assets' })
  if (canRead('asset_types')) managementItems.push({ label: t('menu.assettypes'), icon: 'pi-tags', to: '/asset-types' })
  if (canRead('asset_statuses')) managementItems.push({ label: t('menu.assetstatuses'), icon: 'pi-list', to: '/asset-statuses' })
  
  if (managementItems.length > 0) {
    sections.push({
      label: t('menu.section.management'),
      items: managementItems
    })
  }

  // Sezione Registry
  const registryItems = []
  if (canRead('sites')) registryItems.push({ label: t('menu.sites'), icon: 'pi-building', to: '/sites' })
  
  if (canRead('areas')) registryItems.push({ label: t('menu.areas'), icon: 'pi-sitemap', to: '/areas' })
  
  if (canRead('locations')) registryItems.push({ label: t('menu.locations'), icon: 'pi-map', to: '/locations' })
  if (canRead('suppliers')) registryItems.push({ label: t('menu.suppliers'), icon: 'pi-briefcase', to: '/suppliers' })
  if (canRead('manufacturers')) registryItems.push({ label: t('menu.manufacturers'), icon: 'pi-cog', to: '/manufacturers' })
  if (canRead('contacts')) registryItems.push({ label: t('contacts.title'), icon: 'pi-id-card', to: '/contacts' })
  
  if (registryItems.length > 0) {
    sections.push({
      label: t('menu.section.registry'),
      items: registryItems
    })
  }

  // Sezione Users
  const usersItems = []
  if (canRead('users')) usersItems.push({ label: t('menu.users'), icon: 'pi-users', to: '/users' })
  if (canRead('users')) usersItems.push({ label: t('menu.roles'), icon: 'pi-key', to: '/roles' })
  
  if (usersItems.length > 0) {
    sections.push({
      label: t('menu.section.users'),
      items: usersItems
    })
  }

  // Sezione Utility
  const utilityItems = []
  utilityItems.push({ label: t('menu.dashboard'), icon: 'pi-chart-bar', to: '/' }) // Dashboard sempre visibile
  utilityItems.push({ label: t('menu.networkMap'), icon: 'pi-sitemap', to: '/network-map' }) // Mappa di rete
  utilityItems.push({ label: t('profile.title'), icon: 'pi-user', to: '/profile' }) // Profilo sempre visibile
  if (canRead('utility')) utilityItems.push({ label: t('menu.pcap'), icon: 'pi-upload', to: '/utility' })
  if (canRead('audit_logs')) utilityItems.push({ label: t('auditLogs.title'), icon: 'pi-history', to: '/audit-logs' })
  
  if (utilityItems.length > 0) {
    sections.push({
      label: t('menu.section.utility'),
      items: utilityItems
    })
  }

  // Sezione Setup (solo per admin)
  if (canRead('users')) {
    sections.push({
      label: t('menu.section.setup'),
      items: [
        { label: t('menu.setup'), icon: 'pi-wrench', to: '/setup' }
      ]
    })
  }

  return sections
})

function changeLocale(e) {
  locale.value = e.target.value
}
</script>

<style scoped>
.modern-sidebar {
  width: 260px;
  min-height: 100vh;
  background: #23272f;
  color: #fff;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: width 0.2s;
  border-right: 1px solid #23272f;
}
.modern-sidebar.collapsed {
  width: 70px;
}
.sidebar-header {
  display: flex;
  align-items: center;
  padding: 1.2rem 1rem 1rem 1rem;
  gap: 0.7rem;
  border-bottom: 1px solid #2d323c;
}
.logo {
  width: 150px;
  height: 150px;
}
.app-title {
  font-size: 1.3rem;
  font-weight: bold;
  letter-spacing: 1px;
}
.collapse-btn {
  background: none;
  border: none;
  color: #fff;
  margin-left: auto;
  font-size: 1.2rem;
  cursor: pointer;
}
.sidebar-sections {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-top: 1.5rem;
}
.sidebar-section {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}
.section-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #b0b4bb;
  margin: 0 0 0.5rem 1.2rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.sidebar-link {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.7rem 1.2rem;
  color: #fff;
  text-decoration: none;
  border-radius: 6px;
  transition: background 0.15s, color 0.15s;
  font-size: 1.05rem;
}
.sidebar-link:hover, .sidebar-link.router-link-exact-active {
  background: #3a4050;
  color: #ffd700;
}
.sidebar-icon {
  font-size: 1.3rem;
  min-width: 1.3rem;
  text-align: center;
}
.sidebar-lang {
  padding: 0 1rem 2rem 1rem;
  margin-top: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.7rem;
}
.lang-select {
  width: 100%;
  padding: 0.4rem 0.7rem;
  border-radius: 6px;
  border: 1px solid #2d323c;
  background: #23272f;
  color: #fff;
  font-size: 1rem;
}
.lang-flag {
  font-size: 1.2rem;
  margin-right: 0.4rem;
}
.sidebar-logout {
  margin-bottom: 1.5rem;
  padding: 0 1rem;
}
.logout-link {
  color: #ff7675;
}
.logout-link:hover {
  background: #2d323c;
  color: #fff;
}

.modern-sidebar.collapsed .app-title,
.modern-sidebar.collapsed .section-title,
.modern-sidebar.collapsed .sidebar-link span {
  display: none;
}
.modern-sidebar.collapsed .sidebar-link {
  justify-content: center;
  padding-left: 0.5rem;
  padding-right: 0.5rem;
}
</style> 