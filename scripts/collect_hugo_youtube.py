#!/usr/bin/env python3
"""
Collecte YouTube Hugo Decrypte - Semantic Pulse X
Collecte les dernières vidéos de Hugo Decrypte pour l'analyse émotionnelle
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HugoYouTubeCollector:
    """Collecteur YouTube pour Hugo Decrypte"""
    
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        self.channel_id = "UCsXVk37bltHxD1rDPwtNM8Q"  # Hugo Decrypte
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
    def collect_latest_videos(self, max_results=10):
        """Collecte les dernières vidéos de Hugo Decrypte"""
        
        if not self.api_key:
            logger.error("Clé API YouTube manquante")
            return []
        
        try:
            # 1. Récupérer les dernières vidéos
            videos_url = f"{self.base_url}/search"
            params = {
                'key': self.api_key,
                'channelId': self.channel_id,
                'part': 'snippet',
                'order': 'date',
                'type': 'video',
                'maxResults': max_results
            }
            
            response = requests.get(videos_url, params=params, timeout=30)
            response.raise_for_status()
            
            search_data = response.json()
            video_ids = [item['id']['videoId'] for item in search_data['items']]
            
            # 2. Récupérer les détails des vidéos
            details_url = f"{self.base_url}/videos"
            details_params = {
                'key': self.api_key,
                'id': ','.join(video_ids),
                'part': 'snippet,statistics'
            }
            
            details_response = requests.get(details_url, params=details_params, timeout=30)
            details_response.raise_for_status()
            
            details_data = details_response.json()
            
            # 3. Formater les données
            videos = []
            for video in details_data['items']:
                video_data = {
                    'video_id': video['id'],
                    'title': video['snippet']['title'],
                    'description': video['snippet']['description'],
                    'published_at': video['snippet']['publishedAt'],
                    'view_count': int(video['statistics'].get('viewCount', 0)),
                    'like_count': int(video['statistics'].get('likeCount', 0)),
                    'comment_count': int(video['statistics'].get('commentCount', 0)),
                    'thumbnail': video['snippet']['thumbnails']['default']['url'],
                    'channel_title': video['snippet']['channelTitle'],
                    'collected_at': datetime.now().isoformat()
                }
                videos.append(video_data)
            
            logger.info(f"SUCCESS: {len(videos)} videos Hugo Decrypte collectees")
            return videos
            
        except Exception as e:
            logger.error(f"ERROR: Erreur collecte YouTube: {e}")
            return []
    
    def save_to_file(self, videos, output_dir="data/raw/external_apis"):
        """Sauvegarde les vidéos dans un fichier JSON"""
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hugo_youtube_{timestamp}.json"
        filepath = output_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(videos, f, ensure_ascii=False, indent=2)
        
        logger.info(f"SAVED: Videos sauvegardees: {filepath}")
        return filepath

def main():
    """Point d'entrée principal"""
    print("YouTube: Collecte Hugo Decrypte")
    print("=" * 40)
    
    collector = HugoYouTubeCollector()
    
    # Collecter les vidéos
    videos = collector.collect_latest_videos(max_results=15)
    
    if videos:
        # Sauvegarder
        filepath = collector.save_to_file(videos)
        
        print(f"SUCCESS: {len(videos)} videos collectees")
        print(f"SAVED: {filepath}")
        
        # Afficher quelques exemples
        print("\nEXAMPLES:")
        for i, video in enumerate(videos[:3]):
            print(f"  {i+1}. {video['title'][:50]}...")
            print(f"     Views: {video['view_count']:,}")
            print(f"     Likes: {video['like_count']:,}")
    else:
        print("ERROR: Aucune video collectee")

if __name__ == "__main__":
    main()
