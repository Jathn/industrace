import uuid
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class TenantSMTPConfig(Base):
    __tablename__ = "tenant_smtp_config"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(
        UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, unique=True
    )
    host = Column(String, nullable=False)
    port = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)  
    from_email = Column(String, nullable=False)
    use_tls = Column(Boolean, default=True)
    tenant = relationship("Tenant", back_populates="smtp_config")
