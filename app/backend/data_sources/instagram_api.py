"""
Source Instagram API - Semantic Pulse X
Collecte des posts et commentaires Instagram
"""

import requests
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import time
import json
from pathlib import Path
import numpy as np

from app.backend.core.anonymization import anonymizer
from app.backend.core.config import settings


class InstagramAPISource:
    """Source de données Instagram API"""
    
    def __init__(self):
        self.access_token = settings.instagram_access_token
        self.base_url = "https://graph.instagram.com"
        self.data_dir = Path("data/raw/instagram")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Comptes Instagram populaires pour l'analyse
        self.accounts = {
            "TF1": "tf1",
            "France 2": "france2",
            "BFM TV": "bfmtv",
            "Canal+": "canalplus"
        }
    
    def get_user_posts(self, username: str, count: int = 25) -> List[Dict[str, Any]]:
        """Récupère les posts d'un utilisateur Instagram"""
        print(f"📸 Récupération des posts Instagram de @{username}")
        
        if not self.access_token:
            print("⚠️ Token Instagram non configuré, utilisation de données simulées")
            return self._simulate_posts(username, count)
        
        try:
            # D'abord, récupérer l'ID utilisateur
            user_id = self._get_user_id(username)
            if not user_id:
                return self._simulate_posts(username, count)
            
            # Récupérer les posts
            url = f"{self.base_url}/{user_id}/media"
            params = {
                "fields": "id,caption,media_type,media_url,thumbnail_url,timestamp,like_count,comments_count",
                "limit": count,
                "access_token": self.access_token
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            posts = []
            
            for item in data.get("data", []):
                post = {
                    "post_id": item["id"],
                    "username": username,
                    "caption": anonymizer.anonymize_text(item.get("caption", "")),
                    "media_type": item["media_type"],
                    "media_url": item.get("media_url", ""),
                    "thumbnail_url": item.get("thumbnail_url", ""),
                    "timestamp": item["timestamp"],
                    "like_count": item.get("like_count", 0),
                    "comments_count": item.get("comments_count", 0)
                }
                posts.append(post)
            
            print(f"✅ {len(posts)} posts récupérés")
            return posts
            
        except Exception as e:
            print(f"❌ Erreur récupération posts Instagram: {e}")
            return self._simulate_posts(username, count)
    
    def get_post_comments(self, post_id: str, count: int = 100) -> List[Dict[str, Any]]:
        """Récupère les commentaires d'un post Instagram"""
        print(f"💬 Récupération des commentaires du post {post_id}")
        
        if not self.access_token:
            print("⚠️ Token Instagram non configuré, utilisation de données simulées")
            return self._simulate_comments(post_id, count)
        
        try:
            url = f"{self.base_url}/{post_id}/comments"
            params = {
                "fields": "id,text,timestamp,like_count,username",
                "limit": count,
                "access_token": self.access_token
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            comments = []
            
            for item in data.get("data", []):
                comment = {
                    "comment_id": item["id"],
                    "post_id": post_id,
                    "text": anonymizer.anonymize_text(item["text"]),
                    "username": item["username"],
                    "timestamp": item["timestamp"],
                    "like_count": item.get("like_count", 0)
                }
                comments.append(comment)
            
            print(f"✅ {len(comments)} commentaires récupérés")
            return comments
            
        except Exception as e:
            print(f"❌ Erreur récupération commentaires: {e}")
            return self._simulate_comments(post_id, count)
    
    def search_hashtags(self, hashtag: str, count: int = 50) -> List[Dict[str, Any]]:
        """Recherche des posts par hashtag"""
        print(f"🔍 Recherche de posts avec le hashtag #{hashtag}")
        
        if not self.access_token:
            print("⚠️ Token Instagram non configuré, utilisation de données simulées")
            return self._simulate_hashtag_posts(hashtag, count)
        
        try:
            # Note: L'API Instagram Basic Display ne supporte pas la recherche par hashtag
            # Cette fonctionnalité nécessite l'API Instagram Business
            print("⚠️ Recherche par hashtag non supportée avec l'API actuelle")
            return self._simulate_hashtag_posts(hashtag, count)
            
        except Exception as e:
            print(f"❌ Erreur recherche hashtag: {e}")
            return self._simulate_hashtag_posts(hashtag, count)
    
    def analyze_post_engagement(self, post_id: str) -> Dict[str, Any]:
        """Analyse l'engagement d'un post"""
        comments = self.get_post_comments(post_id)
        
        if not comments:
            return {"error": "Aucun commentaire trouvé"}
        
        # Analyser les sentiments des commentaires
        sentiments = []
        for comment in comments:
            text = comment["text"]
            
            # Analyse simple du sentiment
            positive_words = ["bien", "bon", "excellent", "génial", "super", "parfait", "❤️", "🔥", "👏"]
            negative_words = ["mal", "mauvais", "nul", "décevant", "horrible", "terrible", "😡", "👎"]
            
            positive_count = sum(1 for word in positive_words if word in text.lower())
            negative_count = sum(1 for word in negative_words if word in text.lower())
            
            if positive_count > negative_count:
                sentiment = "positif"
                polarity = 0.7
            elif negative_count > positive_count:
                sentiment = "negatif"
                polarity = -0.7
            else:
                sentiment = "neutre"
                polarity = 0.0
            
            sentiments.append({
                "sentiment": sentiment,
                "polarity": polarity,
                "text": text,
                "like_count": comment["like_count"]
            })
        
        # Calculer les statistiques
        sentiment_counts = {}
        for s in sentiments:
            sentiment_counts[s["sentiment"]] = sentiment_counts.get(s["sentiment"], 0) + 1
        
        avg_polarity = sum(s["polarity"] for s in sentiments) / len(sentiments)
        total_likes = sum(s["like_count"] for s in sentiments)
        
        return {
            "post_id": post_id,
            "total_comments": len(comments),
            "total_likes": total_likes,
            "sentiment_distribution": sentiment_counts,
            "average_polarity": avg_polarity,
            "dominant_sentiment": max(sentiment_counts, key=sentiment_counts.get),
            "engagement_rate": (len(comments) + total_likes) / max(len(comments), 1),
            "top_comments": sorted(sentiments, key=lambda x: x["like_count"], reverse=True)[:5]
        }
    
    def get_trending_content(self, count: int = 50) -> List[Dict[str, Any]]:
        """Récupère le contenu tendance (simulation)"""
        print("📈 Récupération du contenu tendance Instagram")
        
        # Simulation de contenu tendance
        trending_topics = [
            "actualité", "sport", "mode", "cuisine", "voyage", 
            "technologie", "musique", "cinéma", "politique", "économie"
        ]
        
        trending_posts = []
        for i in range(count):
            topic = np.random.choice(trending_topics)
            engagement = np.random.randint(100, 10000)
            
            post = {
                "post_id": f"trending_{i}",
                "username": f"user_{i}",
                "caption": f"Post tendance sur {topic} #{topic}",
                "hashtags": [f"#{topic}", "#tendance", "#viral"],
                "like_count": engagement,
                "comments_count": engagement // 10,
                "timestamp": datetime.now() - timedelta(hours=np.random.randint(0, 24*7)),
                "engagement_rate": engagement / 1000
            }
            trending_posts.append(post)
        
        print(f"✅ {len(trending_posts)} posts tendance récupérés")
        return trending_posts
    
    def _get_user_id(self, username: str) -> Optional[str]:
        """Récupère l'ID utilisateur Instagram"""
        try:
            url = f"{self.base_url}/me"
            params = {
                "fields": "id,username",
                "access_token": self.access_token
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return data.get("id")
            
        except Exception as e:
            print(f"❌ Erreur récupération ID utilisateur: {e}")
            return None
    
    def _simulate_posts(self, username: str, count: int) -> List[Dict[str, Any]]:
        """Simule des posts Instagram"""
        posts = []
        for i in range(count):
            posts.append({
                "post_id": f"post_{i}",
                "username": username,
                "caption": f"Post Instagram #{i+1} de @{username}",
                "media_type": "IMAGE",
                "media_url": f"https://example.com/instagram_{i}.jpg",
                "timestamp": (datetime.now() - timedelta(hours=i)).isoformat() + "Z",
                "like_count": np.random.randint(10, 1000),
                "comments_count": np.random.randint(0, 100)
            })
        return posts
    
    def _simulate_comments(self, post_id: str, count: int) -> List[Dict[str, Any]]:
        """Simule des commentaires Instagram"""
        comments = []
        comment_templates = [
            "Super ! 🔥",
            "J'adore ! ❤️",
            "Très beau",
            "Pas mal",
            "Génial ! 👏",
            "Bof...",
            "Excellent !",
            "Magnifique !",
            "Pas terrible",
            "Parfait !"
        ]
        
        for i in range(count):
            comment_text = np.random.choice(comment_templates)
            comments.append({
                "comment_id": f"comment_{i}",
                "post_id": post_id,
                "text": anonymizer.anonymize_text(comment_text),
                "username": f"user_{i}",
                "timestamp": (datetime.now() - timedelta(hours=i)).isoformat() + "Z",
                "like_count": np.random.randint(0, 50)
            })
        return comments
    
    def _simulate_hashtag_posts(self, hashtag: str, count: int) -> List[Dict[str, Any]]:
        """Simule des posts par hashtag"""
        posts = []
        for i in range(count):
            posts.append({
                "post_id": f"hashtag_{i}",
                "username": f"user_{i}",
                "caption": f"Post avec #{hashtag} #{hashtag}",
                "hashtags": [f"#{hashtag}", "#trending"],
                "like_count": np.random.randint(50, 500),
                "comments_count": np.random.randint(5, 50),
                "timestamp": datetime.now() - timedelta(hours=np.random.randint(0, 24*3))
            })
        return posts
    
    def save_data(self, data: List[Dict[str, Any]], filename: str):
        """Sauvegarde les données"""
        filepath = self.data_dir / filename
        
        if filename.endswith('.json'):
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        else:
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False)
        
        print(f"✅ Données Instagram sauvegardées: {filepath}")


# Instance globale
instagram_api_source = InstagramAPISource()
