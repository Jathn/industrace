# Administration Guide

## Overview

This administration guide provides comprehensive instructions for managing and maintaining Industrace, the Configuration Management Database for Industrial Control Systems. It covers system administration, user management, security configuration, and operational procedures.

## Table of Contents

1. [System Administration](#system-administration)
2. [User and Role Management](#user-and-role-management)
3. [Multi-Tenant Configuration](#multi-tenant-configuration)
4. [Security Administration](#security-administration)
5. [Database Management](#database-management)
6. [Backup and Recovery](#backup-and-recovery)
7. [Monitoring and Logging](#monitoring-and-logging)
8. [Performance Tuning](#performance-tuning)
9. [Troubleshooting](#troubleshooting)
10. [Maintenance Procedures](#maintenance-procedures)

## System Administration

### Initial Setup

1. **System Requirements Verification**
   ```bash
   # Check system resources
   docker system df
   docker stats
   
   # Verify disk space
   df -h
   
   # Check memory usage
   free -h
   ```

2. **Environment Configuration**
   - Review `production.env` settings
   - Configure database connections
   - Set up SMTP for notifications
   - Configure backup settings

3. **First Boot Configuration**
   ```bash
   # Start the system
   docker-compose up -d
   
   # Check service status
   docker-compose ps
   
   # Verify database migrations
   docker-compose logs backend | grep "migration"
   ```

### System Health Monitoring

1. **Service Status Check**
   ```bash
   # Check all services
   docker-compose ps
   
   # Check specific service logs
   docker-compose logs backend
   docker-compose logs frontend
   docker-compose logs postgres
   ```

2. **Health Endpoints**
   ```bash
   # Backend health
   curl http://localhost:8000/health
   
   # Database connectivity
   curl http://localhost:8000/health/db
   
   # System status
   curl http://localhost:8000/health/system
   ```

3. **Resource Monitoring**
   - CPU usage monitoring
   - Memory consumption tracking
   - Disk space monitoring
   - Network traffic analysis

## User and Role Management

### User Administration

1. **Creating Users**
   - Navigate to Administration → Users
   - Click "Add New User"
   - Fill required information:
     - Email address
     - Full name
     - Role assignment
     - Tenant assignment

2. **User Roles and Permissions**
   - **Administrator**: Full system access
   - **Manager**: Asset and user management
   - **Operator**: Asset operations
   - **Viewer**: Read-only access

3. **Role Configuration**
   ```python
   # Example role permissions
   ADMIN_PERMISSIONS = [
       "users:read", "users:write", "users:delete",
       "assets:read", "assets:write", "assets:delete",
       "system:admin", "reports:admin"
   ]
   ```

### Access Control

1. **Authentication Settings**
   - JWT token configuration
   - Session timeout settings
   - Password policy enforcement
   - Multi-factor authentication setup

2. **API Key Management**
   - Generate API keys for external access
   - Configure key permissions
   - Monitor API usage
   - Rotate keys regularly

3. **Audit Logging**
   - User activity tracking
   - System access monitoring
   - Change history maintenance
   - Security event logging

## Multi-Tenant Configuration

### Tenant Setup

1. **Creating Tenants**
   ```sql
   -- Create new tenant
   INSERT INTO tenants (name, domain, settings)
   VALUES ('Company A', 'company-a.local', '{}');
   ```

2. **Tenant Isolation**
   - Database schema separation
   - File storage isolation
   - Network access control
   - Resource allocation limits

3. **Tenant Configuration**
   - SMTP settings per tenant
   - Custom branding options
   - Feature enablement/disablement
   - Storage quotas

### Data Isolation

1. **Database Isolation**
   - Tenant-specific schemas
   - Row-level security
   - Cross-tenant access prevention
   - Data encryption per tenant

2. **File Storage Isolation**
   - Separate upload directories
   - Access control lists
   - Backup isolation
   - Quota management

## Security Administration

### Security Configuration

1. **SSL/TLS Setup**
   ```nginx
   # Nginx SSL configuration
   server {
       listen 443 ssl;
       ssl_certificate /path/to/cert.pem;
       ssl_certificate_key /path/to/key.pem;
       # ... other SSL settings
   }
   ```

2. **Firewall Configuration**
   ```bash
   # Allow only necessary ports
   ufw allow 80/tcp
   ufw allow 443/tcp
   ufw allow 22/tcp
   ufw enable
   ```

3. **Security Headers**
   ```python
   # Security middleware configuration
   SECURITY_HEADERS = {
       "X-Frame-Options": "DENY",
       "X-Content-Type-Options": "nosniff",
       "X-XSS-Protection": "1; mode=block",
       "Strict-Transport-Security": "max-age=31536000"
   }
   ```

### Vulnerability Management

1. **Regular Security Updates**
   ```bash
   # Update system packages
   apt update && apt upgrade
   
   # Update Docker images
   docker-compose pull
   docker-compose up -d
   ```

2. **Security Scanning**
   - Container vulnerability scanning
   - Dependency vulnerability checks
   - Code security analysis
   - Penetration testing

3. **Incident Response**
   - Security incident procedures
   - Breach notification processes
   - Recovery procedures
   - Post-incident analysis

## Database Management

### Database Administration

1. **PostgreSQL Management**
   ```bash
   # Connect to database
   docker-compose exec postgres psql -U industrace
   
   # Check database size
   SELECT pg_size_pretty(pg_database_size('industrace'));
   
   # List tables
   \dt
   ```

2. **Database Maintenance**
   ```sql
   -- Analyze tables for query optimization
   ANALYZE;
   
   -- Vacuum to reclaim storage
   VACUUM ANALYZE;
   
   -- Check for bloat
   SELECT schemaname, tablename, n_dead_tup, n_live_tup
   FROM pg_stat_user_tables;
   ```

3. **Performance Optimization**
   - Index creation and maintenance
   - Query optimization
   - Connection pooling
   - Cache configuration

### Migration Management

1. **Alembic Migrations**
   ```bash
   # Check migration status
   docker-compose exec backend alembic current
   
   # Apply pending migrations
   docker-compose exec backend alembic upgrade head
   
   # Create new migration
   docker-compose exec backend alembic revision --autogenerate -m "Description"
   ```

2. **Migration Best Practices**
   - Test migrations in development
   - Backup before applying migrations
   - Monitor migration performance
   - Rollback procedures

## Backup and Recovery

### Backup Procedures

1. **Database Backup**
   ```bash
   # Create database backup
   docker-compose exec postgres pg_dump -U industrace industrace > backup.sql
   
   # Automated backup script
   #!/bin/bash
   DATE=$(date +%Y%m%d_%H%M%S)
   docker-compose exec postgres pg_dump -U industrace industrace > backup_$DATE.sql
   ```

2. **File Backup**
   ```bash
   # Backup uploads directory
   tar -czf uploads_backup_$(date +%Y%m%d).tar.gz uploads/
   
   # Backup configuration files
   cp production.env backup_env_$(date +%Y%m%d)
   ```

3. **Backup Verification**
   - Test backup restoration
   - Verify backup integrity
   - Monitor backup success
   - Document backup procedures

### Recovery Procedures

1. **Database Recovery**
   ```bash
   # Restore from backup
   docker-compose exec postgres psql -U industrace industrace < backup.sql
   
   # Point-in-time recovery
   docker-compose exec postgres psql -U industrace industrace -c "SELECT pg_switch_wal();"
   ```

2. **System Recovery**
   - Service restart procedures
   - Configuration restoration
   - Data validation
   - Performance verification

## Monitoring and Logging

### System Monitoring

1. **Application Monitoring**
   ```bash
   # Monitor application logs
   docker-compose logs -f backend
   
   # Check error rates
   grep "ERROR" logs/backend.log | wc -l
   
   # Monitor response times
   curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health
   ```

2. **Resource Monitoring**
   ```bash
   # Monitor Docker resources
   docker stats --no-stream
   
   # Monitor disk usage
   df -h
   
   # Monitor memory usage
   free -h
   ```

3. **Alert Configuration**
   - CPU usage alerts
   - Memory threshold alerts
   - Disk space warnings
   - Service failure notifications

### Log Management

1. **Log Configuration**
   ```python
   # Logging configuration
   LOGGING_CONFIG = {
       "version": 1,
       "handlers": {
           "file": {
               "class": "logging.FileHandler",
               "filename": "logs/industrace.log",
               "formatter": "detailed"
           }
       }
   }
   ```

2. **Log Analysis**
   - Error pattern analysis
   - Performance bottleneck identification
   - Security event monitoring
   - User activity analysis

3. **Log Rotation**
   ```bash
   # Configure logrotate
   /var/log/industrace/*.log {
       daily
       rotate 30
       compress
       delaycompress
       missingok
       notifempty
   }
   ```

## Performance Tuning

### Application Performance

1. **Database Optimization**
   ```sql
   -- Create indexes for common queries
   CREATE INDEX idx_assets_tenant_id ON assets(tenant_id);
   CREATE INDEX idx_assets_status ON assets(status);
   CREATE INDEX idx_assets_type ON assets(type);
   ```

2. **Caching Configuration**
   ```python
   # Redis caching setup
   CACHE_CONFIG = {
       "CACHE_TYPE": "redis",
       "CACHE_REDIS_URL": "redis://localhost:6379/0",
       "CACHE_DEFAULT_TIMEOUT": 300
   }
   ```

3. **Connection Pooling**
   ```python
   # Database connection pooling
   DATABASE_CONFIG = {
       "pool_size": 20,
       "max_overflow": 30,
       "pool_timeout": 30,
       "pool_recycle": 3600
   }
   ```

### System Performance

1. **Docker Optimization**
   ```yaml
   # docker-compose.yml optimizations
   services:
     backend:
       deploy:
         resources:
           limits:
             memory: 2G
             cpus: '1.0'
           reservations:
             memory: 1G
             cpus: '0.5'
   ```

2. **Network Optimization**
   - Load balancer configuration
   - CDN setup for static files
   - Compression configuration
   - Connection pooling

## Troubleshooting

### Common Issues

1. **Service Failures**
   ```bash
   # Check service status
   docker-compose ps
   
   # Restart failed service
   docker-compose restart backend
   
   # Check service logs
   docker-compose logs backend
   ```

2. **Database Issues**
   ```bash
   # Check database connectivity
   docker-compose exec postgres pg_isready -U industrace
   
   # Check database locks
   docker-compose exec postgres psql -U industrace -c "SELECT * FROM pg_locks;"
   ```

3. **Performance Issues**
   ```bash
   # Check slow queries
   docker-compose exec postgres psql -U industrace -c "SELECT * FROM pg_stat_activity WHERE state = 'active';"
   
   # Monitor resource usage
   docker stats
   ```

### Diagnostic Tools

1. **System Diagnostics**
   ```bash
   # System information
   uname -a
   cat /etc/os-release
   
   # Docker information
   docker version
   docker info
   ```

2. **Network Diagnostics**
   ```bash
   # Check network connectivity
   ping localhost
   curl -I http://localhost:8000/health
   
   # Check port availability
   netstat -tulpn | grep :8000
   ```

## Maintenance Procedures

### Regular Maintenance

1. **Daily Tasks**
   - Check system health
   - Review error logs
   - Monitor resource usage
   - Verify backup success

2. **Weekly Tasks**
   - Database maintenance
   - Log rotation
   - Security updates
   - Performance analysis

3. **Monthly Tasks**
   - Full system backup
   - Security audit
   - Performance optimization
   - Documentation updates

### Update Procedures

1. **Application Updates**
   ```bash
   # Pull latest changes
   git pull origin main
   
   # Update Docker images
   docker-compose pull
   
   # Apply database migrations
   docker-compose exec backend alembic upgrade head
   
   # Restart services
   docker-compose up -d
   ```

2. **System Updates**
   ```bash
   # Update system packages
   apt update && apt upgrade
   
   # Update Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```

3. **Rollback Procedures**
   - Database rollback procedures
   - Application rollback
   - Configuration restoration
   - Data recovery

### Emergency Procedures

1. **System Outage Response**
   - Immediate assessment
   - Service restoration
   - Communication procedures
   - Post-incident analysis

2. **Data Loss Recovery**
   - Backup restoration
   - Data validation
   - Service verification
   - Documentation updates

3. **Security Incident Response**
   - Incident containment
   - Evidence preservation
   - System restoration
   - Lessons learned

---

**Industrace** - Configuration Management Database for Industrial Control Systems  
**Author**: Maurizio Bertaboni (BeSafe S.r.l.)  
**Website**: https://besafe.it/industrace  
**Contact**: industrace@besafe.it 