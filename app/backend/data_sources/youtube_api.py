"""
Source YouTube API - Semantic Pulse X
Collecte des commentaires et métadonnées YouTube
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import requests

from app.backend.core.anonymization import anonymizer
from app.backend.core.config import settings


class YouTubeAPISource:
    """Source de données YouTube API"""

    def __init__(self):
        self.api_key = settings.youtube_api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.data_dir = Path("data/raw/youtube")
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Chaînes YouTube populaires pour l'analyse
        self.channels = {
            "TF1": "UC8QMv3u5ASFM8JaqxKz_0XA",
            "France 2": "UC8QMv3u5ASFM8JaqxKz_0XA",
            "BFM TV": "UC8QMv3u5ASFM8JaqxKz_0XA",
            "Canal+": "UC8QMv3u5ASFM8JaqxKz_0XA"
        }

    def search_videos(self, query: str, max_results: int = 50) -> list[dict[str, Any]]:
        """Recherche des vidéos YouTube"""
        print(f"🔍 Recherche de vidéos pour: {query}")

        if not self.api_key:
            print("⚠️ Clé API YouTube non configurée, utilisation de données simulées")
            return self._simulate_video_search(query, max_results)

        try:
            url = f"{self.base_url}/search"
            params = {
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": max_results,
                "key": self.api_key,
                "publishedAfter": (datetime.now() - timedelta(days=30)).isoformat() + "Z"
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            videos = []

            for item in data.get("items", []):
                video = {
                    "video_id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "channel_title": item["snippet"]["channelTitle"],
                    "published_at": item["snippet"]["publishedAt"],
                    "thumbnail": item["snippet"]["thumbnails"]["default"]["url"]
                }
                videos.append(video)

            print(f"✅ {len(videos)} vidéos trouvées")
            return videos

        except Exception as e:
            print(f"❌ Erreur recherche YouTube: {e}")
            return self._simulate_video_search(query, max_results)

    def get_video_comments(self, video_id: str, max_results: int = 100) -> list[dict[str, Any]]:
        """Récupère les commentaires d'une vidéo"""
        print(f"💬 Récupération des commentaires pour la vidéo {video_id}")

        if not self.api_key:
            print("⚠️ Clé API YouTube non configurée, utilisation de données simulées")
            return self._simulate_comments(video_id, max_results)

        try:
            url = f"{self.base_url}/commentThreads"
            params = {
                "part": "snippet",
                "videoId": video_id,
                "maxResults": max_results,
                "key": self.api_key,
                "order": "time"
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            comments = []

            for item in data.get("items", []):
                comment = item["snippet"]["topLevelComment"]["snippet"]

                # Anonymiser le commentaire
                anonymized_text = anonymizer.anonymize_text(comment["textDisplay"])

                comment_data = {
                    "comment_id": item["id"],
                    "video_id": video_id,
                    "text": anonymized_text,
                    "author": comment["authorDisplayName"],
                    "published_at": comment["publishedAt"],
                    "like_count": comment["likeCount"],
                    "reply_count": comment["totalReplyCount"]
                }
                comments.append(comment_data)

            print(f"✅ {len(comments)} commentaires récupérés")
            return comments

        except Exception as e:
            print(f"❌ Erreur récupération commentaires: {e}")
            return self._simulate_comments(video_id, max_results)

    def get_channel_videos(self, channel_id: str, max_results: int = 50) -> list[dict[str, Any]]:
        """Récupère les vidéos d'une chaîne"""
        print(f"📺 Récupération des vidéos de la chaîne {channel_id}")

        if not self.api_key:
            print("⚠️ Clé API YouTube non configurée, utilisation de données simulées")
            return self._simulate_channel_videos(channel_id, max_results)

        try:
            # D'abord, récupérer l'ID de la chaîne
            url = f"{self.base_url}/channels"
            params = {
                "part": "contentDetails",
                "id": channel_id,
                "key": self.api_key
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            uploads_playlist_id = data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

            # Récupérer les vidéos de la playlist
            url = f"{self.base_url}/playlistItems"
            params = {
                "part": "snippet",
                "playlistId": uploads_playlist_id,
                "maxResults": max_results,
                "key": self.api_key
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            videos = []

            for item in data.get("items", []):
                video = {
                    "video_id": item["snippet"]["resourceId"]["videoId"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "published_at": item["snippet"]["publishedAt"],
                    "thumbnail": item["snippet"]["thumbnails"]["default"]["url"]
                }
                videos.append(video)

            print(f"✅ {len(videos)} vidéos récupérées de la chaîne")
            return videos

        except Exception as e:
            print(f"❌ Erreur récupération chaîne: {e}")
            return self._simulate_channel_videos(channel_id, max_results)

    def analyze_video_sentiment(self, video_id: str) -> dict[str, Any]:
        """Analyse le sentiment d'une vidéo basé sur ses commentaires"""
        comments = self.get_video_comments(video_id)

        if not comments:
            return {"error": "Aucun commentaire trouvé"}

        # Analyser les sentiments des commentaires
        sentiments = []
        for comment in comments:
            text = comment["text"]

            # Analyse simple du sentiment
            positive_words = ["bien", "bon", "excellent", "génial", "super", "parfait"]
            negative_words = ["mal", "mauvais", "nul", "décevant", "horrible", "terrible"]

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
                "text": text
            })

        # Calculer les statistiques
        sentiment_counts = {}
        for s in sentiments:
            sentiment_counts[s["sentiment"]] = sentiment_counts.get(s["sentiment"], 0) + 1

        avg_polarity = sum(s["polarity"] for s in sentiments) / len(sentiments)

        return {
            "video_id": video_id,
            "total_comments": len(comments),
            "sentiment_distribution": sentiment_counts,
            "average_polarity": avg_polarity,
            "dominant_sentiment": max(sentiment_counts, key=sentiment_counts.get),
            "comments": sentiments[:10]  # Top 10 commentaires
        }

    def _simulate_video_search(self, query: str, max_results: int) -> list[dict[str, Any]]:
        """Simule une recherche de vidéos"""
        videos = []
        for i in range(min(max_results, 20)):
            videos.append({
                "video_id": f"video_{i}",
                "title": f"Vidéo sur {query} #{i+1}",
                "description": f"Description de la vidéo sur {query}",
                "channel_title": f"Chaîne {i%5}",
                "published_at": (datetime.now() - timedelta(days=i)).isoformat() + "Z",
                "thumbnail": f"https://example.com/thumb_{i}.jpg"
            })
        return videos

    def _simulate_comments(self, video_id: str, max_results: int) -> list[dict[str, Any]]:
        """Simule des commentaires"""
        comments = []
        comment_templates = [
            "Super vidéo !",
            "Très intéressant",
            "Je ne suis pas d'accord",
            "Excellent travail",
            "Bof, pas terrible",
            "Génial !",
            "Décevant...",
            "Merci pour le partage",
            "C'est n'importe quoi",
            "Parfait !"
        ]

        for i in range(min(max_results, 50)):
            comment_text = np.random.choice(comment_templates)
            comments.append({
                "comment_id": f"comment_{i}",
                "video_id": video_id,
                "text": anonymizer.anonymize_text(comment_text),
                "author": f"user_{i}",
                "published_at": (datetime.now() - timedelta(hours=i)).isoformat() + "Z",
                "like_count": np.random.randint(0, 100),
                "reply_count": np.random.randint(0, 10)
            })
        return comments

    def _simulate_channel_videos(self, channel_id: str, max_results: int) -> list[dict[str, Any]]:
        """Simule des vidéos de chaîne"""
        videos = []
        for i in range(min(max_results, 30)):
            videos.append({
                "video_id": f"channel_video_{i}",
                "title": f"Vidéo de chaîne #{i+1}",
                "description": "Description de la vidéo de chaîne",
                "published_at": (datetime.now() - timedelta(days=i)).isoformat() + "Z",
                "thumbnail": f"https://example.com/channel_thumb_{i}.jpg"
            })
        return videos

    def save_data(self, data: list[dict[str, Any]], filename: str):
        """Sauvegarde les données"""
        filepath = self.data_dir / filename

        if filename.endswith('.json'):
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        else:
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False)

        print(f"✅ Données sauvegardées: {filepath}")


# Instance globale
youtube_api_source = YouTubeAPISource()
