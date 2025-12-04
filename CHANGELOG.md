# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Future features and improvements

## [1.1.0] - 2025-12-04

### Added
- **Trash Management for Areas**
  - Soft delete for areas with `deleted_at` column
  - Endpoint `/areas/trash` to view deleted areas
  - Endpoint `PATCH /areas/{id}/restore` to restore areas
  - Endpoint `DELETE /areas/{id}/hard` for permanent deletion
  - Endpoint `DELETE /areas/trash/empty` to empty trash
  - UI aligned with Sites and Locations for trash management

- **Multilingual Printed Kit**
  - PDF generation in Italian/English
  - Automatic support based on user interface language
  - `language` parameter in API request
  - Complete translations for all printed kit sections

- **Restructured Translation System**
  - Translation file consolidation (40 files deleted, 19 new)
  - Complete IT/EN translation alignment
  - New centralized loader (`loader-final.js`)
  - Translation automation scripts (`sync-translations.js`, `translate-keys.js`)
  - New translation files: `auditlog.json`, `globalsearch.json`, `pcap.json`, `areas.json`

- **Improved Global Search**
  - Fixed join with Area for Locations
  - Auto-search when query changes
  - Improved result descriptions with area name
  - Fixed search that wasn't finding results

- **Performance Optimizations**
  - New database indexes to improve query performance
  - Dashboard cache (`dashboard_cache.py`)
  - Performance test scripts

- **Documentation**
  - Complete upgrade guide (`docs/UPGRADE.md`)
  - Performance documentation

### Changed
- **Translation System**
  - Complete translation system restructuring
  - Consolidation of fragmented files into unified files
  - Deleted old files: `assetCommunications.json`, `assetConnections.json`, `assetCustomFields.json`, `assetDetail.json`, `assetForm.json`, `auditLogs.json`, `documents.json`, `errors.json`, `forms.json`, `interfaces.json`, `permissions.json`, `utility.json`
  - New more efficient centralized loader
  - Automatic IT/EN key alignment

- **Asset Timeline**
  - Now shows only changes related to the specific asset
  - `entity_id` filter in backend
  - Improved query performance

- **Global Search**
  - Correct join with Area for Locations
  - Improved result descriptions
  - Auto-search implemented

### Fixed
- Asset timeline showed all changes instead of only those of the specific asset
- Global search didn't find results for Locations (fixed Area join)
- IT/EN translation alignment (missing keys added)
- Fixed global search that wasn't working correctly

### Migration
- Added `deleted_at` column to `areas` table (migration `f5b3589a115e`)
- Added indexes to improve query performance (migration `add_performance_indexes`)

### Technical
- Backend: New endpoints for areas trash management
- Backend: `entity_id` filter for audit logs
- Backend: `language` parameter for printed kit
- Backend: Dashboard cache implemented
- Frontend: Translation system restructuring
- Frontend: Translation automation scripts
- Database: New Alembic migrations

## [1.0.0] - 2025 august

### 🎉 Initial Release

#### Added
- **Complete Asset Management System**
  - Full lifecycle management for industrial assets
  - Asset creation, editing, deletion, and restoration
  - Bulk operations (update, delete, restore)
  - Asset duplication functionality
  - Custom fields support for flexible asset properties
  - Asset search and filtering capabilities

- **Multi-tenant Architecture**
  - Support for multiple organizations
  - Complete data isolation between tenants
  - Tenant-specific configurations
  - Multi-tenant user management

- **Role-based Access Control (RBAC)**
  - Three predefined roles: Admin, Editor, Viewer
  - Granular permissions system
  - Permission-based UI rendering
  - Role assignment and management

- **Network Topology Visualization**
  - Interactive network mapping
  - Asset connection visualization
  - Communication flow analysis
  - Network graph with zoom and pan

- **Risk Assessment Engine**
  - Advanced risk scoring algorithm
  - Composite risk calculation (Vulnerability 35%, Impact 40%, Operational 25%)
  - Risk score breakdown and suggestions
  - Automated risk recalculation
  - Risk overview dashboard

- **Document Management**
  - Asset photo upload and management
  - Document upload and organization
  - File type validation
  - Image preview and thumbnails

- **Audit Trail System**
  - Complete activity logging
  - Change tracking for all entities
  - User action history
  - Exportable audit logs
  - IP address tracking

- **Import/Export System**
  - Excel/CSV import with preview
  - Data validation before import
  - Error reporting and correction
  - Template downloads
  - Bulk data operations

- **Print System**
  - PDF report generation
  - QR code generation for assets
  - Customizable print templates
  - Print history tracking
  - Asset card printing

- **PCAP Analysis**
  - Network traffic file upload
  - Protocol detection and analysis
  - Asset communication mapping
  - Network interface discovery

- **Floor Plan Integration**
  - Floor plan upload and management
  - Asset positioning on floor plans
  - Interactive floor plan navigation
  - Visual asset placement

- **Dashboard and Analytics**
  - Real-time dashboard with metrics
  - Asset statistics and charts
  - Risk overview visualization
  - Recent activity tracking
  - System health monitoring

- **User Interface**
  - Responsive design for all devices
  - Modern Vue.js 3 interface
  - PrimeVue component library
  - Dark/light theme support
  - Internationalization (Italian/English)

- **API and Integration**
  - Complete RESTful API
  - OpenAPI/Swagger documentation
  - JWT authentication
  - API key management
  - External API endpoints

#### Technical Features
- **Backend**: FastAPI with SQLAlchemy ORM
- **Database**: PostgreSQL with Alembic migrations
- **Frontend**: Vue.js 3 with Vite build system
- **Authentication**: JWT with secure cookies
- **Containerization**: Docker and Docker Compose
- **Testing**: Pytest framework with test coverage
- **Security**: Input validation, CORS, rate limiting
- **Performance**: Optimized queries, caching support

#### Security Features
- JWT-based authentication with refresh tokens
- Role-based access control
- Input validation and sanitization
- CORS protection
- Rate limiting
- Secure cookie configuration
- Audit logging for security events

#### Deployment Features
- Docker containerization
- Docker Compose for easy deployment
- Environment-based configuration
- Health check endpoints
- Production-ready configuration
- Backup and restore capabilities

### Fixed
- Asset name clickability in tables
- Dashboard risk threshold alignment
- Table column display issues
- Checkbox visual state updates
- Comprehensive error handling
- Null checks in data table functions

### Documentation
- Complete user manual
- API documentation
- Installation guides
- Development setup instructions
- Security best practices
- Troubleshooting guide

---

## Version History

- **v1.0.0** (August 2025): Initial release with complete asset management system
