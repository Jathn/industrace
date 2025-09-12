# Industrace Development Makefile
# ===============================

.PHONY: help init clean demo test dev prod

# Default target
help:
	@echo "🏭 Industrace Development Commands"
	@echo "=================================="
	@echo ""
	@echo "📋 Available commands:"
	@echo "  make init      - Initialize system with demo data (clean start)"
	@echo "  make demo      - Add demo data to existing system"
	@echo "  make clean     - Clean system completely"
	@echo "  make dev       - Start development environment (localhost:5173/8000)"
	@echo "  make prod      - Start production environment (HTTPS with Traefik)"
	@echo "  make test      - Run tests"
	@echo "  make logs      - Show logs"
	@echo "  make stop      - Stop all containers"
	@echo "  make config    - Show configuration information"
	@echo "  make traefik   - Show Traefik dashboard information"
	@echo "  make create-tenant - Create new tenant (see usage below)"
	@echo "  make create-tenant-default - Create tenant with default values"
	@echo ""
	@echo "🔐 Custom Certificates:"
	@echo "  make custom-certs-setup - Setup custom certificates deployment"
	@echo "  make custom-certs-start - Start with custom certificates"
	@echo "  make custom-certs-stop  - Stop custom certificates deployment"
	@echo "  make custom-certs-logs  - Show custom certificates logs"
	@echo ""
	@echo "🏗️  Tenant Management:"
	@echo "  make create-tenant TENANT_NAME=\"My Company\" TENANT_SLUG=\"my-company\" ADMIN_EMAIL=\"admin@mycompany.com\" ADMIN_PASSWORD=\"pass\""
	@echo "  make reset-admin-password TENANT_SLUG=\"my-company\" ADMIN_EMAIL=\"admin@mycompany.com\""
	@echo "  make list-tenants - List all available tenants"
	@echo "  make list-admins TENANT_SLUG=\"my-company\" - List admin users in tenant"
	@echo ""

# Initialize system with demo data
init:
	@echo "🚀 Initializing Industrace system..."
	docker-compose -f docker-compose.dev.yml up -d
	@echo "⏳ Waiting for services to start..."
	sleep 10
	@echo "📊 Running database migrations..."
	docker-compose -f docker-compose.dev.yml exec backend alembic upgrade head
	@echo "🌱 Seeding demo data..."
	docker-compose -f docker-compose.dev.yml exec backend python -m app.init_demo_data
	@echo "✅ System initialized successfully!"

# Add demo data to existing system
demo:
	@echo "🌱 Adding demo data to existing system..."
	docker-compose -f docker-compose.dev.yml exec backend python -m app.init_demo_data
	@echo "✅ Demo data added successfully!"

# Clean system completely
clean:
	@echo "🧹 Cleaning Industrace system..."
	docker-compose -f docker-compose.dev.yml down -v
	docker-compose down -v
	docker system prune -f
	@echo "🧹 Cleaning temporary files..."
	@rm -f .env.dev .env.prod .env.custom
	@echo "✅ System cleaned successfully"

# Clean everything including images
clean-all:
	@echo "🧹 Cleaning everything..."
	docker-compose -f docker-compose.dev.yml down -v --rmi all
	docker-compose down -v --rmi all
	docker system prune -af
	@echo "✅ Everything cleaned successfully"

# Start development environment
dev:
	@echo "🔧 Starting development environment..."
	@echo "📝 Setting CORS for development (localhost:5173)..."
	@echo "CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://localhost:8080" > .env.dev
	@echo "VITE_API_URL=http://localhost:8000" >> .env.dev
	docker-compose -f docker-compose.dev.yml --env-file .env.dev up -d
	@echo "✅ Development environment started!"
	@echo "🌐 Frontend: http://localhost:5173"
	@echo "🌐 Backend:  http://localhost:8000"

# Start production environment
prod:
	@echo "🚀 Starting production environment..."
	@echo "📝 Setting CORS for production (HTTPS)..."
	@echo "CORS_ORIGINS=https://industrace.local,https://www.industrace.local" > .env.prod
	@echo "SECURE_COOKIES=true" >> .env.prod
	@echo "SAME_SITE_COOKIES=strict" >> .env.prod
	docker-compose --env-file .env.prod up -d
	@echo "✅ Production environment started!"
	@echo "🌐 Access your application at: https://industrace.local"

# Run tests
test:
	@echo "🧪 Running tests..."
	docker-compose -f docker-compose.dev.yml exec backend pytest

# Show logs
logs:
	@echo "📋 Showing logs..."
	docker-compose -f docker-compose.dev.yml logs -f

# Show backend logs only
logs-backend:
	@echo "📋 Showing backend logs..."
	docker-compose -f docker-compose.dev.yml logs -f backend

# Show frontend logs only
logs-frontend:
	@echo "📋 Showing frontend logs..."
	docker-compose -f docker-compose.dev.yml logs -f frontend

# Stop all containers
stop:
	@echo "🛑 Stopping all containers..."
	docker-compose -f docker-compose.dev.yml down
	docker-compose down

# Build images
build:
	@echo "🔨 Building images..."
	docker-compose -f docker-compose.dev.yml build

# Rebuild images (no cache)
rebuild:
	@echo "🔨 Rebuilding images (no cache)..."
	docker-compose -f docker-compose.dev.yml build --no-cache

# Check system status
status:
	@echo "📊 System status:"
	docker-compose -f docker-compose.dev.yml ps

# Access backend shell
shell:
	@echo "🐚 Opening backend shell..."
	docker-compose -f docker-compose.dev.yml exec backend bash

# Run database migrations
migrate:
	@echo "📊 Running database migrations..."
	docker-compose -f docker-compose.dev.yml exec backend alembic upgrade head

# Create new migration
migration:
	@echo "📝 Creating new migration..."
	docker-compose -f docker-compose.dev.yml exec backend alembic revision --autogenerate -m "$(message)"

# Reset database (drop and recreate)
reset-db:
	@echo "🔄 Resetting database..."
	docker-compose -f docker-compose.dev.yml down
	docker volume rm industrace_industrace_postgres_data || true
	docker-compose -f docker-compose.dev.yml up -d db
	sleep 10
	docker-compose -f docker-compose.dev.yml up -d backend
	sleep 15
	make migrate
	make init

# Quick restart (for development)
restart:
	@echo "🔄 Quick restart..."
	docker-compose -f docker-compose.dev.yml restart

# Show system info
info:
	@echo "ℹ️  System Information:"
	@echo "======================"
	@echo "Frontend: http://localhost:5173"
	@echo "Backend:  http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"
	@echo ""
	@echo "Default credentials:"
	@echo "Admin:   admin@example.com / admin123"
	@echo "Editor:  editor@example.com / editor123"
	@echo "Viewer:  viewer@example.com / viewer123"

# Show configuration info
config:
	@echo "⚙️  Configuration Information:"
	@echo "============================="
	@echo ""
	@echo "🔧 Development (make dev):"
	@echo "  - CORS: http://localhost:5173, http://localhost:3000, http://localhost:8080"
	@echo "  - API URL: http://localhost:8000"
	@echo "  - Cookies: Insecure (development)"
	@echo "  - Proxy: Vite dev server"
	@echo ""
	@echo "🚀 Production (make prod):"
	@echo "  - CORS: https://industrace.local, https://www.industrace.local"
	@echo "  - API URL: https://industrace.local (via Traefik)"
	@echo "  - Cookies: Secure, SameSite=strict"
	@echo "  - Proxy: Traefik + Let's Encrypt"
	@echo "  - Dashboard: http://localhost:8080"
	@echo ""
	@echo "🔐 Custom Certs (make custom-certs-start):"
	@echo "  - CORS: https://[DOMAIN], https://www.[DOMAIN]"
	@echo "  - API URL: https://[DOMAIN] (via nginx)"
	@echo "  - Cookies: Secure, SameSite=strict"
	@echo "  - Proxy: Nginx + Custom certificates"
	@echo ""
	@if [ -f "custom-certs.env" ]; then \
		DOMAIN=$$(grep DOMAIN custom-certs.env | cut -d= -f2); \
		echo "📋 Current custom domain: $$DOMAIN"; \
	fi

# Show Traefik dashboard info
traefik:
	@echo "🦌 Traefik Information:"
	@echo "======================"
	@echo "Dashboard: http://localhost:8080"
	@echo "Services: http://localhost:8080/api/http/services"
	@echo "Routers: http://localhost:8080/api/http/routers"
	@echo ""
	@echo "🔍 Checking Traefik status..."
	@if docker ps | grep -q traefik; then \
		echo "✅ Traefik is running"; \
		echo "🌐 Access dashboard at: http://localhost:8080"; \
	else \
		echo "❌ Traefik is not running"; \
		echo "💡 Start with: make prod"; \
	fi

# Create new tenant
create-tenant:
	@echo "🏗️  Creating new tenant..."
	@echo "Usage: make create-tenant TENANT_NAME=\"My Company\" TENANT_SLUG=\"my-company\" ADMIN_EMAIL=\"admin@mycompany.com\""
	@if [ -z "$(TENANT_NAME)" ] || [ -z "$(TENANT_SLUG)" ] || [ -z "$(ADMIN_EMAIL)" ]; then \
		echo "❌ Please provide TENANT_NAME, TENANT_SLUG, and ADMIN_EMAIL parameters"; \
		echo "Example: make create-tenant TENANT_NAME=\"My Company\" TENANT_SLUG=\"my-company\" ADMIN_EMAIL=\"admin@mycompany.com\""; \
		exit 1; \
	fi
	@if [ -z "$(ADMIN_PASSWORD)" ]; then \
		echo "🔐 No password provided, generating secure password..."; \
		PASSWORD=$$(openssl rand -base64 12 | tr -d "=+/" | cut -c1-12); \
		echo "Generated password: $$PASSWORD"; \
		docker-compose -f docker-compose.dev.yml exec backend python -m app.init_tenant "$(TENANT_NAME)" "$(TENANT_SLUG)" "$(ADMIN_EMAIL)" "$$PASSWORD" "$(ADMIN_NAME)"; \
	else \
		echo "🔐 Using provided password..."; \
		docker-compose -f docker-compose.dev.yml exec backend python -m app.init_tenant "$(TENANT_NAME)" "$(TENANT_SLUG)" "$(ADMIN_EMAIL)" "$(ADMIN_PASSWORD)" "$(ADMIN_NAME)"; \
	fi

# Create tenant with default values
create-tenant-default:
	@echo "🏗️  Creating tenant with default values..."
	@echo "🔐 Generating secure password..."
	@PASSWORD=$$(openssl rand -base64 12 | tr -d "=+/" | cut -c1-12); \
	echo "Generated password: $$PASSWORD"; \
	docker-compose -f docker-compose.dev.yml exec backend python -m app.init_tenant "Nuovo Tenant" "nuovo-tenant" "admin@example.com" "$$PASSWORD"

# Custom Certificates Commands
# ============================

# Setup custom certificates deployment
custom-certs-setup:
	@echo "🔐 Setting up custom certificates deployment..."
	@if [ ! -f "custom-certs.env" ]; then \
		echo "❌ custom-certs.env not found!"; \
		echo "📋 Please copy custom-certs.env.example to custom-certs.env and configure it:"; \
		echo "   cp custom-certs.env.example custom-certs.env"; \
		echo "   nano custom-certs.env"; \
		exit 1; \
	fi
	@echo "✅ Running setup validation..."
	./setup-custom-certs.sh

# Start with custom certificates
custom-certs-start:
	@echo "🚀 Starting Industrace with custom certificates..."
	@if [ ! -f "custom-certs.env" ]; then \
		echo "❌ custom-certs.env not found!"; \
		echo "📋 Please run 'make custom-certs-setup' first"; \
		exit 1; \
	fi
	docker-compose -f docker-compose.custom-certs.yml --env-file custom-certs.env up -d
	@echo "✅ Services started with custom certificates!"
	@echo "🌐 Access your application at: https://$(grep DOMAIN custom-certs.env | cut -d= -f2)"

# Stop custom certificates deployment
custom-certs-stop:
	@echo "🛑 Stopping custom certificates deployment..."
	docker-compose -f docker-compose.custom-certs.yml --env-file custom-certs.env down

# Show custom certificates logs
custom-certs-logs:
	@echo "📋 Showing custom certificates logs..."
	docker-compose -f docker-compose.custom-certs.yml --env-file custom-certs.env logs -f

# Reset admin password
reset-admin-password:
	@echo "🔐 Resetting admin password..."
	@if [ -z "$(TENANT_SLUG)" ] || [ -z "$(ADMIN_EMAIL)" ]; then \
		echo "❌ Please provide TENANT_SLUG and ADMIN_EMAIL parameters"; \
		echo "Example: make reset-admin-password TENANT_SLUG=\"my-company\" ADMIN_EMAIL=\"admin@mycompany.com\""; \
		exit 1; \
	fi
	@if [ -z "$(NEW_PASSWORD)" ]; then \
		echo "🔐 No new password provided, generating secure password..."; \
		PASSWORD=$$(openssl rand -base64 12 | tr -d "=+/" | cut -c1-12); \
		echo "Generated password: $$PASSWORD"; \
		docker-compose -f docker-compose.dev.yml exec backend python -m app.reset_admin_password "$(TENANT_SLUG)" "$(ADMIN_EMAIL)" "$$PASSWORD"; \
	else \
		echo "🔐 Using provided password..."; \
		docker-compose -f docker-compose.dev.yml exec backend python -m app.reset_admin_password "$(TENANT_SLUG)" "$(ADMIN_EMAIL)" "$(NEW_PASSWORD)"; \
	fi

# List all tenants
list-tenants:
	@echo "🏢 Listing all tenants..."
	docker-compose -f docker-compose.dev.yml exec backend python -m app.reset_admin_password list-tenants

# List admin users in a tenant
list-admins:
	@echo "👤 Listing admin users in tenant..."
	@if [ -z "$(TENANT_SLUG)" ]; then \
		echo "❌ Please provide TENANT_SLUG parameter"; \
		echo "Example: make list-admins TENANT_SLUG=\"my-company\""; \
		exit 1; \
	fi
	docker-compose -f docker-compose.dev.yml exec backend python -m app.reset_admin_password list-admins "$(TENANT_SLUG)"
