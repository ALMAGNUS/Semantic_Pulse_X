#!/bin/bash

echo "🚀 Démarrage de Semantic Pulse X - Tous les services"
echo "=================================================="

echo ""
echo "📦 Démarrage des conteneurs..."
docker-compose up -d

echo ""
echo "⏳ Attente du démarrage des services..."
sleep 10

echo ""
echo "📊 Vérification du statut des services..."
docker-compose ps

echo ""
echo "🌐 Services disponibles :"
echo "  - Streamlit    : http://localhost:8501"
echo "  - FastAPI      : http://localhost:8000"
echo "  - Grafana      : http://localhost:3000"
echo "  - Prometheus   : http://localhost:9090"
echo "  - Prefect      : http://localhost:4200"
echo "  - Ollama       : http://localhost:11434"

echo ""
echo "✅ Semantic Pulse X est démarré !"
echo ""
echo "💡 Pour voir les logs : docker-compose logs -f"
echo "💡 Pour arrêter : docker-compose down"
echo ""
