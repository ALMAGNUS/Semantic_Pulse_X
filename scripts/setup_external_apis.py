#!/usr/bin/env python3
"""
Configuration des APIs externes - Phase 2 - Semantic Pulse X
Setup progressif des 3 APIs externes manquantes
"""

import os
import logging
import json
from pathlib import Path
from datetime import datetime

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ExternalAPISetup:
    """
    Configuration des APIs externes pour la Phase 2
    Approche progressive et sécurisée
    """
    
    def __init__(self):
        """Initialise le setup des APIs"""
        self.config_file = Path("config/external_apis.json")
        self.config_file.parent.mkdir(exist_ok=True)
        self.apis_config = {}
        logger.info("🔧 Setup des APIs externes initialisé")
    
    def setup_newsapi(self) -> bool:
        """Configuration de NewsAPI"""
        logger.info("📰 Configuration NewsAPI")
        
        # Vérification de la clé API
        api_key = os.getenv('NEWSAPI_KEY')
        if not api_key:
            logger.warning("⚠️ NEWSAPI_KEY non définie dans les variables d'environnement")
            logger.info("💡 Pour obtenir une clé gratuite: https://newsapi.org/register")
            api_key = input("Entrez votre clé NewsAPI (ou appuyez sur Entrée pour ignorer): ").strip()
        
        if api_key:
            # Test de la clé API
            try:
                import requests
                url = f"https://newsapi.org/v2/top-headlines?country=fr&apiKey={api_key}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"✅ NewsAPI connecté - {data['totalResults']} articles disponibles")
                    
                    self.apis_config['newsapi'] = {
                        'api_key': api_key,
                        'base_url': 'https://newsapi.org/v2',
                        'status': 'active',
                        'tested_at': datetime.now().isoformat()
                    }
                    return True
                else:
                    logger.error(f"❌ Erreur NewsAPI: {response.status_code}")
                    return False
                    
            except Exception as e:
                logger.error(f"❌ Erreur test NewsAPI: {e}")
                return False
        else:
            logger.info("⏭️ NewsAPI ignoré (pas de clé)")
            self.apis_config['newsapi'] = {'status': 'disabled'}
            return True
    
    def setup_youtube_api(self) -> bool:
        """Configuration YouTube Data API"""
        logger.info("📺 Configuration YouTube Data API")
        
        # Vérification de la clé API
        api_key = os.getenv('YOUTUBE_API_KEY')
        if not api_key:
            logger.warning("⚠️ YOUTUBE_API_KEY non définie dans les variables d'environnement")
            logger.info("💡 Pour obtenir une clé: https://console.developers.google.com/")
            api_key = input("Entrez votre clé YouTube API (ou appuyez sur Entrée pour ignorer): ").strip()
        
        if api_key:
            # Test de la clé API
            try:
                import requests
                url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q=test&key={api_key}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"✅ YouTube API connecté - {len(data['items'])} résultats de test")
                    
                    self.apis_config['youtube'] = {
                        'api_key': api_key,
                        'base_url': 'https://www.googleapis.com/youtube/v3',
                        'status': 'active',
                        'tested_at': datetime.now().isoformat()
                    }
                    return True
                else:
                    logger.error(f"❌ Erreur YouTube API: {response.status_code}")
                    return False
                    
            except Exception as e:
                logger.error(f"❌ Erreur test YouTube API: {e}")
                return False
        else:
            logger.info("⏭️ YouTube API ignoré (pas de clé)")
            self.apis_config['youtube'] = {'status': 'disabled'}
            return True
    
    def setup_instagram_api(self) -> bool:
        """Configuration Instagram Basic Display API"""
        logger.info("📸 Configuration Instagram Basic Display API")
        
        # Vérification des tokens
        access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        if not access_token:
            logger.warning("⚠️ INSTAGRAM_ACCESS_TOKEN non défini")
            logger.info("💡 Pour obtenir un token: https://developers.facebook.com/docs/instagram-basic-display-api/")
            access_token = input("Entrez votre token Instagram (ou appuyez sur Entrée pour ignorer): ").strip()
        
        if access_token:
            # Test du token
            try:
                import requests
                url = f"https://graph.instagram.com/me?fields=id,username&access_token={access_token}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"✅ Instagram API connecté - Utilisateur: {data.get('username', 'N/A')}")
                    
                    self.apis_config['instagram'] = {
                        'access_token': access_token,
                        'base_url': 'https://graph.instagram.com',
                        'status': 'active',
                        'tested_at': datetime.now().isoformat()
                    }
                    return True
                else:
                    logger.error(f"❌ Erreur Instagram API: {response.status_code}")
                    return False
                    
            except Exception as e:
                logger.error(f"❌ Erreur test Instagram API: {e}")
                return False
        else:
            logger.info("⏭️ Instagram API ignoré (pas de token)")
            self.apis_config['instagram'] = {'status': 'disabled'}
            return True
    
    def setup_web_scraping(self) -> bool:
        """Configuration du web scraping"""
        logger.info("🕷️ Configuration Web Scraping")
        
        # Vérification des dépendances
        try:
            import requests
            import beautifulsoup4
            logger.info("✅ Dépendances web scraping installées")
            
            # Test de connexion
            test_url = "https://httpbin.org/get"
            response = requests.get(test_url, timeout=10)
            
            if response.status_code == 200:
                logger.info("✅ Connexion web scraping testée")
                
                self.apis_config['web_scraping'] = {
                    'user_agent': 'SemanticPulseX/1.0 (Educational Research)',
                    'delay_between_requests': 1.0,
                    'max_retries': 3,
                    'status': 'active',
                    'tested_at': datetime.now().isoformat()
                }
                return True
            else:
                logger.error(f"❌ Erreur test web scraping: {response.status_code}")
                return False
                
        except ImportError as e:
            logger.error(f"❌ Dépendances manquantes: {e}")
            logger.info("💡 Installez avec: pip install requests beautifulsoup4")
            return False
        except Exception as e:
            logger.error(f"❌ Erreur web scraping: {e}")
            return False
    
    def save_config(self) -> bool:
        """Sauvegarde la configuration"""
        try:
            config_data = {
                'created_at': datetime.now().isoformat(),
                'apis': self.apis_config,
                'version': '1.0'
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Configuration sauvegardée: {self.config_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde: {e}")
            return False
    
    def generate_env_template(self) -> bool:
        """Génère un template .env pour les clés API"""
        try:
            env_template = """# Configuration des APIs externes - Semantic Pulse X
# Copiez ce fichier vers .env et remplissez vos clés API

# NewsAPI (https://newsapi.org/register)
NEWSAPI_KEY=your_newsapi_key_here

# YouTube Data API (https://console.developers.google.com/)
YOUTUBE_API_KEY=your_youtube_api_key_here

# Instagram Basic Display API (https://developers.facebook.com/)
INSTAGRAM_ACCESS_TOKEN=your_instagram_token_here

# Configuration web scraping
SCRAPING_DELAY=1.0
SCRAPING_MAX_RETRIES=3
"""
            
            env_file = Path(".env.template")
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(env_template)
            
            logger.info(f"📝 Template .env créé: {env_file}")
            logger.info("💡 Copiez vers .env et remplissez vos clés API")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur création template: {e}")
            return False

def main():
    """Fonction principale de configuration"""
    logger.info("🚀 DÉMARRAGE CONFIGURATION PHASE 2 - APIs EXTERNES")
    logger.info("=" * 70)
    
    # Initialisation
    setup = ExternalAPISetup()
    
    # Configuration des APIs
    apis = [
        ("NewsAPI", setup.setup_newsapi),
        ("YouTube API", setup.setup_youtube_api),
        ("Instagram API", setup.setup_instagram_api),
        ("Web Scraping", setup.setup_web_scraping)
    ]
    
    success_count = 0
    total_apis = len(apis)
    
    for api_name, setup_func in apis:
        logger.info(f"\n🔧 Configuration: {api_name}")
        try:
            if setup_func():
                success_count += 1
                logger.info(f"✅ {api_name} configuré")
            else:
                logger.warning(f"⚠️ {api_name} non configuré")
        except Exception as e:
            logger.error(f"❌ Erreur {api_name}: {e}")
    
    # Sauvegarde de la configuration
    if setup.save_config():
        logger.info("✅ Configuration sauvegardée")
    else:
        logger.error("❌ Erreur sauvegarde configuration")
    
    # Génération du template .env
    if setup.generate_env_template():
        logger.info("✅ Template .env généré")
    
    # Résumé final
    logger.info("\n" + "=" * 70)
    logger.info(f"📊 Configuration terminée: {success_count}/{total_apis} APIs configurées")
    
    if success_count > 0:
        logger.info("🎉 Au moins une API est configurée!")
        logger.info("🚀 Prêt pour la collecte de données")
    else:
        logger.info("⚠️ Aucune API configurée")
        logger.info("💡 Configurez au moins une API pour continuer")
    
    logger.info("=" * 70)
    
    return success_count > 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)




