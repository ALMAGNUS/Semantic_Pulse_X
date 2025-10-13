#!/usr/bin/env python3
"""
Installation des dépendances Phase 2 - Semantic Pulse X
Installation progressive des packages pour APIs externes
"""

import subprocess
import logging
import sys

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def install_package(package_name, description=""):
    """Installe un package avec gestion d'erreur"""
    try:
        logger.info(f"📦 Installation: {package_name} {description}")
        result = subprocess.run([sys.executable, "-m", "pip", "install", package_name], 
                              capture_output=True, text=True, check=True)
        logger.info(f"✅ {package_name} installé avec succès")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Erreur installation {package_name}: {e}")
        return False

def main():
    """Installation des dépendances Phase 2"""
    logger.info("🚀 INSTALLATION DÉPENDANCES PHASE 2 - APIs EXTERNES")
    logger.info("=" * 60)
    
    # Dépendances Phase 2
    packages = [
        ("python-dotenv", "Gestion variables d'environnement"),
        ("requests", "Requêtes HTTP"),
        ("beautifulsoup4", "Parsing HTML"),
        ("google-api-python-client", "YouTube Data API"),
        ("google-auth", "Authentification Google"),
        ("google-auth-oauthlib", "OAuth Google"),
        ("google-auth-httplib2", "HTTP lib Google"),
        ("selenium", "Web scraping avancé"),
        ("scrapy", "Framework scraping")
    ]
    
    success_count = 0
    total_packages = len(packages)
    
    for package, description in packages:
        if install_package(package, description):
            success_count += 1
    
    # Résumé
    logger.info("\n" + "=" * 60)
    logger.info(f"📊 Installation terminée: {success_count}/{total_packages} packages")
    
    if success_count == total_packages:
        logger.info("🎉 Toutes les dépendances Phase 2 installées!")
        logger.info("🚀 Prêt pour la collecte Instagram & YouTube")
    else:
        logger.warning("⚠️ Certains packages n'ont pas pu être installés")
        logger.info("💡 Vérifiez les erreurs ci-dessus")
    
    logger.info("=" * 60)
    
    return success_count == total_packages

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)




