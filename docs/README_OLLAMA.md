# 🤖 Ollama - Modèles IA Locaux pour Semantic Pulse X

## 🎯 Pourquoi Ollama ?

**Ollama** est la solution IA générative **gratuite et la plus efficace** pour Semantic Pulse X :

### ✅ **Avantages clés :**
- **100% gratuit** - Aucun coût d'API
- **RGPD-compliant** - Données restent sur votre serveur
- **Performance excellente** - Optimisé pour la production
- **Modèles français** - Mistral, Llama 2, CodeLlama
- **Facile à intégrer** - API REST simple
- **Ressources contrôlées** - Pas de dépendance externe

## 🚀 Installation rapide

### 1. **Démarrage d'Ollama**
```bash
# Démarrer tous les services (Ollama inclus)
docker-compose up -d

# Vérifier le statut d'Ollama
curl http://localhost:11434/api/tags

# Vérifier tous les services
docker-compose ps
```

### 2. **Configuration automatique**
```bash
# Installer et configurer les modèles
python scripts/setup_ollama.py

# Ou en mode Docker (si Ollama est dans un conteneur)
docker-compose exec app python scripts/setup_ollama.py
```

### 3. **Test de l'installation**
```bash
# Test rapide
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "mistral:7b", "prompt": "Bonjour!"}'
```

## 📊 Modèles recommandés

| Modèle | Taille | Usage | Performance |
|--------|--------|-------|-------------|
| **mistral:7b** | 7B | Modèle principal | ⭐⭐⭐⭐⭐ |
| **llama2:7b** | 7B | Modèle alternatif | ⭐⭐⭐⭐ |
| **codellama:7b** | 7B | Génération de code | ⭐⭐⭐⭐ |
| **phi3:3.8b** | 3.8B | Modèle léger | ⭐⭐⭐ |

## 🎛️ Interface de gestion

### **Dashboard Streamlit**
- **URL** : http://localhost:8501 (onglet "🤖 Ollama IA")
- **Fonctionnalités** :
  - Gestion des modèles
  - Tests en temps réel
  - Chat interactif
  - Configuration avancée

### **API REST**
```python
from app.ai.ollama_client import ollama_client

# Génération de texte
response = ollama_client.generate_text(
    prompt="Analysez les tendances émotionnelles",
    model="mistral:7b",
    temperature=0.7
)

# Analyse des émotions
insights = ollama_client.analyze_emotion_trends(emotion_data)
```

## 🔧 Configuration avancée

### **Variables d'environnement**
```env
# Ollama
OLLAMA_HOST=localhost
OLLAMA_PORT=11434
OLLAMA_MODEL=mistral:7b
```

### **Configuration GPU (optionnel)**
```yaml
# docker-compose.ollama.yml
services:
  ollama:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

## 📈 Utilisation dans Semantic Pulse X

### **1. Analyse émotionnelle**
```python
# Analyse des tendances
trends = ollama_client.analyze_emotion_trends(emotion_data)

# Génération d'insights
insights = ollama_client.generate_insights(data)
```

### **2. Détection d'anomalies**
```python
# Détection automatique
anomalies = ollama_client.detect_anomalies(data)

# Génération d'alertes
alert = ollama_client.generate_alert(anomaly)
```

### **3. Chat interactif**
```python
# Réponses contextuelles
answer = ollama_client.answer_question(question, context)
```

## 🛠️ Dépannage

### **Problèmes courants**

#### Ollama ne démarre pas
```bash
# Vérifier les logs
docker-compose logs ollama

# Redémarrer Ollama
docker-compose restart ollama

# Redémarrer tous les services
docker-compose restart
```

#### Modèles non disponibles
```bash
# Lister les modèles
curl http://localhost:11434/api/tags

# Télécharger un modèle
curl -X POST http://localhost:11434/api/pull \
  -H "Content-Type: application/json" \
  -d '{"name": "mistral:7b"}'
```

#### Performance lente
```bash
# Vérifier les ressources
docker stats semantic-pulse-ollama

# Optimiser la mémoire
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_MAX_LOADED_MODELS=1
```

## 📊 Monitoring

### **Métriques disponibles**
- **Temps de réponse** - Latence des requêtes
- **Utilisation mémoire** - Consommation RAM
- **Modèles actifs** - Nombre de modèles chargés
- **Requêtes par minute** - Volume de trafic

### **Logs**
```bash
# Logs Ollama
docker logs semantic-pulse-ollama

# Logs de l'application
tail -f logs/semantic_pulse.log
```

## 🔄 Mise à jour

### **Mise à jour d'Ollama**
```bash
# Mettre à jour l'image
docker-compose pull ollama

# Redémarrer Ollama
docker-compose up -d ollama

# Ou redémarrer tous les services
docker-compose up -d
```

### **Mise à jour des modèles**
```bash
# Mettre à jour un modèle
curl -X POST http://localhost:11434/api/pull \
  -H "Content-Type: application/json" \
  -d '{"name": "mistral:7b", "stream": false}'
```

## 🆘 Support

### **Documentation**
- [Ollama GitHub](https://github.com/ollama/ollama)
- [Modèles disponibles](https://ollama.ai/library)
- [API Reference](https://github.com/ollama/ollama/blob/main/docs/api.md)

### **Communauté**
- [Discord Ollama](https://discord.gg/ollama)
- [GitHub Issues](https://github.com/ollama/ollama/issues)

### **Semantic Pulse X**
- **Issues** : https://github.com/your-username/semantic-pulse-x/issues
- **Email** : support@semantic-pulse.com

## 🎯 Prochaines étapes

1. **Installer tous les services** avec `docker-compose up -d`
2. **Configurer les modèles** avec `python scripts/setup_ollama.py`
3. **Tester l'interface** sur http://localhost:8501
4. **Intégrer dans vos workflows** Semantic Pulse X

**Ollama est maintenant intégré dans Semantic Pulse X !** 🚀
