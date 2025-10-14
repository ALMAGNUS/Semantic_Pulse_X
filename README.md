# 🧠 Semantic Pulse X - Cartographie dynamique des émotions médiatiques

> **L'IA qui prédit les vagues émotionnelles médiatiques avant qu'elles n'arrivent**

## 🎯 Vision

Solution d'intelligence artificielle avancée capable de cartographier en temps réel les émotions et thématiques dominantes dans les médias, avec prédiction proactive des tendances émotionnelles.

## 🏗️ Architecture

### Structure du Projet
```
Semantic_Pulse_X/
├── app/
│   ├── backend/          # Code backend (API, ETL, IA, etc.)
│   │   ├── ai/          # Modules d'intelligence artificielle
│   │   ├── api/         # Endpoints REST FastAPI
│   │   ├── core/        # Configuration et base de données
│   │   ├── data_sources/# Collecte de données
│   │   ├── etl/         # Pipeline de traitement
│   │   ├── models/      # Modèles de données
│   │   └── orchestration/# Prefect et monitoring
│   └── frontend/        # Interface utilisateur
│       ├── streamlit_app.py
│       └── wordcloud_generator.py
├── scripts/             # Scripts utilitaires
├── docs/               # Documentation complète
├── data/               # Données (raw, processed)
├── docker-compose.yml  # Orchestration Docker
└── requirements.txt    # Dépendances Python
```

### Core Stack
- **FastAPI** - API backend optimisée
- **Streamlit** - Interface analystes
- **LangChain** - Moteur IA central
- **Pandas + NumPy** - Traitement données haute performance
- **PostgreSQL + SQLite** - Stockage relationnel + Data Lake
- **MinIO** - Stockage objet Big Data
- **Prometheus + Grafana** - Monitoring IA
- **Ollama** - IA locale gratuite

### Sources de données (RGPD-compliant)
1. **Fichiers plats** - Datasets publics anonymisés (Kaggle, CSV)
2. **Base relationnelle** - PostgreSQL/SQLite avec schéma MERISE complet
3. **Big Data** - Parquet/Data Lake (GDELT 2.0, données volumétriques)
4. **Scraping web** - Yahoo Actualités FR, Franceinfo (Selenium)
5. **API REST** - YouTube Data API v3, NewsAPI

## 🧠 Intelligence Artificielle

- **Embeddings** - Sentence Transformers pour vectorisation
- **Emotion AI** - Hugging Face + analyse lexicale française
- **Clustering** - BERTopic pour regroupement thématique
- **Prédiction** - Prophet/ARIMA/LSTM pour vagues émotionnelles
- **Causalité** - Granger Causality + attention transformers

## 🚀 Démarrage rapide

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

# 4. Configurer les variables d'environnement
cp env.template .env
# Éditer .env avec vos clés API

# 5. Lancer l'application
python scripts/start_semantic_pulse.bat  # Windows
# ou
streamlit run app/frontend/streamlit_app.py --server.port 8501
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
# Web scraping Yahoo Actualités
python scripts/scrape_yahoo.py --discover --pays FR --domaine politique

# Web scraping Franceinfo
python scripts/scrape_franceinfo.py --discover --pays FR --domaine politique

# Agrégation multi-sources avec filtres qualité
python scripts/aggregate_sources.py --inputs data/raw/scraped/*.json \
    --output-dir data/processed --min-text-len 50 --drop-empty-title

# Génération schéma ORM complet
python scripts/generate_orm_schema.py --output-dir app/backend/models

# Prédiction émotionnelle (baseline)
python scripts/predict_emotions.py --inputs data/processed/integrated_all_sources_*.json --output-dir data/processed

# Ingestion Big Data GDELT 2.0
python scripts/ingest_gdelt.py --days 7 --output-dir data/processed/bigdata

# Collecter des données YouTube
python scripts/collect_hugo_youtube.py

# Test complet du pipeline
python scripts/test_components_individual.py
```

## 📊 Monitoring

- **Streamlit** : http://localhost:8501 (Interface principale)
- **API FastAPI** : http://localhost:8000 (Backend API)
- **Documentation API** : http://localhost:8000/docs (Swagger UI)
- **Grafana** : http://localhost:3000 (Monitoring)
- **Prometheus** : http://localhost:9090 (Métriques)
- **Ollama** : http://localhost:11434 (IA locale)

## 🎯 Fonctionnalités démontrées

### ✅ Data Engineering
- **Web scraping réel** : Yahoo Actualités FR, Franceinfo avec Selenium
- **Agrégation multi-sources** : Déduplication par (URL, titre), gestion valeurs manquantes
- **Filtres qualité** : Longueur texte minimale, suppression titres vides
- **Nettoyage de données** : Suppression caractères spéciaux, normalisation
- **Anonymisation RGPD** : Hachage SHA-256, suppression données personnelles
- **Pipeline ETL** : Extraction → Nettoyage → Transformation → Agrégation → Chargement

### ✅ Intelligence Artificielle
- **Classification émotionnelle** : Hugging Face + analyse lexicale française
- **Embeddings sémantiques** : Sentence Transformers
- **Clustering thématique** : BERTopic pour regroupement
- **Génération de contenu** : LangChain + Ollama (IA locale gratuite)
- **Analyse temps réel** : Détection émotions sur événements actuels

### ✅ Visualisation
- **Nuages de mots** : Visualisation des vagues émotionnelles
- **Dashboards interactifs** : Streamlit responsive
- **Graphiques temporels** : Plotly pour tendances
- **Comparaisons d'émotions** : Analyse comparative
- **Métriques en temps réel** : Volumes de données par source

### ✅ Architecture
- **API REST** : FastAPI avec documentation Swagger
- **Interface utilisateur** : Streamlit modulaire
- **Base de données** : SQLite/PostgreSQL avec schéma MERISE
- **Containerisation** : Docker + Docker Compose
- **Monitoring** : Prometheus + Grafana

## 🛡️ Conformité RGPD

- **Anonymisation** : Suppression automatique des PII (emails, téléphones)
- **Pseudonymisation** : Hachage SHA-256 des identifiants
- **Minimisation** : Seules les données nécessaires sont collectées
- **Traçabilité** : Logs complets de toutes les opérations
- **Droits utilisateurs** : Effacement, portabilité, accès

## 📊 Modélisation MERISE

### MCD (Modèle Conceptuel de Données)
- **5 entités principales** : Programme, Diffusion, Utilisateur, Réaction, Source
- **Relations 1:N** entre les entités
- **Attributs RGPD-compliant**

### MLD (Modèle Logique de Données)
- **Tables relationnelles** avec clés primaires/étrangères
- **Logs d'ingestion** pour traçabilité RGPD
- **Contraintes d'intégrité**

### MLP (Modèle Physique de Données)
- **PostgreSQL** : Base principale
- **SQLite** : Développement local
- **Parquet** : Stockage analytique Big Data
- **MinIO** : Data Lake pour fichiers volumineux

## 📚 Documentation Complète

- **📋 Résumé Exécutif** : `docs/RESUME_EXECUTIF.md`
- **🎯 Guide Jury** : `docs/JURY_DEMONSTRATION_GUIDE.md`
- **🔧 Installation** : `docs/INSTALLATION_GUIDE.md`
- **📊 Statut** : `docs/STATUS_APPLICATION.md`
- **🏗️ Architecture** : `docs/ARCHITECTURE.md`
- **🔒 RGPD** : `docs/RGPD.md`
- **🗄️ Merise** : `docs/MERISE_MODELING.md`
- **📊 Schéma MERISE** : `docs/SCHEMA_MERISE_COMPLET.md`
- **🎨 Code Mermaid** : `docs/CODE_MERMAID_MERISE.md`
- **📋 Découpage Artificiel** : `docs/DECOUPAGE_ARTIFICIEL.md`
- **📋 Méthodologie SCRUM** : `docs/SCRUM_METHODOLOGY.md`

## 🎯 Cas d'usage démontrés

### Analyse temps réel
- **Événement** : "Nouveau gouvernement Lecornu 2"
- **Collecte** : Web scraping sites français
- **Analyse** : Détection émotions (déçu, inquiet, sceptique)
- **Confiance** : 90% avec analyse lexicale française
- **Réponse IA** : Synthèse en français des réactions

### Sources de données intégrées
- **YouTube** : 180 vidéos collectées
- **Kaggle** : 10,000 tweets analysés
- **Base de données** : 1,000 enregistrements (schéma MERISE complet)
- **Big Data** : GDELT 2.0 + 16,984 lignes Parquet
- **Web Scraping** : Yahoo Actualités FR + Franceinfo (Selenium)

## 🏆 Statut du projet

**✅ PROJET OPÉRATIONNEL ET CONFORME**

- ✅ **Sources de données** : 5 types implémentés
- ✅ **Pipeline ETL** : Complet et fonctionnel
- ✅ **MERISE** : MCD/MLD/MLP respectés
- ✅ **RGPD** : Anonymisation et traçabilité complètes
- ✅ **IA** : Classification émotionnelle opérationnelle
- ✅ **Interface** : Streamlit avec données réelles
- ✅ **Documentation** : Complète et à jour
- ✅ **Tests** : Pipeline end-to-end validé

**Le projet est prêt pour la présentation au jury !** 🎯✅

## 📞 Support

Pour toute question ou problème :
1. Consulter la documentation dans `docs/`
2. Vérifier les logs dans `data/logs/`
3. Tester les composants avec `scripts/test_components_individual.py`
4. Consulter l'interface Streamlit pour le statut en temps réel