// Configurazione dell'applicazione
export const appConfig = {
  // Versione dell'applicazione
  version: '1.0.0',
  
  // Nome dell'applicazione
  name: 'Industrace',
  
  // Descrizione
  description: 'Configuration Management Database for Industrial Control Systems',
  
  // Informazioni sul copyright
  copyright: {
    company: 'BeSafe',
    year: '2024',
    url: 'https://www.besafe.it'
  },
  
  // Link utili
  links: {
    website: 'https://www.besafe.it',
    github: 'https://github.com/besafe/industrace',
    issues: 'https://github.com/besafe/industrace/issues',
    license: 'https://github.com/besafe/industrace/blob/main/LICENSE'
  },
  
  // Configurazione API
  api: {
    baseUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    timeout: 30000
  },
  
  // Configurazione paginazione
  pagination: {
    defaultPageSize: 25,
    pageSizeOptions: [10, 25, 50, 100]
  },
  
  // Configurazione upload
  upload: {
    maxFileSize: 10 * 1024 * 1024, // 10MB
    allowedTypes: ['image/*', 'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
  }
}

export default appConfig 