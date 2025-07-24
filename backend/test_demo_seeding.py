#!/usr/bin/env python3
"""
Test script for demo data seeding
Run this script to test the demo data seeding functionality
"""

import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.init_demo_data import seed_demo_data, seed_demo_data_sql, seed_demo_data_python
from app.database import SessionLocal
from app.models import Tenant, User, Site, Area, Asset, Manufacturer, Supplier, Contact

def test_demo_seeding():
    """Test the demo data seeding functionality"""
    print("🧪 Testing demo data seeding...")
    
    # Test SQL seeding first
    print("\n1. Testing SQL seeding...")
    if seed_demo_data_sql():
        print("✅ SQL seeding successful")
    else:
        print("⚠️  SQL seeding failed, will test Python seeding")
    
    # Test Python seeding
    print("\n2. Testing Python seeding...")
    try:
        seed_demo_data_python()
        print("✅ Python seeding successful")
    except Exception as e:
        print(f"❌ Python seeding failed: {e}")
        return False
    
    # Verify data was created
    print("\n3. Verifying seeded data...")
    db = SessionLocal()
    
    try:
        # Check tenant
        tenant = db.query(Tenant).first()
        if tenant:
            print(f"✅ Tenant found: {tenant.name}")
        else:
            print("❌ No tenant found")
            return False
        
        # Check users
        users = db.query(User).all()
        print(f"✅ Users found: {len(users)}")
        for user in users:
            print(f"   - {user.email} ({user.role.name})")
        
        # Check sites
        sites = db.query(Site).all()
        print(f"✅ Sites found: {len(sites)}")
        for site in sites:
            print(f"   - {site.name}")
        
        # Check areas
        areas = db.query(Area).all()
        print(f"✅ Areas found: {len(areas)}")
        
        # Check manufacturers
        manufacturers = db.query(Manufacturer).all()
        print(f"✅ Manufacturers found: {len(manufacturers)}")
        
        # Check suppliers
        suppliers = db.query(Supplier).all()
        print(f"✅ Suppliers found: {len(suppliers)}")
        
        # Check contacts
        contacts = db.query(Contact).all()
        print(f"✅ Contacts found: {len(contacts)}")
        
        # Check assets
        assets = db.query(Asset).all()
        print(f"✅ Assets found: {len(assets)}")
        
        print("\n🎉 Demo data seeding test completed successfully!")
        print("\n🔑 Login credentials:")
        print("   • Admin: admin@example.com / admin123")
        print("   • Editor: editor@example.com / editor123")
        print("   • Viewer: viewer@example.com / viewer123")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = test_demo_seeding()
    sys.exit(0 if success else 1) 