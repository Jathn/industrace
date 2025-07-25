from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Asset, AssetStatus
from app.services.audit_decorator import audit_log_action
from app.services.auth import get_current_user
from app.services.audit_log import create_audit_log

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
)


# Dashboard endpoints
@router.get("/stats")
def get_dashboard_stats(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    from datetime import datetime, timedelta
    from sqlalchemy import func, and_
    
    # Statistiche base
    total_assets = (
        db.query(Asset).filter(Asset.tenant_id == current_user.tenant_id).count()
    )
    
    # Asset critici (business_criticality >= 4)
    critical_assets = (
        db.query(Asset)
        .filter(
            and_(
                Asset.tenant_id == current_user.tenant_id,
                Asset.business_criticality >= '4'
            )
        )
        .count()
    )
    
    # Asset a rischio (risk_score >= 7)
    assets_at_risk = (
        db.query(Asset)
        .filter(
            and_(
                Asset.tenant_id == current_user.tenant_id,
                Asset.risk_score >= 7
            )
        )
        .count()
    )
    
    # Modifiche recenti (ultime 24 ore)
    yesterday = datetime.utcnow() - timedelta(days=1)
    recent_changes = (
        db.query(Asset)
        .filter(
            and_(
                Asset.tenant_id == current_user.tenant_id,
                Asset.updated_at >= yesterday
            )
        )
        .count()
    )
    
    # Asset attivi/inattivi
    active_assets = (
        db.query(Asset)
        .join(AssetStatus)
        .filter(
            and_(
                Asset.tenant_id == current_user.tenant_id,
                AssetStatus.name == "Active"
            )
        )
        .count()
    )
    
    inactive_assets = total_assets - active_assets
    
    # Statistiche per status
    statuses = (
        db.query(AssetStatus)
        .filter(AssetStatus.tenant_id == current_user.tenant_id)
        .all()
    )
    status_stats = []
    for status in statuses:
        count = (
            db.query(Asset)
            .filter(
                Asset.tenant_id == current_user.tenant_id, 
                Asset.status_id == status.id
            )
            .count()
        )
        status_stats.append({
            "status_id": str(status.id),
            "name": status.name,
            "color": status.color,
            "count": count,
        })
    
    # Statistiche per tipo di asset
    from app.models import AssetType
    asset_types = (
        db.query(AssetType)
        .filter(AssetType.tenant_id == current_user.tenant_id)
        .all()
    )
    type_stats = []
    for asset_type in asset_types:
        count = (
            db.query(Asset)
            .filter(
                Asset.tenant_id == current_user.tenant_id, 
                Asset.asset_type_id == asset_type.id
            )
            .count()
        )
        type_stats.append({
            "type_id": str(asset_type.id),
            "name": asset_type.name,
            "asset_count": count,
        })
    
    return {
        "total_assets": total_assets,
        "critical_assets": critical_assets,
        "assets_at_risk": assets_at_risk,
        "recent_changes": recent_changes,
        "active_assets": active_assets,
        "inactive_assets": inactive_assets,
        "status_stats": status_stats,
        "type_stats": type_stats
    }


@router.get("/risky-assets")
def get_risky_assets(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Ottieni gli asset più a rischio"""
    from sqlalchemy import and_
    from sqlalchemy.orm import joinedload
    
    from app.models import AssetType, Site
    
    risky_assets = (
        db.query(Asset)
        .options(
            joinedload(Asset.interfaces),
            joinedload(Asset.asset_type),
            joinedload(Asset.site)
        )
        .filter(
            and_(
                Asset.tenant_id == current_user.tenant_id,
                Asset.risk_score >= 7
            )
        )
        .order_by(Asset.risk_score.desc())
        .limit(limit)
        .all()
    )
    
    return [
        {
            "id": str(asset.id),
            "name": asset.name,
            "risk_score": asset.risk_score,
            "business_criticality": asset.business_criticality,
            "asset_type_name": asset.asset_type.name if asset.asset_type else "N/A",
            "site_name": asset.site.name if asset.site else "N/A",
            "manufacturer_name": asset.manufacturer.name if asset.manufacturer else "N/A",
            "ip_address": asset.interfaces[0].ip_address if asset.interfaces else None,
            "created_at": asset.created_at.isoformat() if asset.created_at else None,
            "updated_at": asset.updated_at.isoformat() if asset.updated_at else None
        }
        for asset in risky_assets
    ]
