# 📋 Guide d'Installation - Semantic Pulse X

## 🎯 Prérequis

### Système
- **Python** : 3.9+ (recommandé 3.11+)
- **RAM** : 8GB minimum (16GB recommandé pour l'IA)
- **Espace disque** : 5GB pour les modèles IA
- **OS** : Windows 10+, macOS 10.15+, Ubuntu 20.04+

### Outils
- **Git** : Pour cloner le repository
- **Docker** : Optionnel, pour le déploiement conteneurisé
- **VS Code** : Recommandé pour le développement

## 🚀 Installation Locale

### 1. Cloner le projet
```bash
git clone <repository-url>
cd Semantic_Pulse_X
```

### 2. Créer l'environnement virtuel
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances
```bash
# Installation complète
pip install -r requirements.txt

# Vérification
pip list | grep -E "(fastapi|streamlit|transformers|langchain)"
```

### 4. Configuration
```bash
# Créer le fichier de configuration
cp .env.example .env

# Éditer les paramètres si nécessaire
# Les valeurs par défaut fonctionnent pour la démo
```

## 🐳 Installation Docker

### 1. Prérequis Docker
```bash
# Vérifier Docker
docker --version
docker-compose --version
```

### 2. Démarrage des services
```bash
# Démarrer tous les services
docker-compose up -d

# Vérifier le statut
docker-compose ps

# Voir les logs
docker-compose logs -f
```

### 3. Services disponibles
- **Streamlit** : http://localhost:8501
- **FastAPI** : http://localhost:8000
- **PostgreSQL** : localhost:5432
- **MinIO** : http://localhost:9000
- **Grafana** : http://localhost:3000

## 🧪 Tests et Validation

### 1. Test de l'installation
```bash
# Test des imports
python -c "from app.backend.main import app; print('✅ FastAPI OK')"
python -c "from app.frontend.streamlit_app import main; print('✅ Streamlit OK')"
```

### 2. Test des modèles IA
```bash
# Test des modèles
python scripts/test_wordcloud.py
```

### 3. Test complet
```bash
# Audit du projet
python scripts/audit_projet.py

# Génération de démonstration
python scripts/generate_wordcloud_demo.py
```

## 🔧 Résolution de problèmes

### Erreurs courantes

#### ModuleNotFoundError
```bash
# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall

# Vérifier le PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### Erreurs de mémoire (IA)
```bash
# Réduire la taille des modèles
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

# Utiliser CPU uniquement
export CUDA_VISIBLE_DEVICES=""
```

#### Erreurs de port
```bash
# Vérifier les ports utilisés
netstat -an | findstr :8501
netstat -an | findstr :8000

# Arrêter les processus
taskkill /f /im streamlit.exe
taskkill /f /im python.exe
```

### Logs et débogage
```bash
# Logs détaillés
python -m uvicorn app.backend.main:app --reload --log-level debug

# Mode verbose
streamlit run app/frontend/streamlit_simple.py --logger.level debug
```

## 📊 Vérification de l'installation

### Checklist
- [ ] Python 3.9+ installé
- [ ] Environnement virtuel activé
- [ ] Toutes les dépendances installées
- [ ] Base de données initialisée
- [ ] Modèles IA téléchargés
- [ ] Services démarrés
- [ ] Interface accessible

### Tests de fonctionnement
```bash
# 1. Test API
curl http://localhost:8000/health

# 2. Test Streamlit
# Ouvrir http://localhost:8501

# 3. Test des nuages de mots
python scripts/generate_wordcloud_demo.py

# 4. Test data engineering
python scripts/visualiser_resultats.py
```

## 🎯 Démonstration rapide

### 1. Lancer l'application
```bash
python launch_streamlit.py
```

### 2. Ouvrir l'interface
- **Streamlit** : http://localhost:8501
- **API** : http://localhost:8000/docs

### 3. Générer un nuage de mots
- Sélectionner une émotion
- Cliquer sur "Générer le nuage de mots"
- Voir les résultats

### 4. Voir les données traitées
- Cliquer sur "Voir les résultats de traitement"
- Explorer les données anonymisées

## 📚 Documentation complète

- **Architecture** : `docs/ARCHITECTURE.md`
- **RGPD** : `docs/RGPD.md`
- **Merise** : `docs/MERISE_MODELING.md`
- **API** : http://localhost:8000/docs
- **Résultats** : `docs/DEMO_FINAL_RESULTS.md`

## 🆘 Support

En cas de problème :
1. Vérifier les logs
2. Consulter la documentation
3. Tester avec les scripts de démonstration
4. Vérifier les prérequis système
