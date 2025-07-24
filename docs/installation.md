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

### Method 1: Docker Compose (Recommended)

#### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd industrace
```

#### Step 2: Configure Environment
```bash
# Copy environment template
cp production.env.example production.env

# Edit configuration (optional)
nano production.env
```

#### Step 3: Start the Application
```bash
# Start all services
docker-compose up -d

# Verify services are running
docker-compose ps
```

#### Step 4: Initialize the System
```bash
# Check system status
curl http://localhost:8000/setup/status

# If not initialized, run initialization
curl -X POST http://localhost:8000/setup/initialize
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

### First Steps
1. **Change Default Password**: Update the admin password immediately
2. **Configure SMTP**: Set up email notifications
3. **Create Tenant**: Set up your organization
4. **Add Users**: Create user accounts for your team
5. **Configure Asset Types**: Define your asset categories

### Environment Configuration

Key environment variables:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/industrace

# Security
SECRET_KEY=your-secret-key-here
JWT_ISSUER=industrace-api
JWT_AUDIENCE=industrace-client

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# File Uploads
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760  # 10MB

# API Settings
EXTERNAL_API_ENABLED=true
EXTERNAL_API_DOCS_ENABLED=true
```

## Verification

### Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:00:00",
  "version": "1.0.0",
  "environment": "production"
}
```

### System Status
```bash
curl http://localhost:8000/setup/status
```

Expected response:
```json
{
  "is_configured": true,
  "tenant_count": 1,
  "user_count": 3,
  "role_count": 3,
  "database_connected": true,
  "error": null
}
```

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Check what's using the port
lsof -i :8000
lsof -i :5173

# Stop conflicting services or change ports in docker-compose.yml
```

#### Database Connection Issues
```bash
# Check database container
docker-compose logs db

# Restart database
docker-compose restart db
```

#### Permission Issues
```bash
# Fix upload directory permissions
sudo chown -R 1000:1000 uploads/
```

### Logs
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db

# Follow logs in real-time
docker-compose logs -f backend
```

## Next Steps

After successful installation:

1. **Read the User Manual**: Learn how to use Industrace
2. **Configure Security**: Set up proper authentication and authorization
3. **Import Data**: Import your existing asset data
4. **Set Up Monitoring**: Configure health checks and monitoring
5. **Backup Strategy**: Implement regular backups

## Support

If you encounter issues during installation:

1. Check the troubleshooting guide
2. Review the logs for error messages
3. Verify system requirements are met
4. Check the GitHub issues page for known problems 