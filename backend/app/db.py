from typing import Generator
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from flask import current_app

NAMING = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
})

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