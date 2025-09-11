import { createI18n } from 'vue-i18n'

// Import translations directly
import enCommon from './en/common.json'
import enAssets from './en/assets.json'
import enUsers from './en/users.json'
import enSites from './en/sites.json'
import enSuppliers from './en/suppliers.json'
import enSetup from './en/setup.json'
import enForms from './en/forms.json'
import enMenu from './en/menu.json'
import enErrors from './en/errors.json'
import enDashboard from './en/dashboard.json'

// Import English asset-related translation files
import enAssetConnections from './en/assetConnections.json'
import enAssetCommunications from './en/assetCommunications.json'
import enAssetCustomFields from './en/assetCustomFields.json'
import enAssetPhotoUpload from './en/assetPhotoUpload.json'
import enAssetDocumentUpload from './en/assetDocumentUpload.json'
import enAssetSuppliersTab from './en/assetSuppliersTab.json'
import enAssetTimeline from './en/assetTimeline.json'
import enAssetDetail from './en/assetDetail.json'
import enRiskBreakdown from './en/riskBreakdown.json'
import enAssetForm from './en/assetForm.json'
import enUtility from './en/utility.json'
import enAuditLogs from './en/auditLogs.json'
import enProfile from './en/profile.json'
import enRoles from './en/roles.json'
import enRoleForm from './en/roleForm.json'
import enPermissions from './en/permissions.json'
import enPrint from './en/print.json'
import enLogin from './en/login.json'
import enNetworkMap from './en/networkMap.json'
import enFloorplanPositioning from './en/floorplanPositioning.json'

// Import new English translation files
import enLocations from './en/locations.json'
import enAssetTypes from './en/assettypes.json'
import enAssetStatuses from './en/assetstatuses.json'
import enManufacturers from './en/manufacturers.json'
import enContacts from './en/contacts.json'
import enDocuments from './en/documents.json'
import enInterfaces from './en/interfaces.json'
import enAreas from './en/areas.json'

import itCommon from './it/common.json'
import itAssets from './it/assets.json'
import itUsers from './it/users.json'
import itSites from './it/sites.json'
import itSuppliers from './it/suppliers.json'
import itSetup from './it/setup.json'
import itForms from './it/forms.json'
import itMenu from './it/menu.json'
import itErrors from './it/errors.json'
import itDashboard from './it/dashboard.json'
import itLocations from './it/locations.json'
import itAssetTypes from './it/assettypes.json'
import itAssetStatuses from './it/assetstatuses.json'
import itManufacturers from './it/manufacturers.json' 
import itContacts from './it/contacts.json'
import itDocuments from './it/documents.json'
import itInterfaces from './it/interfaces.json'
import itAreas from './it/areas.json'
import itUtility from './it/utility.json'
import itAuditLogs from './it/auditLogs.json'
import itProfile from './it/profile.json'
import itRoles from './it/roles.json'
import itRoleForm from './it/roleForm.json'
import itPermissions from './it/permissions.json'
import itPrint from './it/print.json'
import itLogin from './it/login.json'
import itNetworkMap from './it/networkMap.json'
import itFloorplanPositioning from './it/floorplanPositioning.json'

// Import new asset-related translation files
import itAssetConnections from './it/assetConnections.json'
import itAssetCommunications from './it/assetCommunications.json'
import itAssetCustomFields from './it/assetCustomFields.json'
import itAssetPhotoUpload from './it/assetPhotoUpload.json'
import itAssetDocumentUpload from './it/assetDocumentUpload.json'
import itAssetSuppliersTab from './it/assetSuppliersTab.json'
import itAssetTimeline from './it/assetTimeline.json'
import itAssetDetail from './it/assetDetail.json'
import itRiskBreakdown from './it/riskBreakdown.json'
import itAssetForm from './it/assetForm.json'

// Helper function to flatten nested objects
const flattenObject = (obj, prefix = '') => {
  const flattened = {}
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      const newKey = prefix ? `${prefix}.${key}` : key
      if (typeof obj[key] === 'object' && obj[key] !== null && !Array.isArray(obj[key])) {
        Object.assign(flattened, flattenObject(obj[key], newKey))
      } else {
        flattened[newKey] = obj[key]
      }
    }
  }
  return flattened
}

// Load all translation files with flattened structure
const messages = {
  en: flattenObject({
    common: enCommon,
    assets: enAssets,
    users: enUsers,
    sites: enSites,
    suppliers: enSuppliers,
    setup: enSetup,
    forms: enForms,
    menu: enMenu,
    errors: enErrors,
    dashboard: enDashboard,
    locations: enLocations,
    assettypes: enAssetTypes,
    assetstatuses: enAssetStatuses,
    manufacturers: enManufacturers,
    contacts: enContacts,
    documents: enDocuments,
    interfaces: enInterfaces,
    areas: enAreas,
    assetConnections: enAssetConnections,
    assetCommunications: enAssetCommunications,
    assetCustomFields: enAssetCustomFields,
    assetPhotoUpload: enAssetPhotoUpload,
    assetDocumentUpload: enAssetDocumentUpload,
    assetSuppliersTab: enAssetSuppliersTab,
    assetTimeline: enAssetTimeline,
    assetDetail: enAssetDetail,
    riskBreakdown: enRiskBreakdown,
    assetForm: enAssetForm,
    utility: enUtility,
    auditLogs: enAuditLogs,
    profile: enProfile,
    roles: enRoles,
    roleForm: enRoleForm,
    permissions: enPermissions,
    print: enPrint,
    login: enLogin,
    networkMap: enNetworkMap,
    floorplanPositioning: enFloorplanPositioning
  }),
  it: flattenObject({
    common: itCommon,
    assets: itAssets,
    users: itUsers,
    sites: itSites,
    suppliers: itSuppliers,
    setup: itSetup,
    forms: itForms,
    menu: itMenu,
    errors: itErrors,
    dashboard: itDashboard,
    locations: itLocations,
    assettypes: itAssetTypes,
    assetstatuses: itAssetStatuses,
    manufacturers: itManufacturers,
    contacts: itContacts,
    documents: itDocuments,
    interfaces: itInterfaces,
    areas: itAreas,
    assetConnections: itAssetConnections,
    assetCommunications: itAssetCommunications,
    assetCustomFields: itAssetCustomFields,
    assetPhotoUpload: itAssetPhotoUpload,
    assetDocumentUpload: itAssetDocumentUpload,
    assetSuppliersTab: itAssetSuppliersTab,
    assetTimeline: itAssetTimeline,
    assetDetail: itAssetDetail,
    riskBreakdown: itRiskBreakdown,
    assetForm: itAssetForm,
    utility: itUtility,
    auditLogs: itAuditLogs,
    profile: itProfile,
    roles: itRoles,
    roleForm: itRoleForm,
    permissions: itPermissions,
    print: itPrint,
    login: itLogin,
    networkMap: itNetworkMap,
    floorplanPositioning: itFloorplanPositioning
  })
}

// Get user's preferred language from localStorage or browser
const getUserLanguage = () => {
  if (typeof localStorage !== 'undefined') {
    const savedLang = localStorage.getItem('user-lang')
    if (savedLang && messages[savedLang]) {
      return savedLang
    }
  }
  
  // Try to detect browser language
  if (typeof navigator !== 'undefined' && navigator.language) {
    const browserLang = navigator.language.split('-')[0] // Get primary language code
    if (messages[browserLang]) {
      return browserLang
    }
  }
  
  // Default to Italian for this project
  return 'it'
}


// Create i18n instance
export const i18n = createI18n({
  legacy: false,
  locale: getUserLanguage(),
  fallbackLocale: 'en',
  messages,
  globalInjection: true,
  silentTranslationWarn: process.env.NODE_ENV === 'production',
  missingWarn: false,
  fallbackWarn: false
})

// Initialize i18n for Node.js environment (for testing)
async function initializeI18n() {
  // In browser environment, i18n is already initialized
  return i18n
}

// Function to change language
export const changeLanguage = (locale) => {
  if (messages[locale]) {
    i18n.global.locale.value = locale
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem('user-lang', locale)
    }
  }
}

// Function to get available languages
export const getAvailableLanguages = () => {
  return Object.keys(messages).map(lang => ({
    code: lang,
    name: lang === 'en' ? 'English' : lang === 'it' ? 'Italiano' : lang
  }))
}

// Function to get current language
export const getCurrentLanguage = () => {
  return i18n.global.locale.value
}

// Function to check if a translation key exists
export const hasTranslation = (key, locale = null) => {
  const currentLocale = locale || i18n.global.locale.value
  const keys = key.split('.')
  let obj = messages[currentLocale]
  
  for (const k of keys) {
    if (obj && typeof obj === 'object' && k in obj) {
      obj = obj[k]
    } else {
      return false
    }
  }
  
  return true
}

// Function to get translation without fallback
export const getTranslation = (key, locale = null) => {
  const currentLocale = locale || i18n.global.locale.value
  const keys = key.split('.')
  let obj = messages[currentLocale]
  
  for (const k of keys) {
    if (obj && typeof obj === 'object' && k in obj) {
      obj = obj[k]
    } else {
      return null
    }
  }
  
  return obj
}

// Function to validate translation completeness
export const validateTranslations = () => {
  const issues = []
  const languages = Object.keys(messages)
  
  if (languages.length < 2) {
    issues.push('At least two languages are required')
    return issues
  }
  
  const baseLang = 'en'
  const baseKeys = getAllKeys(messages[baseLang])
  
  languages.forEach(lang => {
    if (lang === baseLang) return
    
    const langKeys = getAllKeys(messages[lang])
    const missingKeys = baseKeys.filter(key => !langKeys.includes(key))
    const extraKeys = langKeys.filter(key => !baseKeys.includes(key))
    
    if (missingKeys.length > 0) {
      issues.push(`Missing translations in ${lang}: ${missingKeys.join(', ')}`)
    }
    
    if (extraKeys.length > 0) {
      issues.push(`Extra translations in ${lang}: ${extraKeys.join(', ')}`)
    }
  })
  
  return issues
}

// Helper function to get all keys from an object
const getAllKeys = (obj, prefix = '') => {
  const keys = []
  
  for (const key in obj) {
    const newKey = prefix ? `${prefix}.${key}` : key
    if (typeof obj[key] === 'object' && obj[key] !== null) {
      keys.push(...getAllKeys(obj[key], newKey))
    } else {
      keys.push(newKey)
    }
  }
  
  return keys
}

export { initializeI18n }
export default i18n 