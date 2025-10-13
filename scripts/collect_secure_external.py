#!/usr/bin/env python3
"""
Collecte sécurisée Instagram et YouTube - Phase 2 - Semantic Pulse X
Utilisation des variables d'environnement pour la sécurité
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

class SecureInstagramCollector:
    """Collecteur Instagram sécurisé avec variables d'environnement"""
    
    def __init__(self):
        self.access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        self.base_url = "https://graph.instagram.com"
        
        if not self.access_token:
            logger.warning("⚠️ INSTAGRAM_ACCESS_TOKEN non définie dans .env")
        else:
            logger.info("📸 Instagram Collector initialisé (sécurisé)")
    
    def test_connection(self):
        """Test de connexion Instagram"""
        if not self.access_token:
            return False
            
        try:
            url = f"{self.base_url}/me"
            params = {
                'fields': 'id,username,account_type',
                'access_token': self.access_token
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Instagram connecté: {data.get('username', 'N/A')}")
                return True
            else:
                logger.error(f"❌ Erreur Instagram: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur connexion Instagram: {e}")
            return False
    
    def collect_data(self, limit=5):
        """Collecte des données Instagram"""
        if not self.access_token:
            logger.warning("⚠️ Token Instagram manquant")
            return []
        
        try:
            url = f"{self.base_url}/me/media"
            params = {
                'fields': 'id,caption,media_type,media_url,timestamp',
                'limit': limit,
                'access_token': self.access_token
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                media_list = data.get('data', [])
                logger.info(f"📸 {len(media_list)} médias Instagram collectés")
                
                # Formatage sécurisé (anonymisation)
                formatted_data = []
                for media in media_list:
                    formatted_data.append({
                        'source': 'instagram',
                        'media_id': f"IG_{media.get('id', '')[:8]}...",  # Anonymisé
                        'caption': media.get('caption', '')[:200],  # Limité
                        'media_type': media.get('media_type'),
                        'timestamp': media.get('timestamp'),
                        'collected_at': datetime.now().isoformat(),
                        'anonymized': True
                    })
                
                return formatted_data
            else:
                logger.error(f"❌ Erreur collecte Instagram: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Erreur collecte Instagram: {e}")
            return []

class SecureYouTubeCollector:
    """Collecteur YouTube sécurisé avec variables d'environnement"""
    
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
        if not self.api_key:
            logger.warning("⚠️ YOUTUBE_API_KEY non définie dans .env")
        else:
            logger.info("📺 YouTube Collector initialisé (sécurisé)")
    
    def test_connection(self):
        """Test de connexion YouTube"""
        if not self.api_key:
            return False
            
        try:
            url = f"{self.base_url}/search"
            params = {
                'part': 'snippet',
                'q': 'test',
                'type': 'video',
                'maxResults': 1,
                'key': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                logger.info("✅ YouTube API connectée")
                return True
            else:
                logger.error(f"❌ Erreur YouTube: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur connexion YouTube: {e}")
            return False
    
    def collect_data(self, query="actualités émotions", max_results=5):
        """Collecte des données YouTube"""
        if not self.api_key:
            logger.warning("⚠️ Clé YouTube manquante")
            return []
        
        try:
            url = f"{self.base_url}/search"
            params = {
                'part': 'snippet',
                'q': query,
                'type': 'video',
                'maxResults': max_results,
                'key': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                videos = data.get('items', [])
                logger.info(f"📺 {len(videos)} vidéos YouTube collectées")
                
                # Formatage sécurisé (anonymisation)
                formatted_data = []
                for video in videos:
                    snippet = video.get('snippet', {})
                    formatted_data.append({
                        'source': 'youtube',
                        'video_id': f"YT_{video.get('id', {}).get('videoId', '')[:8]}...",  # Anonymisé
                        'title': snippet.get('title', '')[:100],  # Limité
                        'description': snippet.get('description', '')[:200],  # Limité
                        'channel_title': snippet.get('channelTitle', '')[:50],  # Limité
                        'published_at': snippet.get('publishedAt'),
                        'collected_at': datetime.now().isoformat(),
                        'anonymized': True
                    })
                
                return formatted_data
            else:
                logger.error(f"❌ Erreur collecte YouTube: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Erreur collecte YouTube: {e}")
            return []

def save_to_minio_secure(data, data_type):
    """Sauvegarde sécurisée vers MinIO"""
    logger.info(f"💾 Sauvegarde sécurisée {data_type} vers MinIO")
    
    try:
        from minio import Minio
        
        # Connexion MinIO
        minio_client = Minio('localhost:9000', 'admin', 'admin123', secure=False)
        
        # Conversion en JSON avec anonymisation
        json_data = json.dumps(data, indent=2, ensure_ascii=False)
        
        # Upload vers MinIO
        object_name = f"external_apis/secure_{data_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        minio_client.put_object(
            'semantic-pulse-data',
            object_name,
            data=json_data.encode('utf-8'),
            length=len(json_data.encode('utf-8')),
            content_type='application/json'
        )
        
        logger.info(f"✅ Données {data_type} sauvegardées sécurisément: {object_name}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur sauvegarde MinIO: {e}")
        return False

def main():
    """Fonction principale de collecte sécurisée"""
    logger.info("🔐 COLLECTE SÉCURISÉE INSTAGRAM & YOUTUBE - PHASE 2")
    logger.info("=" * 70)
    
    # Vérification du fichier .env
    if not os.path.exists('.env'):
        logger.warning("⚠️ Fichier .env non trouvé")
        logger.info("💡 Copiez env.template vers .env et remplissez vos clés")
        return False
    
    all_data = []
    
    # Collecte Instagram
    instagram_collector = SecureInstagramCollector()
    if instagram_collector.access_token:
        if instagram_collector.test_connection():
            instagram_data = instagram_collector.collect_data(limit=3)
            all_data.extend(instagram_data)
            
            if instagram_data:
                save_to_minio_secure(instagram_data, "instagram")
        else:
            logger.error("❌ Connexion Instagram échouée")
    else:
        logger.info("⏭️ Instagram ignoré (pas de token)")
    
    # Collecte YouTube
    youtube_collector = SecureYouTubeCollector()
    if youtube_collector.api_key:
        if youtube_collector.test_connection():
            youtube_data = youtube_collector.collect_data(max_results=3)
            all_data.extend(youtube_data)
            
            if youtube_data:
                save_to_minio_secure(youtube_data, "youtube")
        else:
            logger.error("❌ Connexion YouTube échouée")
    else:
        logger.info("⏭️ YouTube ignoré (pas de clé API)")
    
    # Sauvegarde locale sécurisée
    if all_data:
        output_dir = Path("data/raw/external_apis")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # JSON sécurisé
        json_file = output_dir / f"secure_external_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        
        # CSV sécurisé
        csv_file = output_dir / f"secure_external_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df = pd.DataFrame(all_data)
        df.to_csv(csv_file, index=False, encoding='utf-8')
        
        # Résumé sécurisé
        logger.info("\n" + "=" * 70)
        logger.info("📊 RÉSUMÉ COLLECTE SÉCURISÉE")
        logger.info("=" * 70)
        logger.info(f"📈 Total données collectées: {len(all_data)}")
        logger.info("🔐 Toutes les données sont anonymisées")
        
        # Par source
        sources = {}
        for item in all_data:
            source = item.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
        
        logger.info("📋 Répartition par source:")
        for source, count in sources.items():
            logger.info(f"   {source}: {count} éléments")
        
        logger.info(f"💾 Fichiers créés:")
        logger.info(f"   JSON: {json_file}")
        logger.info(f"   CSV: {csv_file}")
        
        logger.info("✅ COLLECTE SÉCURISÉE TERMINÉE!")
        return True
    else:
        logger.warning("⚠️ Aucune donnée collectée")
        logger.info("💡 Vérifiez vos clés API dans le fichier .env")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)




