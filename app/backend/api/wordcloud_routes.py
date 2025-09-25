"""
Routes API pour les nuages de mots - Semantic Pulse X
Endpoints pour la génération et la gestion des nuages de mots
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

from app.frontend.visualization.wordcloud_generator import wordcloud_generator
from app.backend.models.schemas import APIResponse, ErrorResponse

# Router pour les nuages de mots
wordcloud_router = APIRouter()


@wordcloud_router.get("/generate", response_model=APIResponse)
async def generate_wordcloud(
    emotion: Optional[str] = Query(None, description="Émotion à filtrer"),
    max_words: int = Query(100, ge=10, le=500, description="Nombre maximum de mots"),
    width: int = Query(800, ge=400, le=1200, description="Largeur du nuage"),
    height: int = Query(400, ge=300, le=800, description="Hauteur du nuage")
):
    """Génère un nuage de mots pour une émotion spécifique"""
    try:
        # Simulation de données (en production, récupérer depuis la DB)
        sample_data = generate_sample_data()
        
        if not sample_data:
            raise HTTPException(status_code=404, detail="Aucune donnée disponible")
        
        # Extraire les textes et émotions
        texts = [item['text'] for item in sample_data]
        emotions = [item['emotion'] for item in sample_data]
        
        # Générer le nuage de mots
        wordcloud_data = wordcloud_generator.generate_emotion_wordcloud(
            texts, emotions, 
            emotion_filter=emotion,
            max_words=max_words,
            width=width,
            height=height
        )
        
        return APIResponse(
            success=True,
            message="Nuage de mots généré avec succès",
            data=wordcloud_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@wordcloud_router.get("/emotions/comparison", response_model=APIResponse)
async def generate_emotion_comparison(
    emotions: List[str] = Query(..., description="Liste des émotions à comparer"),
    max_words: int = Query(50, ge=10, le=200, description="Nombre maximum de mots par émotion")
):
    """Génère des nuages de mots pour comparer les émotions"""
    try:
        # Simulation de données
        sample_data = generate_sample_data()
        
        if not sample_data:
            raise HTTPException(status_code=404, detail="Aucune donnée disponible")
        
        # Générer la comparaison
        comparison_data = wordcloud_generator.generate_emotion_comparison_wordclouds(
            sample_data, emotions, max_words
        )
        
        return APIResponse(
            success=True,
            message="Comparaison des émotions générée",
            data=comparison_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@wordcloud_router.get("/temporal", response_model=APIResponse)
async def generate_temporal_wordclouds(
    time_window: str = Query("day", description="Fenêtre temporelle (hour, day, week)"),
    max_words: int = Query(50, ge=10, le=200, description="Nombre maximum de mots")
):
    """Génère des nuages de mots temporels"""
    try:
        # Simulation de données temporelles
        sample_data = generate_temporal_sample_data()
        
        if not sample_data:
            raise HTTPException(status_code=404, detail="Aucune donnée temporelle disponible")
        
        # Générer les nuages temporels
        temporal_wordclouds = wordcloud_generator.generate_temporal_wordclouds(
            sample_data, time_window, max_words
        )
        
        return APIResponse(
            success=True,
            message="Nuages temporels générés",
            data={
                "wordclouds": temporal_wordclouds,
                "time_window": time_window,
                "total_periods": len(temporal_wordclouds)
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@wordcloud_router.get("/trending", response_model=APIResponse)
async def generate_trending_words(
    time_periods: int = Query(3, ge=2, le=10, description="Nombre de périodes temporelles"),
    max_words: int = Query(30, ge=10, le=100, description="Nombre maximum de mots en tendance")
):
    """Génère un nuage de mots des tendances"""
    try:
        # Simulation de données temporelles
        sample_data = generate_temporal_sample_data()
        
        if not sample_data:
            raise HTTPException(status_code=404, detail="Aucune donnée temporelle disponible")
        
        # Générer l'analyse des tendances
        trending_data = wordcloud_generator.generate_trending_words_cloud(
            sample_data, time_periods, max_words
        )
        
        return APIResponse(
            success=True,
            message="Analyse des tendances générée",
            data=trending_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@wordcloud_router.get("/interactive", response_model=APIResponse)
async def generate_interactive_wordcloud(
    emotion: Optional[str] = Query(None, description="Émotion à filtrer"),
    max_words: int = Query(50, ge=10, le=200, description="Nombre maximum de mots")
):
    """Génère un nuage de mots interactif"""
    try:
        # Simulation de données
        sample_data = generate_sample_data()
        
        if not sample_data:
            raise HTTPException(status_code=404, detail="Aucune donnée disponible")
        
        # Filtrer par émotion si spécifiée
        if emotion:
            sample_data = [item for item in sample_data if item.get('emotion') == emotion]
        
        if not sample_data:
            raise HTTPException(status_code=404, detail=f"Aucune donnée pour l'émotion '{emotion}'")
        
        # Générer le graphique interactif
        fig = wordcloud_generator.generate_interactive_wordcloud(sample_data, emotion)
        
        # Convertir en JSON pour l'API
        fig_json = fig.to_json()
        
        return APIResponse(
            success=True,
            message="Nuage de mots interactif généré",
            data={
                "plotly_figure": json.loads(fig_json),
                "emotion": emotion,
                "max_words": max_words
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@wordcloud_router.get("/statistics", response_model=APIResponse)
async def get_word_statistics(
    emotion: Optional[str] = Query(None, description="Émotion à analyser")
):
    """Retourne les statistiques des mots"""
    try:
        # Simulation de données
        sample_data = generate_sample_data()
        
        if not sample_data:
            raise HTTPException(status_code=404, detail="Aucune donnée disponible")
        
        # Filtrer par émotion si spécifiée
        if emotion:
            sample_data = [item for item in sample_data if item.get('emotion') == emotion]
        
        if not sample_data:
            raise HTTPException(status_code=404, detail=f"Aucune donnée pour l'émotion '{emotion}'")
        
        # Calculer les statistiques
        stats = wordcloud_generator.get_word_statistics(sample_data)
        
        return APIResponse(
            success=True,
            message="Statistiques des mots calculées",
            data=stats
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@wordcloud_router.get("/emotions", response_model=APIResponse)
async def get_available_emotions():
    """Retourne la liste des émotions disponibles"""
    try:
        # Simulation de données
        sample_data = generate_sample_data()
        
        emotions = list(set(item['emotion'] for item in sample_data))
        emotion_counts = {}
        
        for emotion in emotions:
            count = sum(1 for item in sample_data if item['emotion'] == emotion)
            emotion_counts[emotion] = count
        
        return APIResponse(
            success=True,
            message="Émotions disponibles récupérées",
            data={
                "emotions": emotions,
                "counts": emotion_counts,
                "total_emotions": len(emotions)
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def generate_sample_data() -> List[Dict[str, Any]]:
    """Génère des données d'exemple pour les tests"""
    emotions = ["joie", "colere", "tristesse", "surprise", "peur", "neutre", "positif", "negatif"]
    
    sample_texts = [
        "Super émission hier soir, vraiment génial !",
        "Je n'aime pas du tout cette émission",
        "Très intéressant, j'ai appris beaucoup",
        "C'est n'importe quoi, complètement ridicule",
        "Excellent travail, bravo à toute l'équipe",
        "Décevant, je m'attendais à mieux",
        "Fantastique, j'ai adoré chaque minute",
        "Horrible, je ne regarderai plus jamais",
        "Pas mal, mais peut mieux faire",
        "Extraordinaire, un véritable chef-d'œuvre"
    ]
    
    data = []
    for i in range(100):
        data.append({
            "text": sample_texts[i % len(sample_texts)],
            "emotion": emotions[i % len(emotions)],
            "timestamp": (datetime.now() - timedelta(hours=i)).isoformat(),
            "polarity": (i % 3 - 1) * 0.5
        })
    
    return data


def generate_temporal_sample_data() -> List[Dict[str, Any]]:
    """Génère des données temporelles d'exemple"""
    emotions = ["joie", "colere", "tristesse", "surprise", "peur", "neutre"]
    
    data = []
    for i in range(200):
        # Répartir sur plusieurs jours
        days_ago = i // 20
        hours_ago = i % 24
        
        data.append({
            "text": f"Commentaire {i+1} sur l'actualité",
            "emotion": emotions[i % len(emotions)],
            "timestamp": (datetime.now() - timedelta(days=days_ago, hours=hours_ago)).isoformat(),
            "polarity": (i % 3 - 1) * 0.5
        })
    
    return data


# Routes de santé
@wordcloud_router.get("/health")
async def wordcloud_health():
    """Vérification de santé du service nuages de mots"""
    return {"status": "healthy", "service": "wordcloud"}
