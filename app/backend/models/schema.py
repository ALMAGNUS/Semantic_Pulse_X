#!/usr/bin/env python3
"""
Schéma relationnel complet - SQLAlchemy ORM
Généré automatiquement par generate_orm_schema.py
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class DimPays(Base):
    """Table de dimension Pays"""
    __tablename__ = 'dim_pays'

    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False, unique=True)
    code_iso = Column(String(3), nullable=False, unique=True)

    # Relations
    contenus = relationship("Contenu", back_populates="pays")


class DimDomaine(Base):
    """Table de dimension Domaine"""
    __tablename__ = 'dim_domaine'

    id = Column(Integer, primary_key=True)
    nom = Column(String(50), nullable=False, unique=True)
    description = Column(Text)

    # Relations
    contenus = relationship("Contenu", back_populates="domaine")


class DimHumeur(Base):
    """Table de dimension Humeur"""
    __tablename__ = 'dim_humeur'

    id = Column(Integer, primary_key=True)
    nom = Column(String(30), nullable=False, unique=True)
    couleur = Column(String(7))  # #RRGGBB
    description = Column(Text)

    # Relations
    reactions = relationship("Reaction", back_populates="humeur")


class Source(Base):
    """Table Sources"""
    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False, unique=True)
    type = Column(String(20), nullable=False)  # 'api', 'scraping', 'file', 'bigdata'
    url_base = Column(String(500))
    actif = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relations
    contenus = relationship("Contenu", back_populates="source")


class Contenu(Base):
    """Table principale Contenus"""
    __tablename__ = 'contenus'

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey('sources.id'), nullable=False)
    pays_id = Column(Integer, ForeignKey('dim_pays.id'), nullable=False)
    domaine_id = Column(Integer, ForeignKey('dim_domaine.id'), nullable=False)

    url = Column(String(1000), nullable=False)
    titre = Column(Text, nullable=False)
    resume = Column(Text)
    texte = Column(Text, nullable=False)

    publication_date = Column(DateTime)
    auteur = Column(String(200))
    langue = Column(String(5), default='fr')
    collected_at = Column(DateTime, default=datetime.utcnow)

    # Champs GDELT
    sentiment = Column(String(30), default='neutre')
    confidence = Column(Float, default=0.0)
    themes = Column(Text)
    source_type = Column(String(50), default='web')

    # Relations
    source = relationship("Source", back_populates="contenus")
    pays = relationship("DimPays", back_populates="contenus")
    domaine = relationship("DimDomaine", back_populates="contenus")
    reactions = relationship("Reaction", back_populates="contenu")

    # Index pour performance
    __table_args__ = (
        Index('idx_contenus_source', 'source_id'),
        Index('idx_contenus_pays', 'pays_id'),
        Index('idx_contenus_domaine', 'domaine_id'),
        Index('idx_contenus_date', 'publication_date'),
        Index('idx_contenus_collected', 'collected_at'),
        Index('idx_contenus_sentiment', 'sentiment'),
        Index('idx_contenus_source_type', 'source_type'),
        UniqueConstraint('url', 'titre', name='uq_contenus_url_titre'),
    )


class Reaction(Base):
    """Table Réactions (analyses émotionnelles)"""
    __tablename__ = 'reactions'

    id = Column(Integer, primary_key=True)
    contenu_id = Column(Integer, ForeignKey('contenus.id'), nullable=False)
    humeur_id = Column(Integer, ForeignKey('dim_humeur.id'), nullable=False)

    score = Column(Float, nullable=False)  # Score émotionnel
    confidence = Column(Float, nullable=False)  # Confiance de l'analyse
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relations
    contenu = relationship("Contenu", back_populates="reactions")
    humeur = relationship("DimHumeur", back_populates="reactions")

    # Index pour performance
    __table_args__ = (
        Index('idx_reactions_contenu', 'contenu_id'),
        Index('idx_reactions_humeur', 'humeur_id'),
        Index('idx_reactions_date', 'created_at'),
    )
