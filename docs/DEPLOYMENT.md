# 🚀 Guide de déploiement - Semantic Pulse X

## Prérequis

### 1. **Système d'exploitation**
- Windows 10/11 (PowerShell)
- macOS 10.15+
- Linux Ubuntu 20.04+

### 2. **Logiciels requis**
- **Docker** 20.10+
- **Docker Compose** 2.0+
- **Git** 2.30+

### 3. **Ressources système**
- **RAM** : 8 GB minimum (16 GB recommandé)
- **CPU** : 4 cœurs minimum
- **Stockage** : 20 GB d'espace libre
- **Réseau** : Connexion internet stable

## 🐳 Installation Docker

### Windows
1. Télécharger Docker Desktop : https://www.docker.com/products/docker-desktop
2. Installer et redémarrer
3. Vérifier l'installation :
```powershell
docker --version
docker-compose --version
```

### macOS
```bash
# Installer via Homebrew
brew install --cask docker

# Ou télécharger depuis le site officiel
# https://www.docker.com/products/docker-desktop
```

### Linux
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose

# CentOS/RHEL
sudo yum install docker docker-compose
```

## 📥 Installation du projet

### 1. **Cloner le repository**
```bash
git clone https://github.com/your-username/semantic-pulse-x.git
cd semantic-pulse-x
```

### 2. **Configuration**
```bash
# Copier le fichier d'environnement
cp env.example .env

# Éditer la configuration si nécessaire
notepad .env  # Windows
nano .env     # Linux/macOS
```

### 3. **Variables d'environnement**
```env
# Configuration de base
DATABASE_URL=postgresql://admin:admin123@postgres:5432/semantic_pulse
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=admin
MINIO_SECRET_KEY=admin123
REDIS_URL=redis://redis:6379

# Clés API (optionnelles)
OPENAI_API_KEY=your_openai_key_here
TWITTER_BEARER_TOKEN=your_twitter_token_here
NEWSAPI_KEY=your_newsapi_key_here
```

## 🚀 Démarrage

### 1. **Démarrage automatique**
```bash
# Windows
scripts\start.bat

# Linux/macOS
./scripts/start.sh
```

### 2. **Démarrage manuel**
```bash
# Créer les répertoires
mkdir -p data/raw data/processed data/models
mkdir -p monitoring/grafana/dashboards monitoring/grafana/datasources

# Démarrer les services
docker-compose up -d

# Vérifier l'état
docker-compose ps
```

### 3. **Vérification**
```bash
# Voir les logs
docker-compose logs -f

# Tester l'API
curl http://localhost:8000/health

# Tester Streamlit
curl http://localhost:8501
```

## 🌐 Accès aux services

### URLs d'accès
- **API** : http://localhost:8000
- **Streamlit** : http://localhost:8501
- **Grafana** : http://localhost:3000
- **Prometheus** : http://localhost:9090
- **MinIO** : http://localhost:9001

### Identifiants par défaut
- **Grafana** : admin / admin
- **MinIO** : admin / admin123

## 🔧 Configuration avancée

### 1. **Base de données**
```yaml
# docker-compose.yml
postgres:
  environment:
    POSTGRES_DB: semantic_pulse
    POSTGRES_USER: admin
    POSTGRES_PASSWORD: admin123
  volumes:
    - postgres_data:/var/lib/postgresql/data
```

### 2. **MinIO (Stockage)**
```yaml
minio:
  environment:
    MINIO_ROOT_USER: admin
    MINIO_ROOT_PASSWORD: admin123
  volumes:
    - minio_data:/data
```

### 3. **Monitoring**
```yaml
prometheus:
  volumes:
    - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml

grafana:
  volumes:
    - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
    - ./monitoring/grafana/datasources:/etc/grafana/provisioning/datasources
```

## 📊 Monitoring et logs

### 1. **Logs des services**
```bash
# Tous les services
docker-compose logs -f

# Service spécifique
docker-compose logs -f app
docker-compose logs -f postgres
docker-compose logs -f grafana
```

### 2. **Métriques Prometheus**
- URL : http://localhost:9090
- Métriques : http://localhost:9090/metrics
- Requêtes : http://localhost:9090/graph

### 3. **Dashboards Grafana**
- URL : http://localhost:3000
- Login : admin / admin
- Dashboards : Semantic Pulse X

## 🔄 Maintenance

### 1. **Mise à jour**
```bash
# Arrêter les services
docker-compose down

# Mettre à jour le code
git pull origin main

# Redémarrer
docker-compose up -d
```

### 2. **Sauvegarde**
```bash
# Sauvegarder la base de données
docker-compose exec postgres pg_dump -U admin semantic_pulse > backup.sql

# Sauvegarder les données
tar -czf data_backup.tar.gz data/
```

### 3. **Nettoyage**
```bash
# Supprimer les conteneurs arrêtés
docker-compose down --remove-orphans

# Nettoyer les images inutilisées
docker system prune -a

# Supprimer les volumes
docker volume prune
```

## 🐛 Dépannage

### 1. **Problèmes courants**

#### Port déjà utilisé
```bash
# Vérifier les ports utilisés
netstat -an | findstr :8000

# Changer le port dans docker-compose.yml
ports:
  - "8001:8000"  # Au lieu de 8000:8000
```

#### Erreur de permissions
```bash
# Linux/macOS
sudo chown -R $USER:$USER data/
sudo chmod -R 755 data/
```

#### Mémoire insuffisante
```bash
# Augmenter la limite Docker
# Docker Desktop > Settings > Resources > Memory
```

### 2. **Logs d'erreur**
```bash
# Logs détaillés
docker-compose logs --tail=100 app

# Logs avec timestamps
docker-compose logs -t app
```

### 3. **Redémarrage des services**
```bash
# Redémarrer un service
docker-compose restart app

# Redémarrer tous les services
docker-compose restart
```

## 🔒 Sécurité

### 1. **Changer les mots de passe**
```env
# .env
POSTGRES_PASSWORD=your_secure_password
MINIO_ROOT_PASSWORD=your_secure_password
```

### 2. **HTTPS en production**
```yaml
# Ajouter un reverse proxy (nginx)
nginx:
  image: nginx:alpine
  ports:
    - "443:443"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf
    - ./ssl:/etc/nginx/ssl
```

### 3. **Firewall**
```bash
# Ouvrir seulement les ports nécessaires
# 8000, 8501, 3000, 9090, 9000, 9001
```

## 📈 Performance

### 1. **Optimisation Docker**
```yaml
# docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
```

### 2. **Monitoring des ressources**
```bash
# Utilisation des ressources
docker stats

# Logs de performance
docker-compose logs app | grep "performance"
```

## 🆘 Support

### 1. **Documentation**
- [Architecture](ARCHITECTURE.md)
- [RGPD](RGPD.md)
- [API](API.md)

### 2. **Issues**
- GitHub Issues : https://github.com/your-username/semantic-pulse-x/issues
- Email : support@semantic-pulse.com

### 3. **Communauté**
- Discord : https://discord.gg/semantic-pulse
- Forum : https://forum.semantic-pulse.com


