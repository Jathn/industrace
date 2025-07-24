from app.database import get_db
from app.models.asset_status import AssetStatus


def setup_asset_statuses():
    db = next(get_db())
    from app.models import Tenant

    # Get the first tenant (Demo Tenant)
    tenant = db.query(Tenant).first()
    if not tenant:
        # print("No tenant found. Create a tenant first.")
        return

    stati = [
        {"name": "Active", "description": "Operational asset"},
        {"name": "Disposed", "description": "Asset no longer in use"},
        {"name": "In stock", "description": "Asset in stock"},
        {"name": "Faulty", "description": "Faulty asset"},
        {"name": "In maintenance", "description": "Asset in maintenance"},
    ]
    for stato in stati:
        if (
            not db.query(AssetStatus)
            .filter_by(name=stato["name"], tenant_id=tenant.id)
            .first()
        ):
            db.add(AssetStatus(**stato, tenant_id=tenant.id))
    db.commit()
    # print("Stati asset predefiniti creati per il tenant:", tenant.name)
