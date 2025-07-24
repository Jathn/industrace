import uuid
from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import TenantSMTPConfig, Tenant, User
from app.schemas.tenant_smtp_config import (
    TenantSMTPConfigRead,
    TenantSMTPConfigCreate,
    TenantSMTPConfigUpdate,
)
from app.services.auth import get_current_user
from app.errors.exceptions import ErrorCodeException
from app.errors.error_codes import ErrorCode
from pydantic import EmailStr
import smtplib
from email.message import EmailMessage

router = APIRouter(
    prefix="/smtp-config",
    tags=["smtp-config"],
)


@router.get("", response_model=TenantSMTPConfigRead)
def get_smtp_config(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    config = (
        db.query(TenantSMTPConfig)
        .filter(TenantSMTPConfig.tenant_id == current_user.tenant_id)
        .first()
    )
    if not config:
        raise ErrorCodeException(
            status_code=404, error_code=ErrorCode.SMTP_CONFIG_NOT_FOUND
        )
    return config


@router.post("", response_model=TenantSMTPConfigRead)
def set_smtp_config(
    config_in: TenantSMTPConfigCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    config = (
        db.query(TenantSMTPConfig)
        .filter(TenantSMTPConfig.tenant_id == current_user.tenant_id)
        .first()
    )
    if config:
        for field, value in config_in.dict().items():
            setattr(config, field, value)
    else:
        config = TenantSMTPConfig(**config_in.dict(), tenant_id=current_user.tenant_id)
        db.add(config)
    db.commit()
    db.refresh(config)
    return config


@router.post("/test")
def test_smtp_config(
    to_email: EmailStr,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    config = (
        db.query(TenantSMTPConfig)
        .filter(TenantSMTPConfig.tenant_id == current_user.tenant_id)
        .first()
    )
    if not config:
        raise ErrorCodeException(
            status_code=404, error_code=ErrorCode.SMTP_CONFIG_NOT_FOUND
        )
    try:
        msg = EmailMessage()
        msg["Subject"] = "Test SMTP"
        msg["From"] = config.from_email
        msg["To"] = to_email
        msg.set_content("This is an SMTP test email.")
        with smtplib.SMTP(config.host, config.port) as server:
            if config.use_tls:
                server.starttls()
            server.login(config.username, config.password)
            server.send_message(msg)
        return {"detail": "Test email sent"}
    except Exception as e:
        raise ErrorCodeException(status_code=400, error_code=ErrorCode.SMTP_SEND_ERROR)
