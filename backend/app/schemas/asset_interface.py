from pydantic import BaseModel, Field, ConfigDict, validator
from typing import Optional, Dict, List
from datetime import datetime
from uuid import UUID
import re
import ipaddress
from app.errors.validation_errors import InvalidIPAddressError, InvalidMACAddressError, InvalidVLANError


class AssetInterfaceBase(BaseModel):
    name: Optional[str] = Field(None, max_length=50, description="Interface name")
    type: Optional[str] = Field(None, max_length=50, description="Interface type")
    vlan: Optional[str] = Field(None, max_length=50, description="VLAN")
    logical_port: Optional[str] = Field(None, max_length=100, description="Logical port")
    physical_plug_label: Optional[str] = Field(None, max_length=100, description="Physical plug label")
    details: Optional[Dict] = Field(default_factory=dict)
    ip_address: Optional[str] = Field(None, max_length=50, description="IP address")
    subnet_mask: Optional[str] = Field(None, max_length=50, description="Subnet mask")
    default_gateway: Optional[str] = Field(None, max_length=50, description="Default gateway")
    mac_address: Optional[str] = Field(None, max_length=50, description="MAC address")
    other: Optional[str] = Field(None, max_length=255, description="Other information")
    protocols: Optional[List[str]] = Field(default_factory=list, description="Industrial protocols supported by this interface")

    @validator('ip_address')
    def validate_ip_address(cls, v):
        if v is None or v == "":
            return v
        try:
            ipaddress.IPv4Address(v)
            return v
        except ipaddress.AddressValueError:
            raise InvalidIPAddressError('ip_address')

    @validator('subnet_mask')
    def validate_subnet_mask(cls, v):
        if v is None or v == "":
            return v
        try:
            ipaddress.IPv4Address(v)
            return v
        except ipaddress.AddressValueError:
            raise InvalidIPAddressError('subnet_mask')

    @validator('default_gateway')
    def validate_default_gateway(cls, v):
        if v is None or v == "":
            return v
        try:
            ipaddress.IPv4Address(v)
            return v
        except ipaddress.AddressValueError:
            raise InvalidIPAddressError('default_gateway')

    @validator('mac_address')
    def validate_mac_address(cls, v):
        if v is None or v == "":
            return v
        # Pattern per MAC address (xx:xx:xx:xx:xx:xx o xx-xx-xx-xx-xx-xx)
        mac_pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
        if not mac_pattern.match(v):
            raise InvalidMACAddressError('mac_address')
        return v

    @validator('vlan')
    def validate_vlan(cls, v):
        if v is None or v == "":
            return v
        # Pattern per VLAN (1-4094)
        vlan_pattern = re.compile(r'^([1-9]|[1-9]\d{1,2}|[1-3]\d{3}|40[0-9][0-4])$')
        if not vlan_pattern.match(v):
            raise InvalidVLANError('vlan')
        return v


class AssetInterfaceCreate(AssetInterfaceBase):
    asset_id: UUID
    tenant_id: UUID


class AssetInterfaceUpdate(AssetInterfaceBase):
    id: Optional[UUID] = None


class AssetInterface(AssetInterfaceBase):
    id: UUID
    asset_id: UUID
    tenant_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
