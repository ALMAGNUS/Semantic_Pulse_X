"""
Configuration base de données - Semantic Pulse X
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.backend.core.config import settings

# Engine
engine = create_engine(
    settings.database_url,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base
Base = declarative_base()

# Metadata
metadata = MetaData()


async def init_db():
    """Initialisation de la base de données"""
    # Créer les tables
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dépendance pour obtenir une session DB"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
