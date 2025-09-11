# Configurazioni di Deployment

Industrace supporta diverse configurazioni di deployment per adattarsi a vari scenari di sviluppo e produzione.

## 🏗️ Configurazioni Disponibili

### 1. Sviluppo (`make dev`)
**Scopo**: Sviluppo locale con hot-reload
- **Frontend**: http://localhost:5173 (Vite dev server)
- **Backend**: http://localhost:8000 (FastAPI)
- **CORS**: Configurato per localhost
- **Cookies**: Insecure (per sviluppo)
- **Database**: PostgreSQL in container

**Caratteristiche**:
- Hot-reload per frontend e backend
- Debug completo
- CORS permissive per localhost
- Logging dettagliato

### 2. Produzione (`make prod`)
**Scopo**: Produzione con Traefik e HTTPS
- **Frontend**: https://industrace.local (Traefik)
- **Backend**: https://industrace.local/api (Traefik proxy)
- **CORS**: Configurato per dominio di produzione
- **Cookies**: Secure, SameSite=strict
- **Database**: PostgreSQL in container

**Caratteristiche**:
- Traefik come reverse proxy
- HTTPS con certificati Let's Encrypt automatici
- Auto-discovery dei servizi Docker
- Dashboard Traefik su http://localhost:8080
- CORS ristretto al dominio di produzione
- Configurazione di sicurezza ottimizzata

### 3. Custom Certificates (`make custom-certs-start`)
**Scopo**: Produzione con certificati personalizzati
- **Frontend**: https://industrace.local (nginx)
- **Backend**: https://industrace.local/api (nginx proxy)
- **CORS**: Configurato per dominio personalizzato
- **Cookies**: Secure, SameSite=strict
- **Database**: PostgreSQL in container

**Caratteristiche**:
- Certificati SSL personalizzati
- Dominio configurabile
- CORS dinamico basato sul dominio
- Configurazione di sicurezza ottimizzata

## ⚙️ Configurazione CORS

Il sistema gestisce automaticamente le configurazioni CORS in base all'ambiente:

### Sviluppo
```bash
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://localhost:8080
SECURE_COOKIES=false
SAME_SITE_COOKIES=lax
```

### Produzione
```bash
CORS_ORIGINS=https://industrace.local,https://www.industrace.local
SECURE_COOKIES=true
SAME_SITE_COOKIES=strict
```

### Custom Certificates
```bash
CORS_ORIGINS=https://[DOMAIN],https://www.[DOMAIN]
SECURE_COOKIES=true
SAME_SITE_COOKIES=strict
```

## 🚀 Comandi Makefile

### Comandi Base
- `make dev` - Avvia ambiente di sviluppo
- `make prod` - Avvia ambiente di produzione
- `make custom-certs-start` - Avvia con certificati personalizzati
- `make stop` - Ferma tutti i container
- `make clean` - Pulisce il sistema

### Comandi di Configurazione
- `make config` - Mostra informazioni di configurazione
- `make custom-certs-setup` - Configura certificati personalizzati

### Comandi di Gestione
- `make init` - Inizializza sistema con dati demo
- `make demo` - Aggiunge dati demo al sistema esistente
- `make test` - Esegue i test
- `make logs` - Mostra i log

## 🔧 Configurazione Frontend

Il frontend si adatta automaticamente all'ambiente:

### Sviluppo
- `VITE_API_URL=http://localhost:8000`
- Proxy Vite per le API
- Hot-reload abilitato

### Produzione/Custom Certs
- `VITE_API_URL=https://[DOMAIN]`
- Nginx come reverse proxy
- Build ottimizzato per produzione

## 📋 Variabili d'Ambiente

### Backend
- `CORS_ORIGINS` - Origini consentite per CORS
- `SECURE_COOKIES` - Abilita cookie sicuri
- `SAME_SITE_COOKIES` - Configurazione SameSite per cookie
- `DATABASE_URL` - URL del database
- `SECRET_KEY` - Chiave segreta per JWT

### Frontend
- `VITE_API_URL` - URL dell'API backend
- `VITE_APP_TITLE` - Titolo dell'applicazione

## 🛡️ Sicurezza

### Sviluppo
- CORS permissive per localhost
- Cookie non sicuri
- Debug abilitato

### Produzione
- CORS ristretto al dominio
- Cookie sicuri con HTTPS
- Debug disabilitato
- Logging di sicurezza

## 📝 Note

1. **Sviluppo**: Usa sempre `make dev` per lo sviluppo locale
2. **Produzione**: Usa `make prod` per deployment standard
3. **Custom**: Usa `make custom-certs-start` per domini personalizzati
4. **Configurazione**: Usa `make config` per verificare le impostazioni attive

## 🔄 Migrazione tra Ambienti

Per passare da un ambiente all'altro:

1. Ferma l'ambiente corrente: `make stop`
2. Pulisci i file temporanei: `make clean`
3. Avvia il nuovo ambiente: `make [dev|prod|custom-certs-start]`
4. Verifica la configurazione: `make config`
