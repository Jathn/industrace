# Industrace

**Configuration Management Database for Industrial Control Systems**

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL%203.0-blue.svg)](https://opensource.org/licenses/AGPL-3.0)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-green.svg)](https://www.python.org/)
[![Vue](https://img.shields.io/badge/Vue-3.0+-green.svg)](https://vuejs.org/)

## About

Industrace is an open-source Configuration Management Database (CMDB) specifically designed for Industrial Control Systems. It provides comprehensive asset management, network analysis, risk assessment, and reporting capabilities for industrial environments.

### Features

- **Multi-tenant Architecture**: Complete isolation between organizations
- **Asset Management**: Comprehensive industrial asset tracking
- **Network Analysis**: Connection mapping and protocol analysis
- **Risk Assessment**: Automated risk scoring and monitoring
- **Document Management**: File uploads and document tracking
- **Reporting**: Customizable reports and dashboards
- **API Integration**: REST APIs for external integrations
- **Security**: Role-based access control and audit logging

## 🚀 Quick Start

**Quick Start?** Go to [Quick Start Guide](docs/QUICK_START.md) for a quick installation **in less than 5 minutes**.

### Prerequisites
- Docker and Docker Compose
- 4GB RAM minimum (8GB recommended)
- 20GB disk space minimum

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd industrace

# Start the application
docker-compose up -d

# Access the application
open http://localhost:5173
```

### Default Credentials
- **URL**: http://localhost:5173
- **Email**: admin@example.com
- **Password**: admin123

## Documentation

Complete documentation is available in the [docs](docs/) directory:

- [Installation Guide](docs/installation.md)
- [API Documentation](docs/api-documentation.md)
- [Docker Deployment](docs/docker-deployment.md)
- [Configuration Guide](docs/configuration.md)
- [Troubleshooting](docs/troubleshooting.md)

## API

Industrace provides a comprehensive REST API with OpenAPI documentation:

- **API Documentation**: http://localhost:8000/docs
- **API Reference**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Architecture

- **Backend**: FastAPI + PostgreSQL
- **Frontend**: Vue 3 + PrimeVue
- **Database**: PostgreSQL 15+
- **Containerization**: Docker + Docker Compose
- **Authentication**: JWT with role-based access control

## License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**. This means you are free to use, modify, and distribute the software, but any modifications must also be released under the same license.

See the [LICENSE](LICENSE) file for details.

## Author and Support

- **Author**: Maurizio Bertaboni
- **Company**: BeSafe S.r.l.
- **Website**: https://besafe.it
- **Industrace Site**: https://besafe.it/industrace
- **Contact**: industrace@besafe.it

## Contributing

Industrace is open source and welcomes contributions! Please see our contributing guidelines for more information on how to get involved.

## Support

For support and questions:
1. Check the [troubleshooting guide](docs/troubleshooting.md)
2. Review the [API documentation](docs/api-documentation.md)
3. Check system logs: `docker-compose logs backend`
4. Verify system health: `curl http://localhost:8000/health`
5. Contact: industrace@besafe.it

---

**Industrace** - Configuration Management Database for Industrial Control Systems  
**Author**: Maurizio Bertaboni (BeSafe S.r.l.)  
**Website**: https://besafe.it/industrace  
**Contact**: industrace@besafe.it 