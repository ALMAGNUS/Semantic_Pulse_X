"""
Schémas Pydantic - Semantic Pulse X
Validation et sérialisation des données
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


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
    genre: Optional[str] = Field(None, max_length=50)
    duree_minutes: Optional[int] = Field(None, ge=0)
    date_diffusion: datetime
    description: Optional[str] = None


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
    audience_estimee: Optional[int] = Field(None, ge=0)


class DiffusionCreate(DiffusionBase):
    pass


class Diffusion(DiffusionBase):
    id: UUID
    created_at: datetime


# Utilisateur schemas - MCD Merise
class UtilisateurBase(BaseSchema):
    hash_anonyme: str = Field(..., max_length=64)
    region_anonymisee: Optional[str] = Field(None, max_length=20)
    age_groupe: Optional[str] = Field(None, max_length=10)
    langue_preferee: str = Field(default="fr", max_length=5)


class UtilisateurCreate(UtilisateurBase):
    pass


class Utilisateur(UtilisateurBase):
    id: UUID
    created_at: datetime
    last_activity: Optional[datetime] = None


# Réaction schemas - MCD Merise
class ReactionBase(BaseSchema):
    programme_id: Optional[UUID] = None
    diffusion_id: Optional[UUID] = None
    utilisateur_id: Optional[UUID] = None
    source_id: UUID
    texte_anonymise: Optional[str] = None
    langue: str = Field(default="fr", max_length=5)
    emotion_principale: Optional[str] = Field(None, max_length=50)
    score_emotion: Optional[float] = Field(None, ge=0.0, le=1.0)
    polarite: Optional[float] = Field(None, ge=-1.0, le=1.0)
    confiance: Optional[float] = Field(None, ge=0.0, le=1.0)
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
    url: Optional[str] = Field(None, max_length=500)
    configuration: Optional[Dict[str, Any]] = None
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
    message: Optional[str] = None
    configuration_utilisee: Optional[Dict[str, Any]] = None


class LogIngestionCreate(LogIngestionBase):
    pass


class LogIngestion(LogIngestionBase):
    id: UUID


# Agrégation émotionnelle schemas - MLP Merise
class AgregationEmotionnelleBase(BaseSchema):
    programme_id: Optional[UUID] = None
    diffusion_id: Optional[UUID] = None
    periode_debut: datetime
    periode_fin: datetime
    emotion_dominante: Optional[str] = Field(None, max_length=50)
    score_moyen: Optional[float] = Field(None, ge=0.0, le=1.0)
    polarite_moyenne: Optional[float] = Field(None, ge=-1.0, le=1.0)
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
    top_emotions: List[EmotionAnalytics]


class TemporalAnalytics(BaseSchema):
    timestamp: datetime
    emotions: List[EmotionAnalytics]
    topics: List[TopicAnalytics]


# API Response schemas
class APIResponse(BaseSchema):
    success: bool = True
    message: str
    data: Optional[Any] = None


class ErrorResponse(BaseSchema):
    success: bool = False
    error: str
    details: Optional[Dict[str, Any]] = None
