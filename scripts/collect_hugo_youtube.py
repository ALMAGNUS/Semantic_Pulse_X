#!/usr/bin/env python3
"""
Collecte YouTube spécifique - Hugo Decrypte - Semantic Pulse X
Collecte les données d'une chaîne YouTube spécifique
"""

import os
import requests
import logging
import json
from pathlib import Path
from datetime import datetime
import time
import pandas as pd
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HugoYouTubeCollector:
    """Collecteur spécialisé pour la chaîne Hugo Decrypte"""
    
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        self.channel_id = "UCAcAnMF0OrCtUep3Y4M-ZPw"  # Hugo Decrypte
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.output_dir = Path("data/raw/external_apis")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.api_key:
            logger.error("❌ YOUTUBE_API_KEY non définie dans .env")
        else:
            logger.info("📺 Collecteur Hugo YouTube initialisé")
            logger.info(f"🎯 Chaîne cible: {self.channel_id}")
    
    def get_channel_info(self):
        """Récupère les informations de la chaîne"""
        logger.info("📊 Récupération des informations de la chaîne...")
        
        try:
            url = f"{self.base_url}/channels"
            params = {
                'part': 'snippet,statistics',
                'id': self.channel_id,
                'key': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            channels = data.get('items', [])
            
            if channels:
                channel = channels[0]
                info = {
                    'channel_id': self.channel_id,
                    'title': channel['snippet']['title'],
                    'description': channel['snippet']['description'],
                    'subscriber_count': channel['statistics'].get('subscriberCount', '0'),
                    'video_count': channel['statistics'].get('videoCount', '0'),
                    'view_count': channel['statistics'].get('viewCount', '0'),
                    'collected_at': datetime.now().isoformat()
                }
                
                logger.info(f"✅ Chaîne trouvée: {info['title']}")
                logger.info(f"   👥 Abonnés: {info['subscriber_count']}")
                logger.info(f"   📹 Vidéos: {info['video_count']}")
                logger.info(f"   👀 Vues totales: {info['view_count']}")
                
                return info
            else:
                logger.error("❌ Chaîne non trouvée")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erreur récupération chaîne: {e}")
            return None
    
    def get_recent_videos(self, max_results=10):
        """Récupère les vidéos récentes de la chaîne"""
        logger.info(f"📹 Récupération des {max_results} vidéos récentes...")
        
        try:
            url = f"{self.base_url}/search"
            params = {
                'part': 'snippet',
                'channelId': self.channel_id,
                'type': 'video',
                'order': 'date',
                'maxResults': max_results,
                'key': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            videos = data.get('items', [])
            
            video_details = []
            for video in videos:
                video_id = video['id']['videoId']
                snippet = video['snippet']
                
                # Récupérer les détails supplémentaires
                details = self.get_video_details(video_id)
                if details:
                    video_info = {
                        'video_id': video_id,
                        'title': snippet['title'],
                        'description': snippet['description'],
                        'published_at': snippet['publishedAt'],
                        'channel_title': snippet['channelTitle'],
                        'view_count': details.get('view_count', 0),
                        'like_count': details.get('like_count', 0),
                        'comment_count': details.get('comment_count', 0),
                        'duration': details.get('duration', ''),
                        'tags': details.get('tags', []),
                        'collected_at': datetime.now().isoformat()
                    }
                    video_details.append(video_info)
                
                # Pause pour éviter les limites de rate
                time.sleep(0.1)
            
            logger.info(f"✅ {len(video_details)} vidéos récupérées")
            return video_details
            
        except Exception as e:
            logger.error(f"❌ Erreur récupération vidéos: {e}")
            return []
    
    def get_video_details(self, video_id):
        """Récupère les détails d'une vidéo spécifique"""
        try:
            url = f"{self.base_url}/videos"
            params = {
                'part': 'statistics,contentDetails',
                'id': video_id,
                'key': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            videos = data.get('items', [])
            
            if videos:
                video = videos[0]
                return {
                    'view_count': int(video['statistics'].get('viewCount', 0)),
                    'like_count': int(video['statistics'].get('likeCount', 0)),
                    'comment_count': int(video['statistics'].get('commentCount', 0)),
                    'duration': video['contentDetails']['duration']
                }
            return None
            
        except Exception as e:
            logger.warning(f"⚠️ Erreur détails vidéo {video_id}: {e}")
            return None
    
    def anonymize_data(self, data):
        """Anonymise les données pour RGPD"""
        logger.info("🛡️ Anonymisation des données...")
        
        anonymized_data = []
        for item in data:
            # Supprimer les informations personnelles
            anonymized_item = {
                'content': item.get('title', '') + ' ' + item.get('description', ''),
                'source': 'youtube_hugo',
                'timestamp': item.get('published_at', ''),
                'metadata': {
                    'video_id_hash': hash(item.get('video_id', '')) % (10**8),
                    'view_count': item.get('view_count', 0),
                    'like_count': item.get('like_count', 0),
                    'duration': item.get('duration', '')
                },
                'anonymized': True,
                'collected_at': item.get('collected_at', '')
            }
            anonymized_data.append(anonymized_item)
        
        logger.info(f"✅ {len(anonymized_data)} éléments anonymisés")
        return anonymized_data
    
    def save_data(self, channel_info, videos_data, anonymized_data):
        """Sauvegarde les données collectées"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Sauvegarde des informations de la chaîne
        channel_file = self.output_dir / f"hugo_channel_info_{timestamp}.json"
        with open(channel_file, 'w', encoding='utf-8') as f:
            json.dump(channel_info, f, ensure_ascii=False, indent=2)
        
        # Sauvegarde des vidéos détaillées
        videos_file = self.output_dir / f"hugo_videos_{timestamp}.json"
        with open(videos_file, 'w', encoding='utf-8') as f:
            json.dump(videos_data, f, ensure_ascii=False, indent=2)
        
        # Sauvegarde des données anonymisées
        anonymized_file = self.output_dir / f"hugo_anonymized_{timestamp}.json"
        with open(anonymized_file, 'w', encoding='utf-8') as f:
            json.dump(anonymized_data, f, ensure_ascii=False, indent=2)
        
        # Sauvegarde CSV pour analyse
        csv_file = self.output_dir / f"hugo_data_{timestamp}.csv"
        df = pd.DataFrame(anonymized_data)
        df.to_csv(csv_file, index=False, encoding='utf-8')
        
        logger.info(f"💾 Données sauvegardées:")
        logger.info(f"   📊 Chaîne: {channel_file}")
        logger.info(f"   📹 Vidéos: {videos_file}")
        logger.info(f"   🛡️ Anonymisées: {anonymized_file}")
        logger.info(f"   📈 CSV: {csv_file}")
        
        return {
            'channel_file': str(channel_file),
            'videos_file': str(videos_file),
            'anonymized_file': str(anonymized_file),
            'csv_file': str(csv_file)
        }
    
    def collect_hugo_data(self, max_videos=10):
        """Collecte complète des données Hugo"""
        logger.info("🚀 DÉBUT DE LA COLLECTE HUGO DECRYPTE")
        logger.info("=" * 60)
        
        if not self.api_key:
            logger.error("❌ Clé API YouTube manquante")
            return False
        
        # 1. Informations de la chaîne
        channel_info = self.get_channel_info()
        if not channel_info:
            return False
        
        # 2. Vidéos récentes
        videos_data = self.get_recent_videos(max_videos)
        if not videos_data:
            logger.warning("⚠️ Aucune vidéo récupérée")
            return False
        
        # 3. Anonymisation
        anonymized_data = self.anonymize_data(videos_data)
        
        # 4. Sauvegarde
        files = self.save_data(channel_info, videos_data, anonymized_data)
        
        # 5. Résumé
        logger.info("\n" + "=" * 60)
        logger.info("📊 RÉSUMÉ DE LA COLLECTE")
        logger.info("=" * 60)
        logger.info(f"📺 Chaîne: {channel_info['title']}")
        logger.info(f"👥 Abonnés: {channel_info['subscriber_count']}")
        logger.info(f"📹 Vidéos collectées: {len(videos_data)}")
        logger.info(f"🛡️ Données anonymisées: {len(anonymized_data)}")
        logger.info("=" * 60)
        
        return True

def main():
    """Fonction principale"""
    logger.info("📺 COLLECTE HUGO DECRYPTE - SEMANTIC PULSE X")
    
    collector = HugoYouTubeCollector()
    
    try:
        success = collector.collect_hugo_data(max_videos=15)
        if success:
            logger.info("🎉 Collecte Hugo terminée avec succès!")
            return True
        else:
            logger.error("❌ Échec de la collecte Hugo")
            return False
    except Exception as e:
        logger.error(f"❌ Erreur lors de la collecte: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)




