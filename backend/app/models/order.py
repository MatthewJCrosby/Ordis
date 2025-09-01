from __future__ import annotations
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Numeric, String, Integer, DateTime, ForeignKey, func
from app.db import Base



class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False, index=True)
    customer = relationship("Customer", back_populates="orders", lazy="selectin")
    service_tech_id: Mapped[int | None] = mapped_column(ForeignKey("employees.id", ondelete="SET NULL"), index=True, nullable=True)
    service_tech = relationship("Employee", back_populates="orders", lazy="selectin")
    line_items = relationship("LineItem", back_populates="order", lazy="selectin", cascade="all, delete-orphan", passive_deletes=True)
    total: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=True)

    def update_total(self): 
        if not self.line_items:
            self.total = Decimal('0.00')
        else:
            total_value = sum(item.price * item.qty for item in self.line_items)
            self.total = Decimal(str(total_value))