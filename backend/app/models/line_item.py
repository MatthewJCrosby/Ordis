from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, ForeignKey, func, Numeric
from app.db import Base
from decimal import Decimal



class LineItem(Base):
    __tablename__ = "line_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    qty: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)
    product = relationship("Product", back_populates="line_items", lazy="selectin")

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    order = relationship("Order", back_populates="line_items", lazy="selectin")


def calculate_line_item_total(self) -> Decimal:
    return self.price * self.qty
