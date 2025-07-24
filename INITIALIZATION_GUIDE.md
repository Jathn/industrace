# Industrace Initialization Guide

## 🎯 Overview

This document describes the new Industrace initialization system that provides a clean and automated routine to configure the system with `@example.com` accounts and pre-populated demo data.

## 🚀 Quick Start

### Complete Initialization (Recommended)
```bash
# Clone the repository
git clone https://github.com/industrace/industrace.git
cd industrace

# Initialize the system with demo data
make init
# or
python3 init_system.py --clean

# Access the application
open http://localhost:5173
```

### Access Credentials
```
Admin:   admin@example.com / admin123
Editor:  editor@example.com / editor123
Viewer:  viewer@example.com / viewer123
```

## 📋 Available Commands

### Makefile Commands
```bash
make help      # Show all available commands
make init      # Initialize system with demo data (clean start)
make demo      # Add demo data to existing system
make clean     # Clean system completely
make dev       # Start development environment
make prod      # Start production environment
make test      # Run tests
make logs      # Show logs
make stop      # Stop all containers
make info      # Show system information
```

### Python Scripts
```bash
# Complete initialization
python3 init_system.py --clean

# Demo data only
python3 init_system.py --demo-only

# Complete cleanup
python3 clean_system.py

# Complete cleanup with images
python3 clean_system.py --all
```

## 🔧 Technical Details

### Configuration Files
- `docker-compose.dev.yml` - Development environment
- `docker-compose.yml` - Production environment
- `init_system.py` - Initialization script
- `clean_system.py` - Cleanup script
- `Makefile` - Simplified commands

### Initialization Process
1. **Docker Check** - Verify Docker is running
2. **Database Cleanup** - Remove existing volumes (if --clean)
3. **Service Startup** - Start containers with docker-compose.dev.yml
4. **Migrations** - Run Alembic migrations
5. **System Setup** - Create tenant, roles and base users
6. **Demo Data** - Populate industrial demo data
7. **Verification** - Test API and login

### Included Demo Data
- **3 Sites**: Main Production Plant, Research & Development Center, Distribution Warehouse
- **12 Areas**: Assembly Lines, Quality Control, Maintenance, Control Rooms, Labs
- **4 Manufacturers**: Siemens, Rockwell Automation, Schneider Electric, ABB
- **4 Suppliers**: Specialized in industrial automation
- **6 Contacts**: Managers and specialized technicians
- **3 Assets**: PLC, HMI, Robot with realistic configurations

## 🛠️ Development

### Development Environment
```bash
# Start development environment
make dev

# Add demo data
make demo

# Show logs
make logs-backend
make logs-frontend

# Backend shell access
make shell

# Restart services
make restart
```

### Database
```bash
# Run migrations
make migrate

# Create new migration
make migration message="migration description"

# Reset database
make reset-db
```

### Testing
```bash
# Run tests
make test

# System status
make status
```

## 🧹 Cleanup

### Standard Cleanup
```bash
# Clean containers, volumes and networks
make clean
# or
python3 clean_system.py
```

### Complete Cleanup
```bash
# Clean everything including Docker images
python3 clean_system.py --all
```

### Manual Cleanup
```bash
# Stop containers
docker-compose -f docker-compose.dev.yml down

# Remove volumes
docker volume rm industrace_industrace_postgres_data

# Remove images
docker rmi industrace-backend industrace-frontend
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Port 8000 not available
```bash
# Check running containers
make status

# Check logs
make logs-backend
```

#### 2. Database connection issues
```bash
# Reset database
make reset-db

# Check environment variables
docker-compose -f docker-compose.dev.yml exec backend env | grep DATABASE
```

#### 3. Login not working
```bash
# Check users in database
docker-compose -f docker-compose.dev.yml exec backend python -c "
from app.database import SessionLocal
from app.models import User
db = SessionLocal()
users = db.query(User).all()
for user in users:
    print(f'{user.email} - {user.role.name}')
db.close()
"
```

#### 4. Missing demo data
```bash
# Add demo data
make demo

# Verify data
docker-compose -f docker-compose.dev.yml exec backend python -c "
from app.database import SessionLocal
from app.models import Site, Area, Asset
db = SessionLocal()
print(f'Sites: {db.query(Site).count()}')
print(f'Areas: {db.query(Area).count()}')
print(f'Assets: {db.query(Asset).count()}')
db.close()
"
```

## 📊 Monitoring

### Access URLs
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

### Logs
```bash
# All logs
make logs

# Backend only
make logs-backend

# Frontend only
make logs-frontend
```

### System Status
```bash
# Container status
make status

# System information
make info
```

## 🔄 Development Workflow

### New Development
```bash
# 1. Clone repository
git clone https://github.com/industrace/industrace.git
cd industrace

# 2. Initialize system
make init

# 3. Start development
make dev

# 4. Develop and test
# ... code ...

# 5. Clean when finished
make clean
```

### Continuous Development
```bash
# 1. Start environment
make dev

# 2. Add demo data if needed
make demo

# 3. Develop
# ... code ...

# 4. Restart if necessary
make restart

# 5. Test
make test
```

## ✅ Functionality Verification

### Automatic Tests
The initialization routine includes automatic tests:
- ✅ Docker verification
- ✅ API health test
- ✅ Admin login test
- ✅ Demo data verification

### Manual Tests
```bash
# Login test
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=admin@example.com&password=admin123"

# API health test
curl http://localhost:8000/api/health

# Frontend test
curl http://localhost:5173
```

## 🎉 Final Result

After initialization, you will have:
- ✅ Fully functional system
- ✅ Admin account with `@example.com` email
- ✅ Realistic industrial demo data
- ✅ Ready development environment
- ✅ Accessible API documentation
- ✅ Working test system

The system is now ready for development and testing with pre-populated demo data and standardized credentials! 