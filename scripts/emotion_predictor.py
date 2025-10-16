#!/usr/bin/env python3
"""
Système de Prédiction Émotionnelle - Semantic Pulse X
Prédit les émotions futures du peuple français sur les événements
"""

import json
import logging
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmotionPredictor:
    """Prédicteur d'émotions pour le peuple français"""
    
    def __init__(self):
        self.db_path = "semantic_pulse.db"
        self.model = None
        self.feature_columns = [
            'sentiment_score', 'confidence', 'source_diversity', 
            'time_decay', 'volume_trend', 'domain_weight'
        ]
    
    def load_training_data(self) -> pd.DataFrame:
        """Charge les données d'entraînement depuis la base"""
        conn = sqlite3.connect(self.db_path)
        
        try:
            # Récupérer les données avec sentiment
            query = """
            SELECT 
                texte, sentiment, confidence, source_type, 
                collected_at, domaine_id
            FROM contenus 
            WHERE sentiment IS NOT NULL 
            AND confidence IS NOT NULL
            """
            
            df = pd.read_sql_query(query, conn)
            
            if len(df) == 0:
                logger.warning("Aucune donnée d'entraînement trouvée")
                return pd.DataFrame()
            
            # Préparer les features
            df = self._prepare_features(df)
            
            logger.info(f"DATA: {len(df)} échantillons d'entraînement chargés")
            return df
            
        finally:
            conn.close()
    
    def _prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prépare les features pour l'entraînement"""
        
        # Sentiment score (numérique)
        sentiment_map = {
            'positif': 1.0, 'neutre': 0.0, 'négatif': -1.0,
            'déçu': -0.5, 'incertain': 0.0, 'joy': 0.8,
            'anger': -0.8, 'fear': -0.6, 'trust': 0.7
        }
        df['sentiment_score'] = df['sentiment'].map(sentiment_map).fillna(0.0)
        
        # Source diversity (nombre de sources uniques)
        df['source_diversity'] = df.groupby('collected_at')['source_type'].transform('nunique')
        
        # Time decay (poids temporel)
        df['collected_at'] = pd.to_datetime(df['collected_at'])
        now = datetime.now()
        df['time_decay'] = (now - df['collected_at']).dt.days / 30.0  # Décroissance sur 30 jours
        
        # Volume trend (tendance du volume)
        df['volume_trend'] = df.groupby('collected_at').size() / df.groupby('collected_at').size().mean()
        
        # Domain weight (poids par domaine)
        domain_weights = {'politique': 1.0, 'sport': 0.7, 'culture': 0.8, 'économie': 0.9}
        df['domain_weight'] = df['domaine_id'].map(domain_weights).fillna(0.5)
        
        return df
    
    def train_model(self) -> Dict:
        """Entraîne le modèle de prédiction"""
        
        # Charger les données
        df = self.load_training_data()
        
        if len(df) < 50:
            logger.warning("Pas assez de données pour l'entraînement")
            return {'success': False, 'error': 'Données insuffisantes'}
        
        try:
            # Préparer X et y
            X = df[self.feature_columns]
            y = df['sentiment_score']
            
            # Diviser train/test
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Entraîner le modèle
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            
            # Classification binaire : positif/négatif
            y_train_binary = (y_train > 0).astype(int)
            y_test_binary = (y_test > 0).astype(int)
            
            self.model.fit(X_train, y_train_binary)
            
            # Évaluer
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test_binary, y_pred)
            
            logger.info(f"SUCCESS: Modèle entraîné - Précision: {accuracy:.2%}")
            
            return {
                'success': True,
                'accuracy': accuracy,
                'samples': len(df),
                'features': len(self.feature_columns)
            }
            
        except Exception as e:
            logger.error(f"ERROR: Erreur entraînement: {e}")
            return {'success': False, 'error': str(e)}
    
    def predict_emotion_trend(self, event_description: str, days_ahead: int = 7) -> Dict:
        """Prédit l'évolution émotionnelle pour un événement"""
        
        if not self.model:
            logger.error("Modèle non entraîné")
            return {'success': False, 'error': 'Modèle non entraîné'}
        
        try:
            # Simuler des features pour l'événement
            features = {
                'sentiment_score': 0.0,  # Neutre initial
                'confidence': 0.5,       # Confiance modérée
                'source_diversity': 3.0, # 3 sources
                'time_decay': 0.0,       # Événement récent
                'volume_trend': 1.5,     # Volume élevé
                'domain_weight': 1.0      # Politique
            }
            
            # Prédiction
            X_pred = pd.DataFrame([features])
            prediction = self.model.predict(X_pred)[0]
            probability = self.model.predict_proba(X_pred)[0]
            
            # Interprétation
            emotion = "positif" if prediction == 1 else "négatif"
            confidence = max(probability)
            
            # Prédiction temporelle
            trend_prediction = self._predict_temporal_trend(days_ahead, features)
            
            return {
                'success': True,
                'event': event_description,
                'predicted_emotion': emotion,
                'confidence': float(confidence),
                'days_ahead': days_ahead,
                'trend': trend_prediction,
                'recommendations': self._generate_recommendations(emotion, confidence)
            }
            
        except Exception as e:
            logger.error(f"ERROR: Erreur prédiction: {e}")
            return {'success': False, 'error': str(e)}
    
    def _predict_temporal_trend(self, days: int, features: Dict) -> List[Dict]:
        """Prédit l'évolution temporelle des émotions"""
        
        trends = []
        base_sentiment = features['sentiment_score']
        
        for day in range(1, days + 1):
            # Simulation d'évolution temporelle
            decay_factor = 1.0 - (day * 0.05)  # Décroissance de 5% par jour
            volatility = np.random.normal(0, 0.1)  # Volatilité aléatoire
            
            predicted_sentiment = base_sentiment * decay_factor + volatility
            predicted_sentiment = max(-1.0, min(1.0, predicted_sentiment))  # Clamp [-1, 1]
            
            trends.append({
                'day': day,
                'sentiment_score': float(predicted_sentiment),
                'emotion': 'positif' if predicted_sentiment > 0.2 else 'négatif' if predicted_sentiment < -0.2 else 'neutre'
            })
        
        return trends
    
    def _generate_recommendations(self, emotion: str, confidence: float) -> List[str]:
        """Génère des recommandations basées sur la prédiction"""
        
        recommendations = []
        
        if emotion == "positif" and confidence > 0.7:
            recommendations.extend([
                "Maintenir la communication positive",
                "Capitaliser sur le momentum émotionnel",
                "Communiquer les succès rapidement"
            ])
        elif emotion == "négatif" and confidence > 0.7:
            recommendations.extend([
                "Préparer une communication de crise",
                "Adapter la stratégie de communication",
                "Surveiller l'évolution quotidienne"
            ])
        else:
            recommendations.extend([
                "Surveiller l'évolution des sentiments",
                "Maintenir une communication équilibrée",
                "Préparer des plans d'action adaptatifs"
            ])
        
        return recommendations

def main():
    """Point d'entrée principal"""
    print("SYSTEME: Système de Prédiction Émotionnelle")
    print("=" * 50)
    
    predictor = EmotionPredictor()
    
    # Entraîner le modèle
    print("TRAINING: Entraînement du modèle...")
    train_result = predictor.train_model()
    
    if train_result['success']:
        print(f"SUCCESS: Modèle entraîné - Précision: {train_result['accuracy']:.2%}")
        print(f"SAMPLES: Échantillons: {train_result['samples']}")
        
        # Test de prédiction
        print("\nPREDICTION: Test de prédiction...")
        prediction = predictor.predict_emotion_trend(
            "Nouveau gouvernement Lecornu", 
            days_ahead=7
        )
        
        if prediction['success']:
            print(f"EVENT: Événement: {prediction['event']}")
            print(f"EMOTION: Émotion prédite: {prediction['predicted_emotion']}")
            print(f"CONFIDENCE: Confiance: {prediction['confidence']:.2%}")
            print(f"TIMELINE: Prédiction sur {prediction['days_ahead']} jours:")
            
            for trend in prediction['trend']:
                print(f"  Jour {trend['day']}: {trend['emotion']} ({trend['sentiment_score']:.2f})")
            
            print("\nRECOMMENDATIONS:")
            for rec in prediction['recommendations']:
                print(f"  {rec}")
        else:
            print(f"ERROR: Erreur prédiction: {prediction['error']}")
    else:
        print(f"ERROR: Erreur entraînement: {train_result['error']}")

if __name__ == "__main__":
    main()
