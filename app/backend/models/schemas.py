"""
Schémas Pydantic - Semantic Pulse X
Validation et sérialisation des données
"""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


# Base schemas
class BaseSchema(BaseModel):
    """Schéma de base avec configuration"""
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


# Programme schemas
class ProgrammeBase(BaseSchema):
    titre: str = Field(..., max_length=255)
    chaine: str = Field(..., max_length=100)
    genre: str | None = Field(None, max_length=50)
    duree_minutes: int | None = Field(None, ge=0)
    date_diffusion: datetime
    description: str | None = None


class ProgrammeCreate(ProgrammeBase):
    pass


class Programme(ProgrammeBase):
    id: UUID
    created_at: datetime


# Diffusion schemas
class DiffusionBase(BaseSchema):
    programme_id: UUID
    date_debut: datetime
    date_fin: datetime
    audience_estimee: int | None = Field(None, ge=0)


class DiffusionCreate(DiffusionBase):
    pass


class Diffusion(DiffusionBase):
    id: UUID
    created_at: datetime


# Utilisateur schemas - MCD Merise
class UtilisateurBase(BaseSchema):
    hash_anonyme: str = Field(..., max_length=64)
    region_anonymisee: str | None = Field(None, max_length=20)
    age_groupe: str | None = Field(None, max_length=10)
    langue_preferee: str = Field(default="fr", max_length=5)


class UtilisateurCreate(UtilisateurBase):
    pass


class Utilisateur(UtilisateurBase):
    id: UUID
    created_at: datetime
    last_activity: datetime | None = None


# Réaction schemas - MCD Merise
class ReactionBase(BaseSchema):
    programme_id: UUID | None = None
    diffusion_id: UUID | None = None
    utilisateur_id: UUID | None = None
    source_id: UUID
    texte_anonymise: str | None = None
    langue: str = Field(default="fr", max_length=5)
    emotion_principale: str | None = Field(None, max_length=50)
    score_emotion: float | None = Field(None, ge=0.0, le=1.0)
    polarite: float | None = Field(None, ge=-1.0, le=1.0)
    confiance: float | None = Field(None, ge=0.0, le=1.0)
    timestamp: datetime


class ReactionCreate(ReactionBase):
    pass


class Reaction(ReactionBase):
    id: UUID
    created_at: datetime


# Source schemas - MCD Merise
class SourceBase(BaseSchema):
    nom: str = Field(..., max_length=100)
    type_source: str = Field(..., max_length=20)  # "file", "sql", "bigdata", "scraping", "api"
    url: str | None = Field(None, max_length=500)
    configuration: dict[str, Any] | None = None
    actif: bool = True


class SourceCreate(SourceBase):
    pass


class Source(SourceBase):
    id: UUID
    created_at: datetime


# Logs d'ingestion schemas - MLD Merise
class LogIngestionBase(BaseSchema):
    source_id: UUID
    date_ingestion: datetime
    nombre_records: int = Field(default=0, ge=0)
    statut: str = Field(..., max_length=20)  # "success", "error", "partial"
    message: str | None = None
    configuration_utilisee: dict[str, Any] | None = None


class LogIngestionCreate(LogIngestionBase):
    pass


class LogIngestion(LogIngestionBase):
    id: UUID


# Agrégation émotionnelle schemas - MLP Merise
class AgregationEmotionnelleBase(BaseSchema):
    programme_id: UUID | None = None
    diffusion_id: UUID | None = None
    periode_debut: datetime
    periode_fin: datetime
    emotion_dominante: str | None = Field(None, max_length=50)
    score_moyen: float | None = Field(None, ge=0.0, le=1.0)
    polarite_moyenne: float | None = Field(None, ge=-1.0, le=1.0)
    nombre_reactions: int = Field(default=0, ge=0)


class AgregationEmotionnelleCreate(AgregationEmotionnelleBase):
    pass


class AgregationEmotionnelle(AgregationEmotionnelleBase):
    id: UUID
    created_at: datetime


# Analytics schemas
class EmotionAnalytics(BaseSchema):
    emotion: str
    count: int
    percentage: float
    avg_score: float
    trend: str  # "up", "down", "stable"


class TopicAnalytics(BaseSchema):
    topic: str
    count: int
    avg_polarity: float
    top_emotions: list[EmotionAnalytics]


class TemporalAnalytics(BaseSchema):
    timestamp: datetime
    emotions: list[EmotionAnalytics]
    topics: list[TopicAnalytics]


# API Response schemas
class APIResponse(BaseSchema):
    success: bool = True
    message: str
    data: Any | None = None


class ErrorResponse(BaseSchema):
    success: bool = False
    error: str
    details: dict[str, Any] | None = None
