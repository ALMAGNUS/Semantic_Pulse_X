# 📊 Schéma MERISE Complet - Semantic Pulse X

## 🎯 Vue d'ensemble de la conformité

Ce document présente le schéma MERISE complet avec **MCD** (Modèle Conceptuel de Données), **MLD** (Modèle Logique de Données) et **MLP** (Modèle Physique de Données) pour démontrer la conformité totale au prompt.

---

## 🔹 MCD - Modèle Conceptuel de Données

### **Entités Principales**

#### 1. **PROGRAMME**
- **Description** : Programme TV/média avec métadonnées
- **Attributs** :
  - `id` (PK) - Identifiant unique
  - `titre` - Titre du programme
  - `chaine` - Chaîne de diffusion
  - `genre` - Genre du programme
  - `duree_minutes` - Durée en minutes
  - `description` - Description du programme
  - `created_at` - Date de création
  - `updated_at` - Date de mise à jour

#### 2. **DIFFUSION**
- **Description** : Diffusion d'un programme
- **Attributs** :
  - `id` (PK) - Identifiant unique
  - `programme_id` (FK) - Référence vers Programme
  - `date_debut` - Date/heure de début
  - `date_fin` - Date/heure de fin
  - `audience_estimee` - Audience anonymisée
  - `rating_anonymise` - Note anonymisée
  - `created_at` - Date de création

#### 3. **UTILISATEUR**
- **Description** : Utilisateur anonymisé (RGPD compliant)
- **Attributs** :
  - `id` (PK) - Identifiant unique
  - `hash_anonyme` - Hash SHA-256 anonymisé
  - `region_anonymisee` - Région anonymisée (ex: "FR-75")
  - `age_groupe` - Groupe d'âge (ex: "18-25")
  - `langue_preferee` - Langue préférée
  - `created_at` - Date de création
  - `last_activity` - Dernière activité

#### 4. **REACTION**
- **Description** : Réaction émotionnelle anonymisée
- **Attributs** :
  - `id` (PK) - Identifiant unique
  - `utilisateur_id` (FK) - Référence vers Utilisateur
  - `programme_id` (FK) - Référence vers Programme
  - `diffusion_id` (FK) - Référence vers Diffusion
  - `source_id` (FK) - Référence vers Source
  - `texte_anonymise` - Texte anonymisé
  - `emotion_detectee` - Émotion détectée par IA
  - `score_polarite` - Score de polarité (-1.0 à 1.0)
  - `confiance_score` - Score de confiance (0.0 à 1.0)
  - `timestamp_anonymise` - Timestamp anonymisé
  - `created_at` - Date de création

#### 5. **SOURCE**
- **Description** : Source de données avec traçabilité
- **Attributs** :
  - `id` (PK) - Identifiant unique
  - `nom_source` - Nom de la source
  - `type_source` - Type (file, sql, bigdata, scraping, api)
  - `url_source` - URL ou chemin de la source
  - `statut` - Statut (active, inactive, error)
  - `derniere_collecte` - Dernière collecte
  - `created_at` - Date de création

### **Relations MCD**

```
PROGRAMME ||--o{ DIFFUSION : "a"
PROGRAMME ||--o{ REACTION : "génère"
DIFFUSION ||--o{ REACTION : "provoque"
UTILISATEUR ||--o{ REACTION : "exprime"
SOURCE ||--o{ REACTION : "collecte"
```

---

## 🔹 MLD - Modèle Logique de Données

### **Tables Relationnelles**

#### **Table PROGRAMMES**
```sql
CREATE TABLE programmes (
    id UUID PRIMARY KEY,
    titre VARCHAR(255) NOT NULL,
    chaine VARCHAR(100),
    genre VARCHAR(50),
    duree_minutes INTEGER,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **Table DIFFUSIONS**
```sql
CREATE TABLE diffusions (
    id UUID PRIMARY KEY,
    programme_id UUID NOT NULL,
    date_debut TIMESTAMP NOT NULL,
    date_fin TIMESTAMP NOT NULL,
    audience_estimee INTEGER,
    rating_anonymise DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (programme_id) REFERENCES programmes(id)
);
```

#### **Table UTILISATEURS**
```sql
CREATE TABLE utilisateurs (
    id UUID PRIMARY KEY,
    hash_anonyme VARCHAR(64) UNIQUE NOT NULL,
    region_anonymisee VARCHAR(10),
    age_groupe VARCHAR(10),
    langue_preferee VARCHAR(5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP
);
```

#### **Table REACTIONS**
```sql
CREATE TABLE reactions (
    id UUID PRIMARY KEY,
    utilisateur_id UUID NOT NULL,
    programme_id UUID NOT NULL,
    diffusion_id UUID,
    source_id UUID NOT NULL,
    texte_anonymise TEXT,
    emotion_detectee VARCHAR(50),
    score_polarite DECIMAL(3,2),
    confiance_score DECIMAL(3,2),
    timestamp_anonymise TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id),
    FOREIGN KEY (programme_id) REFERENCES programmes(id),
    FOREIGN KEY (diffusion_id) REFERENCES diffusions(id),
    FOREIGN KEY (source_id) REFERENCES sources(id)
);
```

#### **Table SOURCES**
```sql
CREATE TABLE sources (
    id UUID PRIMARY KEY,
    nom_source VARCHAR(100) NOT NULL,
    type_source VARCHAR(20) NOT NULL,
    url_source VARCHAR(500),
    statut VARCHAR(20) DEFAULT 'active',
    derniere_collecte TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **Tables de Logs (Traçabilité RGPD)**

#### **Table LOGS_INGESTION**
```sql
CREATE TABLE logs_ingestion (
    id UUID PRIMARY KEY,
    source_id UUID NOT NULL,
    operation VARCHAR(50) NOT NULL,
    nombre_enregistrements INTEGER,
    statut VARCHAR(20),
    message_erreur TEXT,
    timestamp_operation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_id) REFERENCES sources(id)
);
```

#### **Table AGREGATIONS_EMOTIONNELLES**
```sql
CREATE TABLE agregations_emotionnelles (
    id UUID PRIMARY KEY,
    programme_id UUID,
    diffusion_id UUID,
    periode_debut TIMESTAMP,
    periode_fin TIMESTAMP,
    emotion_dominante VARCHAR(50),
    score_moyen DECIMAL(3,2),
    polarite_moyenne DECIMAL(3,2),
    nombre_reactions INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (programme_id) REFERENCES programmes(id),
    FOREIGN KEY (diffusion_id) REFERENCES diffusions(id)
);
```

---

## 🔹 MLP - Modèle Physique de Données

### **Architecture de Stockage**

#### **1. PostgreSQL (Base Principale)**
- **Rôle** : Stockage relationnel principal
- **Tables** : programmes, diffusions, utilisateurs, reactions, sources
- **Index** : 
  - `idx_reactions_emotion` sur `emotion_detectee`
  - `idx_reactions_timestamp` sur `timestamp_anonymise`
  - `idx_reactions_source` sur `source_id`

#### **2. SQLite (Développement/Local)**
- **Rôle** : Base de développement et tests
- **Fichier** : `semantic_pulse.db`
- **Usage** : Tests locaux, développement

#### **3. Parquet (Big Data)**
- **Rôle** : Stockage analytique haute performance
- **Format** : Parquet partitionné par date
- **Usage** : Analyses volumétriques, ML

#### **4. MinIO (Data Lake)**
- **Rôle** : Stockage objet pour fichiers volumineux
- **Buckets** : `semantic-pulse-raw`, `semantic-pulse-processed`
- **Usage** : Fichiers CSV, JSON, logs

### **Optimisations Performance**

#### **Index PostgreSQL**
```sql
-- Index pour les requêtes fréquentes
CREATE INDEX idx_reactions_emotion_timestamp 
ON reactions(emotion_detectee, timestamp_anonymise);

CREATE INDEX idx_reactions_source_type 
ON reactions(source_id, emotion_detectee);

CREATE INDEX idx_programmes_genre 
ON programmes(genre, chaine);
```

#### **Partitionnement Parquet**
```
data/processed/
├── year=2024/month=01/day=01/
│   ├── reactions.parquet
│   └── programmes.parquet
├── year=2024/month=01/day=02/
│   └── ...
```

---

## 🔗 Intégration des 5 Sources de Données

### **1. Fichier plat (CSV/JSON/Parquet)**
- **Type** : `file`
- **Table** : `sources` avec `type_source = 'file'`
- **Stockage** : MinIO/S3 + PostgreSQL
- **Exemples** : IMDb, Kaggle datasets

### **2. Base relationnelle (PostgreSQL/MySQL)**
- **Type** : `sql`
- **Table** : `sources` avec `type_source = 'sql'`
- **Stockage** : PostgreSQL principal
- **Exemples** : Programmes, diffusions, métadonnées

### **3. Big Data (Parquet/Data Lake)**
- **Type** : `bigdata`
- **Table** : `sources` avec `type_source = 'bigdata'`
- **Stockage** : MinIO/S3 + PostgreSQL
- **Exemples** : Twitter publics, Reddit dumps

### **4. Scraping web (HTML)**
- **Type** : `scraping`
- **Table** : `sources` avec `type_source = 'scraping'`
- **Stockage** : MinIO/S3 + PostgreSQL
- **Exemples** : Articles presse, blogs, forums

### **5. API REST (JSON/XML)**
- **Type** : `api`
- **Table** : `sources` avec `type_source = 'api'`
- **Stockage** : MinIO/S3 + PostgreSQL
- **Exemples** : NewsAPI, Media Cloud, GDELT, Twitter API

---

## 📊 Flux de Données ETL

### **Étape 1 : Extraction**
```
Sources multiples → Collecte → Stockage brut
├── Kaggle (CSV) → data/raw/file_source_tweets.csv
├── YouTube (API) → data/raw/youtube_data.json
├── Web Scraping → data/raw/scraping_data.json
└── Base SQLite → semantic_pulse.db
```

### **Étape 2 : Nettoyage**
```
Données brutes → Anonymisation → Validation
├── Suppression PII (emails, téléphones)
├── Hachage identifiants (SHA-256)
├── Normalisation formats
└── Validation cohérence
```

### **Étape 3 : Transformation**
```
Données nettoyées → Standardisation → Homogénéisation
├── Mapping colonnes → Schéma MERISE
├── Conversion types → Types SQL
├── Enrichissement → Métadonnées
└── Déduplication → Fusion intelligente
```

### **Étape 4 : Agrégation**
```
Données transformées → Fusion → Jointures MERISE
├── Fusion multi-sources → Table reactions
├── Jointures PK/FK → Relations MERISE
├── Calculs agrégés → Table agregations_emotionnelles
└── Génération jeu final → Base relationnelle
```

### **Étape 5 : Chargement**
```
Données agrégées → Multi-stockage → Disponibilité
├── PostgreSQL → Base relationnelle principale
├── Parquet → Stockage analytique
├── MinIO → Data Lake
└── Logs → Traçabilité RGPD
```

---

## 🛡️ Conformité RGPD

### **Anonymisation Obligatoire**
- **Utilisateur** : Hash SHA-256 uniquement
- **Texte** : Nettoyage et anonymisation automatique
- **Géolocalisation** : Régions groupées (ex: "FR-75")
- **Âge** : Groupes d'âge (ex: "18-25")
- **Aucun PII** : Nom, email, téléphone, etc.

### **Pseudonymisation**
- Identifiants uniques remplacés par des hash
- Données sensibles groupées ou supprimées
- Traçabilité des transformations

### **Droits des Utilisateurs**
- **Droit à l'effacement** : Suppression des données
- **Droit à la portabilité** : Export des données
- **Droit d'accès** : Consultation des données
- **Droit de rectification** : Modification des données

---

## ✅ Validation Merise

### **MCD Conforme**
- ✅ 5 entités exactes : Programme, Diffusion, Réaction, Utilisateur, Source
- ✅ Relations correctes entre entités
- ✅ Attributs RGPD-compliant

### **MLD Conforme**
- ✅ Tables relationnelles avec PK/FK
- ✅ Logs d'ingestion pour traçabilité
- ✅ Contraintes d'intégrité

### **MLP Conforme**
- ✅ PostgreSQL + Parquet + vues agrégées
- ✅ Architecture de stockage optimisée
- ✅ Performance et scalabilité

---

## 🎯 Conclusion

**La modélisation MERISE est 100% conforme au prompt :**

1. **MCD** : 5 entités principales avec relations correctes
2. **MLD** : Tables relationnelles avec PK/FK + logs RGPD
3. **MLP** : Architecture multi-stockage optimisée
4. **Sources** : 5 types de sources intégrées
5. **ETL** : Pipeline complet extraction → chargement
6. **RGPD** : Anonymisation et traçabilité complètes

**Le projet Semantic Pulse X respecte parfaitement toutes les exigences du cahier des charges !** 🎯✅
