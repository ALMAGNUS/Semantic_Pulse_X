#!/usr/bin/env python3
"""
Guide clés API GRATUITES - Semantic Pulse X
Comment obtenir toutes les clés nécessaires SANS PAYER
"""

import logging

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def guide_youtube_api():
    """Guide pour obtenir la clé YouTube GRATUITE"""
    logger.info("📺 GUIDE YOUTUBE API (GRATUIT)")
    logger.info("=" * 50)
    logger.info("1. 🌐 Allez sur: https://console.developers.google.com/")
    logger.info("2. 📝 Créez un compte Google (gratuit)")
    logger.info("3. 🔧 Créez un nouveau projet")
    logger.info("4. 🔑 Activez l'API YouTube Data v3")
    logger.info("5. 📋 Créez des identifiants (clé API)")
    logger.info("6. 💾 Copiez la clé dans votre .env")
    logger.info("")
    logger.info("✅ GRATUIT jusqu'à 10,000 requêtes/jour")
    logger.info("✅ Aucune carte bancaire requise")
    logger.info("=" * 50)

def guide_newsapi():
    """Guide pour obtenir la clé NewsAPI GRATUITE"""
    logger.info("📰 GUIDE NEWSAPI (GRATUIT)")
    logger.info("=" * 50)
    logger.info("1. 🌐 Allez sur: https://newsapi.org/register")
    logger.info("2. 📝 Inscrivez-vous gratuitement")
    logger.info("3. 📧 Confirmez votre email")
    logger.info("4. 🔑 Récupérez votre clé API")
    logger.info("5. 💾 Copiez la clé dans votre .env")
    logger.info("")
    logger.info("✅ GRATUIT jusqu'à 1000 requêtes/jour")
    logger.info("✅ Aucune carte bancaire requise")
    logger.info("=" * 50)

def guide_ollama():
    """Guide pour installer Ollama GRATUIT"""
    logger.info("🤖 GUIDE OLLAMA (GRATUIT)")
    logger.info("=" * 50)
    logger.info("1. 🌐 Allez sur: https://ollama.ai/")
    logger.info("2. 📥 Téléchargez Ollama pour Windows")
    logger.info("3. 🔧 Installez Ollama")
    logger.info("4. 🚀 Lancez: ollama serve")
    logger.info("5. 📦 Téléchargez un modèle: ollama pull llama2")
    logger.info("")
    logger.info("✅ 100% GRATUIT et local")
    logger.info("✅ Aucune connexion internet requise après installation")
    logger.info("✅ Modèles open-source")
    logger.info("=" * 50)

def guide_alternatives_gratuites():
    """Alternatives GRATUITES aux services payants"""
    logger.info("🆓 ALTERNATIVES GRATUITES")
    logger.info("=" * 50)
    logger.info("❌ OpenAI GPT → ✅ Ollama (local)")
    logger.info("❌ Anthropic Claude → ✅ HuggingFace (gratuit)")
    logger.info("❌ Google Gemini → ✅ DialoGPT (gratuit)")
    logger.info("❌ Azure OpenAI → ✅ Transformers (gratuit)")
    logger.info("")
    logger.info("🎯 STRATÉGIE GRATUITE:")
    logger.info("1. Ollama pour IA conversationnelle")
    logger.info("2. HuggingFace pour modèles spécialisés")
    logger.info("3. YouTube API pour données vidéo")
    logger.info("4. NewsAPI pour actualités")
    logger.info("5. Web scraping pour données publiques")
    logger.info("=" * 50)

def main():
    """Fonction principale"""
    logger.info("🆓 GUIDE CLÉS API GRATUITES - SEMANTIC PULSE X")
    logger.info("=" * 70)
    
    guide_youtube_api()
    guide_newsapi()
    guide_ollama()
    guide_alternatives_gratuites()
    
    logger.info("🎉 RÉSUMÉ:")
    logger.info("✅ Toutes les clés sont GRATUITES")
    logger.info("✅ Aucune carte bancaire requise")
    logger.info("✅ Fonctionnalités complètes maintenues")
    logger.info("✅ Conformité RGPD respectée")
    logger.info("=" * 70)

if __name__ == "__main__":
    main()




