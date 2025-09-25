@echo off
REM Script de démarrage Semantic Pulse X pour Windows

echo 🚀 Démarrage de Semantic Pulse X...

REM Vérifier Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker n'est pas installé
    exit /b 1
)

docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose n'est pas installé
    exit /b 1
)

REM Créer les répertoires nécessaires
if not exist "data\raw" mkdir data\raw
if not exist "data\processed" mkdir data\processed
if not exist "data\models" mkdir data\models
if not exist "monitoring\grafana\dashboards" mkdir monitoring\grafana\dashboards
if not exist "monitoring\grafana\datasources" mkdir monitoring\grafana\datasources

REM Copier le fichier d'environnement
if not exist ".env" (
    copy env.example .env
    echo ✅ Fichier .env créé depuis env.example
)

REM Démarrer les services
echo 🐳 Démarrage des services Docker...
docker-compose up -d

REM Attendre que les services soient prêts
echo ⏳ Attente du démarrage des services...
timeout /t 30 /nobreak >nul

REM Vérifier l'état des services
echo 🔍 Vérification de l'état des services...
docker-compose ps

REM Afficher les URLs
echo.
echo ✅ Semantic Pulse X est démarré !
echo.
echo 🌐 URLs d'accès :
echo    - API: http://localhost:8000
echo    - Streamlit: http://localhost:8501
echo    - Grafana: http://localhost:3000 (admin/admin)
echo    - Prometheus: http://localhost:9090
echo    - MinIO: http://localhost:9001 (admin/admin123)
echo.
echo 📚 Documentation:
echo    - API Docs: http://localhost:8000/docs
echo    - README: ./README.md
echo.
echo 🛠️ Commandes utiles:
echo    - Voir les logs: docker-compose logs -f
echo    - Arrêter: docker-compose down
echo    - Redémarrer: docker-compose restart
echo.
