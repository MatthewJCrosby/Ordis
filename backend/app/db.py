from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from flask import current_app

class Base(DeclarativeBase):
    pass

def _engine():
    url = current_app.config["DATABASE_URL"]
    echo = current_app.config.get("SQL_ECHO", False)
    return create_engine(url, echo=echo, future=True)

def _session_factory():
    return sessionmaker(bind=_engine(), autoflush=False, autocommit=False, expire_on_commit=False, future=True)

def get_session():
    return _session_factory()()