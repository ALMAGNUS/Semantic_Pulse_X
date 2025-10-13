#!/usr/bin/env python3
"""
Guide détaillé YouTube Data API v3 - Semantic Pulse X
Instructions pas à pas pour obtenir la clé API YouTube
"""

import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def show_youtube_api_guide():
    """Guide détaillé pour YouTube Data API v3"""
    logger.info("📺 GUIDE DÉTAILLÉ YOUTUBE DATA API v3")
    logger.info("=" * 60)
    
    logger.info("🔑 ÉTAPE 1: Créer un compte Google")
    logger.info("   1. Allez sur: https://accounts.google.com/")
    logger.info("   2. Créez un compte Google si vous n'en avez pas")
    logger.info("   3. Connectez-vous avec votre compte")
    
    logger.info("\n🏗️ ÉTAPE 2: Créer un projet dans Google Developers Console")
    logger.info("   1. Allez sur: https://console.developers.google.com/")
    logger.info("   2. Cliquez sur 'Sélectionner un projet' en haut")
    logger.info("   3. Cliquez sur 'NOUVEAU PROJET'")
    logger.info("   4. Nommez votre projet: 'Semantic Pulse X'")
    logger.info("   5. Cliquez sur 'CRÉER'")
    logger.info("   6. Attendez que le projet soit créé")
    
    logger.info("\n📚 ÉTAPE 3: Activer l'API YouTube Data v3")
    logger.info("   1. Dans votre projet, allez dans 'APIs et services' > 'Bibliothèque'")
    logger.info("   2. Recherchez 'YouTube Data API v3'")
    logger.info("   3. Cliquez sur 'YouTube Data API v3'")
    logger.info("   4. Cliquez sur 'ACTIVER'")
    logger.info("   5. Attendez l'activation")
    
    logger.info("\n🔐 ÉTAPE 4: Créer des identifiants (Clé API)")
    logger.info("   1. Allez dans 'APIs et services' > 'Identifiants'")
    logger.info("   2. Cliquez sur '+ CRÉER DES IDENTIFIANTS'")
    logger.info("   3. Sélectionnez 'Clé API'")
    logger.info("   4. Une clé API sera générée automatiquement")
    logger.info("   5. Copiez cette clé (commence par 'AIza...')")
    
    logger.info("\n⚙️ ÉTAPE 5: Configurer les restrictions (Optionnel mais recommandé)")
    logger.info("   1. Cliquez sur l'icône crayon à côté de votre clé API")
    logger.info("   2. Dans 'Restrictions d'application':")
    logger.info("      - Sélectionnez 'Aucune' pour les tests")
    logger.info("      - Ou 'Adresses IP HTTP' pour la production")
    logger.info("   3. Dans 'Restrictions d'API':")
    logger.info("      - Sélectionnez 'Restreindre la clé'")
    logger.info("      - Cochez 'YouTube Data API v3'")
    logger.info("   4. Cliquez sur 'ENREGISTRER'")
    
    logger.info("\n🧪 ÉTAPE 6: Tester votre clé API")
    logger.info("   1. Ouvrez un terminal")
    logger.info("   2. Testez avec curl:")
    logger.info("      curl 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=test&key=VOTRE_CLE_API'")
    logger.info("   3. Vous devriez voir une réponse JSON")

def show_instagram_api_guide():
    """Guide pour Instagram Basic Display API"""
    logger.info("\n📸 GUIDE INSTAGRAM BASIC DISPLAY API")
    logger.info("=" * 60)
    
    logger.info("🔑 ÉTAPE 1: Créer un compte Facebook Developer")
    logger.info("   1. Allez sur: https://developers.facebook.com/")
    logger.info("   2. Cliquez sur 'Commencer'")
    logger.info("   3. Connectez-vous avec votre compte Facebook")
    logger.info("   4. Acceptez les conditions d'utilisation")
    
    logger.info("\n🏗️ ÉTAPE 2: Créer une application")
    logger.info("   1. Cliquez sur 'Mes applications'")
    logger.info("   2. Cliquez sur 'Créer une application'")
    logger.info("   3. Sélectionnez 'Consommateur'")
    logger.info("   4. Nommez votre app: 'Semantic Pulse X'")
    logger.info("   5. Ajoutez votre email de contact")
    logger.info("   6. Cliquez sur 'Créer une application'")
    
    logger.info("\n📱 ÉTAPE 3: Ajouter Instagram Basic Display")
    logger.info("   1. Dans votre app, cliquez sur 'Ajouter un produit'")
    logger.info("   2. Trouvez 'Instagram Basic Display'")
    logger.info("   3. Cliquez sur 'Configurer'")
    logger.info("   4. Cliquez sur 'Créer un nouvel app'")
    
    logger.info("\n⚙️ ÉTAPE 4: Configurer les paramètres")
    logger.info("   1. Dans 'Instagram Basic Display' > 'Paramètres de base':")
    logger.info("   2. Valid OAuth Redirect URIs: http://localhost:8080")
    logger.info("   3. Deauthorize Callback URL: http://localhost:8080")
    logger.info("   4. Cliquez sur 'Enregistrer les modifications'")
    
    logger.info("\n🔐 ÉTAPE 5: Obtenir le token d'accès")
    logger.info("   1. Allez dans 'Instagram Basic Display' > 'Utilisateurs de test'")
    logger.info("   2. Ajoutez votre compte Instagram")
    logger.info("   3. Générez un token d'accès utilisateur")
    logger.info("   4. Copiez le token (commence par 'IGQVJ...')")

def show_setup_instructions():
    """Instructions de configuration locale"""
    logger.info("\n🔧 CONFIGURATION LOCALE")
    logger.info("=" * 60)
    
    logger.info("📝 ÉTAPE 1: Créer le fichier .env")
    logger.info("   1. Copiez le template:")
    logger.info("      cp env.template .env")
    logger.info("   2. Éditez le fichier .env:")
    logger.info("      INSTAGRAM_ACCESS_TOKEN=IGQVJ...")
    logger.info("      YOUTUBE_API_KEY=AIza...")
    
    logger.info("\n🧪 ÉTAPE 2: Tester la configuration")
    logger.info("   1. Lancez le test de connexion:")
    logger.info("      python scripts/collect_secure_external.py")
    logger.info("   2. Vérifiez les logs pour les erreurs")
    
    logger.info("\n📊 ÉTAPE 3: Collecter les données")
    logger.info("   1. Si les tests passent, lancez la collecte")
    logger.info("   2. Les données seront sauvegardées dans:")
    logger.info("      - data/raw/external_apis/ (local)")
    logger.info("      - MinIO Data Lake (cloud)")

def show_troubleshooting():
    """Guide de dépannage"""
    logger.info("\n🔧 DÉPANNAGE")
    logger.info("=" * 60)
    
    logger.info("❌ Erreur 401 Unauthorized:")
    logger.info("   - Vérifiez que votre clé API est correcte")
    logger.info("   - Vérifiez que l'API est activée")
    
    logger.info("\n❌ Erreur 403 Forbidden:")
    logger.info("   - Vérifiez les restrictions de votre clé API")
    logger.info("   - Assurez-vous que YouTube Data API v3 est autorisé")
    
    logger.info("\n❌ Erreur 429 Too Many Requests:")
    logger.info("   - Vous avez atteint la limite de quota")
    logger.info("   - Attendez avant de refaire des requêtes")
    
    logger.info("\n❌ Token Instagram invalide:")
    logger.info("   - Vérifiez que le token commence par 'IGQVJ'")
    logger.info("   - Régénérez le token si nécessaire")
    
    logger.info("\n❌ Erreur de connexion:")
    logger.info("   - Vérifiez votre connexion internet")
    logger.info("   - Vérifiez que les services sont accessibles")

def main():
    """Fonction principale"""
    logger.info("🚀 GUIDE COMPLET APIs EXTERNES - PHASE 2")
    logger.info("=" * 80)
    
    show_youtube_api_guide()
    show_instagram_api_guide()
    show_setup_instructions()
    show_troubleshooting()
    
    logger.info("\n" + "=" * 80)
    logger.info("✅ Guide terminé!")
    logger.info("💡 Suivez les étapes dans l'ordre pour obtenir vos clés API")
    logger.info("🚀 Une fois configuré, lancez: python scripts/collect_secure_external.py")

if __name__ == "__main__":
    main()




