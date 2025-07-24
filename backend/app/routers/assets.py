import uuid
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, Request, UploadFile, File, Form
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
import pandas as pd
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import User, Asset, AssetCommunication
from app.services.audit_decorator import audit_log_action
from app.schemas import (
    AssetRead as AssetSchema,
    AssetCreate,
    AssetUpdate,
    AssetCustomFieldUpdate,
    AssetRead,
    PositionUpdate,
)
from app.services.auth import get_current_user
from app.services.audit_log import create_audit_log
from app.crud import assets as crud_assets
from app.errors.exceptions import ErrorCodeException
from app.errors.error_codes import ErrorCode
from app.schemas.asset_status import AssetStatus as AssetStatusSchema
from app.schemas.contact import Contact as ContactSchema
from app.schemas.asset import AssetBulkUpdateRequest, AssetBulkSoftDeleteRequest
from app.schemas.asset import RiskScoreRequest, RiskScoreResponse, RiskOverviewResponse
from app.services.risk_scoring import CompositeRiskScoringEngine
import io
import json
import math
from app.models.asset_interface import AssetInterface
from app.models.print_history import PrintHistory
from app.models.supplier import Supplier
from app.schemas.supplier import Supplier as SupplierSchema

router = APIRouter(
    prefix="/assets",
    tags=["assets"],
)


# Create asset
@router.post("", response_model=AssetSchema)
@audit_log_action("create", "Asset", model_class=Asset)
def create_asset(
    asset_in: AssetCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Inserisco tenant_id nel body
    data = asset_in.dict()
    data["tenant_id"] = current_user.tenant_id
    return crud_assets.create_asset(db, AssetCreate(**data), current_user.tenant_id)


# List assets (with optional filters)
@router.get("", response_model=List[AssetSchema])
def list_assets(
    skip: int = 0,
    limit: int = 100,
    status_id: Optional[uuid.UUID] = None,
    site_id: Optional[uuid.UUID] = None,
    area_id: Optional[uuid.UUID] = None,
    global_search: Optional[str] = None,
    business_criticality: Optional[str] = None,
    risk_score_min: Optional[float] = None,
    risk_score_max: Optional[float] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = (
        db.query(Asset)
        .options(
            joinedload(Asset.interfaces),
            joinedload(Asset.site),
            joinedload(Asset.location),
            joinedload(Asset.status),
            joinedload(Asset.manufacturer),
            joinedload(Asset.asset_type),
        )
        .filter(Asset.tenant_id == current_user.tenant_id, Asset.deleted_at == None)
    )

    # Filtri specifici
    if status_id:
        query = query.filter(Asset.status_id == status_id)
    if site_id:
        query = query.filter(Asset.site_id == site_id)
    if area_id:
        query = query.filter(Asset.area_id == area_id)
    if business_criticality:
        query = query.filter(Asset.business_criticality == business_criticality)
    if risk_score_min is not None:
        query = query.filter(Asset.risk_score >= risk_score_min)
    if risk_score_max is not None:
        query = query.filter(Asset.risk_score <= risk_score_max)

    # Ricerca globale
    if global_search:
        search_term = f"%{global_search}%"
        from sqlalchemy import or_

        query = query.filter(or_(Asset.name.ilike(search_term)))

    assets = query.offset(skip).limit(limit).all()
    if assets:
        # Aggiungi i campi area_name e area_code a ogni asset
        result = []
        for asset in assets:
            asset_dict = AssetRead.from_orm(asset).dict()
            if asset.area_id:
                from app.models.area import Area
                area = db.query(Area).filter(Area.id == asset.area_id).first()
                if area:
                    asset_dict["area_name"] = area.name
                    asset_dict["area_code"] = area.code
            result.append(asset_dict)
        return result
    return []


# Trash: lista asset eliminati
@router.get("/trash", response_model=List[AssetSchema])
def list_assets_trash(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(Asset)
        .filter(Asset.tenant_id == current_user.tenant_id, Asset.deleted_at != None)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/risk-overview", response_model=RiskOverviewResponse)
def get_risk_overview(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Restituisce l'overview generale del risk scoring (nuova logica composita)"""
    assets = (
        db.query(Asset)
        .filter(Asset.tenant_id == current_user.tenant_id, Asset.deleted_at == None)
        .all()
    )

    risk_engine = CompositeRiskScoringEngine()

    # Calculate risk score for all assets
    total_score = 0
    high_risk_count = 0
    medium_risk_count = 0
    low_risk_count = 0

    for asset in assets:
        breakdown = risk_engine.calculate(asset)
        risk_score = breakdown["final_score"]
        if risk_score is not None:
            total_score += risk_score
            # Update asset if the score has changed
            if asset.risk_score != risk_score:
                asset.risk_score = risk_score
                asset.last_risk_assessment = datetime.utcnow()
            # Count by risk level
            if risk_score >= 7:
                high_risk_count += 1
            elif risk_score >= 4:
                medium_risk_count += 1
            else:
                low_risk_count += 1

    db.commit()

    # Top 10 risky assets
    top_risk_assets = sorted(assets, key=lambda x: x.risk_score or 0, reverse=True)[:10]
    top_risk_data = []
    for asset in top_risk_assets:
        top_risk_data.append(
            {
                "id": str(asset.id),
                "name": asset.name,
                "risk_score": asset.risk_score,
                "risk_level": (
                    "alto"
                    if asset.risk_score is not None and asset.risk_score >= 7
                    else (
                        "medio"
                        if asset.risk_score is not None and asset.risk_score >= 4
                        else "basso"
                    )
                ),
                "business_criticality": getattr(asset, "business_criticality", None),
                "site_name": asset.site.name if asset.site else None,
            }
        )

    return RiskOverviewResponse(
        high_risk_count=high_risk_count,
        medium_risk_count=medium_risk_count,
        low_risk_count=low_risk_count,
        total_assets=len(assets),
        average_risk_score=round(total_score / len(assets), 2) if assets else 0,
        top_risk_assets=top_risk_data,
    )


@router.post("/recalculate-all-risk-scores")
def recalculate_all_risk_scores(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Recalculate the risk score for all tenant assets (new composite logic)"""
    assets = (
        db.query(Asset)
        .filter(Asset.tenant_id == current_user.tenant_id, Asset.deleted_at == None)
        .all()
    )

    risk_engine = CompositeRiskScoringEngine()
    updated_count = 0

    for asset in assets:
        breakdown = risk_engine.calculate(asset)
        new_score = breakdown["final_score"]
        old_score = asset.risk_score
        if new_score is not None and old_score != new_score:
            asset.risk_score = new_score
            asset.last_risk_assessment = datetime.utcnow()
            updated_count += 1

    db.commit()

    return {
        "message": f"Risk scores ricalcolati per {updated_count} asset su {len(assets)} totali",
        "updated_count": updated_count,
        "total_count": len(assets),
    }


@router.delete("/trash/empty")
@audit_log_action("empty_trash", "Asset", model_class=Asset)
def empty_assets_trash(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    from app.models.asset_interface import AssetInterface
    from app.models.asset_document import AssetDocument
    from app.models.asset_photo import AssetPhoto
    from app.models.asset_connection import AssetConnection
    from app.models.asset_communication import AssetCommunication
    from app.models.contact import Contact

    assets = (
        db.query(Asset)
        .filter(Asset.tenant_id == current_user.tenant_id, Asset.deleted_at != None)
        .all()
    )
    count = 0
    for asset in assets:
        # Delete communications where the asset's interfaces are involved
        interface_ids = [
            i.id
            for i in db.query(AssetInterface).filter(
                AssetInterface.asset_id == asset.id
            )
        ]
        if interface_ids:
            db.query(AssetCommunication).filter(
                (AssetCommunication.src_interface_id.in_(interface_ids))
                | (AssetCommunication.dst_interface_id.in_(interface_ids))
            ).delete(synchronize_session=False)
        # Delete connections where the asset is involved
        db.query(AssetConnection).filter(
            (AssetConnection.parent_asset_id == asset.id)
            | (AssetConnection.child_asset_id == asset.id)
        ).delete(synchronize_session=False)
        # Delete documents
        db.query(AssetDocument).filter(AssetDocument.asset_id == asset.id).delete(
            synchronize_session=False
        )
        # Delete photos
        db.query(AssetPhoto).filter(AssetPhoto.asset_id == asset.id).delete(
            synchronize_session=False
        )
        # Delete interfaces
        db.query(AssetInterface).filter(AssetInterface.asset_id == asset.id).delete(
            synchronize_session=False
        )
        # Delete associated contacts (many-to-many table)
        asset.contacts = []
        # Delete print history connected
        db.query(PrintHistory).filter(PrintHistory.asset_id == asset.id).delete(
            synchronize_session=False
        )
        db.delete(asset)
        count += 1
    db.commit()
    return {"detail": f"Trash emptied: {count} assets deleted"}


@router.post("/import/xlsx/preview")
def import_assets_xlsx_preview(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from sqlalchemy import func
    from app.models.manufacturer import Manufacturer
    from app.models.asset_interface import AssetInterface
    import os

    try:
        filename = file.filename.lower()
        if filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        else:
            df = pd.read_excel(file.file, engine="openpyxl")
    except Exception as e:
        return {"error": f"Errore nella lettura del file: {str(e)}"}
    to_create, to_update, errors = [], [], []
    for idx, row in df.iterrows():
        name = row.get("nome") or row.get("name")
        tag = row.get("tag")
        site_code = row.get("site_code")
        asset_type_name = row.get("asset_type") or row.get("asset_type_name")
        ip_address = row.get("ip_address")
        manufacturer_name = row.get("manufacturer")
        missing = []
        # Handle NaN, None, empty string
        if pd.isna(name) or name is None or str(name).strip() == "":
            missing.append("name")
        if pd.isna(site_code) or site_code is None or str(site_code).strip() == "":
            missing.append("site_code")
        if (
            pd.isna(asset_type_name)
            or asset_type_name is None
            or str(asset_type_name).strip() == ""
        ):
            missing.append("asset_type")
        site_id = None
        asset_type_id = None
        manufacturer_id = None
        # Validation of site_code and asset_type
        if not missing:
            from app.crud.sites import get_site_by_code

            site = get_site_by_code(db, current_user.tenant_id, site_code)
            if not site:
                errors.append(
                    {
                        "row": int(idx) + 2,
                        "error": f"Site con code '{site_code}' non trovato",
                    }
                )
            else:
                site_id = site.id
            from app.models.asset_type import AssetType

            asset_type = (
                db.query(AssetType)
                .filter(
                    AssetType.name == asset_type_name,
                    (AssetType.tenant_id == current_user.tenant_id)
                    | (AssetType.tenant_id == None),
                )
                .first()
            )
            if not asset_type:
                errors.append(
                    {
                        "row": int(idx) + 2,
                        "error": f"AssetType con name '{asset_type_name}' non trovato",
                    }
                )
            else:
                asset_type_id = asset_type.id
        # Validation/lookup/creation of manufacturer
        if not missing and manufacturer_name and str(manufacturer_name).strip() != "":
            manufacturer = (
                db.query(Manufacturer)
                .filter(
                    func.lower(Manufacturer.name)
                    == str(manufacturer_name).strip().lower(),
                    Manufacturer.tenant_id == current_user.tenant_id,
                )
                .first()
            )
            if not manufacturer:
                # We don't really create the manufacturer in preview, but we report that it will be created
                manufacturer_id = None
                manufacturer_action = "create"
            else:
                manufacturer_id = manufacturer.id
                manufacturer_action = "use_existing"
        else:
            manufacturer_action = None
        if missing or not site_id or not asset_type_id:
            if missing:
                errors.append(
                    {
                        "row": int(idx) + 2,
                        "error": f"Campi obbligatori mancanti: {', '.join(missing)}",
                    }
                )
            continue
        # Search asset only if tag is filled
        if tag is not None and not pd.isna(tag) and str(tag).strip() != "":
            asset = (
                db.query(Asset)
                .filter(Asset.tag == tag, Asset.tenant_id == current_user.tenant_id)
                .first()
            )
        else:
            asset = None
        # Prepare preview of interfaces
        interfaces = []
        if ip_address and not pd.isna(ip_address) and str(ip_address).strip() != "":
            interfaces.append(
                {
                    "name": "LAN",
                    "type": "ethernet",
                    "ip_address": str(ip_address).strip(),
                }
            )
        if asset:
            diff = {}
            for field, new in [
                ("name", name),
                ("site_id", site_id),
                ("asset_type_id", asset_type_id),
                ("manufacturer", manufacturer_name),
            ]:
                old = getattr(asset, field, None)
                if field == "manufacturer":
                    # compare the manufacturer name
                    old_manuf = asset.manufacturer.name if asset.manufacturer else None
                    if (
                        str(old_manuf).strip().lower()
                        != str(manufacturer_name).strip().lower()
                    ):
                        diff[field] = {"old": old_manuf, "new": manufacturer_name}
                else:
                    if str(old) != str(new):
                        diff[field] = {"old": old, "new": new}
            if diff or interfaces:
                to_update.append(
                    {
                        "tag": tag,
                        "diff": diff,
                        "interfaces": interfaces,
                        "manufacturer_action": manufacturer_action,
                    }
                )
        else:
            to_create.append(
                {
                    "name": name,
                    "tag": tag,
                    "site_id": str(site_id),
                    "asset_type_id": str(asset_type_id),
                    "manufacturer": manufacturer_name,
                    "manufacturer_action": manufacturer_action,
                    "interfaces": interfaces,
                }
            )
    return sanitize_for_json(
        {"to_create": to_create, "to_update": to_update, "errors": errors}
    )


@router.post("/import/xlsx/confirm")
@audit_log_action("import_assets_xlsx_confirm", "Asset", model_class=Asset)
def import_assets_xlsx_confirm(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from app.models.manufacturer import Manufacturer
    from app.models.asset_interface import AssetInterface
    from sqlalchemy import func
    import os

    try:
        filename = file.filename.lower()
        if filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        else:
            df = pd.read_excel(file.file, engine="openpyxl")
    except Exception as e:
        return {"error": f"Errore nella lettura del file: {str(e)}"}
    created, updated, errors = [], [], []
    for idx, row in df.iterrows():
        name = row.get("nome") or row.get("name")
        tag = row.get("tag")
        site_code = row.get("site_code")
        asset_type_name = row.get("asset_type") or row.get("asset_type_name")
        ip_address = row.get("ip_address")
        manufacturer_name = row.get("manufacturer")
        missing = []
        if pd.isna(name) or name is None or str(name).strip() == "":
            missing.append("name")
        if pd.isna(site_code) or site_code is None or str(site_code).strip() == "":
            missing.append("site_code")
        if (
            pd.isna(asset_type_name)
            or asset_type_name is None
            or str(asset_type_name).strip() == ""
        ):
            missing.append("asset_type")
        site_id = None
        asset_type_id = None
        manufacturer_id = None
        if not missing:
            from app.crud.sites import get_site_by_code

            site = get_site_by_code(db, current_user.tenant_id, site_code)
            if not site:
                errors.append(
                    {
                        "row": int(idx) + 2,
                        "error": f"Site con code '{site_code}' non trovato",
                    }
                )
            else:
                site_id = site.id
            from app.models.asset_type import AssetType

            asset_type = (
                db.query(AssetType)
                .filter(
                    AssetType.name == asset_type_name,
                    (AssetType.tenant_id == current_user.tenant_id)
                    | (AssetType.tenant_id == None),
                )
                .first()
            )
            if not asset_type:
                errors.append(
                    {
                        "row": int(idx) + 2,
                        "error": f"AssetType con name '{asset_type_name}' non trovato",
                    }
                )
            else:
                asset_type_id = asset_type.id
        # Lookup/creazione manufacturer
        if not missing and manufacturer_name and str(manufacturer_name).strip() != "":
            manufacturer = (
                db.query(Manufacturer)
                .filter(
                    func.lower(Manufacturer.name)
                    == str(manufacturer_name).strip().lower(),
                    Manufacturer.tenant_id == current_user.tenant_id,
                )
                .first()
            )
            if not manufacturer:
                try:
                    manufacturer = Manufacturer(
                        name=str(manufacturer_name).strip(),
                        tenant_id=current_user.tenant_id,
                    )
                    db.add(manufacturer)
                    db.commit()
                    db.refresh(manufacturer)
                except Exception as e:
                    db.rollback()
                    errors.append(
                        {
                            "row": int(idx) + 2,
                            "error": f"Errore creazione manufacturer: {str(e)}",
                        }
                    )
                    continue
            manufacturer_id = manufacturer.id
        if missing or not site_id or not asset_type_id:
            if missing:
                errors.append(
                    {
                        "row": int(idx) + 2,
                        "error": f"Campi obbligatori mancanti: {', '.join(missing)}",
                    }
                )
            continue
        # Search assets only if tag is provided
        if tag is not None and not pd.isna(tag) and str(tag).strip() != "":
            asset = (
                db.query(Asset)
                .filter(Asset.tag == tag, Asset.tenant_id == current_user.tenant_id)
                .first()
            )
        else:
            asset = None
        try:
            if asset:
                asset.name = name
                asset.site_id = site_id
                asset.asset_type_id = asset_type_id
                if manufacturer_id:
                    asset.manufacturer_id = manufacturer_id
                db.commit()
                updated.append(tag)
                # If ip_address present, create LAN interface if not already present
                if (
                    ip_address
                    and not pd.isna(ip_address)
                    and str(ip_address).strip() != ""
                ):
                    existing_iface = (
                        db.query(AssetInterface)
                        .filter(
                            AssetInterface.asset_id == asset.id,
                            func.lower(AssetInterface.name) == "lan",
                            AssetInterface.type == "ethernet",
                            AssetInterface.ip_address == str(ip_address).strip(),
                        )
                        .first()
                    )
                    if not existing_iface:
                        interface = AssetInterface(
                            asset_id=asset.id,
                            name="LAN",
                            type="ethernet",
                            ip_address=str(ip_address).strip(),
                            tenant_id=current_user.tenant_id,
                        )
                        db.add(interface)
                        db.commit()
            else:
                new_asset = Asset(
                    name=name,
                    tag=tag,
                    site_id=site_id,
                    asset_type_id=asset_type_id,
                    tenant_id=current_user.tenant_id,
                    manufacturer_id=manufacturer_id,
                )
                db.add(new_asset)
                db.commit()
                created.append(tag)
                # If ip_address present, create LAN interface if not already present
                if (
                    ip_address
                    and not pd.isna(ip_address)
                    and str(ip_address).strip() != ""
                ):
                    interface = AssetInterface(
                        asset_id=new_asset.id,
                        name="LAN",
                        type="ethernet",
                        ip_address=str(ip_address).strip(),
                        tenant_id=current_user.tenant_id,
                    )
                    db.add(interface)
                    db.commit()
        except IntegrityError as e:
            db.rollback()
            errors.append(
                {"row": int(idx) + 2, "error": f"Errore di integrità: {str(e)}"}
            )
        except Exception as e:
            db.rollback()
            errors.append({"row": int(idx) + 2, "error": str(e)})
    return sanitize_for_json({"created": created, "updated": updated, "errors": errors})


@router.post("/bulk-update")
@audit_log_action("bulk_update", "Asset", model_class=Asset)
def bulk_update_assets(
    req: AssetBulkUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated, errors = [], []

    # Get the field names for the description
    field_names = []
    for field in req.fields.keys():
        field_labels = {
            "manufacturer_id": "produttore",
            "asset_status_id": "stato",
            "site_id": "sito",
            "location_id": "posizione",
            "asset_type_id": "tipo",
            "risk_score": "risk score",
            "purdue_level": "livello Purdue",
            "impact_value": "valore impatto",
            "access_ease": "facilità accesso",
            "exposure_level": "livello esposizione",
            "update_status": "stato aggiornamento",
        }
        field_names.append(field_labels.get(field, field))

    for asset_id in req.ids:
        asset = (
            db.query(Asset)
            .filter(Asset.id == asset_id, Asset.tenant_id == current_user.tenant_id)
            .first()
        )
        if not asset:
            errors.append({"id": str(asset_id), "error": "Asset non trovato"})
            continue

        # Prepare old data with names
        old_data = {}
        for field in req.fields.keys():
            if hasattr(asset, field):
                old_data[field] = getattr(asset, field)

        # Apply the changes
        for field, value in req.fields.items():
            if hasattr(asset, field):
                setattr(asset, field, value)

        try:
            db.commit()
            updated.append(str(asset_id))

            # Create readable description
            asset_name = asset.name or str(asset_id)
            fields_text = ", ".join(field_names)
            description = (
                f"Aggiornamento massivo: modificati {fields_text} per '{asset_name}'"
            )

            # Audit log with automatic translation
            create_audit_log(
                db=db,
                user_id=current_user.id,
                tenant_id=current_user.tenant_id,
                action="bulk_update",
                entity="Asset",
                entity_id=asset_id,
                old_data=old_data,
                new_data=req.fields,
                description=description,
            )
        except Exception as e:
            db.rollback()
            errors.append({"id": str(asset_id), "error": str(e)})

    return {"updated": updated, "errors": errors}


# Bulk soft delete
@router.post("/bulk-soft-delete")
@audit_log_action("bulk_soft_delete", "Asset", model_class=Asset)
def bulk_soft_delete_assets(
    req: AssetBulkSoftDeleteRequest,  # Riutilizziamo lo stesso schema per gli ID
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted, errors = [], []

    for asset_id in req.ids:
        asset = (
            db.query(Asset)
            .filter(
                Asset.id == asset_id, 
                Asset.tenant_id == current_user.tenant_id,
                Asset.deleted_at == None
            )
            .first()
        )
        if not asset:
            errors.append({"id": str(asset_id), "error": "Asset non trovato o già nel cestino"})
            continue

        try:
            # Soft delete
            asset.deleted_at = datetime.utcnow()
            
            # Create readable description
            asset_name = asset.name or str(asset_id)
            description = f"Asset '{asset_name}' spostato nel cestino"

            # Commit the soft delete
            db.commit()
            deleted.append(str(asset_id))

            # Create audit log after successful commit
            try:
                create_audit_log(
                    db=db,
                    user_id=current_user.id,
                    tenant_id=current_user.tenant_id,
                    action="soft_delete",
                    entity="Asset",
                    entity_id=asset_id,
                    old_data={"deleted_at": None},
                    new_data={"deleted_at": asset.deleted_at.isoformat()},
                    description=description,
                )
            except Exception as audit_error:
                # Log audit error but don't rollback the soft delete
                # print(f"Audit log error for asset {asset_id}: {audit_error}")
                pass
                
        except Exception as e:
            db.rollback()
            errors.append({"id": str(asset_id), "error": str(e)})

    return {"deleted": deleted, "errors": errors}


# Get single asset
@router.get("/{asset_id}", response_model=AssetRead)
def get_asset(
    asset_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    asset = crud_assets.get_asset(db, asset_id)
    if not asset or asset.tenant_id != current_user.tenant_id:
        raise ErrorCodeException(status_code=404, error_code=ErrorCode.ASSET_NOT_FOUND)
    
    # Carica l'area se l'asset ha un area_id
    if asset.area_id:
        from app.models.area import Area
        area = db.query(Area).filter(Area.id == asset.area_id).first()
        if area:
            # Assegna direttamente i campi dell'area all'asset
            asset.area_name = area.name
            asset.area_code = area.code
    
    return asset


# Update asset
@router.put("/{asset_id}", response_model=AssetSchema)
@audit_log_action("update", "Asset", model_class=Asset)
def update_asset(
    asset_id: uuid.UUID,
    asset_update: AssetUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    asset = crud_assets.get_asset(db, asset_id)
    if not asset:
        raise ErrorCodeException(status_code=404, error_code=ErrorCode.ASSET_NOT_FOUND)
    return crud_assets.update_asset(db, asset_id, asset_update, current_user.tenant_id)


# Soft delete
@router.delete("/{asset_id}")
@audit_log_action("soft_delete", "Asset", model_class=Asset)
def soft_delete_asset(
    asset_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    asset = (
        db.query(Asset)
        .filter(
            Asset.id == asset_id,
            Asset.tenant_id == current_user.tenant_id,
            Asset.deleted_at == None,
        )
        .first()
    )
    if not asset:
        raise ErrorCodeException(status_code=404, error_code=ErrorCode.ASSET_NOT_FOUND)
    asset.deleted_at = datetime.utcnow()
    db.commit()
    return {"detail": "Asset moved to trash"}


# Restore
@router.patch("/{asset_id}/restore")
@audit_log_action("restore", "Asset", model_class=Asset)
def restore_asset(
    asset_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    asset = (
        db.query(Asset)
        .filter(
            Asset.id == asset_id,
            Asset.tenant_id == current_user.tenant_id,
            Asset.deleted_at != None,
        )
        .first()
    )
    if not asset:
        raise ErrorCodeException(status_code=404, error_code=ErrorCode.ASSET_NOT_FOUND)
    asset.deleted_at = None
    db.commit()
    return {"detail": "Asset restored"}


    # Hard delete (only if already in trash)
@router.delete("/{asset_id}/hard")
@audit_log_action("hard_delete", "Asset", model_class=Asset)
def hard_delete_asset(
    asset_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    asset = (
        db.query(Asset)
        .filter(
            Asset.id == asset_id,
            Asset.tenant_id == current_user.tenant_id,
            Asset.deleted_at != None,
        )
        .first()
    )
    if not asset:
        raise ErrorCodeException(status_code=404, error_code=ErrorCode.ASSET_NOT_FOUND)
    db.delete(asset)
    db.commit()
    return {"detail": "Asset deleted definitively"}


@router.patch("/{asset_id}/custom-fields", response_model=AssetSchema)
@audit_log_action("update_custom_fields", "Asset", model_class=Asset)
def patch_custom_fields(
    asset_id: uuid.UUID,
    custom_fields_update: AssetCustomFieldUpdate,
    db: Session = Depends(get_db),
):
    asset = crud_assets.update_asset_custom_fields(db, asset_id, custom_fields_update)
    if not asset:
        raise ErrorCodeException(status_code=404, error_code=ErrorCode.ASSET_NOT_FOUND)
    return asset


@router.patch("/{asset_id}/position")
@audit_log_action("update_position", "Asset", model_class=Asset)
def update_asset_position_endpoint(
    asset_id: uuid.UUID,
    position: PositionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    asset = crud_assets.update_asset_position(
        db, asset_id, position.map_x, position.map_y
    )
    if not asset or asset.tenant_id != current_user.tenant_id:
        raise ErrorCodeException(status_code=404, error_code=ErrorCode.ASSET_NOT_FOUND)
    return {"id": asset_id, "map_x": asset.map_x, "map_y": asset.map_y}


@router.get("/{asset_id}/communications")
def get_asset_communications(asset_id: uuid.UUID, db: Session = Depends(get_db)):
    # Check if asset exists
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise ErrorCodeException(status_code=404, error_code="ASSET_NOT_FOUND")

    # Find all interfaces of this asset
    interfaces = (
        db.query(AssetInterface).filter(AssetInterface.asset_id == asset_id).all()
    )
    interface_ids = [i.id for i in interfaces]
    if not interface_ids:
        return []

    # Search communications where one of the interfaces is involved
    comms = (
        db.query(AssetCommunication)
        .filter(
            (AssetCommunication.src_interface_id.in_(interface_ids))
            | (AssetCommunication.dst_interface_id.in_(interface_ids))
        )
        .all()
    )

    results = []
    for c in comms:
        # Retrieve all involved entities
        src_iface = c.src_interface
        dst_iface = c.dst_interface
        src_asset = (
            db.query(Asset).filter(Asset.id == src_iface.asset_id).first()
            if src_iface
            else None
        )
        dst_asset = (
            db.query(Asset).filter(Asset.id == dst_iface.asset_id).first()
            if dst_iface
            else None
        )
        if not src_asset or not dst_asset:
            continue
        # Direction relative to the requested asset
        if src_iface and src_iface.asset_id == asset_id:
            direction = "outgoing"
        elif dst_iface and dst_iface.asset_id == asset_id:
            direction = "incoming"
        else:
            direction = "unknown"
        results.append(
            {
                "src_asset": {"id": str(src_asset.id), "name": src_asset.name},
                "src_interface": (
                    {
                        "id": str(src_iface.id),
                        "name": src_iface.name,
                        "mac_address": src_iface.mac_address,
                        "ip_address": src_iface.ip_address,
                    }
                    if src_iface
                    else None
                ),
                "dst_asset": {"id": str(dst_asset.id), "name": dst_asset.name},
                "dst_interface": (
                    {
                        "id": str(dst_iface.id),
                        "name": dst_iface.name,
                        "mac_address": dst_iface.mac_address,
                        "ip_address": dst_iface.ip_address,
                    }
                    if dst_iface
                    else None
                ),
                "packet_count": c.packet_count,
                "direction": direction,
            }
        )

    return results


@router.get("/{asset_id}/contacts", response_model=List[ContactSchema])
def list_asset_contacts(
    asset_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    asset = (
        db.query(Asset)
        .filter(Asset.id == asset_id, Asset.tenant_id == current_user.tenant_id)
        .first()
    )
    if not asset:
        raise ErrorCodeException(status_code=404, error_code=ErrorCode.ASSET_NOT_FOUND)
    return [ContactSchema.from_orm(c) for c in asset.contacts]


@router.put("/{asset_id}/contacts", response_model=List[ContactSchema])
@audit_log_action("update_contacts", "Asset", model_class=Asset)
def update_asset_contacts(
    asset_id: uuid.UUID,
    contact_ids: List[uuid.UUID],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from app.models.contact import Contact

    asset = (
        db.query(Asset)
        .filter(Asset.id == asset_id, Asset.tenant_id == current_user.tenant_id)
        .first()
    )
    if not asset:
        raise ErrorCodeException(status_code=404, error_code=ErrorCode.ASSET_NOT_FOUND)
    contacts = (
        db.query(Contact)
        .filter(
            Contact.id.in_(contact_ids), Contact.tenant_id == current_user.tenant_id
        )
        .all()
    )
    asset.contacts = contacts
    db.commit()
    db.refresh(asset)
    return [ContactSchema.from_orm(c) for c in asset.contacts]


@router.delete("/{asset_id}/contacts/{contact_id}", status_code=204)
@audit_log_action("delete_contact", "Asset", model_class=Asset)
def delete_asset_contact(
    asset_id: uuid.UUID,
    contact_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    asset = (
        db.query(Asset)
        .filter(Asset.id == asset_id, Asset.tenant_id == current_user.tenant_id)
        .first()
    )
    if not asset:
        raise ErrorCodeException(status_code=404, error_code=ErrorCode.ASSET_NOT_FOUND)
    asset.contacts = [c for c in asset.contacts if c.id != contact_id]
    db.commit()
    return None


@router.get("/{asset_id}/suppliers", response_model=List[SupplierSchema])
def list_asset_suppliers(
    asset_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    asset = (
        db.query(Asset)
        .filter(Asset.id == asset_id, Asset.tenant_id == current_user.tenant_id)
        .first()
    )
    if not asset:
        raise ErrorCodeException(status_code=404, error_code=ErrorCode.ASSET_NOT_FOUND)
    return asset.suppliers


@router.put("/{asset_id}/suppliers", response_model=List[SupplierSchema])
@audit_log_action("update_suppliers", "Asset", model_class=Asset)
def update_asset_suppliers(
    asset_id: uuid.UUID,
    supplier_ids: List[uuid.UUID],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    asset = (
        db.query(Asset)
        .filter(Asset.id == asset_id, Asset.tenant_id == current_user.tenant_id)
        .first()
    )
    if not asset:
        raise ErrorCodeException(status_code=404, error_code=ErrorCode.ASSET_NOT_FOUND)
    suppliers = (
        db.query(Supplier)
        .filter(
            Supplier.id.in_(supplier_ids), Supplier.tenant_id == current_user.tenant_id
        )
        .all()
    )
    asset.suppliers = suppliers
    db.commit()
    db.refresh(asset)
    return asset.suppliers


@router.post("/{asset_id}/calculate-risk", response_model=RiskScoreResponse)
def calculate_asset_risk(
    asset_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Calculate the risk score for a single asset (new composite logic)"""
    asset = crud_assets.get_asset(db, asset_id)
    if not asset or asset.tenant_id != current_user.tenant_id:
        raise ErrorCodeException(status_code=404, error_code=ErrorCode.ASSET_NOT_FOUND)

    risk_engine = CompositeRiskScoringEngine()
    breakdown = risk_engine.calculate(asset)
    risk_score = breakdown["final_score"]
    # Determine level and severity
    if risk_score is None:
        risk_level = "undefined"
        risk_severity = "info"
    elif risk_score >= 7:
        risk_level = "high"
        risk_severity = "danger"
    elif risk_score >= 4:
        risk_level = "medium"
        risk_severity = "warning"
    else:
        risk_level = "low"
        risk_severity = "success"
    # Update asset only if risk_score is calculated
    if risk_score is not None:
        asset.risk_score = risk_score
        asset.last_risk_assessment = datetime.utcnow()
        db.commit()
    return RiskScoreResponse(
        asset_id=asset_id,
        risk_score=risk_score,
        risk_level=risk_level,
        risk_severity=risk_severity,
        breakdown=breakdown,
    )


def sanitize_for_json(obj):
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(x) for x in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    else:
        return obj
