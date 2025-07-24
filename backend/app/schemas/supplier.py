# backend/schemas/supplier.py

from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional
from datetime import datetime
import uuid
import re
from app.errors.validation_errors import InvalidURLError, InvalidVATNumberError, InvalidTaxCodeError, InvalidPhoneError, InvalidEmailError


class SupplierBase(BaseModel):
    name: str = Field(..., max_length=255, description="Supplier name")
    description: Optional[str] = Field(None, max_length=10000, description="Supplier description")
    vat_number: Optional[str] = Field(None, max_length=50, description="VAT number")
    tax_code: Optional[str] = Field(None, max_length=50, description="Tax code")
    address: Optional[str] = Field(None, max_length=255, description="Address")
    city: Optional[str] = Field(None, max_length=100, description="City")
    zip_code: Optional[str] = Field(None, max_length=20, description="ZIP code")
    province: Optional[str] = Field(None, max_length=50, description="Province")
    country: Optional[str] = Field(None, max_length=100, description="Country")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")
    email: Optional[str] = Field(None, max_length=255, description="Email address")
    website: Optional[str] = Field(None, max_length=255, description="Website URL")
    notes: Optional[str] = Field(None, max_length=10000, description="Notes")

    @validator('phone')
    def validate_phone(cls, v):
        if v is None or v == "":
            return v
        # Rimuovi spazi e caratteri speciali per la validazione
        phone_clean = re.sub(r'[\s\-\(\)\+]', '', v)
        # Verifica che contenga solo numeri e sia di lunghezza ragionevole
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

    @validator('vat_number')
    def validate_vat_number(cls, v):
        if v is None or v == "":
            return v
        # Verifica formato base per P.IVA italiana (11 cifre)
        if not re.match(r'^[A-Z]{2}\d{11}$', v.upper()):
            raise InvalidVATNumberError('vat_number')
        return v.upper()

    @validator('tax_code')
    def validate_tax_code(cls, v):
        if v is None or v == "":
            return v
        # Verifica formato codice fiscale italiano (16 caratteri alfanumerici)
        if not re.match(r'^[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]$', v.upper()):
            raise InvalidTaxCodeError('tax_code')
        return v.upper()

    @validator('email')
    def validate_email(cls, v):
        if v is None or v == "":
            return v
        # Verifica formato email base
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise InvalidEmailError('email')
        return v.lower()


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255, description="Supplier name")
    description: Optional[str] = Field(None, max_length=10000, description="Supplier description")
    vat_number: Optional[str] = Field(None, max_length=50, description="VAT number")
    tax_code: Optional[str] = Field(None, max_length=50, description="Tax code")
    address: Optional[str] = Field(None, max_length=255, description="Address")
    city: Optional[str] = Field(None, max_length=100, description="City")
    zip_code: Optional[str] = Field(None, max_length=20, description="ZIP code")
    province: Optional[str] = Field(None, max_length=50, description="Province")
    country: Optional[str] = Field(None, max_length=100, description="Country")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")
    email: Optional[str] = Field(None, max_length=255, description="Email address")
    website: Optional[str] = Field(None, max_length=255, description="Website URL")
    notes: Optional[str] = Field(None, max_length=10000, description="Notes")

    @validator('phone')
    def validate_phone(cls, v):
        if v is None or v == "":
            return v
        phone_clean = re.sub(r'[\s\-\(\)\+]', '', v)
        if not re.match(r'^\+?[\d\s\-\(\)]{7,20}$', v):
            raise InvalidPhoneError('phone')
        return v

    @validator('website')
    def validate_website(cls, v):
        if v is None or v == "":
            return v
        if not re.match(r'^https?://[^\s/$.?#].[^\s]*$', v):
            raise InvalidURLError('website')
        return v

    @validator('vat_number')
    def validate_vat_number(cls, v):
        if v is None or v == "":
            return v
        if not re.match(r'^[A-Z]{2}\d{11}$', v.upper()):
            raise InvalidVATNumberError('vat_number')
        return v.upper()

    @validator('tax_code')
    def validate_tax_code(cls, v):
        if v is None or v == "":
            return v
        if not re.match(r'^[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]$', v.upper()):
            raise InvalidTaxCodeError('tax_code')
        return v.upper()

    @validator('email')
    def validate_email(cls, v):
        if v is None or v == "":
            return v
        # Verifica formato email base
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise InvalidEmailError('email')
        return v.lower()


class SupplierDocumentBase(BaseModel):
    filename: str
    filepath: str


class SupplierDocumentCreate(SupplierDocumentBase):
    tenant_id: uuid.UUID


class SupplierDocument(SupplierDocumentBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    uploaded_at: datetime

    class Config:
        orm_mode = True


class Supplier(SupplierBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    documents: List[SupplierDocument] = []

    class Config:
        orm_mode = True


# Update forward references
Supplier.update_forward_refs()
SupplierDocument.update_forward_refs()
