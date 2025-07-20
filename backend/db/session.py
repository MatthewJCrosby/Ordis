# db/session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
from app.models import db  # <-- use db from your Flask app

# Load env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

# SQLAlchemy engine & session
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))
db_session = SessionLocal()


def init_db():
    import app.models  # triggers dynamic model load, required
    app.models.db.metadata.create_all(bind=engine)  # use db.metadata instead of Base.metadata
