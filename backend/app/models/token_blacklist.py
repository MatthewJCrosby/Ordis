from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.db import Base



class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id: Mapped[int] = mapped_column(primary_key=True)
    jti: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

