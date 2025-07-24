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
	@echo "  make dev       - Start development environment"
	@echo "  make prod      - Start production environment"
	@echo "  make test      - Run tests"
	@echo "  make logs      - Show logs"
	@echo "  make stop      - Stop all containers"
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
	docker-compose -f docker-compose.dev.yml up -d

# Start production environment
prod:
	@echo "🚀 Starting production environment..."
	docker-compose up -d

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