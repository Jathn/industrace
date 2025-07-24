from app.database import get_db
from app.models.asset_type import AssetType


def setup_asset_types():
    db = next(get_db())
    from app.models import Tenant

    # Get the first tenant (Demo Tenant)
    tenant = db.query(Tenant).first()
    if not tenant:
        # print("No tenant found. Create a tenant first.")
        return

    tipi = [
        {
            "name": "PLC",
            "description": "Programmable Logic Controller",
            "purdue_level": 1,
        },
        {"name": "HMI", "description": "Human Machine Interface", "purdue_level": 2},
        {"name": "Gateway", "description": "Industrial Gateway", "purdue_level": 1.5},
        {
            "name": "Switch",
            "description": "Industrial network switch",
            "purdue_level": 1,
        },
        {"name": "Server", "description": "Server", "purdue_level": 3},
        {"name": "Workstation", "description": "Workstation", "purdue_level": 3},
        {"name": "Firewall", "description": "Firewall", "purdue_level": 2},
        {"name": "Router", "description": "Router", "purdue_level": 2},
        {"name": "Sensor", "description": "Field Sensor", "purdue_level": 0},
        {"name": "Actuator", "description": "Field Actuator", "purdue_level": 0},
    ]
    for tipo in tipi:
        if (
            not db.query(AssetType)
            .filter_by(name=tipo["name"], tenant_id=tenant.id)
            .first()
        ):
            db.add(AssetType(**tipo, tenant_id=tenant.id))
    db.commit()
    # print("Default asset types created for tenant:", tenant.name)
