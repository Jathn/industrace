import uuid
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path
import os

from app.database import get_db
from app.models import User, LocationFloorplan, Location
from app.schemas import LocationFloorplanCreate, LocationFloorplanRead
from app.services.auth import get_current_user
from app.errors.exceptions import ErrorCodeException
from app.errors.error_codes import ErrorCode
from app.services.audit_decorator import audit_log_action

router = APIRouter(
    prefix="/locations/{location_id}/floorplan",
    tags=["locations_floorplan"],
)
UPLOAD_DIR = Path("uploads")


def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)


@router.post("", response_model=LocationFloorplanRead)
@audit_log_action("create", "LocationFloorplan", model_class=LocationFloorplan)
def upload_floorplan(
    location_id: uuid.UUID,
    request: Request,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Verify location exists and belongs to tenant
    location = (
        db.query(Location)
        .filter_by(id=location_id, tenant_id=current_user.tenant_id)
        .first()
    )
    if not location:
        raise ErrorCodeException(
            status_code=404, error_code=ErrorCode.LOCATION_NOT_FOUND
        )

    # Check if there is already a floorplan for this location and tenant
    existing = (
        db.query(LocationFloorplan)
        .filter_by(location_id=location_id, tenant_id=current_user.tenant_id)
        .first()
    )
    if existing:
        # Delete old file
        old_path = UPLOAD_DIR / existing.file_path
        if old_path.exists():
            old_path.unlink()
        db.delete(existing)
        db.commit()

    # Generate unique filename and path
    unique_filename = f"{uuid.uuid4()}{Path(file.filename).suffix}"
    relative_path = (
        Path("tenants") / str(current_user.tenant_id) / "floorplans" / unique_filename
    )
    file_location = UPLOAD_DIR / relative_path

    # Save file to disk
    save_upload_file(file, file_location)

    # Create new floorplan record
    floorplan = LocationFloorplan(
        location_id=location_id,
        tenant_id=current_user.tenant_id,
        file_path=str(relative_path),
    )
    db.add(floorplan)
    db.commit()
    db.refresh(floorplan)

    return floorplan


@router.delete("/{floorplan_id}", status_code=204)
@audit_log_action("delete", "LocationFloorplan", model_class=LocationFloorplan)
def delete_floorplan(
    location_id: uuid.UUID,
    floorplan_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    floorplan = (
        db.query(LocationFloorplan)
        .filter_by(
            id=floorplan_id, location_id=location_id, tenant_id=current_user.tenant_id
        )
        .first()
    )
    if not floorplan:
        raise ErrorCodeException(
            status_code=404, error_code=ErrorCode.LOCATION_FLOORPLAN_NOT_FOUND
        )

    # Remove physical file
    file_path = UPLOAD_DIR / floorplan.file_path
    if file_path.exists():
        file_path.unlink()

    db.delete(floorplan)
    db.commit()

    return


@router.get("/{floorplan_id}")
def get_floorplan_file(
    location_id: uuid.UUID,
    floorplan_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    floorplan = (
        db.query(LocationFloorplan)
        .filter_by(
            id=floorplan_id, location_id=location_id, tenant_id=current_user.tenant_id
        )
        .first()
    )
    if not floorplan:
        raise ErrorCodeException(
            status_code=404, error_code=ErrorCode.LOCATION_FLOORPLAN_NOT_FOUND
        )

    full_path = UPLOAD_DIR / floorplan.file_path
    if not full_path.exists():
        raise ErrorCodeException(
            status_code=404, error_code=ErrorCode.LOCATION_FLOORPLAN_NOT_FOUND
        )

    return FileResponse(full_path)
