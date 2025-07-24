import uuid
from app.database import SessionLocal
from app.models import Tenant, User, Role
from app.services.auth import get_password_hash
from app.init_roles import seed_roles
from app.init_print_template import init_default_templates
from app.init_manufacturers import seed_manufacturers
from app.init_asset_statuses import setup_asset_statuses
from app.init_asset_types import setup_asset_types

ADMIN_EMAIL = "admin@demo.com"
EDITOR_EMAIL = "editor@demo.com"
VIEWER_EMAIL = "viewer@demo.com"
ADMIN_PASSWORD = "admin123"
EDITOR_PASSWORD = "editor123"
VIEWER_PASSWORD = "viewer123"
TENANT_NAME = "Demo Tenant"
TENANT_SLUG = "demo-tenant"


def setup_system():
    db = SessionLocal()
    # 1. Tenant
    tenant = db.query(Tenant).filter_by(slug=TENANT_SLUG).first()
    if not tenant:
        tenant = Tenant(
            id=uuid.uuid4(), name=TENANT_NAME, slug=TENANT_SLUG, settings={}
        )
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        # print(f"Tenant created: {TENANT_NAME}")
    else:
        # print(f"Tenant already exists: {TENANT_NAME}")
        pass
    tenant_id = tenant.id

    # 2. Roles
    seed_roles()
    roles = {r.name: r for r in db.query(Role).all()}

    # 3. Base users
    users = [
        {
            "name": "Admin",
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD,
            "role": "admin",
        },
        {
            "name": "Editor",
            "email": EDITOR_EMAIL,
            "password": EDITOR_PASSWORD,
            "role": "editor",
        },
        {
            "name": "Viewer",
            "email": VIEWER_EMAIL,
            "password": VIEWER_PASSWORD,
            "role": "viewer",
        },
    ]
    for u in users:
        existing = db.query(User).filter_by(email=u["email"]).first()
        if not existing:
            user = User(
                id=uuid.uuid4(),
                tenant_id=tenant_id,
                email=u["email"],
                password_hash=get_password_hash(u["password"]),
                name=u["name"],
                role_id=roles[u["role"]].id,
                is_active=True,
            )
            db.add(user)
            # print(f"User created: {u['email']} ({u['role']})")
        else:
            # print(f"User already exists: {u['email']}")
            pass
    db.commit()

    # 4. Print templates
    init_default_templates(tenant_id=tenant_id)

    # 5. Manufacturers ICS/OT
    seed_manufacturers()

    setup_asset_statuses()
    setup_asset_types()

    db.close()
    # print("\nSetup system completed!\nExample credentials:")
    # print(f"Admin: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
    # print(f"Editor: {EDITOR_EMAIL} / {EDITOR_PASSWORD}")
    # print(f"Viewer: {VIEWER_EMAIL} / {VIEWER_PASSWORD}")


if __name__ == "__main__":
    setup_system()
