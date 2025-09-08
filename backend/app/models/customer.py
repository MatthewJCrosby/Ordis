from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, DateTime, func
from app.db import Base

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    orders = relationship("Order", back_populates="customer", lazy="selectin", cascade="all, delete-orphan", passive_deletes=True)
    
    user_id = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="customer", uselist=False)



