"""
Database engine and session management.

We use SQLAlchemy 2.0 style with a declarative Base that all domain
models inherit from, and a scoped per-request session via FastAPI's
dependency injection (see api/deps.py).
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,   # avoids stale-connection errors on long-lived pools
    pool_size=10,
    max_overflow=20,
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


class Base(DeclarativeBase):
    """Base class for all ORM models. Import this, never create a second Base."""
    pass


def get_db_session():
    """Yields a DB session and guarantees it is closed after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
