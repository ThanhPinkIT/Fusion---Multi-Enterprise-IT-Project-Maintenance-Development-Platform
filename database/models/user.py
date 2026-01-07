from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    email = Column(String(200), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    created_tasks = relationship(
        "Task",
        back_populates="creator",
        foreign_keys="Task.creator_id"
    )

    assigned_tasks = relationship(
        "Task",
        back_populates="assignee",
        foreign_keys="Task.assignee_id"
    )

    tenant_memberships = relationship(
    "TenantUser",
    back_populates="user",
    cascade="all, delete-orphan"
    )


    projects = relationship("Project", back_populates="owner")

    member_projects = relationship("ProjectMember", back_populates="user")
