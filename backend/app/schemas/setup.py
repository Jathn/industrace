from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from app.errors.validation_errors import InvalidTenantSlugError, InvalidPasswordError


class SetupStatus(BaseModel):
    """Stato del sistema per il setup"""
    is_configured: bool
    tenant_count: int
    user_count: int
    role_count: int
    database_connected: bool
    error: Optional[str] = None


class SetupRequest(BaseModel):
    """Dati per l'inizializzazione del sistema"""
    tenant_name: str
    tenant_slug: str
    admin_name: str
    admin_email: EmailStr
    admin_password: str
    language: str = "en"
    
    @validator('tenant_slug')
    def validate_tenant_slug(cls, v):
        if not v.replace('-', '').replace('_', '').isalnum():
            raise InvalidTenantSlugError('tenant_slug')
        return v.lower()
    
    @validator('admin_password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise InvalidPasswordError('admin_password')
        return v


class SetupResponse(BaseModel):
    """Risposta dell'inizializzazione"""
    success: bool
    message: str
    tenant_id: str
    admin_user_id: str 