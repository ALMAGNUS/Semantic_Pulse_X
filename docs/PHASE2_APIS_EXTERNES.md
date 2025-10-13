# 🌐 Phase 2 - APIs externes - Semantic Pulse X

## 🎯 Objectif de la Phase 2

Intégrer les **3 APIs externes** manquantes pour compléter les **5 sources de données** obligatoires :

1. ✅ **Flat files** (CSV/JSON/Parquet) - Terminé Phase 1
2. ✅ **Relational database** (PostgreSQL) - Terminé Phase 1  
3. ✅ **Big Data** (Parquet/Data Lake) - Terminé Phase 1
4. 🔄 **Web scraping** (HTML) - À implémenter
5. 🔄 **REST API** (JSON/XML) - À implémenter

## 📋 Plan d'action Phase 2

### Étape 2.1 : Configuration des APIs externes
- **NewsAPI** : Articles de presse en temps réel
- **YouTube API** : Commentaires et métadonnées vidéos
- **Instagram Basic Display API** : Posts et commentaires publics

### Étape 2.2 : Web Scraping intelligent
- **Articles de presse** : Le Monde, Le Figaro, etc.
- **Forums publics** : Reddit, forums spécialisés
- **Blogs** : Articles d'opinion et analyses

### Étape 2.3 : Intégration et tests
- **Pipeline ETL** complet avec les 5 sources
- **Tests de performance** et de fiabilité
- **Validation RGPD** de toutes les sources

## 🔧 Technologies utilisées

### APIs externes
- **NewsAPI** : `newsapi-python` - Articles de presse
- **YouTube Data API** : `google-api-python-client` - Vidéos et commentaires
- **Instagram Basic Display** : `requests` - Posts publics

### Web Scraping
- **BeautifulSoup4** : Parsing HTML
- **Selenium** : JavaScript et contenu dynamique
- **Scrapy** : Scraping à grande échelle

### Gestion des données
- **Pandas** : Manipulation des données
- **Polars** : Performance optimisée
- **MinIO** : Stockage Data Lake

## 📊 Architecture Phase 2

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   APIs externes │    │   Web Scraping  │    │   Data Lake     │
│                 │    │                 │    │                 │
│ • NewsAPI       │───▶│ • Articles      │───▶│ • MinIO         │
│ • YouTube       │    │ • Forums        │    │ • PostgreSQL    │
│ • Instagram     │    │ • Blogs         │    │ • Parquet       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   ETL Pipeline  │
                    │                 │
                    │ • Anonymisation  │
                    │ • Nettoyage      │
                    │ • Agrégation     │
                    └─────────────────┘
```

## 🔐 Conformité RGPD

### Anonymisation obligatoire
- **Pseudonymisation** : Hachage SHA-256 des identifiants
- **Filtrage PII** : Suppression des données personnelles
- **Consentement** : Seules les données publiques collectées

### Sources autorisées
- **Articles de presse** : Contenu éditorial public
- **Commentaires publics** : YouTube, forums ouverts
- **Posts Instagram** : Comptes publics uniquement

## 📈 Métriques de performance attendues

### Collecte de données
- **NewsAPI** : 100 articles/jour
- **YouTube** : 50 vidéos/jour + commentaires
- **Instagram** : 30 posts/jour
- **Web scraping** : 200 articles/jour

### Performance
- **Latence** : < 5s par source
- **Fiabilité** : 99% de disponibilité
- **Stockage** : Compression 80%+ avec Parquet

## 🚀 Scripts de la Phase 2

### Configuration
- `scripts/setup_external_apis.py` - Configuration des clés API
- `scripts/test_api_connections.py` - Test des connexions

### Collecte
- `scripts/collect_newsapi.py` - Articles de presse
- `scripts/collect_youtube.py` - Vidéos et commentaires
- `scripts/collect_instagram.py` - Posts Instagram
- `scripts/scrape_articles.py` - Web scraping

### Tests
- `scripts/test_phase2_complete.py` - Tests complets Phase 2
- `scripts/validate_rgpd_compliance.py` - Validation RGPD

## 📋 Checklist Phase 2

### Configuration
- [ ] Obtenir les clés API (NewsAPI, YouTube, Instagram)
- [ ] Configurer les proxies pour web scraping
- [ ] Tester les connexions API

### Collecte
- [ ] Implémenter NewsAPI
- [ ] Implémenter YouTube API
- [ ] Implémenter Instagram API
- [ ] Implémenter web scraping

### Intégration
- [ ] Pipeline ETL avec les 5 sources
- [ ] Tests de performance
- [ ] Validation RGPD
- [ ] Documentation complète

## 🎯 Prochaines étapes

1. **Configuration des APIs** - Obtenir les clés et tester les connexions
2. **Implémentation progressive** - Une source à la fois
3. **Tests et validation** - Performance et conformité RGPD
4. **Documentation** - Guides d'utilisation et maintenance

---

**Phase 2 prête à démarrer ! 🚀**
