"""
Modèles d'entités - Semantic Pulse X
Modélisation Merise conforme au prompt : Programme, Diffusion, Réaction, Utilisateur, Source
Conception RGPD-compliant : aucun PII, anonymisation intégrée
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid

from app.backend.core.database import Base


class Programme(Base):
    """
    Entité Programme - MCD Merise
    Programme TV/média avec métadonnées anonymisées
    """
    __tablename__ = "programmes"
    
    # Clé primaire
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Attributs du programme
    titre = Column(String(255), nullable=False)
    chaine = Column(String(100), nullable=False)
    genre = Column(String(50))
    duree_minutes = Column(Integer)
    description = Column(Text)
    
    # Métadonnées temporelles
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations Merise
    diffusions = relationship("Diffusion", back_populates="programme", cascade="all, delete-orphan")
    reactions = relationship("Reaction", back_populates="programme")


class Diffusion(Base):
    """
    Entité Diffusion - MCD Merise
    Diffusion d'un programme avec métadonnées anonymisées
    """
    __tablename__ = "diffusions"
    
    # Clé primaire
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Clé étrangère vers Programme
    programme_id = Column(UUID(as_uuid=True), ForeignKey("programmes.id"), nullable=False)
    
    # Attributs de la diffusion
    date_debut = Column(DateTime, nullable=False)
    date_fin = Column(DateTime, nullable=False)
    audience_estimee = Column(Integer)  # Anonymisé - pas de données individuelles
    rating_anonymise = Column(Float)  # Note anonymisée
    
    # Métadonnées temporelles
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations Merise
    programme = relationship("Programme", back_populates="diffusions")
    reactions = relationship("Reaction", back_populates="diffusion")


class Utilisateur(Base):
    """
    Entité Utilisateur - MCD Merise
    Utilisateur anonymisé - RGPD compliant
    Uniquement ID anonymisé, aucun PII
    """
    __tablename__ = "utilisateurs"
    
    # Clé primaire
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Identifiant anonymisé (hash SHA-256)
    hash_anonyme = Column(String(64), unique=True, nullable=False)
    
    # Données anonymisées (pas de PII)
    region_anonymisee = Column(String(20))  # Ex: "FR-75", "US-CA"
    age_groupe = Column(String(10))  # Ex: "18-25", "26-35"
    langue_preferee = Column(String(5), default="fr")
    
    # Métadonnées temporelles
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime)
    
    # Relations Merise
    reactions = relationship("Reaction", back_populates="utilisateur")


class Reaction(Base):
    """
    Entité Réaction - MCD Merise
    Réaction émotionnelle anonymisée
    """
    __tablename__ = "reactions"
    
    # Clé primaire
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Clés étrangères Merise
    programme_id = Column(UUID(as_uuid=True), ForeignKey("programmes.id"))
    diffusion_id = Column(UUID(as_uuid=True), ForeignKey("diffusions.id"))
    utilisateur_id = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id"))
    source_id = Column(UUID(as_uuid=True), ForeignKey("sources.id"), nullable=False)
    
    # Contenu anonymisé
    texte_anonymise = Column(Text)  # Texte nettoyé et anonymisé
    langue = Column(String(5), default="fr")
    
    # Analyse émotionnelle
    emotion_principale = Column(String(50))  # "joie", "colere", "tristesse", "surprise", "peur", "neutre"
    score_emotion = Column(Float)  # 0.0 à 1.0
    polarite = Column(Float)  # -1.0 à 1.0
    confiance = Column(Float)  # 0.0 à 1.0
    
    # Métadonnées temporelles
    timestamp = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations Merise
    programme = relationship("Programme", back_populates="reactions")
    diffusion = relationship("Diffusion", back_populates="reactions")
    utilisateur = relationship("Utilisateur", back_populates="reactions")
    source = relationship("Source", back_populates="reactions")


class Source(Base):
    """
    Entité Source - MCD Merise
    Source de données (fichier, SQL, Big Data, Scraping, API)
    """
    __tablename__ = "sources"
    
    # Clé primaire
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Attributs de la source
    nom = Column(String(100), nullable=False)
    type_source = Column(String(20), nullable=False)  # "file", "sql", "bigdata", "scraping", "api"
    url = Column(String(500))
    configuration = Column(JSONB)  # Configuration anonymisée
    
    # Statut et métadonnées
    actif = Column(Boolean, default=True)
    last_sync = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations Merise
    reactions = relationship("Reaction", back_populates="source")


# Tables de logs d'ingestion (MLD Merise)
class LogIngestion(Base):
    """
    Log d'ingestion - MLD Merise
    Traçabilité des données collectées
    """
    __tablename__ = "logs_ingestion"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("sources.id"), nullable=False)
    
    # Métadonnées d'ingestion
    date_ingestion = Column(DateTime, nullable=False)
    nombre_records = Column(Integer, default=0)
    statut = Column(String(20), nullable=False)  # "success", "error", "partial"
    message = Column(Text)
    
    # Configuration utilisée
    configuration_utilisee = Column(JSONB)
    
    # Relations
    source = relationship("Source")


# Tables d'agrégation (MLP Merise)
class AgregationEmotionnelle(Base):
    """
    Agrégation émotionnelle - MLP Merise
    Vues agrégées pour l'analyse
    """
    __tablename__ = "agregations_emotionnelles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    programme_id = Column(UUID(as_uuid=True), ForeignKey("programmes.id"))
    diffusion_id = Column(UUID(as_uuid=True), ForeignKey("diffusions.id"))
    
    # Agrégations temporelles
    periode_debut = Column(DateTime, nullable=False)
    periode_fin = Column(DateTime, nullable=False)
    
    # Métriques agrégées
    emotion_dominante = Column(String(50))
    score_moyen = Column(Float)
    polarite_moyenne = Column(Float)
    nombre_reactions = Column(Integer)
    
    # Métadonnées
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    programme = relationship("Programme")
    diffusion = relationship("Diffusion")
