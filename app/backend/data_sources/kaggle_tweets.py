"""
Source Kaggle Tweets - Semantic Pulse X
Gestion du dataset Kaggle sur les tweets avec découpage en 3 sources
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import os
from pathlib import Path
import requests
import zipfile
import json

from app.backend.core.anonymization import anonymizer
from app.backend.core.config import settings


class KaggleTweetsSource:
    """Source de données Kaggle pour les tweets"""
    
    def __init__(self):
        self.data_dir = Path("data/raw/kaggle_tweets")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # URLs des datasets Kaggle populaires
        self.datasets = {
            "sentiment140": "https://www.kaggle.com/datasets/kazanova/sentiment140",
            "twitter_sentiment": "https://www.kaggle.com/datasets/jp797498e/emotion-dataset",
            "covid_tweets": "https://www.kaggle.com/datasets/gpreda/covid19-tweets"
        }
    
    def download_kaggle_dataset(self, dataset_name: str = "sentiment140") -> str:
        """Télécharge un dataset Kaggle (simulation)"""
        print(f"📥 Téléchargement du dataset {dataset_name}...")
        
        # Simulation de téléchargement - en réalité, utiliser kaggle API
        # kaggle datasets download -d kazanova/sentiment140
        
        # Créer des données simulées basées sur le dataset réel
        if dataset_name == "sentiment140":
            return self._create_sentiment140_data()
        elif dataset_name == "twitter_sentiment":
            return self._create_emotion_dataset()
        elif dataset_name == "covid_tweets":
            return self._create_covid_tweets_data()
        else:
            raise ValueError(f"Dataset {dataset_name} non supporté")
    
    def _create_sentiment140_data(self) -> str:
        """Crée des données simulées Sentiment140"""
        # Structure du dataset Sentiment140
        data = []
        
        # Générer des tweets simulés avec sentiments
        sentiments = [0, 4]  # 0 = négatif, 4 = positif
        topics = ["politics", "sports", "entertainment", "technology", "news"]
        
        for i in range(10000):
            sentiment = np.random.choice(sentiments)
            topic = np.random.choice(topics)
            
            # Générer un tweet simulé
            if sentiment == 0:  # Négatif
                tweet_text = f"Je n'aime pas {topic} aujourd'hui. C'est vraiment décevant."
            else:  # Positif
                tweet_text = f"J'adore {topic} ! C'est fantastique et génial."
            
            data.append({
                "target": sentiment,
                "id": f"tweet_{i}",
                "date": (datetime.now() - timedelta(days=np.random.randint(0, 365))).strftime("%a %b %d %H:%M:%S %z %Y"),
                "flag": "NO_QUERY",
                "user": f"user_{i}",
                "text": tweet_text
            })
        
        # Sauvegarder
        df = pd.DataFrame(data)
        filepath = self.data_dir / "sentiment140.csv"
        df.to_csv(filepath, index=False)
        
        print(f"✅ Dataset Sentiment140 créé: {filepath}")
        return str(filepath)
    
    def _create_emotion_dataset(self) -> str:
        """Crée des données simulées d'émotions"""
        emotions = ["joy", "sadness", "anger", "fear", "surprise", "love"]
        data = []
        
        for i in range(5000):
            emotion = np.random.choice(emotions)
            
            # Générer un tweet basé sur l'émotion
            emotion_tweets = {
                "joy": ["Je suis si heureux !", "C'est fantastique !", "J'adore ça !"],
                "sadness": ["Je suis triste...", "C'est déprimant", "Pourquoi moi ?"],
                "anger": ["Je suis en colère !", "C'est inadmissible !", "Ça m'énerve !"],
                "fear": ["J'ai peur...", "C'est effrayant", "Je suis terrifié"],
                "surprise": ["Wow ! Incroyable !", "Je n'en reviens pas !", "Surprenant !"],
                "love": ["Je t'aime", "C'est magnifique", "Mon cœur fond"]
            }
            
            tweet_text = np.random.choice(emotion_tweets[emotion])
            
            data.append({
                "text": tweet_text,
                "emotion": emotion,
                "id": f"emotion_{i}",
                "timestamp": datetime.now() - timedelta(hours=np.random.randint(0, 24*30))
            })
        
        df = pd.DataFrame(data)
        filepath = self.data_dir / "emotion_dataset.csv"
        df.to_csv(filepath, index=False)
        
        print(f"✅ Dataset émotions créé: {filepath}")
        return str(filepath)
    
    def _create_covid_tweets_data(self) -> str:
        """Crée des données simulées de tweets COVID"""
        topics = ["masque", "vaccin", "confinement", "tests", "hôpital", "économie"]
        sentiments = ["positif", "négatif", "neutre"]
        
        data = []
        for i in range(3000):
            topic = np.random.choice(topics)
            sentiment = np.random.choice(sentiments)
            
            tweet_text = f"COVID-19: {topic} - {sentiment} sentiment"
            
            data.append({
                "text": tweet_text,
                "sentiment": sentiment,
                "topic": topic,
                "id": f"covid_{i}",
                "timestamp": datetime.now() - timedelta(days=np.random.randint(0, 365))
            })
        
        df = pd.DataFrame(data)
        filepath = self.data_dir / "covid_tweets.csv"
        df.to_csv(filepath, index=False)
        
        print(f"✅ Dataset COVID créé: {filepath}")
        return str(filepath)
    
    def split_into_three_sources(self, dataset_path: str) -> Dict[str, str]:
        """Découpe le dataset en 3 sources : fichier, base classique, big data"""
        print("🔄 Découpage du dataset en 3 sources...")
        
        # Charger le dataset
        df = pd.read_csv(dataset_path)
        
        # Diviser en 3 parties
        total_rows = len(df)
        part_size = total_rows // 3
        
        # Source 1: Fichier plat (CSV/JSON)
        file_data = df.iloc[:part_size].copy()
        file_path = self.data_dir / "file_source_tweets.csv"
        file_data.to_csv(file_path, index=False)
        
        # Source 2: Base classique (SQL)
        db_data = df.iloc[part_size:2*part_size].copy()
        db_path = self.data_dir / "db_source_tweets.csv"
        db_data.to_csv(db_path, index=False)
        
        # Source 3: Big Data (Parquet)
        bigdata_data = df.iloc[2*part_size:].copy()
        bigdata_path = self.data_dir / "bigdata_source_tweets.parquet"
        bigdata_data.to_parquet(bigdata_path, index=False)
        
        print(f"✅ Dataset découpé en 3 sources:")
        print(f"   - Fichier: {file_path} ({len(file_data)} lignes)")
        print(f"   - Base: {db_path} ({len(db_data)} lignes)")
        print(f"   - Big Data: {bigdata_path} ({len(bigdata_data)} lignes)")
        
        return {
            "file_source": str(file_path),
            "db_source": str(db_path),
            "bigdata_source": str(bigdata_path)
        }
    
    def process_tweets_for_semantic_pulse(self, dataset_path: str) -> List[Dict[str, Any]]:
        """Traite les tweets pour Semantic Pulse X"""
        print("🔄 Traitement des tweets pour Semantic Pulse...")
        
        # Charger le dataset
        df = pd.read_csv(dataset_path)
        
        processed_tweets = []
        
        for _, row in df.iterrows():
            # Anonymiser le texte
            anonymized_text = anonymizer.anonymize_text(row['text'])
            
            # Déterminer l'émotion basée sur le sentiment
            if 'target' in row:
                emotion = "positif" if row['target'] == 4 else "negatif"
            elif 'emotion' in row:
                emotion = row['emotion']
            elif 'sentiment' in row:
                emotion = row['sentiment']
            else:
                emotion = "neutre"
            
            # Calculer la polarité
            polarity = 1.0 if emotion in ["positif", "joy", "love"] else -1.0 if emotion in ["negatif", "sadness", "anger", "fear"] else 0.0
            
            processed_tweet = {
                "texte_anonymise": anonymized_text,
                "emotion_principale": emotion,
                "polarite": polarity,
                "score_emotion": abs(polarity),
                "confiance": 0.8,
                "timestamp": datetime.now() - timedelta(hours=np.random.randint(0, 24*7)),
                "source": "kaggle_tweets",
                "langue": "fr",
                "programme": "tweets_generaux"
            }
            
            processed_tweets.append(processed_tweet)
        
        print(f"✅ {len(processed_tweets)} tweets traités")
        return processed_tweets
    
    def get_tweet_statistics(self, dataset_path: str) -> Dict[str, Any]:
        """Retourne les statistiques du dataset"""
        df = pd.read_csv(dataset_path)
        
        stats = {
            "total_tweets": len(df),
            "columns": list(df.columns),
            "date_range": {
                "start": df['timestamp'].min() if 'timestamp' in df.columns else "N/A",
                "end": df['timestamp'].max() if 'timestamp' in df.columns else "N/A"
            },
            "emotion_distribution": df['emotion'].value_counts().to_dict() if 'emotion' in df.columns else {},
            "sentiment_distribution": df['sentiment'].value_counts().to_dict() if 'sentiment' in df.columns else {}
        }
        
        return stats


# Instance globale
kaggle_tweets_source = KaggleTweetsSource()
