import uuid
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import (
    User, Role, Tenant, Asset, Location, Site, Area, 
    Supplier, Manufacturer, Contact, AssetType, AssetStatus
)
from app.services.auth import get_password_hash
from datetime import datetime, timedelta
import random


def seed_demo_data():
    """Populate database with realistic demo data in English"""
    db: Session = SessionLocal()
    
    print("🌱 Seeding demo data...")
    
    # Get or create tenant
    tenant = db.query(Tenant).first()
    if not tenant:
        tenant = Tenant(
            id=uuid.uuid4(),
            name="Industrial Solutions Corp",
            slug="industrial-solutions",
            settings={"theme": "industrial", "language": "en"}
        )
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        print(f"✅ Created tenant: {tenant.name}")
    
    # Get roles
    admin_role = db.query(Role).filter_by(name="admin").first()
    editor_role = db.query(Role).filter_by(name="editor").first()
    viewer_role = db.query(Role).filter_by(name="viewer").first()
    
    # Get asset types and statuses
    asset_types = db.query(AssetType).all()
    asset_statuses = db.query(AssetStatus).all()
    
    # Create demo sites
    sites_data = [
        {
            "name": "Main Production Plant",
            "description": "Primary manufacturing facility for automotive components",
            "address": "123 Industrial Blvd, Detroit, MI 48201",
            "contact_email": "plant.manager@industrialsolutions.com",
            "contact_phone": "+1-313-555-0100"
        },
        {
            "name": "Research & Development Center",
            "description": "Innovation hub for new product development",
            "address": "456 Tech Park Dr, Austin, TX 78701",
            "contact_email": "rd.director@industrialsolutions.com",
            "contact_phone": "+1-512-555-0200"
        },
        {
            "name": "Distribution Warehouse",
            "description": "Central logistics and distribution facility",
            "address": "789 Logistics Way, Chicago, IL 60601",
            "contact_email": "warehouse.manager@industrialsolutions.com",
            "contact_phone": "+1-312-555-0300"
        }
    ]
    
    sites = []
    for site_data in sites_data:
        existing_site = db.query(Site).filter_by(name=site_data["name"], tenant_id=tenant.id).first()
        if not existing_site:
            site = Site(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                name=site_data["name"],
                description=site_data["description"],
                address=site_data["address"],
                contact_email=site_data["contact_email"],
                contact_phone=site_data["contact_phone"]
            )
            db.add(site)
            sites.append(site)
            print(f"✅ Created site: {site.name}")
        else:
            sites.append(existing_site)
    
    db.commit()
    
    # Create demo areas for each site
    areas_data = [
        # Main Production Plant areas
        {"name": "Assembly Line A", "description": "Primary assembly line for engine components"},
        {"name": "Assembly Line B", "description": "Secondary assembly line for transmission parts"},
        {"name": "Quality Control Lab", "description": "Testing and quality assurance facility"},
        {"name": "Maintenance Bay", "description": "Equipment maintenance and repair area"},
        {"name": "Control Room", "description": "Central monitoring and control center"},
        
        # R&D Center areas
        {"name": "Prototype Lab", "description": "New product prototyping and testing"},
        {"name": "Materials Lab", "description": "Material science research and testing"},
        {"name": "Software Development", "description": "Control system software development"},
        {"name": "Testing Chamber", "description": "Environmental and stress testing"},
        
        # Warehouse areas
        {"name": "Receiving Dock", "description": "Incoming goods receiving area"},
        {"name": "Storage Zone A", "description": "High-value component storage"},
        {"name": "Storage Zone B", "description": "Bulk material storage"},
        {"name": "Shipping Dock", "description": "Outgoing shipments area"}
    ]
    
    areas = []
    for i, area_data in enumerate(areas_data):
        site_index = i // 5  # Distribute areas across sites
        site = sites[site_index] if site_index < len(sites) else sites[0]
        
        existing_area = db.query(Area).filter_by(name=area_data["name"], site_id=site.id).first()
        if not existing_area:
            area = Area(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                site_id=site.id,
                name=area_data["name"],
                description=area_data["description"]
            )
            db.add(area)
            areas.append(area)
            print(f"✅ Created area: {area.name} in {site.name}")
        else:
            areas.append(existing_area)
    
    db.commit()
    
    # Create demo suppliers
    suppliers_data = [
        {
            "name": "Siemens Industrial Automation",
            "description": "Leading provider of industrial automation and control systems",
            "website": "https://www.siemens.com/industrial-automation",
            "email": "sales@siemens-automation.com",
            "phone": "+1-800-333-7421",
            "address": "1000 Deerfield Parkway, Buffalo Grove, IL 60089"
        },
        {
            "name": "Rockwell Automation",
            "description": "Global provider of industrial automation and information solutions",
            "website": "https://www.rockwellautomation.com",
            "email": "info@rockwellautomation.com",
            "phone": "+1-414-382-2000",
            "address": "1201 South Second Street, Milwaukee, WI 53204"
        },
        {
            "name": "Schneider Electric",
            "description": "Energy management and automation solutions provider",
            "website": "https://www.se.com",
            "email": "contact@schneider-electric.com",
            "phone": "+1-888-778-2733",
            "address": "800 Federal Street, Andover, MA 01810"
        },
        {
            "name": "ABB Robotics",
            "description": "Robotics and automation technology solutions",
            "website": "https://www.abb.com/robotics",
            "email": "robotics@abb.com",
            "phone": "+1-248-391-9000",
            "address": "1250 Brown Road, Auburn Hills, MI 48326"
        }
    ]
    
    suppliers = []
    for supplier_data in suppliers_data:
        existing_supplier = db.query(Supplier).filter_by(name=supplier_data["name"], tenant_id=tenant.id).first()
        if not existing_supplier:
            supplier = Supplier(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                name=supplier_data["name"],
                description=supplier_data["description"],
                website=supplier_data["website"],
                email=supplier_data["email"],
                phone=supplier_data["phone"],
                address=supplier_data["address"]
            )
            db.add(supplier)
            suppliers.append(supplier)
            print(f"✅ Created supplier: {supplier.name}")
        else:
            suppliers.append(existing_supplier)
    
    db.commit()
    
    # Create demo contacts
    contacts_data = [
        {"name": "John Smith", "email": "john.smith@siemens-automation.com", "phone": "+1-555-0101", "role": "Sales Manager"},
        {"name": "Sarah Johnson", "email": "sarah.johnson@rockwellautomation.com", "phone": "+1-555-0102", "role": "Technical Support"},
        {"name": "Mike Davis", "email": "mike.davis@schneider-electric.com", "phone": "+1-555-0103", "role": "Account Manager"},
        {"name": "Lisa Wilson", "email": "lisa.wilson@abb.com", "phone": "+1-555-0104", "role": "Project Engineer"},
        {"name": "David Brown", "email": "david.brown@industrialsolutions.com", "phone": "+1-555-0105", "role": "Plant Manager"},
        {"name": "Emily Taylor", "email": "emily.taylor@industrialsolutions.com", "phone": "+1-555-0106", "role": "Maintenance Supervisor"}
    ]
    
    contacts = []
    for contact_data in contacts_data:
        existing_contact = db.query(Contact).filter_by(email=contact_data["email"], tenant_id=tenant.id).first()
        if not existing_contact:
            contact = Contact(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                name=contact_data["name"],
                email=contact_data["email"],
                phone=contact_data["phone"],
                role=contact_data["role"]
            )
            db.add(contact)
            contacts.append(contact)
            print(f"✅ Created contact: {contact.name}")
        else:
            contacts.append(existing_contact)
    
    db.commit()
    
    # Create demo assets
    assets_data = [
        {
            "name": "PLC Controller S7-1500",
            "description": "Siemens S7-1500 Programmable Logic Controller for assembly line control",
            "serial_number": "S7-1500-2024-001",
            "model": "S7-1515-2 PN",
            "manufacturer": "Siemens",
            "location": "Assembly Line A",
            "status": "Operational",
            "criticality": "High",
            "installation_date": datetime.now() - timedelta(days=365),
            "last_maintenance": datetime.now() - timedelta(days=30)
        },
        {
            "name": "HMI Panel KTP900",
            "description": "Siemens KTP900 Basic HMI panel for operator interface",
            "serial_number": "KTP900-2024-002",
            "model": "KTP900 Basic PN",
            "manufacturer": "Siemens",
            "location": "Control Room",
            "status": "Operational",
            "criticality": "Medium",
            "installation_date": datetime.now() - timedelta(days=300),
            "last_maintenance": datetime.now() - timedelta(days=15)
        },
        {
            "name": "Variable Frequency Drive",
            "description": "Rockwell PowerFlex 755 AC drive for motor control",
            "serial_number": "PF755-2024-003",
            "model": "PowerFlex 755",
            "manufacturer": "Rockwell Automation",
            "location": "Assembly Line B",
            "status": "Operational",
            "criticality": "High",
            "installation_date": datetime.now() - timedelta(days=250),
            "last_maintenance": datetime.now() - timedelta(days=45)
        },
        {
            "name": "Safety Relay Module",
            "description": "Schneider Electric safety relay for emergency stop systems",
            "serial_number": "SR-2024-004",
            "model": "XPSMC",
            "manufacturer": "Schneider Electric",
            "location": "Assembly Line A",
            "status": "Operational",
            "criticality": "Critical",
            "installation_date": datetime.now() - timedelta(days=400),
            "last_maintenance": datetime.now() - timedelta(days=60)
        },
        {
            "name": "Industrial Robot IRB 2600",
            "description": "ABB IRB 2600 industrial robot for material handling",
            "serial_number": "IRB2600-2024-005",
            "model": "IRB 2600-20/1.65",
            "manufacturer": "ABB",
            "location": "Assembly Line B",
            "status": "Maintenance",
            "criticality": "High",
            "installation_date": datetime.now() - timedelta(days=200),
            "last_maintenance": datetime.now() - timedelta(days=5)
        },
        {
            "name": "Network Switch",
            "description": "Industrial Ethernet switch for network connectivity",
            "serial_number": "SW-2024-006",
            "model": "Scalance X208",
            "manufacturer": "Siemens",
            "location": "Control Room",
            "status": "Operational",
            "criticality": "Medium",
            "installation_date": datetime.now() - timedelta(days=180),
            "last_maintenance": datetime.now() - timedelta(days=20)
        },
        {
            "name": "Temperature Sensor",
            "description": "RTD temperature sensor for process monitoring",
            "serial_number": "TS-2024-007",
            "model": "PT100",
            "manufacturer": "Rockwell Automation",
            "location": "Quality Control Lab",
            "status": "Operational",
            "criticality": "Low",
            "installation_date": datetime.now() - timedelta(days=150),
            "last_maintenance": datetime.now() - timedelta(days=10)
        },
        {
            "name": "Pressure Transmitter",
            "description": "Smart pressure transmitter for hydraulic system monitoring",
            "serial_number": "PT-2024-008",
            "model": "3051S",
            "manufacturer": "Rockwell Automation",
            "location": "Maintenance Bay",
            "status": "Operational",
            "criticality": "Medium",
            "installation_date": datetime.now() - timedelta(days=120),
            "last_maintenance": datetime.now() - timedelta(days=25)
        }
    ]
    
    for asset_data in assets_data:
        # Find area by name
        area = db.query(Area).filter_by(name=asset_data["location"], tenant_id=tenant.id).first()
        if not area:
            area = areas[0]  # Default to first area if not found
        
        # Find asset type and status
        asset_type = random.choice(asset_types) if asset_types else None
        asset_status = db.query(AssetStatus).filter_by(name=asset_data["status"]).first()
        
        # Find supplier by manufacturer name
        supplier = db.query(Supplier).filter(
            Supplier.name.contains(asset_data["manufacturer"]),
            Supplier.tenant_id == tenant.id
        ).first()
        
        existing_asset = db.query(Asset).filter_by(serial_number=asset_data["serial_number"], tenant_id=tenant.id).first()
        if not existing_asset:
            asset = Asset(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                area_id=area.id,
                name=asset_data["name"],
                description=asset_data["description"],
                serial_number=asset_data["serial_number"],
                model=asset_data["model"],
                manufacturer_name=asset_data["manufacturer"],
                supplier_id=supplier.id if supplier else None,
                asset_type_id=asset_type.id if asset_type else None,
                asset_status_id=asset_status.id if asset_status else None,
                business_criticality=asset_data["criticality"],
                installation_date=asset_data["installation_date"],
                last_maintenance_date=asset_data["last_maintenance"],
                is_active=True
            )
            db.add(asset)
            print(f"✅ Created asset: {asset.name}")
    
    db.commit()
    db.close()
    
    print("🎉 Demo data seeding completed successfully!")
    print("\n📊 Demo Data Summary:")
    print(f"   • Sites: {len(sites)}")
    print(f"   • Areas: {len(areas)}")
    print(f"   • Suppliers: {len(suppliers)}")
    print(f"   • Contacts: {len(contacts)}")
    print(f"   • Assets: {len(assets_data)}")
    print("\n🔑 Login with demo credentials:")
    print("   • Admin: admin@demo.com / admin123")
    print("   • Editor: editor@demo.com / editor123")
    print("   • Viewer: viewer@demo.com / viewer123")


if __name__ == "__main__":
    seed_demo_data() 