from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, ForeignKey, func, Numeric, Enum
from app.db import Base
from decimal import Decimal
import enum


class DepartmentEnum(str, enum.Enum):
    CUSTOMER_SERVICE = 'Customer Service'
    SERVICE_TECHNICIAN = 'Service Technician'
    MANAGER = 'Manager'


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    department: Mapped[DepartmentEnum] = mapped_column(Enum(DepartmentEnum, name="department_enum"), nullable=False)
    orders = relationship("Order", back_populates="service_tech", lazy="selectin")
    
    user_id = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="employee", uselist=False)