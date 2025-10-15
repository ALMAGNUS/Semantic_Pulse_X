"""
Routes API - Semantic Pulse X
Endpoints pour l'API REST
"""

from datetime import datetime, timedelta

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.backend.ai.emotion_classifier import emotion_classifier
from app.backend.ai.langchain_agent import semantic_agent
from app.backend.core.database import get_db
from app.backend.core.metrics import track_model_accuracy, track_model_drift
from app.backend.etl.pipeline import etl_pipeline
from app.backend.models.schemas import (
    APIResponse,
)
from scripts.model_drift_monitor import ModelDriftMonitor

# Routers
emotions = APIRouter()
predictions = APIRouter()
data_sources = APIRouter()


@emotions.get("/", response_model=APIResponse)
async def get_emotions(
    limit: int = 100,
    offset: int = 0,
    emotion: str | None = None,
    db: Session = Depends(get_db)
):
    """Récupère les réactions émotionnelles"""
    try:
        # Simulation de données (en production, utiliser la DB)
        data = {
            "emotions": [
                {
                    "id": "1",
                    "emotion": "joie",
                    "score": 0.8,
                    "polarity": 0.7,
                    "confidence": 0.9,
                    "timestamp": datetime.now().isoformat()
                },
                {
                    "id": "2",
                    "emotion": "colere",
                    "score": 0.6,
                    "polarity": -0.8,
                    "confidence": 0.7,
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "total": 2,
            "limit": limit,
            "offset": offset
        }

        return APIResponse(
            success=True,
            message="Émotions récupérées avec succès",
            data=data
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@emotions.post("/analyze", response_model=APIResponse)
async def analyze_emotion(
    text: str,
    background_tasks: BackgroundTasks
):
    """Analyse l'émotion d'un texte"""
    try:
        if not text.strip():
            raise HTTPException(status_code=400, detail="Texte vide")

        # Classification émotionnelle
        result = emotion_classifier.classify_emotion(text)

        # Ajouter le texte original
        result["text"] = text
        result["timestamp"] = datetime.now().isoformat()

        return APIResponse(
            success=True,
            message="Analyse émotionnelle terminée",
            data=result
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@emotions.get("/analytics", response_model=APIResponse)
async def get_emotion_analytics(
    start_date: str | None = None,
    end_date: str | None = None,
    source: str | None = None
):
    """Récupère les analytics émotionnelles"""
    try:
        # Simulation de données analytics
        analytics = {
            "emotion_distribution": {
                "joie": 45,
                "colere": 20,
                "tristesse": 15,
                "surprise": 10,
                "peur": 5,
                "neutre": 5
            },
            "polarity_trend": {
                "current": 0.2,
                "previous": 0.1,
                "change": 0.1
            },
            "top_emotions": [
                {"emotion": "joie", "count": 45, "percentage": 45.0},
                {"emotion": "colere", "count": 20, "percentage": 20.0},
                {"emotion": "tristesse", "count": 15, "percentage": 15.0}
            ],
            "time_range": {
                "start": start_date or (datetime.now() - timedelta(days=7)).isoformat(),
                "end": end_date or datetime.now().isoformat()
            }
        }

        return APIResponse(
            success=True,
            message="Analytics émotionnelles récupérées",
            data=analytics
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@predictions.get("/", response_model=APIResponse)
async def get_predictions(
    horizon: int = 24,
    emotion: str | None = None
):
    """Récupère les prédictions émotionnelles"""
    try:
        # Simulation de prédictions
        predictions = []
        for i in range(horizon):
            predictions.append({
                "timestamp": (datetime.now() + timedelta(hours=i)).isoformat(),
                "emotion": emotion or "joie",
                "confidence": 0.7 + (i * 0.01),
                "trend": "positive" if i % 2 == 0 else "negative"
            })

        return APIResponse(
            success=True,
            message="Prédictions générées",
            data={
                "predictions": predictions,
                "horizon_hours": horizon,
                "generated_at": datetime.now().isoformat()
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@predictions.post("/analyze", response_model=APIResponse)
async def analyze_trends(
    texts: list[str],
    background_tasks: BackgroundTasks
):
    """Analyse les tendances émotionnelles"""
    try:
        if not texts:
            raise HTTPException(status_code=400, detail="Aucun texte fourni")

        # Classification des émotions
        emotion_results = emotion_classifier.classify_batch(texts)

        # Analyse des tendances
        trend_analysis = emotion_classifier.detect_emotion_trend(
            [(text, datetime.now().isoformat()) for text in texts]
        )

        # Génération d'insights
        insights = semantic_agent.analyze_emotion_trends(emotion_results)

        return APIResponse(
            success=True,
            message="Analyse des tendances terminée",
            data={
                "emotion_results": emotion_results,
                "trend_analysis": trend_analysis,
                "insights": insights,
                "total_texts": len(texts)
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@data_sources.get("/", response_model=APIResponse)
async def get_data_sources():
    """Récupère la liste des sources de données"""
    try:
        sources = [
            {
                "id": "file",
                "name": "Fichiers plats",
                "type": "file",
                "status": "active",
                "last_update": datetime.now().isoformat()
            },
            {
                "id": "database",
                "name": "Base de données",
                "type": "database",
                "status": "active",
                "last_update": datetime.now().isoformat()
            },
            {
                "id": "bigdata",
                "name": "Big Data",
                "type": "bigdata",
                "status": "active",
                "last_update": datetime.now().isoformat()
            },
            {
                "id": "scraping",
                "name": "Scraping web",
                "type": "scraping",
                "status": "active",
                "last_update": datetime.now().isoformat()
            },
            {
                "id": "api",
                "name": "API REST",
                "type": "api",
                "status": "active",
                "last_update": datetime.now().isoformat()
            }
        ]

        return APIResponse(
            success=True,
            message="Sources de données récupérées",
            data={"sources": sources}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@data_sources.post("/sync", response_model=APIResponse)
async def sync_data_sources(
    background_tasks: BackgroundTasks,
    source: str | None = None
):
    """Synchronise les sources de données"""
    try:
        # Exécuter le pipeline ETL en arrière-plan
        background_tasks.add_task(run_etl_pipeline, source)

        return APIResponse(
            success=True,
            message="Synchronisation des sources démarrée",
            data={"status": "started", "source": source}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@data_sources.get("/metrics")
async def get_prometheus_metrics():
    """Expose les métriques Prometheus"""
    try:
        from fastapi import Response
        from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

        # Générer les métriques Prometheus
        metrics_data = generate_latest()

        return Response(
            content=metrics_data,
            media_type=CONTENT_TYPE_LATEST
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@data_sources.get("/drift-monitoring", response_model=APIResponse)
async def get_drift_monitoring():
    """Surveillance de la dérive des modèles"""
    try:
        monitor = ModelDriftMonitor()
        results = monitor.run_monitoring()

        # Track metrics in Prometheus
        track_model_drift(
            model_type="emotion_classifier",
            psi_score=results.get("psi_score", 0.0),
            ks_statistic=results.get("ks_statistic", 0.0),
            alerts=results.get("alerts", [])
        )

        track_model_accuracy(
            model_type="emotion_classifier",
            current_accuracy=0.87,  # Valeur simulée
            reference_accuracy=0.89  # Valeur simulée
        )

        return APIResponse(
            success=True,
            message="Surveillance de dérive exécutée",
            data=results,
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@data_sources.get("/stats", response_model=APIResponse)
async def get_data_sources_stats():
    """Récupère les statistiques des sources"""
    try:
        # Simulation de statistiques
        stats = {
            "total_sources": 5,
            "active_sources": 5,
            "total_records": 1000,
            "last_sync": datetime.now().isoformat(),
            "sources": {
                "file": {"records": 200, "status": "active"},
                "database": {"records": 300, "status": "active"},
                "bigdata": {"records": 250, "status": "active"},
                "scraping": {"records": 150, "status": "active"},
                "api": {"records": 100, "status": "active"}
            }
        }

        return APIResponse(
            success=True,
            message="Statistiques des sources récupérées",
            data=stats
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


async def run_etl_pipeline(source: str | None = None):
    """Exécute le pipeline ETL en arrière-plan"""
    try:
        if source:
            # Exécuter pour une source spécifique
            results = etl_pipeline.run_full_pipeline()
        else:
            # Exécuter pour toutes les sources
            results = etl_pipeline.run_full_pipeline()

        print(f"Pipeline ETL terminé: {results}")

    except Exception as e:
        print(f"Erreur pipeline ETL: {e}")


# Routes de santé
@emotions.get("/health")
async def emotions_health():
    """Vérification de santé du service émotions"""
    return {"status": "healthy", "service": "emotions"}


@predictions.get("/health")
async def predictions_health():
    """Vérification de santé du service prédictions"""
    return {"status": "healthy", "service": "predictions"}


@data_sources.get("/health")
async def data_sources_health():
    """Vérification de santé du service sources"""
    return {"status": "healthy", "service": "data-sources"}
