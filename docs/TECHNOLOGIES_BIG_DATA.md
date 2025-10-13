# 🚀 Technologies Big Data - Semantic Pulse X

## 📊 **Parquet - Format de stockage optimisé**

### Qu'est-ce que Parquet ?
Parquet est un format de fichier colonnaire open-source optimisé pour l'analytique de données volumineuses.

### Avantages clés :
- **Compression** : 80-90% de réduction de taille
- **Performance** : Lecture 10x plus rapide que CSV
- **Compatibilité** : Supporté par tous les outils Big Data
- **Types complexes** : Dates, décimaux, structures imbriquées

### Exemple concret dans notre projet :
```python
# Conversion CSV vers Parquet
CSV: 1.09 MB (10,000 tweets)
Parquet: 0.16 MB (85% de compression)
```

### Utilisation avec Pandas :
```python
import pandas as pd

# Lecture optimisée
df = pd.read_parquet('data/tweets.parquet')

# Écriture avec compression
df.to_parquet('output.parquet', compression='snappy')
```

---

## 🗄️ **MinIO - Data Lake S3-compatible**

### Qu'est-ce que MinIO ?
MinIO est un serveur de stockage objet haute performance, compatible avec l'API Amazon S3.

### Architecture dans Semantic Pulse X :
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Sources       │    │   MinIO         │    │   Analytics     │
│   (CSV/JSON)    │───▶│   Data Lake     │───▶│   (Polars/Duck) │
│                 │    │   (Parquet)     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Organisation des buckets :
- **`semantic-pulse-raw/`** : Données brutes des 5 sources
- **`semantic-pulse-processed/`** : Données nettoyées et anonymisées
- **`semantic-pulse-analytics/`** : Agrégations et métriques

### Configuration Docker :
```yaml
minio:
  image: minio/minio:latest
  command: server /data --console-address ":9001"
  environment:
    MINIO_ROOT_USER: admin
    MINIO_ROOT_PASSWORD: admin123
  ports:
    - "9000:9000"  # API S3
    - "9001:9001"  # Interface web
```

### Utilisation Python :
```python
from minio import Minio

# Connexion
client = Minio('localhost:9000', 'admin', 'admin123', secure=False)

# Upload
client.fput_object('semantic-pulse-data', 'tweets.parquet', 'local_file.parquet')

# Download
client.fget_object('semantic-pulse-data', 'tweets.parquet', 'local_file.parquet')
```

---

## 🔄 **Pipeline Big Data complet**

### 1. Collecte (5 sources)
- **Flat files** : CSV → Parquet
- **Database** : PostgreSQL → Parquet
- **Big Data** : Twitter dumps → Parquet
- **Web scraping** : HTML → JSON → Parquet
- **REST API** : JSON → Parquet

### 2. Stockage MinIO
```python
# Upload automatique
def upload_to_datalake(file_path: str, bucket: str):
    client.fput_object(bucket, os.path.basename(file_path), file_path)
```

### 3. Analytics avec Polars/DuckDB
```python
import polars as pl

# Lecture optimisée depuis MinIO
df = pl.read_parquet('s3://semantic-pulse-data/tweets.parquet')

# Requêtes SQL sur Big Data
result = pl.sql("""
    SELECT emotion, COUNT(*) as count
    FROM df
    WHERE date >= '2024-01-01'
    GROUP BY emotion
""")
```

---

## 📈 **Métriques de performance**

### Compression des données :
| Format | Taille | Compression |
|--------|--------|-------------|
| CSV    | 1.09 MB | - |
| Parquet| 0.16 MB | 85% |

### Vitesse de lecture :
| Format | Temps de lecture |
|--------|------------------|
| CSV    | 2.3s |
| Parquet| 0.2s |

### Économie d'espace totale :
- **Avant** : 5 sources × 1MB = 5MB
- **Après** : 5 sources × 0.15MB = 0.75MB
- **Économie** : 85% d'espace disque

---

## 🛠️ **Outils de développement**

### Scripts disponibles :
- `scripts/convert_csv_to_parquet.py` : Conversion automatique
- `scripts/upload_to_minio.py` : Upload vers Data Lake
- `scripts/test_bigdata_pipeline.py` : Tests de performance

### Monitoring :
- **MinIO Console** : http://localhost:9001
- **Métriques Prometheus** : Stockage, bande passante
- **Logs détaillés** : Upload/download, erreurs

---

## 🎯 **Prochaines étapes**

1. ✅ **Conversion CSV → Parquet** (Terminé)
2. 🔄 **Upload vers MinIO** (En cours)
3. ⏳ **Intégration Polars/DuckDB**
4. ⏳ **Analytics temps réel**
5. ⏳ **Monitoring avancé**
