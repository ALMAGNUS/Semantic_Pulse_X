"""
Classificateur d'émotions - Semantic Pulse X
Classification émotionnelle optimisée
"""

from functools import lru_cache
from typing import Any

import numpy as np
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

from app.backend.core.config import settings


class EmotionClassifier:
    """Classificateur d'émotions optimisé"""

    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.emotion_model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self._load_model()

    def _load_model(self):
        """Charge le modèle de classification émotionnelle"""
        try:
            # Charger le modèle et tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)

            # Créer le pipeline
            self.pipeline = pipeline(
                "text-classification",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1
            )

            print(f"✅ Modèle d'émotions chargé: {self.model_name}")
        except Exception as e:
            print(f"❌ Erreur chargement modèle émotions: {e}")
            # Fallback vers un modèle plus simple
            self._load_fallback_model()

    def _load_fallback_model(self):
        """Charge un modèle de fallback"""
        try:
            self.pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=0 if self.device == "cuda" else -1
            )
            print("✅ Modèle de fallback chargé")
        except Exception as e:
            print(f"❌ Erreur chargement fallback: {e}")
            self.pipeline = None

    @lru_cache(maxsize=500)
    def classify_emotion(self, text: str) -> dict[str, Any]:
        """Classifie l'émotion d'un texte"""
        if not text or not text.strip():
            return self._get_neutral_emotion()

        try:
            # Nettoyer le texte
            cleaned_text = self._clean_text(text)
            if not cleaned_text:
                return self._get_neutral_emotion()

            # Classification
            if self.pipeline:
                result = self.pipeline(cleaned_text)

                if isinstance(result, list) and len(result) > 0:
                    emotion_data = result[0]
                    return self._format_emotion_result(emotion_data)
                else:
                    return self._get_neutral_emotion()
            else:
                return self._get_neutral_emotion()

        except Exception as e:
            print(f"❌ Erreur classification émotion: {e}")
            return self._get_neutral_emotion()

    def classify_batch(self, texts: list[str]) -> list[dict[str, Any]]:
        """Classifie un batch de textes"""
        if not texts:
            return []

        results = []
        for text in texts:
            result = self.classify_emotion(text)
            results.append(result)

        return results

    def _clean_text(self, text: str) -> str:
        """Nettoie un texte pour la classification"""
        if not text:
            return ""

        import re
        # Supprimer les URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

        # Supprimer les mentions @
        text = re.sub(r'@\w+', '', text)

        # Supprimer les caractères spéciaux excessifs
        text = re.sub(r'[^\w\s.,!?]', ' ', text)
        text = re.sub(r'\s+', ' ', text)

        # Limiter la longueur
        max_length = settings.max_text_length
        if len(text) > max_length:
            text = text[:max_length]

        return text.strip()

    def _format_emotion_result(self, emotion_data: dict[str, Any]) -> dict[str, Any]:
        """Formate le résultat de classification"""
        label = emotion_data.get('label', 'NEUTRAL')
        score = emotion_data.get('score', 0.5)

        # Mapping des labels vers nos émotions
        emotion_mapping = {
            'LABEL_0': 'tristesse',
            'LABEL_1': 'joie',
            'LABEL_2': 'amour',
            'LABEL_3': 'colere',
            'LABEL_4': 'peur',
            'LABEL_5': 'surprise',
            'NEGATIVE': 'negatif',
            'POSITIVE': 'positif',
            'NEUTRAL': 'neutre'
        }

        emotion = emotion_mapping.get(label, 'neutre')

        # Calculer la polarité
        if emotion in ['joie', 'amour', 'positif']:
            polarite = score
        elif emotion in ['tristesse', 'colere', 'peur', 'negatif']:
            polarite = -score
        else:
            polarite = 0.0

        return {
            'emotion_principale': emotion,
            'score_emotion': float(score),
            'polarite': float(polarite),
            'confiance': float(score)
        }

    def _get_neutral_emotion(self) -> dict[str, Any]:
        """Retourne une émotion neutre par défaut"""
        return {
            'emotion_principale': 'neutre',
            'score_emotion': 0.5,
            'polarite': 0.0,
            'confiance': 0.5
        }

    def get_emotion_distribution(self, texts: list[str]) -> dict[str, int]:
        """Calcule la distribution des émotions"""
        if not texts:
            return {}

        results = self.classify_batch(texts)
        distribution = {}

        for result in results:
            emotion = result['emotion_principale']
            distribution[emotion] = distribution.get(emotion, 0) + 1

        return distribution

    def detect_emotion_trend(self, texts_with_timestamps: list[tuple[str, str]]) -> dict[str, Any]:
        """Détecte les tendances émotionnelles dans le temps"""
        if not texts_with_timestamps:
            return {'trend': 'stable', 'change': 0.0}

        # Grouper par période (ex: heure)
        from collections import defaultdict
        period_emotions = defaultdict(list)

        for text, timestamp in texts_with_timestamps:
            result = self.classify_emotion(text)
            period_emotions[timestamp].append(result['polarite'])

        # Calculer la moyenne par période
        period_averages = {}
        for period, polarities in period_emotions.items():
            if polarities:
                period_averages[period] = np.mean(polarities)

        # Analyser la tendance
        if len(period_averages) < 2:
            return {'trend': 'stable', 'change': 0.0}

        periods = sorted(period_averages.keys())
        recent_avg = period_averages[periods[-1]]
        older_avg = period_averages[periods[0]]

        change = recent_avg - older_avg

        if change > 0.1:
            trend = 'positive'
        elif change < -0.1:
            trend = 'negative'
        else:
            trend = 'stable'

        return {
            'trend': trend,
            'change': float(change),
            'recent_avg': float(recent_avg),
            'older_avg': float(older_avg)
        }


# Instance globale
emotion_classifier = EmotionClassifier()
