#!/usr/bin/env python3
"""
Guide d'obtention des clés API - Instagram et YouTube
Instructions détaillées pour obtenir les clés API
"""

import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def show_instagram_guide():
    """Guide pour obtenir le token Instagram"""
    logger.info("📸 GUIDE INSTAGRAM BASIC DISPLAY API")
    logger.info("=" * 50)
    logger.info("1. 🌐 Allez sur: https://developers.facebook.com/")
    logger.info("2. 🔑 Créez une application Facebook")
    logger.info("3. 📱 Ajoutez le produit 'Instagram Basic Display'")
    logger.info("4. ⚙️ Configurez les paramètres:")
    logger.info("   - Valid OAuth Redirect URIs: http://localhost:8080")
    logger.info("   - Deauthorize Callback URL: http://localhost:8080")
    logger.info("5. 🔐 Obtenez votre App ID et App Secret")
    logger.info("6. 🚀 Générez un token d'accès utilisateur")
    logger.info("")
    logger.info("💡 Token requis: Access Token utilisateur")
    logger.info("📋 Format: IGQVJ... (long token commençant par IGQVJ)")

def show_youtube_guide():
    """Guide pour obtenir la clé YouTube API"""
    logger.info("📺 GUIDE YOUTUBE DATA API")
    logger.info("=" * 50)
    logger.info("1. 🌐 Allez sur: https://console.developers.google.com/")
    logger.info("2. 🔑 Créez un nouveau projet ou sélectionnez un existant")
    logger.info("3. 📚 Activez l'API YouTube Data API v3")
    logger.info("4. 🔐 Créez des identifiants (Clé API)")
    logger.info("5. ⚙️ Configurez les restrictions:")
    logger.info("   - Restrictions d'application: Aucune")
    logger.info("   - Restrictions d'API: YouTube Data API v3")
    logger.info("6. 📋 Copiez votre clé API")
    logger.info("")
    logger.info("💡 Clé requise: API Key")
    logger.info("📋 Format: AIza... (clé commençant par AIza)")

def show_usage_example():
    """Exemple d'utilisation"""
    logger.info("🚀 EXEMPLE D'UTILISATION")
    logger.info("=" * 50)
    logger.info("1. Obtenez vos clés API (voir guides ci-dessus)")
    logger.info("2. Lancez le script de collecte:")
    logger.info("   python scripts/collect_instagram_youtube.py")
    logger.info("3. Entrez vos clés quand demandé")
    logger.info("4. Les données seront collectées et sauvegardées")
    logger.info("")
    logger.info("📁 Données sauvegardées dans:")
    logger.info("   - data/raw/external_apis/ (local)")
    logger.info("   - MinIO Data Lake (cloud)")

def main():
    """Fonction principale"""
    logger.info("🔑 GUIDE D'OBTENTION DES CLÉS API")
    logger.info("=" * 60)
    
    show_instagram_guide()
    print()
    show_youtube_guide()
    print()
    show_usage_example()
    
    logger.info("=" * 60)
    logger.info("✅ Guide terminé! Obtenez vos clés et lancez la collecte.")

if __name__ == "__main__":
    main()




