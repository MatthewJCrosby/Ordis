from __future__ import annotations
import enum
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, String, DateTime, func
from app.db import Base

class UserTypeEnum(str, enum.Enum):
    CUSTOMER = 'Customer'
    EMPLOYEE = 'Employee'
    ADMIN = 'Admin'

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_login: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
    user_type: Mapped[UserTypeEnum] = mapped_column(Enum(UserTypeEnum, name="user_type_enum"), nullable=False, default=UserTypeEnum.CUSTOMER)

    customer = relationship("Customer", back_populates="user", uselist=False)
    employee = relationship("Employee", back_populates="user", uselist=False)