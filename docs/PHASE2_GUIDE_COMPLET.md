# 🚀 Phase 2 - Guide complet - Semantic Pulse X

## 📋 **Étapes pour démarrer la Phase 2**

### 1. Installation des dépendances
```bash
# Installer les nouvelles dépendances
python scripts/install_phase2_deps.py

# Ou manuellement
pip install python-dotenv requests google-api-python-client beautifulsoup4
```

### 2. Configuration des clés API
```bash
# Copier le template
cp env.template .env

# Éditer le fichier .env avec vos clés
# INSTAGRAM_ACCESS_TOKEN=ton_token_instagram
# YOUTUBE_API_KEY=ta_cle_youtube
```

### 3. Obtenir les clés API

#### 📸 Instagram Basic Display API
1. Allez sur: https://developers.facebook.com/
2. Créez une application Facebook
3. Ajoutez le produit "Instagram Basic Display"
4. Configurez les paramètres OAuth
5. Générez un token d'accès utilisateur

#### 📺 YouTube Data API v3
1. Allez sur: https://console.developers.google.com/
2. Créez un nouveau projet
3. Activez l'API YouTube Data API v3
4. Créez des identifiants (Clé API)
5. Copiez votre clé API

### 4. Test de la collecte
```bash
# Test avec vos clés API
python scripts/collect_secure_external.py
```

## 🔐 **Sécurité et conformité RGPD**

### Anonymisation automatique
- **IDs anonymisés** : `IG_12345678...` au lieu de vrais IDs
- **Contenu limité** : Captions et descriptions tronquées
- **Données publiques uniquement** : Pas de données privées

### Variables d'environnement
- **Fichier .env** : Clés API sécurisées
- **Gitignore** : .env exclu du versioning
- **Template** : env.template pour référence

## 📊 **Données collectées**

### Instagram
- Médias récents (photos/vidéos)
- Captions et descriptions
- Timestamps
- Type de média

### YouTube
- Vidéos recherchées
- Titres et descriptions
- Chaînes
- Dates de publication

## 💾 **Stockage des données**

### Local
- `data/raw/external_apis/` : Fichiers JSON/CSV
- Format anonymisé et sécurisé

### MinIO Data Lake
- Bucket `semantic-pulse-data`
- Dossier `external_apis/`
- Compression automatique

## 🧪 **Tests et validation**

### Test de connexion
```bash
# Test Instagram
python -c "from scripts.collect_secure_external import SecureInstagramCollector; c = SecureInstagramCollector(); print('Instagram OK' if c.test_connection() else 'Instagram KO')"

# Test YouTube
python -c "from scripts.collect_secure_external import SecureYouTubeCollector; c = SecureYouTubeCollector(); print('YouTube OK' if c.test_connection() else 'YouTube KO')"
```

### Test complet Phase 2
```bash
# Test complet (à créer)
python scripts/test_phase2_complete.py
```

## 📈 **Métriques attendues**

### Performance
- **Instagram** : 3-5 médias par collecte
- **YouTube** : 3-5 vidéos par collecte
- **Latence** : < 10s par API
- **Fiabilité** : 95% de succès

### Données
- **Format** : JSON + CSV
- **Anonymisation** : 100% des IDs
- **Compression** : 80%+ avec Parquet
- **Stockage** : Local + MinIO

## 🔧 **Dépannage**

### Erreurs courantes
- **401 Unauthorized** : Vérifiez vos clés API
- **403 Forbidden** : Permissions insuffisantes
- **429 Too Many Requests** : Limite de taux atteinte
- **Timeout** : Problème de connexion

### Solutions
- Vérifiez le fichier `.env`
- Testez vos clés API individuellement
- Augmentez les délais entre requêtes
- Vérifiez la connectivité réseau

## 🎯 **Prochaines étapes**

1. ✅ **Installation** des dépendances
2. 🔑 **Configuration** des clés API
3. 🧪 **Tests** de connexion
4. 📊 **Collecte** des données
5. 💾 **Sauvegarde** sécurisée
6. 🔄 **Intégration** avec Phase 1

---

**Phase 2 prête à démarrer ! 🚀**




