#!/usr/bin/env python3
"""
Guide NewsAPI - Semantic Pulse X
Instructions pour obtenir une clé NewsAPI gratuite
"""

import logging

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Guide pour obtenir une clé NewsAPI."""
    logger.info("📰 GUIDE NEWSAPI - OBTENIR UNE CLÉ GRATUITE")
    logger.info("=" * 60)
    
    logger.info("🔑 ÉTAPE 1: Créer un compte")
    logger.info("   1. Allez sur: https://newsapi.org/register")
    logger.info("   2. Remplissez le formulaire d'inscription")
    logger.info("   3. Confirmez votre email")
    
    logger.info("\n🔑 ÉTAPE 2: Obtenir votre clé API")
    logger.info("   1. Connectez-vous à votre compte")
    logger.info("   2. Allez dans 'API Keys'")
    logger.info("   3. Copiez votre clé API (commence par '...')")
    
    logger.info("\n🔑 ÉTAPE 3: Configurer localement")
    logger.info("   1. Ouvrez le fichier .env")
    logger.info("   2. Ajoutez: NEWSAPI_KEY=votre_cle_ici")
    logger.info("   3. Sauvegardez le fichier")
    
    logger.info("\n🔑 ÉTAPE 4: Tester")
    logger.info("   1. Lancez: python scripts/collect_newsapi.py")
    logger.info("   2. Vérifiez que la connexion fonctionne")
    
    logger.info("\n" + "=" * 60)
    logger.info("💡 AVANTAGES NEWSAPI:")
    logger.info("   ✅ Gratuit jusqu'à 1000 requêtes/jour")
    logger.info("   ✅ Articles français disponibles")
    logger.info("   ✅ Données récentes (7 derniers jours)")
    logger.info("   ✅ Sources fiables (Le Monde, Le Figaro, etc.)")
    logger.info("=" * 60)
    
    logger.info("\n🚀 Une fois votre clé configurée, vous pourrez:")
    logger.info("   📰 Collecter des articles d'actualité français")
    logger.info("   🔍 Rechercher par mots-clés (politique, économie, etc.)")
    logger.info("   📊 Analyser les tendances médiatiques")
    logger.info("   😊 Classifier les émotions dans les articles")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()




