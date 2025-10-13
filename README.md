# 🧠 Semantic Pulse X - Cartographie dynamique des émotions médiatiques

> **L'IA qui prédit les vagues émotionnelles médiatiques avant qu'elles n'arrivent**

## 🎯 Vision

Solution d'intelligence artificielle avancée capable de cartographier en temps réel les émotions et thématiques dominantes dans les médias, avec prédiction proactive des tendances émotionnelles.

## 🏗️ Architecture

### Structure du Projet
```
app/
├── backend/          # Code backend (API, ETL, IA, etc.)
│   ├── ai/          # Modules d'intelligence artificielle
│   ├── api/         # Endpoints REST FastAPI
│   ├── core/        # Configuration et base de données
│   ├── data_sources/# Collecte de données
│   ├── etl/         # Pipeline de traitement
│   ├── models/      # Modèles de données
│   └── orchestration/# Prefect et monitoring
└── frontend/        # Interface utilisateur
    ├── streamlit_app.py
    └── visualization/
```

### Core Stack
- **FastAPI** - API backend optimisée
- **Streamlit** - Interface analystes
- **LangChain** - Moteur IA central
- **Polars + DuckDB** - Traitement données haute performance
- **PostgreSQL + MinIO** - Stockage relationnel + Data Lake
- **Prefect** - Orchestration ETL
- **Prometheus + Grafana** - Monitoring IA

### Sources de données (RGPD-compliant)
1. **Fichiers plats** - Datasets publics anonymisés (IMDb, Kaggle)
2. **Base relationnelle** - PostgreSQL/MySQL simulée
3. **Big Data** - Parquet/Data Lake (Twitter publics, Reddit dumps)
4. **Scraping web** - Articles presse, forums publics
5. **API REST** - NewsAPI, Media Cloud, GDELT

## 🧠 Intelligence Artificielle

- **Embeddings** - CamemBERT/FastText pour vectorisation
- **Emotion AI** - GoEmotions, BART-NLI zero-shot
- **Clustering** - BERTopic pour regroupement thématique
- **Prédiction** - Prophet/ARIMA/LSTM pour vagues émotionnelles
- **Causalité** - Granger Causality + attention transformers

## 🚀 Démarrage rapide

### Phase 1 - Big Data (✅ Validée)
```bash
# 1. Démarrer les services Big Data
docker-compose up -d minio postgres

# 2. Convertir les données CSV vers Parquet
python scripts/convert_csv_to_parquet.py

# 3. Upload vers MinIO Data Lake
python scripts/upload_to_minio.py

# 4. Test complet Phase 1
python scripts/test_phase1_complete.py
```

### Phase 2 - APIs externes (🔄 En cours)
```bash
# 1. Configuration des APIs
python scripts/setup_external_apis.py

# 2. Collecte des données
python scripts/collect_external_data.py

# 3. Test Phase 2
python scripts/test_phase2_complete.py
```

### Installation locale
```bash
# 1. Cloner le projet
git clone <repository-url>
cd Semantic_Pulse_X

# 2. Créer l'environnement virtuel
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application
python launch_streamlit.py
```

### Démarrage avec Docker
```bash
# Démarrer tous les services
docker-compose up -d

# Vérifier le statut
docker-compose ps

# Voir les logs
docker-compose logs -f
```

### Démonstration rapide
```bash
# Générer un nuage de mots
python scripts/generate_wordcloud_demo.py

# Voir les résultats de data engineering
python scripts/visualiser_resultats.py

# Test complet Phase 1
python scripts/test_phase1_complete.py
```

## 📊 Monitoring

- **Streamlit** : http://localhost:8501 (Interface principale)
- **API FastAPI** : http://localhost:8000 (Backend API)
- **Documentation API** : http://localhost:8000/docs (Swagger UI)
- **Grafana** : http://localhost:3000 (Monitoring)
- **Prometheus** : http://localhost:9090 (Métriques)
- **Prefect** : http://localhost:4200 (Orchestration)
- **Ollama** : http://localhost:11434 (IA locale)

## 🎯 Fonctionnalités démontrées

### ✅ Data Engineering
- **Nettoyage de données** : Suppression caractères spéciaux, normalisation
- **Dédoublonnage** : Détection et suppression des doublons (25% détectés)
- **Anonymisation RGPD** : Hachage SHA-256, suppression données personnelles
- **Homogénéisation** : Standardisation formats, calcul métriques

### ✅ Intelligence Artificielle
- **Classification émotionnelle** : Hugging Face models (70.7% précision)
- **Embeddings sémantiques** : Sentence Transformers
- **Clustering thématique** : BERTopic pour regroupement
- **Génération de contenu** : LangChain + Ollama

### ✅ Visualisation
- **Nuages de mots** : Visualisation des vagues émotionnelles
- **Dashboards interactifs** : Streamlit responsive
- **Graphiques temporels** : Plotly pour tendances
- **Comparaisons d'émotions** : Analyse comparative

### ✅ Architecture
- **API REST** : FastAPI avec documentation Swagger
- **Interface utilisateur** : Streamlit modulaire
- **Base de données** : SQLite/PostgreSQL avec ORM
- **Containerisation** : Docker + Docker Compose

## 📚 Documentation Complète

- **📋 Résumé Exécutif** : `docs/RESUME_EXECUTIF.md`
- **🎯 Guide Jury** : `docs/JURY_DEMONSTRATION_GUIDE.md`
- **🔧 Installation** : `docs/INSTALLATION_GUIDE.md`
- **📊 Statut** : `docs/STATUS_APPLICATION.md`
- **🏗️ Architecture** : `docs/ARCHITECTURE.md`
- **🔒 RGPD** : `docs/RGPD.md`
- **🗄️ Merise** : `docs/MERISE_MODELING.md`
