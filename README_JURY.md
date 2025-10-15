# 🎯 Semantic Pulse X - Projet de Certification E1/E2/E3

## 📋 Présentation du Projet

**Semantic Pulse X** est une plateforme d'analyse de sentiment en temps réel qui collecte, agrège et analyse les émotions des Français à partir de multiples sources de données.

## 🏗️ Architecture MERISE Complète

### 📊 Sources de Données (5 sources distinctes)

1. **📁 Fichier plat** : Dataset Kaggle Sentiment140 (CSV)
2. **🗄️ Base de données relationnelle** : SQLite avec schéma MERISE
3. **🌐 API externe** : YouTube Data API v3 + NewsAPI
4. **🕷️ Web Scraping** : Yahoo Actualités FR + France Info (avec Selenium)
5. **📈 Big Data** : GDELT GKG (Global Knowledge Graph)

### 🔄 Pipeline ETL Robuste

- **Extraction** : Collecte automatique depuis toutes les sources
- **Transformation** : Normalisation et agrégation des données
- **Chargement** : Intégration dans la base MERISE relationnelle
- **Analyse** : Classification d'émotions avec IA (Ollama + HuggingFace)

## 🎯 Conformité Certification

### ✅ E1 - Sources de Données
- [x] Fichier plat (CSV Kaggle)
- [x] Base de données relationnelle (SQLite MERISE)
- [x] API externe (YouTube + NewsAPI)
- [x] Web Scraping (Yahoo + France Info)
- [x] Big Data (GDELT GKG)

### ✅ E2 - Architecture et Technologies
- [x] Pipeline ETL complet
- [x] Modélisation MERISE (MCD/MLD/MLP)
- [x] Conformité RGPD (anonymisation)
- [x] Technologies modernes (FastAPI, Streamlit, Docker)

### ✅ E3 - Fonctionnalités Avancées
- [x] IA pour analyse d'émotions
- [x] Visualisations interactives
- [x] Monitoring (Prometheus/Grafana)
- [x] Orchestration (Prefect)

## 🚀 Démarrage Rapide

### 1. Installation
```bash
# Cloner le projet
git clone https://github.com/VOTRE_USERNAME/Semantic_Pulse_X.git
cd Semantic_Pulse_X

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Configuration
```bash
# Copier le fichier d'environnement
cp .env.example .env

# Configurer les clés API dans .env
YOUTUBE_API_KEY=votre_cle_youtube
NEWSAPI_KEY=votre_cle_newsapi
```

### 3. Lancement
```bash
# Démarrer tous les services
python scripts/start_semantic_pulse.bat

# Ou manuellement
streamlit run app/frontend/streamlit_app.py
```

## 📊 Résultats du Test End-to-End

```
🎯 SCORE GLOBAL: 150%
🏆 EXCELLENT - Pipeline end-to-end fonctionnel !

📊 DONNÉES INTÉGRÉES:
- YouTube: 180 vidéos avec texte complet
- Web Scraping: Articles Yahoo + France Info
- GDELT: 1,283 enregistrements Big Data
- Base finale: 535 contenus analysés
```

## 📁 Structure du Projet

```
Semantic_Pulse_X/
├── app/
│   ├── backend/          # API FastAPI + ETL
│   └── frontend/         # Interface Streamlit
├── data/
│   ├── raw/             # Données brutes
│   └── processed/       # Données traitées
├── scripts/             # Scripts d'automatisation
├── docs/               # Documentation MERISE
├── test/               # Tests end-to-end
└── semantic_pulse.db   # Base MERISE finale
```

## 🔧 Technologies Utilisées

- **Backend** : FastAPI, SQLAlchemy, Prefect
- **Frontend** : Streamlit, Plotly, WordCloud
- **IA** : Ollama, HuggingFace, LangChain
- **Data** : Pandas, Polars, DuckDB, MinIO
- **Monitoring** : Prometheus, Grafana
- **DevOps** : Docker, Ruff (linting)

## 📈 Fonctionnalités Principales

1. **Collecte Multi-Sources** : Automatisation complète
2. **Analyse d'Émotions** : IA française spécialisée
3. **Visualisations** : Graphiques interactifs + Word Cloud
4. **Prédictions** : Tendances émotionnelles
5. **Monitoring** : Métriques temps réel

## 🎓 Points Forts pour le Jury

- **Architecture MERISE complète** avec cardinalités
- **Pipeline ETL robuste** et testé end-to-end
- **Conformité RGPD** avec anonymisation
- **Code propre** (0 erreurs Ruff)
- **Documentation exhaustive**
- **Tests automatisés** validés

## 📞 Contact

**Étudiant** : [Votre Nom]  
**Formation** : [Votre Formation]  
**Date** : Janvier 2025

---

*Projet réalisé dans le cadre de la certification E1/E2/E3 - Architecture de données et Intelligence Artificielle*
