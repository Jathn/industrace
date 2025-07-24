# Quick Start - Industrace

**Industrace** is an open-source industrial asset management system. This document will guide you through installation and initial setup in **less than 5 minutes**.

## Prerequisites

- Docker and Docker Compose installed
- Git installed
- Port 80 available on your system

## Quick Installation

### 1. Clone the Repository

```bash
git clone https://github.com/besafe-it/industrace.git
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

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 5. Verify Installation

Open your browser and go to:
- **http://yourdomain.com** (if you configured a domain)
- **http://localhost** (if you used localhost)

## First Access

1. **Login**: Use the credentials configured in `.env`
   - Email: `admin@yourdomain.com`
   - Password: The system will prompt you to set a password during first access

2. **Initial Setup**: The system will automatically guide you through the first tenant configuration

## Main File Structure

```
industrace/
├── .env                    # ← MODIFY HERE (copy from production.env.example)
├── docker-compose.prod.yml # ← DON'T TOUCH
├── backend/                # ← DON'T TOUCH
└── frontend/               # ← DON'T TOUCH
```

## Useful Commands

```bash
# Start the system
docker-compose -f docker-compose.prod.yml up -d

# Stop the system
docker-compose -f docker-compose.prod.yml down

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Restart everything
docker-compose -f docker-compose.prod.yml restart
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
docker-compose -f docker-compose.prod.yml logs

# Recreate containers
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --force-recreate
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
docker-compose -f docker-compose.prod.yml exec db pg_dump -U industrace industrace > backup.sql

# Restore
docker-compose -f docker-compose.prod.yml exec -T db psql -U industrace industrace < backup.sql
```

## Support

- **Documentation**: [docs/](docs/)
- **Website**: https://besafe.it/industrace
- **Email**: industrace@besafe.it
- **GitHub**: https://github.com/besafe-it/industrace

## License

Industrace is distributed under AGPL v3.0 license - see [LICENSE](LICENSE) for details.

---

**Author**: Maurizio Bertaboni - BeSafe S.r.l. (https://besafe.it) 