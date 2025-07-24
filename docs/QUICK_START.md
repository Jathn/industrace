# Quick Start - Industrace

**Industrace** is an open-source industrial asset management system. This document will guide you through installation and initial setup in **less than 5 minutes**.

## Prerequisites

- Docker and Docker Compose installed
- Git installed
- Port 80 available on your system

## Quick Installation

### 1. Clone the Repository

```bash
git clone https://github.com/industrace/industrace.git
cd industrace
```

### 2. Configure Environment

Copy the example configuration file:

```bash
cp production.env.example .env
```

### 3. Edit Configuration (2 minutes)

Open `.env` and modify **only** these lines:

```bash
# === MODIFY THESE LINES ===
DB_PASSWORD=your_secure_password_here

# JWT Configuration
SECRET_KEY=your-super-secure-secret-key-change-this-in-production

# Your server domain (required)
DOMAIN=yourdomain.com
# or for local testing:
# DOMAIN=localhost

# Email for first admin (required)
ADMIN_EMAIL=admin@yourdomain.com

# === END MODIFICATIONS ===
```

**Note**: Replace `yourdomain.com` with your actual domain or use `localhost` for local testing.

**Important**: After creating the `.env` file, you'll also need to update the domain references in `docker-compose.prod.yml` to match your actual domain.

### 3.5. Update Docker Compose (if using custom domain)

If you're using a custom domain (not localhost), you need to update the domain references in `docker-compose.prod.yml`:

```bash
# Replace all occurrences of 'yourdomain.com' with your actual domain
sed -i 's/yourdomain.com/your-actual-domain.com/g' docker-compose.prod.yml
```

### 4. Start the System

**For local development (recommended for first time):**
```bash
make init
```

**For production deployment:**
```bash
make prod
```

### Configuration Differences

- **Development** (`make init`): Direct port access, no SSL, hot reload, automatic demo data
- **Production** (`make prod`): Traefik reverse proxy, SSL certificates, optimized builds

### 5. Verify Installation

Open your browser and go to:
- **http://localhost:5173** (for local development - Frontend)
- **http://localhost:8000/docs** (for local development - API Documentation)
- **http://yourdomain.com** (for production deployment)

## First Access

1. **Login**: Use the default credentials (for development):
   - Email: `admin@example.com`
   - Password: `admin123`

   **Alternative users:**
   - Editor: `editor@example.com` / `editor123`
   - Viewer: `viewer@example.com` / `viewer123`

2. **Demo Data**: The system automatically populates with realistic demo data including:
   - 3 Sites (Production Plant, R&D Center, Distribution Warehouse)
   - 12 Areas (Assembly Lines, Labs, Control Rooms, etc.)
   - 19 Locations (Control Panels, Quality Stations, etc.)
   - 8 Assets (PLCs, HMIs, Robots, Sensors, etc.)
   - 10 Interfaces (Network interfaces with IP addresses)
   - 5 Connections (Network topology)
   - 4 Suppliers (Siemens, Rockwell, Schneider, ABB)
   - 6 Contacts (Sales, Support, Management)

3. **Initial Setup**: The system will automatically guide you through the first tenant configuration

## Main File Structure

```
industrace/
├── .env                    # ← MODIFY HERE (copy from production.env.example)
├── docker-compose.prod.yml # ← DON'T TOUCH
├── Makefile               # ← NEW: Simplified commands
├── backend/                # ← DON'T TOUCH
└── frontend/               # ← DON'T TOUCH
```

## Useful Commands

### Development Commands
```bash
# Initialize system with demo data (recommended)
make init

# Start development environment
make dev

# Stop all services
make stop

# View logs
make logs

# Restart services
make restart

# Clean system completely
make clean

# Show system status
make status
```

### Production Commands
```bash
# Start production system
make prod

# Stop production system
make stop

# View production logs
make logs

# Restart production system
make restart

# Build containers
make build

# Rebuild containers
make rebuild
```

### Additional Commands
```bash
# Add demo data to existing system
make demo

# Run tests
make test

# Open backend shell
make shell

# Run database migrations
make migrate

# Reset database
make reset-db

# Show all available commands
make help
```

## Troubleshooting

### "Port 80 already in use" Error
```bash
# Find what's using port 80
sudo lsof -i :80

# Stop the service (e.g., nginx)
sudo systemctl stop nginx
```

### "Permission denied" Error
```bash
# Set correct permissions
sudo chown -R $USER:$USER .
```

### System won't start
```bash
# Check logs
make logs

# Clean and restart
make clean
make init
```

### Demo data not loading
```bash
# Force demo data seeding
make demo

# Or clean and reinitialize
make clean
make init
```

## Advanced Configuration (Optional)

### Change Port
If port 80 is busy, modify `docker-compose.prod.yml`:

```yaml
ports:
  - "8080:80"  # Change 8080 to your preferred port
```

Then access via `http://localhost:8080`

### Database Backup
```bash
# Backup
make backup

# Restore
make restore
```

### Manual Database Operations
```bash
# Backup (manual)
docker-compose -f docker-compose.prod.yml exec db pg_dump -U industrace industrace > backup.sql

# Restore (manual)
docker-compose -f docker-compose.prod.yml exec -T db psql -U industrace industrace < backup.sql
```

## Support

- **Documentation**: [docs/](docs/)
- **Website**: https://besafe.it/industrace
- **Email**: industrace@besafe.it
- **GitHub**: https://github.com/industrace/industrace

## License

Industrace is distributed under AGPL v3.0 license - see [LICENSE](LICENSE) for details.

---

**Author**: Maurizio Bertaboni - BeSafe S.r.l. (https://besafe.it) 