from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from database.db import Base

class TenantUser(Base):
    __tablename__ = "tenant_users"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)

    role = Column(String(50), nullable=False)
    # TENANT_ADMIN | PM | BA | DEV

    user = relationship("User", back_populates="tenant_memberships")
    tenant = relationship("Tenant", back_populates="users")
