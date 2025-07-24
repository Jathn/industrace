# backend/schemas/manufacturer.py

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
import uuid
import re
from app.errors.validation_errors import InvalidURLError, InvalidPhoneError, InvalidEmailError


class ManufacturerBase(BaseModel):
    name: str = Field(..., max_length=255, description="Manufacturer name")
    description: Optional[str] = Field(None, max_length=10000, description="Manufacturer description")
    website: Optional[str] = Field(None, max_length=255, description="Website URL")
    email: Optional[str] = Field(None, max_length=255, description="Email address")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")

    @validator('phone')
    def validate_phone(cls, v):
        if v is None or v == "":
            return v
        # Verifica formato numero di telefono
        if not re.match(r'^\+?[\d\s\-\(\)]{7,20}$', v):
            raise InvalidPhoneError('phone')
        return v

    @validator('website')
    def validate_website(cls, v):
        if v is None or v == "":
            return v
        # Verifica formato URL base
        if not re.match(r'^https?://[^\s/$.?#].[^\s]*$', v):
            raise InvalidURLError('website')
        return v

    @validator('email')
    def validate_email(cls, v):
        if v is None or v == "":
            return v
        # Verifica formato email base
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise InvalidEmailError('email')
        return v.lower()


class ManufacturerCreate(ManufacturerBase):
    pass


class ManufacturerUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    @validator('phone')
    def validate_phone(cls, v):
        if v is None or v == "":
            return v
        # Verifica formato numero di telefono
        if not re.match(r'^\+?[\d\s\-\(\)]{7,20}$', v):
            raise InvalidPhoneError('phone')
        return v

    @validator('website')
    def validate_website(cls, v):
        if v is None or v == "":
            return v
        # Verifica formato URL base
        if not re.match(r'^https?://[^\s/$.?#].[^\s]*$', v):
            raise InvalidURLError('website')
        return v

    @validator('email')
    def validate_email(cls, v):
        if v is None or v == "":
            return v
        # Verifica formato email base
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise InvalidEmailError('email')
        return v.lower()


class Manufacturer(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    description: Optional[str]
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
