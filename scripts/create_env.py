#!/usr/bin/env python3
"""
Générateur de fichier .env - Semantic Pulse X
"""

def create_env_file():
    """Crée le fichier .env avec toutes les variables nécessaires."""
    
    env_content = """# Configuration Semantic Pulse X
# Copiez ce fichier vers .env et remplissez vos clés API

# Base de données
DATABASE_URL=sqlite:///./semantic_pulse.db

# MinIO/S3 Data Lake
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=admin
MINIO_SECRET_KEY=admin123
MINIO_BUCKET=semantic-pulse

# Redis Cache
REDIS_URL=redis://localhost:6379

# APIs externes
# YouTube Data API v3 - Obtenez votre clé sur: https://console.developers.google.com/
YOUTUBE_API_KEY=your_youtube_api_key_here

# NewsAPI - Obtenez votre clé sur: https://newsapi.org/register
NEWSAPI_KEY=your_newsapi_key_here

# Configuration web scraping
SCRAPING_DELAY=1.0
SCRAPING_MAX_RETRIES=3

# Ollama (IA locale)
OLLAMA_HOST=localhost:11434

# Monitoring
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000

# Modèles IA
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMOTION_MODEL=j-hartmann/emotion-english-distilroberta-base

# Traitement des données
BATCH_SIZE=1000
MAX_TEXT_LENGTH=512
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Fichier .env créé avec succès")
        print("📝 N'oubliez pas de remplir vos clés API:")
        print("   - YOUTUBE_API_KEY: https://console.developers.google.com/")
        print("   - NEWSAPI_KEY: https://newsapi.org/register")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la création du fichier .env: {e}")
        return False

if __name__ == "__main__":
    create_env_file()
