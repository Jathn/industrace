# backend/app/init_tenant.py

import uuid
from app.database import SessionLocal
from app.models import Tenant, User
from app.services.auth import get_password_hash


def create_tenant_with_admin(
    tenant_name, tenant_slug, admin_email, admin_password, admin_name="Admin"
):
    db = SessionLocal()
    try:
        # Create tenant
        tenant = Tenant(name=tenant_name, slug=tenant_slug, settings={})
        db.add(tenant)
        db.flush()  # Get tenant.id

        # Create admin user
        admin_user = User(
            tenant_id=tenant.id,
            email=admin_email,
            password_hash=get_password_hash(admin_password),
            name=admin_name,
            role="admin",
        )
        db.add(admin_user)
        db.commit()
        # print(f"Tenant '{tenant_name}' created with id {tenant.id}")
        # print(f"Admin user '{admin_email}' created with id {admin_user.id}")
    except Exception as e:
        db.rollback()
        # print(f"Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    # Modify these values as needed
    create_tenant_with_admin(
        tenant_name="New Tenant",
        tenant_slug="new-tenant",
        admin_email="admin@demo.com",
        admin_password="admin123",
        admin_name="Super Admin",
    )
