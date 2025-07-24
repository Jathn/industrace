# Installation Guide

This guide provides step-by-step instructions for installing Industrace on your system.

## System Requirements

### Minimum Requirements
- **RAM**: 4GB
- **Storage**: 20GB available space
- **CPU**: 2 cores
- **OS**: Linux, macOS, or Windows with Docker support

### Recommended Requirements
- **RAM**: 8GB or more
- **Storage**: 50GB SSD
- **CPU**: 4+ cores
- **Network**: Stable internet connection

### Software Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- Git

## Installation Methods

### Method 1: Docker Compose with Make (Recommended)

#### Step 1: Clone the Repository
```bash
git clone https://github.com/industrace/industrace.git
cd industrace
```

#### Step 2: Configure Environment
```bash
# Copy environment template
cp production.env.example .env

# Edit configuration (optional)
nano .env
```

#### Step 3: Initialize the System
```bash
# Initialize system with demo data (recommended for first time)
make init

# Or for production deployment
make prod
```

#### Step 4: Verify Installation
```bash
# Check system status
make status

# View logs if needed
make logs
```

#### Step 5: Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Method 2: Development Setup

#### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 15+

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure database
export DATABASE_URL="postgresql://user:password@localhost/industrace"

# Run migrations
alembic upgrade head

# Start backend
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Initial Configuration

### Default Credentials
After installation, you can log in with:
- **Email**: admin@example.com
- **Password**: admin123

### Demo Data
The system automatically populates with comprehensive demo data:
- 3 Sites (Production Plant, R&D Center, Distribution Warehouse)
- 12 Areas (Assembly Lines, Labs, Control Rooms, etc.)
- 19 Locations (Control Panels, Quality Stations, etc.)
- 8 Assets (PLCs, HMIs, Robots, Sensors, etc.)
- 10 Interfaces (Network interfaces with IP addresses)
- 5 Connections (Network topology)
- 4 Suppliers (Siemens, Rockwell, Schneider, ABB)
- 6 Contacts (Sales, Support, Management)

## Available Make Commands

### Basic Commands
```bash
make init      # Initialize system with demo data
make dev       # Start development environment
make prod      # Start production environment
make stop      # Stop all services
make status    # Show service status
make logs      # View logs
```

### Development Commands
```bash
make demo      # Add demo data to existing system
make clean     # Clean system completely
make test      # Run tests
make shell     # Open backend shell
make migrate   # Run database migrations
make reset-db  # Reset database
```

### Build Commands
```bash
make build     # Build containers
make rebuild   # Rebuild containers
make restart   # Restart services
```

### Utility Commands
```bash
make help      # Show all available commands
make info      # Show system information
```

## Manual Docker Commands (Alternative)

If you prefer to use Docker commands directly:

### Development Environment
```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# Stop development environment
docker-compose -f docker-compose.dev.yml down

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Restart services
docker-compose -f docker-compose.dev.yml restart
```

### Production Environment
```bash
# Start production system
docker-compose -f docker-compose.prod.yml up -d

# Stop production system
docker-compose -f docker-compose.prod.yml down

# View production logs
docker-compose -f docker-compose.prod.yml logs -f

# Restart production system
docker-compose -f docker-compose.prod.yml restart
```

## Troubleshooting

### Common Issues

#### System won't start
```bash
# Check logs
make logs

# Clean and restart
make clean
make init
```

#### Demo data not loading
```bash
# Force demo data seeding
make demo

# Or clean and reinitialize
make clean
make init
```

#### Port conflicts
```bash
# Check what's using the ports
sudo lsof -i :5173
sudo lsof -i :8000
sudo lsof -i :5432

# Stop conflicting services
sudo systemctl stop nginx  # if using port 80
```

#### Permission issues
```bash
# Set correct permissions
sudo chown -R $USER:$USER .

# Or run with sudo (not recommended for production)
sudo make init
```

### Database Issues

#### Reset database
```bash
# Complete reset
make clean
make init

# Or just reset database
make reset-db
```

#### Backup and restore
```bash
# Backup
make backup

# Restore
make restore
```

## Configuration Files

### Environment Variables
The main configuration file is `.env` (copied from `production.env.example`):

```bash
# Database Configuration
DB_PASSWORD=your_secure_password_here

# JWT Configuration
SECRET_KEY=your-super-secure-secret-key-change-this-in-production

# Domain Configuration
DOMAIN=yourdomain.com

# Admin Configuration
ADMIN_EMAIL=admin@yourdomain.com
```

### Docker Compose Files
- `docker-compose.dev.yml` - Development environment
- `docker-compose.prod.yml` - Production environment
- `docker-compose.yml` - Default environment

## Next Steps

After successful installation:

1. **Access the application**: http://localhost:5173
2. **Login with default credentials**: admin@example.com / admin123
3. **Explore demo data**: Navigate through sites, areas, assets, and connections
4. **Configure your environment**: Update settings in the admin panel
5. **Add your own data**: Start adding your industrial assets

## Support

- **Documentation**: [docs/](docs/)
- **Quick Start**: [QUICK_START.md](QUICK_START.md)
- **Troubleshooting**: [troubleshooting.md](troubleshooting.md)
- **Website**: https://besafe.it/industrace
- **Email**: industrace@besafe.it

---

**Author**: Maurizio Bertaboni - BeSafe S.r.l. (https://besafe.it) 