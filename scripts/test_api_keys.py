#!/usr/bin/env python3
"""
Test des clés API - Phase 2 - Semantic Pulse X
Test simple et rapide de la connexion YouTube
"""

import os
import requests
import logging
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_youtube_api():
    """Test de la clé YouTube API"""
    logger.info("📺 Test YouTube Data API v3")
    
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        logger.error("❌ YOUTUBE_API_KEY non définie dans .env")
        return False
    
    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            'part': 'snippet',
            'q': 'test',
            'type': 'video',
            'maxResults': 1,
            'key': api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ YouTube API OK - {len(data.get('items', []))} résultat(s)")
            return True
        else:
            logger.error(f"❌ Erreur YouTube API: {response.status_code}")
            logger.error(f"   Réponse: {response.text[:200]}...")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erreur YouTube API: {e}")
        return False

def check_env_file():
    """Vérifie le fichier .env"""
    logger.info("🔍 Vérification du fichier .env")
    
    if not os.path.exists('.env'):
        logger.error("❌ Fichier .env non trouvé")
        logger.info("💡 Copiez env.template vers .env et remplissez vos clés")
        return False
    
    logger.info("✅ Fichier .env trouvé")
    
    # Vérification des variables
    youtube_key = os.getenv('YOUTUBE_API_KEY')
    
    if youtube_key:
        logger.info(f"✅ YOUTUBE_API_KEY définie: {youtube_key[:10]}...")
    else:
        logger.warning("⚠️ YOUTUBE_API_KEY non définie")
    
    return youtube_key is not None

def main():
    """Fonction principale de test"""
    logger.info("🧪 TEST DES CLÉS API - PHASE 2")
    logger.info("=" * 50)
    
    # Vérification du fichier .env
    if not check_env_file():
        logger.error("❌ Configuration manquante")
        return False
    
    # Test de l'API YouTube
    youtube_ok = test_youtube_api()
    
    # Résumé
    logger.info("\n" + "=" * 50)
    logger.info("📊 RÉSUMÉ DES TESTS")
    logger.info("=" * 50)
    
    if youtube_ok:
        logger.info("✅ YouTube API: OK")
        logger.info("🎉 YouTube API fonctionne!")
        logger.info("🚀 Vous pouvez lancer la collecte")
        return True
    else:
        logger.error("❌ YouTube API: KO")
        logger.info("💡 Vérifiez votre clé API dans le fichier .env")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
