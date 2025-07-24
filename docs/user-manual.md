# User Manual

## Overview

This user manual provides comprehensive guidance for using Industrace, the Configuration Management Database for Industrial Control Systems. Whether you're a system administrator, asset manager, or security analyst, this guide will help you effectively use all features of the platform.

## Table of Contents

1. [Getting Started](#getting-started)
2. [User Interface Overview](#user-interface-overview)
3. [Asset Management](#asset-management)
4. [Network Analysis](#network-analysis)
5. [Risk Assessment](#risk-assessment)
6. [Document Management](#document-management)
7. [Reporting and Dashboards](#reporting-and-dashboards)
8. [Search and Filtering](#search-and-filtering)
9. [User Management](#user-management)
10. [Best Practices](#best-practices)

## Getting Started

### First Login

1. **Access the Application**
   - Open your web browser
   - Navigate to your Industrace instance (e.g., http://localhost:5173)
   - Use the default credentials:
     - **Email**: admin@example.com
     - **Password**: admin123

2. **Change Default Password**
   - Go to User Settings (top-right menu)
   - Select "Change Password"
   - Enter a strong password
   - Save changes

3. **Complete Initial Setup**
   - Configure your organization details
   - Set up initial asset types and statuses
   - Create your first locations and sites

### Navigation Basics

- **Top Navigation Bar**: Access main sections and user menu
- **Sidebar**: Quick navigation between modules
- **Breadcrumbs**: Shows current location in the application
- **Search Bar**: Global search across all assets
- **User Menu**: Settings, profile, and logout

## User Interface Overview

### Dashboard

The main dashboard provides an overview of your industrial assets:

- **Asset Statistics**: Total assets by type and status
- **Risk Overview**: Assets by risk level
- **Recent Activity**: Latest changes and updates
- **Quick Actions**: Common tasks and shortcuts
- **System Health**: Database and service status

### Main Sections

1. **Assets**: Core asset management
2. **Network**: Connection and communication analysis
3. **Locations**: Physical location management
4. **Reports**: Analytics and reporting
5. **Administration**: System configuration

## Asset Management

### Creating Assets

1. **Navigate to Assets**
   - Click "Assets" in the main menu
   - Click "Add New Asset" button

2. **Basic Information**
   - **Name**: Descriptive asset name
   - **Type**: Select from predefined types
   - **Status**: Current operational status
   - **Criticality**: Impact level if asset fails
   - **Location**: Physical location assignment

3. **Technical Details**
   - **Manufacturer**: Equipment manufacturer
   - **Model**: Specific model number
   - **Serial Number**: Unique identifier
   - **IP Address**: Network address (if applicable)
   - **MAC Address**: Hardware identifier

4. **Additional Information**
   - **Description**: Detailed description
   - **Notes**: Additional notes
   - **Tags**: Custom tags for organization

### Asset Types

Common asset types include:
- **PLC**: Programmable Logic Controllers
- **HMI**: Human Machine Interfaces
- **SCADA**: Supervisory Control Systems
- **RTU**: Remote Terminal Units
- **Network Equipment**: Switches, routers, firewalls
- **Servers**: Industrial servers and workstations
- **Sensors**: Industrial sensors and instruments
- **Actuators**: Valves, motors, pumps

### Asset Status Management

Track asset lifecycle with statuses:
- **Operational**: Normal operation
- **Maintenance**: Under maintenance
- **Retired**: No longer in use
- **Spare**: Available spare equipment
- **Faulty**: Equipment with issues

### Asset Relationships

1. **Connections**: Network connections between assets
2. **Dependencies**: Assets that depend on others
3. **Locations**: Physical placement relationships
4. **Suppliers**: Vendor relationships

## Network Analysis

### Connection Management

1. **View Connections**
   - Navigate to "Network" section
   - Select "Connections" tab
   - View connection graph or table

2. **Add Connections**
   - Select source asset
   - Choose connection type
   - Specify destination asset
   - Add connection details

3. **Connection Types**
   - **Ethernet**: Network connections
   - **Serial**: Serial communications
   - **Wireless**: Wireless connections
   - **Fieldbus**: Industrial fieldbus protocols

### Communication Analysis

1. **PCAP Upload**
   - Upload network capture files
   - Analyze communication patterns
   - Identify protocols and traffic

2. **Protocol Detection**
   - Automatic protocol identification
   - Traffic analysis
   - Security assessment

3. **Network Topology**
   - Visual network maps
   - Connection graphs
   - Dependency analysis

## Risk Assessment

### Risk Scoring

Industrace automatically calculates risk scores based on:
- **Asset Criticality**: Impact of failure
- **Network Exposure**: Connection complexity
- **Age and Maintenance**: Equipment condition
- **Security Vulnerabilities**: Known issues

### Risk Levels

- **Low**: Minimal risk, standard monitoring
- **Medium**: Moderate risk, enhanced monitoring
- **High**: Significant risk, priority attention
- **Critical**: Maximum risk, immediate action required

### Risk Management

1. **Review Risk Reports**
   - Access risk dashboard
   - Review high-risk assets
   - Analyze risk trends

2. **Mitigation Actions**
   - Document mitigation strategies
   - Track improvement actions
   - Monitor risk reduction

## Document Management

### File Uploads

1. **Asset Documents**
   - Upload manuals and specifications
   - Store maintenance records
   - Archive technical documentation

2. **Photo Management**
   - Upload asset photos
   - Document physical condition
   - Create visual inventory

3. **File Organization**
   - Use descriptive filenames
   - Organize by asset type
   - Maintain version control

### Document Types

- **Manuals**: Equipment manuals and guides
- **Specifications**: Technical specifications
- **Certificates**: Compliance certificates
- **Reports**: Analysis and assessment reports
- **Photos**: Visual documentation

## Reporting and Dashboards

### Standard Reports

1. **Asset Inventory**
   - Complete asset listing
   - Filtered by type, location, status
   - Export to CSV/PDF

2. **Risk Assessment**
   - Risk level distribution
   - High-risk asset identification
   - Trend analysis

3. **Network Analysis**
   - Connection mapping
   - Protocol distribution
   - Traffic analysis

### Custom Dashboards

1. **Create Dashboards**
   - Select relevant widgets
   - Configure data sources
   - Set refresh intervals

2. **Widget Types**
   - Charts and graphs
   - Data tables
   - Status indicators
   - Quick action buttons

### Export Options

- **CSV**: Data export for analysis
- **PDF**: Formatted reports
- **Print**: Physical documentation
- **API**: Programmatic access

## Search and Filtering

### Global Search

1. **Quick Search**
   - Use search bar in header
   - Search across all assets
   - Real-time results

2. **Advanced Search**
   - Multiple criteria
   - Date ranges
   - Status filters

### Filtering Options

1. **Asset Filters**
   - By type, status, location
   - By risk level, criticality
   - By manufacturer, model

2. **Network Filters**
   - By connection type
   - By protocol
   - By traffic volume

3. **Date Filters**
   - Creation date
   - Last modified
   - Maintenance dates

## User Management

### User Roles

1. **Administrator**
   - Full system access
   - User management
   - System configuration

2. **Manager**
   - Asset management
   - Report generation
   - User supervision

3. **Operator**
   - Asset viewing
   - Basic reporting
   - Limited editing

4. **Viewer**
   - Read-only access
   - Basic search
   - Report viewing

### User Permissions

- **Asset Management**: Create, edit, delete assets
- **Network Analysis**: View and analyze connections
- **Reporting**: Generate and export reports
- **User Management**: Manage other users
- **System Administration**: Configure system settings

## Best Practices

### Asset Documentation

1. **Consistent Naming**
   - Use descriptive names
   - Include location information
   - Follow naming conventions

2. **Complete Information**
   - Fill all relevant fields
   - Include serial numbers
   - Document relationships

3. **Regular Updates**
   - Update status changes
   - Record maintenance activities
   - Keep information current

### Network Management

1. **Connection Documentation**
   - Document all connections
   - Include protocol information
   - Update when changes occur

2. **Security Monitoring**
   - Regular network analysis
   - Monitor for anomalies
   - Document security incidents

### Risk Management

1. **Regular Assessments**
   - Monthly risk reviews
   - Quarterly assessments
   - Annual comprehensive review

2. **Action Tracking**
   - Document mitigation actions
   - Track progress
   - Verify effectiveness

### Data Quality

1. **Validation**
   - Verify information accuracy
   - Cross-reference data
   - Regular audits

2. **Backup**
   - Regular data exports
   - Document backups
   - Test restoration procedures

## Troubleshooting

### Common Issues

1. **Login Problems**
   - Check credentials
   - Verify account status
   - Contact administrator

2. **Performance Issues**
   - Clear browser cache
   - Check network connection
   - Contact support

3. **Data Issues**
   - Verify data entry
   - Check for duplicates
   - Review validation rules

### Getting Help

1. **Documentation**
   - Check this manual
   - Review online help
   - Search knowledge base

2. **Support**
   - Contact: industrace@besafe.it
   - Website: https://besafe.it/industrace
   - Check system logs

3. **Community**
   - User forums
   - Best practices sharing
   - Feature requests

---

**Industrace** - Configuration Management Database for Industrial Control Systems  
**Author**: Maurizio Bertaboni (BeSafe S.r.l.)  
**Website**: https://besafe.it/industrace  
**Contact**: industrace@besafe.it 