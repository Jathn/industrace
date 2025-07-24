# Troubleshooting Guide

This guide provides solutions for common issues encountered when using Industrace.

## Quick Commands Reference

### Using Make Commands (Recommended)
```bash
make status    # Check service status
make logs      # View all logs
make restart   # Restart all services
make clean     # Clean system completely
make init      # Reinitialize system
make demo      # Add demo data
make shell     # Open backend shell
make migrate   # Run database migrations
make reset-db  # Reset database
```

### Manual Docker Commands (Alternative)
```bash
docker-compose -f docker-compose.dev.yml ps
docker-compose -f docker-compose.dev.yml logs
docker-compose -f docker-compose.dev.yml restart
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up -d
```

## Quick Diagnostics

### System Health Check
```bash
# Check if all services are running
make status

# Check system health
curl http://localhost:8000/health

# Check setup status
curl http://localhost:8000/setup/status
```

### Log Analysis
```bash
# View all logs
make logs

# View specific service logs
docker-compose -f docker-compose.dev.yml logs backend
docker-compose -f docker-compose.dev.yml logs frontend
docker-compose -f docker-compose.dev.yml logs db

# Follow logs in real-time
docker-compose -f docker-compose.dev.yml logs -f backend
```

## Common Issues

### Installation Issues

#### Docker Not Running
**Symptoms**: `Cannot connect to the Docker daemon`

**Solution**:
```bash
# Start Docker service
sudo systemctl start docker

# Check Docker status
sudo systemctl status docker

# Add user to docker group (if needed)
sudo usermod -aG docker $USER
```

#### Port Conflicts
**Symptoms**: `Port is already allocated` or services fail to start

**Solution**:
```bash
# Check what's using the ports
lsof -i :8000
lsof -i :5173
lsof -i :5432

# Stop conflicting services
sudo systemctl stop nginx
sudo systemctl stop apache2
sudo systemctl stop postgresql

# Or change ports in docker-compose.yml
```

#### Insufficient Permissions
**Symptoms**: `Permission denied` errors

**Solution**:
```bash
# Fix upload directory permissions
sudo chown -R 1000:1000 uploads/
sudo chmod -R 755 uploads/

# Fix Docker permissions
sudo chown -R $USER:$USER /var/run/docker.sock
```

### Database Issues

#### Database Connection Failed
**Symptoms**: `Connection refused` or `database does not exist`

**Solution**:
```bash
# Check database container
make status

# Check database logs
make logs

# Restart database
make restart

# Check database connection
docker-compose -f docker-compose.dev.yml exec db pg_isready -U postgres
```

#### Database Migration Issues
**Symptoms**: `alembic` errors or missing tables

**Solution**:
```bash
# Run migrations manually
docker-compose exec backend alembic upgrade head

# Check migration status
docker-compose exec backend alembic current

# Reset database (WARNING: loses data)
docker-compose down
docker volume rm industrace_postgres_data
docker-compose up -d
```

#### Database Performance Issues
**Symptoms**: Slow queries or timeouts

**Solution**:
```bash
# Check database size
docker-compose exec db psql -U postgres -d industrace -c "SELECT pg_size_pretty(pg_database_size('industrace'));"

# Vacuum database
docker-compose exec db psql -U postgres -d industrace -c "VACUUM ANALYZE;"

# Check active connections
docker-compose exec db psql -U postgres -d industrace -c "SELECT count(*) FROM pg_stat_activity;"
```

### Backend Issues

#### Backend Not Starting
**Symptoms**: Backend container exits immediately

**Solution**:
```bash
# Check backend logs
docker-compose logs backend

# Check environment variables
docker-compose exec backend env | grep DATABASE_URL

# Rebuild backend
docker-compose build backend
docker-compose up -d backend
```

#### API Authentication Issues
**Symptoms**: `INVALID_CREDENTIALS` or `401 Unauthorized`

**Solution**:
```bash
# Check JWT configuration
echo $SECRET_KEY
echo $JWT_ISSUER
echo $JWT_AUDIENCE

# Reset admin password
docker-compose exec backend python -c "
from app.database import get_db
from app.models import User
from app.services.auth import get_password_hash
db = next(get_db())
user = db.query(User).filter(User.email == 'admin@example.com').first()
user.hashed_password = get_password_hash('newpassword123')
db.commit()
"
```

#### File Upload Issues
**Symptoms**: File uploads fail or files not accessible

**Solution**:
```bash
# Check upload directory permissions
ls -la uploads/

# Fix permissions
sudo chown -R 1000:1000 uploads/
sudo chmod -R 755 uploads/

# Check file size limits
echo $MAX_FILE_SIZE

# Check disk space
df -h
```

### Frontend Issues

#### Frontend Not Loading
**Symptoms**: White screen or connection errors

**Solution**:
```bash
# Check frontend container
docker-compose ps frontend

# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose build frontend
docker-compose up -d frontend

# Check API URL configuration
echo $VITE_API_URL
```

#### Build Errors
**Symptoms**: Frontend build fails

**Solution**:
```bash
# Clear node_modules
docker-compose run --rm frontend rm -rf node_modules
docker-compose build frontend

# Check npm cache
docker-compose run --rm frontend npm cache clean --force

# Update dependencies
docker-compose run --rm frontend npm update
```

### Network Issues

#### CORS Errors
**Symptoms**: `CORS policy` errors in browser console

**Solution**:
```bash
# Check CORS configuration
echo $CORS_ORIGINS

# Update CORS settings
export CORS_ORIGINS="http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173"
docker-compose restart backend
```

#### SSL/HTTPS Issues
**Symptoms**: Certificate errors or mixed content warnings

**Solution**:
```bash
# Check Traefik logs
docker-compose logs traefik

# Check certificate files
ls -la letsencrypt/

# Restart Traefik
docker-compose restart traefik

# Check DNS resolution
nslookup yourdomain.com
```

### Performance Issues

#### Slow Response Times
**Symptoms**: API calls take too long

**Solution**:
```bash
# Check system resources
docker stats

# Check database performance
docker-compose exec db psql -U postgres -d industrace -c "SELECT query, mean_time FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;"

# Check slow queries
docker-compose exec db psql -U postgres -d industrace -c "SELECT * FROM pg_stat_activity WHERE state = 'active';"
```

#### High Memory Usage
**Symptoms**: System becomes unresponsive

**Solution**:
```bash
# Check memory usage
free -h
docker stats

# Restart services
docker-compose restart

# Increase swap space (if needed)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Backup and Restore Issues

#### Backup Fails
**Symptoms**: Backup script fails or creates incomplete backups

**Solution**:
```bash
# Check disk space
df -h

# Check backup script permissions
ls -la scripts/backup.py

# Run backup manually
python scripts/backup.py --verbose

# Check backup contents
ls -la backups/
```

#### Restore Fails
**Symptoms**: Restore process fails or data is corrupted

**Solution**:
```bash
# Verify backup integrity
python scripts/backup.py --verify /path/to/backup

# Check backup metadata
cat /path/to/backup/metadata.json

# Stop services before restore
docker-compose down

# Restore step by step
python scripts/restore.py --backup-dir /backup --restore-database
python scripts/restore.py --backup-dir /backup --restore-files
```

## Advanced Troubleshooting

### Debug Mode

#### Enable Debug Logging
```bash
# Set debug environment variables
export DEBUG=true
export LOG_LEVEL=DEBUG

# Restart backend
docker-compose restart backend

# Check debug logs
docker-compose logs -f backend
```

#### Database Debugging
```bash
# Connect to database directly
docker-compose exec db psql -U postgres -d industrace

# Check table structure
\d assets
\d users

# Check recent activity
SELECT * FROM audit_logs ORDER BY created_at DESC LIMIT 10;
```

### Performance Tuning

#### Database Optimization
```sql
-- Check slow queries
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Analyze table statistics
ANALYZE assets;
ANALYZE users;
ANALYZE audit_logs;

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

#### Application Optimization
```bash
# Check API response times
curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:8000/assets"

# Monitor API endpoints
docker-compose exec backend python -c "
import time
import requests
start = time.time()
response = requests.get('http://localhost:8000/assets')
print(f'Response time: {time.time() - start:.2f}s')
print(f'Status: {response.status_code}')
"
```

### Security Issues

#### Security Audit
```bash
# Check for security vulnerabilities
docker-compose exec backend python -c "
from app.config import settings
print(f'DEBUG: {settings.DEBUG}')
print(f'SECURE_COOKIES: {settings.SECURE_COOKIES}')
print(f'ENVIRONMENT: {settings.ENVIRONMENT}')
"

# Check file permissions
find . -type f -exec ls -la {} \;

# Check for exposed secrets
grep -r "password\|secret\|key" . --exclude-dir=node_modules --exclude-dir=.git
```

#### Authentication Debugging
```bash
# Check JWT token
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=admin@example.com&password=admin123" \
  -v

# Decode JWT token (if needed)
python -c "
import jwt
token = 'your-jwt-token-here'
print(jwt.decode(token, options={'verify_signature': False}))
"
```

## Getting Help

### Information to Collect

When reporting issues, collect the following information:

#### System Information
```bash
# System details
uname -a
docker --version
docker-compose --version

# Service status
docker-compose ps
docker-compose logs --tail=100
```

#### Configuration Information
```bash
# Environment variables
env | grep -E "(INDUSTRACE|DATABASE|SECRET|JWT)"

# Configuration files
ls -la *.env
cat docker-compose.yml
```

#### Error Information
```bash
# Recent errors
docker-compose logs --tail=50 backend | grep ERROR
docker-compose logs --tail=50 frontend | grep ERROR

# Health check
curl -v http://localhost:8000/health
```

### Support Channels

1. **Documentation**: Check this troubleshooting guide first
2. **GitHub Issues**: Report bugs and feature requests
3. **Community**: Join community forums and discussions
4. **Professional Support**: Contact for enterprise support

### Escalation Process

1. **Check logs**: Review all relevant logs
2. **Reproduce issue**: Document steps to reproduce
3. **Collect information**: Gather system and error information
4. **Search existing issues**: Check if issue is already reported
5. **Create detailed report**: Include all collected information
6. **Follow up**: Monitor issue updates and provide additional information

## Prevention

### Regular Maintenance

#### Daily Checks
```bash
# Health check
curl http://localhost:8000/health

# Service status
docker-compose ps

# Disk space
df -h
```

#### Weekly Checks
```bash
# Backup verification
python scripts/backup.py --verify-latest

# Database maintenance
docker-compose exec db psql -U postgres -d industrace -c "VACUUM ANALYZE;"

# Log rotation
docker-compose exec backend logrotate /etc/logrotate.conf
```

#### Monthly Checks
```bash
# Security updates
docker-compose pull
docker-compose build --no-cache

# Performance review
docker-compose exec db psql -U postgres -d industrace -c "SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;"

# Configuration review
grep -r "password\|secret" . --exclude-dir=node_modules --exclude-dir=.git
```

### Monitoring Setup

#### Health Monitoring
```bash
# Create monitoring script
cat > monitor.sh << 'EOF'
#!/bin/bash
if ! curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "Industrace is down!" | mail -s "Alert" admin@company.com
fi
EOF

# Add to crontab
echo "*/5 * * * * /path/to/monitor.sh" | crontab -
```

#### Resource Monitoring
```bash
# Monitor disk space
df -h | awk '$5 > "90%" {print "Disk space critical: " $0}'

# Monitor memory usage
free -h | awk '/^Mem:/ {if($3/$2 > 0.9) print "Memory usage critical: " $0}'

# Monitor Docker resources
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
``` 