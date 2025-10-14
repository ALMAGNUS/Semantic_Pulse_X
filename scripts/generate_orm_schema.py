#!/usr/bin/env python3
"""
Génération du schéma relationnel complet en SQLAlchemy ORM
Conforme aux exigences E1/E2/E3 (low-code, indépendant)

Tables de dimension:
- dim_pays (id, nom, code_iso)
- dim_domaine (id, nom, description)
- dim_humeur (id, nom, couleur, description)

Tables principales:
- sources (id, nom, type, url_base, actif)
- contenus (id, source_id, pays_id, domaine_id, url, titre, resume, texte,
           publication_date, auteur, langue, collected_at)
- reactions (id, contenu_id, humeur_id, score, confidence, created_at)

Usage:
  python scripts/generate_orm_schema.py --output-dir app/backend/models
"""

import argparse
from datetime import datetime
from pathlib import Path

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


def generate_schema_file(output_dir: Path) -> None:
    """Génère le fichier schema.py avec toutes les classes ORM"""

    schema_content = '''#!/usr/bin/env python3
"""
Schéma relationnel complet - SQLAlchemy ORM
Généré automatiquement par generate_orm_schema.py
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Float, Boolean,
    ForeignKey, Index, UniqueConstraint
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
'''

    output_dir.mkdir(parents=True, exist_ok=True)
    schema_file = output_dir / "schema.py"

    with schema_file.open("w", encoding="utf-8") as f:
        f.write(schema_content)

    print(f"✅ Schéma ORM généré: {schema_file}")


def generate_init_data(output_dir: Path) -> None:
    """Génère les données d'initialisation des dimensions"""

    init_content = '''#!/usr/bin/env python3
"""
Données d'initialisation des tables de dimension
"""

from sqlalchemy.orm import Session
from .schema import DimPays, DimDomaine, DimHumeur, Source


def init_dimensions(db: Session) -> None:
    """Initialise les tables de dimension avec des données de base"""

    # Pays
    pays_data = [
        {"nom": "France", "code_iso": "FRA"},
        {"nom": "États-Unis", "code_iso": "USA"},
        {"nom": "Royaume-Uni", "code_iso": "GBR"},
        {"nom": "Allemagne", "code_iso": "DEU"},
        {"nom": "Espagne", "code_iso": "ESP"},
    ]

    for p in pays_data:
        existing = db.query(DimPays).filter(DimPays.nom == p["nom"]).first()
        if not existing:
            db.add(DimPays(**p))

    # Domaines
    domaines_data = [
        {"nom": "politique", "description": "Actualités politiques"},
        {"nom": "international", "description": "Actualités internationales"},
        {"nom": "économie", "description": "Actualités économiques"},
        {"nom": "sport", "description": "Actualités sportives"},
        {"nom": "culture", "description": "Actualités culturelles"},
        {"nom": "technologie", "description": "Actualités technologiques"},
        {"nom": "inconnu", "description": "Domaine non identifié"},
    ]

    for d in domaines_data:
        existing = db.query(DimDomaine).filter(DimDomaine.nom == d["nom"]).first()
        if not existing:
            db.add(DimDomaine(**d))

    # Humeurs
    humeurs_data = [
        {"nom": "positif", "couleur": "#4CAF50", "description": "Sentiment positif"},
        {"nom": "négatif", "couleur": "#F44336", "description": "Sentiment négatif"},
        {"nom": "neutre", "couleur": "#9E9E9E", "description": "Sentiment neutre"},
        {"nom": "inquiet", "couleur": "#FF9800", "description": "Inquiétude"},
        {"nom": "content", "couleur": "#2196F3", "description": "Satisfaction"},
        {"nom": "déçu", "couleur": "#795548", "description": "Déception"},
        {"nom": "sceptique", "couleur": "#607D8B", "description": "Scepticisme"},
        {"nom": "incertain", "couleur": "#E91E63", "description": "Incertitude"},
    ]

    for h in humeurs_data:
        existing = db.query(DimHumeur).filter(DimHumeur.nom == h["nom"]).first()
        if not existing:
            db.add(DimHumeur(**h))

    # Sources
    sources_data = [
        {"nom": "YouTube API", "type": "api", "url_base": "https://www.youtube.com/"},
        {"nom": "NewsAPI", "type": "api", "url_base": "https://newsapi.org/"},
        {"nom": "Yahoo Actualités", "type": "scraping", "url_base": "https://fr.news.yahoo.com/"},
        {"nom": "Franceinfo", "type": "scraping", "url_base": "https://www.francetvinfo.fr/"},
        {"nom": "Kaggle Tweets", "type": "file", "url_base": ""},
        {"nom": "GDELT 2.0", "type": "bigdata", "url_base": "https://www.gdeltproject.org/"},
    ]

    for s in sources_data:
        existing = db.query(Source).filter(Source.nom == s["nom"]).first()
        if not existing:
            db.add(Source(**s))

    db.commit()
    print("✅ Données de dimension initialisées")
'''

    init_file = output_dir / "init_data.py"
    with init_file.open("w", encoding="utf-8") as f:
        f.write(init_content)

    print(f"✅ Données d'init générées: {init_file}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Génération schéma ORM")
    parser.add_argument(
        "--output-dir", type=str, default="app/backend/models",
        help="Dossier de sortie"
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)

    # Générer les fichiers
    generate_schema_file(output_dir)
    generate_init_data(output_dir)

    print(f"\n✅ Schéma ORM complet généré dans: {output_dir}")
    print("📋 Tables créées:")
    print("   - dim_pays, dim_domaine, dim_humeur (dimensions)")
    print("   - sources, contenus, reactions (principales)")
    print("   - Index et contraintes pour performance")

    return 0


if __name__ == "__main__":
    exit(main())
