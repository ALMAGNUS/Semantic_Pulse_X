# 🏗️ Architecture Semantic Pulse X

## Vue d'ensemble

Semantic Pulse X est une solution d'intelligence artificielle avancée pour la cartographie dynamique des émotions médiatiques. L'architecture est conçue pour être **modulaire**, **scalable** et **RGPD-compliant**.

## 🎯 Principes architecturaux

### 1. **Économie de code**
- Chaque composant a un rôle précis et réutilisable
- Éviter la duplication de code
- Utilisation de patterns éprouvés

### 2. **RGPD-compliant**
- Anonymisation intégrée dès la collecte
- Aucune donnée personnelle conservée
- Pseudonymisation systématique

### 3. **Scalabilité**
- Architecture microservices
- Traitement par lots optimisé
- Stockage distribué

## 🏛️ Architecture générale

```
┌─────────────────────────────────────────────────────────────┐
│                    Semantic Pulse X                        │
├─────────────────────────────────────────────────────────────┤
│  app/                                                       │
│  ├── frontend/ (Streamlit)  │  backend/ (FastAPI)         │
│  └── Monitoring (Prometheus + Grafana)                     │
├─────────────────────────────────────────────────────────────┤
│  AI Engine (LangChain) │  ETL Pipeline   │  Data Sources   │
├─────────────────────────────────────────────────────────────┤
│  PostgreSQL           │  MinIO/S3       │  Redis          │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Composants principaux

### 1. **Frontend - Streamlit** (`app/frontend/`)
- **Rôle** : Interface utilisateur pour les analystes
- **Technologies** : Streamlit, Plotly, Pandas
- **Fichiers** :
  - `streamlit_app.py` - Application principale
  - `streamlit_ollama_dashboard.py` - Dashboard Ollama
  - `streamlit_wordcloud_dashboard.py` - Dashboard nuages de mots
  - `visualization/` - Modules de visualisation
- **Fonctionnalités** :
  - Dashboard interactif
  - Visualisations en temps réel
  - Exploration des données
  - Assistant IA intégré

### 2. **Backend - FastAPI** (`app/backend/`)
- **Rôle** : API REST et logique métier
- **Technologies** : FastAPI, Pydantic, SQLAlchemy
- **Structure** :
  - `api/` - Endpoints REST
  - `core/` - Configuration et base de données
  - `ai/` - Modules d'intelligence artificielle
  - `etl/` - Pipeline de traitement
  - `models/` - Modèles de données
  - `data_sources/` - Collecte de données
  - `orchestration/` - Prefect et monitoring
- **Endpoints** :
  - `/api/v1/emotions` - Gestion des émotions
  - `/api/v1/predictions` - Prédictions
  - `/api/v1/sources` - Sources de données

### 3. **Moteur IA - LangChain**
- **Rôle** : Intelligence artificielle centrale
- **Technologies** : LangChain, Transformers, BERTopic
- **Modules** :
  - Classification émotionnelle
  - Clustering thématique
  - Génération d'insights
  - Assistant conversationnel

### 4. **Pipeline ETL**
- **Rôle** : Extraction, transformation et chargement
- **Technologies** : Pandas, Polars, DuckDB
- **Sources** :
  - Fichiers plats (CSV/JSON/Parquet)
  - Base de données relationnelle
  - Big Data (Data Lake)
  - Scraping web
  - API REST

### 5. **Stockage de données**
- **PostgreSQL** : Données relationnelles
- **MinIO/S3** : Data Lake pour fichiers volumineux
- **Redis** : Cache et sessions

### 6. **Monitoring**
- **Prometheus** : Collecte de métriques
- **Grafana** : Dashboards et alertes
- **Métriques** :
  - Performance des modèles IA
  - Qualité des données
  - Taux d'anonymisation
  - Temps de réponse API

## 🔄 Flux de données

### 1. **Collecte**
```
Sources → ETL Pipeline → Anonymisation → Stockage
```

### 2. **Traitement**
```
Stockage → IA Engine → Classification → Clustering → Insights
```

### 3. **Visualisation**
```
Insights → API → Frontend → Dashboard
```

## 🛡️ Sécurité et RGPD

### 1. **Anonymisation**
- Suppression des PII dès la collecte
- Hachage irréversible des identifiants
- Agrégation des données sensibles

### 2. **Chiffrement**
- Données en transit : HTTPS/TLS
- Données au repos : Chiffrement des volumes

### 3. **Audit**
- Logs de toutes les opérations
- Traçabilité des données
- Monitoring des accès

## 📊 Modèle de données

### Entités principales
- **Programme** : Émissions TV/médias
- **Diffusion** : Instances de diffusion
- **Réaction** : Réactions émotionnelles anonymisées
- **Utilisateur** : Utilisateurs anonymisés
- **Source** : Sources de données
- **Entité** : Entités extraites (personnes, lieux, concepts)
- **Cooccurrence** : Relations entre entités

### Relations
- Programme → Diffusions (1:N)
- Diffusion → Réactions (1:N)
- Utilisateur → Réactions (1:N)
- Source → Réactions (1:N)
- Entité → Cooccurrences (1:N)

## 🚀 Déploiement

### 1. **Docker Compose**
```bash
docker-compose up -d
```

### 2. **Services**
- **app** : Application principale (FastAPI + Streamlit)
- **postgres** : Base de données
- **minio** : Stockage objet
- **redis** : Cache
- **prometheus** : Métriques
- **grafana** : Monitoring

### 3. **Ports**
- 8000 : API FastAPI
- 8501 : Streamlit
- 3000 : Grafana
- 9090 : Prometheus
- 9000/9001 : MinIO

## 🔧 Configuration

### Variables d'environnement
- `DATABASE_URL` : URL de la base de données
- `MINIO_ENDPOINT` : Endpoint MinIO
- `REDIS_URL` : URL Redis
- `OPENAI_API_KEY` : Clé API OpenAI (optionnel)

### Modèles IA
- `EMBEDDING_MODEL` : Modèle d'embeddings
- `EMOTION_MODEL` : Modèle de classification émotionnelle

## 📈 Monitoring et observabilité

### Métriques clés
- Taux de traitement des émotions
- Qualité des données par source
- Performance des modèles IA
- Temps de réponse API
- Utilisation des ressources

### Alertes
- Taux d'erreur élevé
- Temps de traitement lent
- Faible ingestion de données
- Utilisation mémoire élevée
- Connexion base de données échouée

## 🔮 Évolutions futures

### 1. **Module prédictif**
- Prédiction des vagues émotionnelles
- Détection de signaux faibles
- Alertes proactives

### 2. **Causalité sémantique**
- Analyse des relations causales
- Modèles d'attention
- Granger Causality

### 3. **Graphe social des émotions**
- Visualisation interactive
- Analyse des communautés
- Propagation des émotions

## 📚 Documentation technique

- [API Documentation](API.md)
- [RGPD Compliance](RGPD.md)
- [Deployment Guide](DEPLOYMENT.md)
- [User Guide](USER_GUIDE.md)
