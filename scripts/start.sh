#!/bin/bash

# Script de démarrage Semantic Pulse X

echo "🚀 Démarrage de Semantic Pulse X..."

# Vérifier Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé"
    exit 1
fi

# Créer les répertoires nécessaires
mkdir -p data/raw data/processed data/models
mkdir -p monitoring/grafana/dashboards monitoring/grafana/datasources

# Copier le fichier d'environnement
if [ ! -f .env ]; then
    cp env.example .env
    echo "✅ Fichier .env créé depuis env.example"
fi

# Démarrer les services
echo "🐳 Démarrage des services Docker..."
docker-compose up -d

# Attendre que les services soient prêts
echo "⏳ Attente du démarrage des services..."
sleep 30

# Vérifier l'état des services
echo "🔍 Vérification de l'état des services..."
docker-compose ps

# Afficher les URLs
echo ""
echo "✅ Semantic Pulse X est démarré !"
echo ""
echo "🌐 URLs d'accès :"
echo "   - API: http://localhost:8000"
echo "   - Streamlit: http://localhost:8501"
echo "   - Grafana: http://localhost:3000 (admin/admin)"
echo "   - Prometheus: http://localhost:9090"
echo "   - MinIO: http://localhost:9001 (admin/admin123)"
echo ""
echo "📚 Documentation:"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - README: ./README.md"
echo ""
echo "🛠️ Commandes utiles:"
echo "   - Voir les logs: docker-compose logs -f"
echo "   - Arrêter: docker-compose down"
echo "   - Redémarrer: docker-compose restart"
echo ""


