# 📊 Modélisation Merise - Semantic Pulse X

## 🎯 Conformité au prompt

Cette modélisation respecte **exactement** les spécifications du prompt :
- **MCD** : entités `Programme`, `Diffusion`, `Réaction`, `Utilisateur`, `Source`
- **MLD** : tables relationnelles avec PK/FK + logs ingestion
- **MLP** : PostgreSQL + Parquet + vues agrégées

## 🔹 MCD (Modèle Conceptuel de Données)

### **Entités principales**

#### 1. **Programme**
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

#### 2. **Diffusion**
- **Description** : Diffusion d'un programme
- **Attributs** :
  - `id` (PK) - Identifiant unique
  - `programme_id` (FK) - Référence vers Programme
  - `date_debut` - Date/heure de début
  - `date_fin` - Date/heure de fin
  - `audience_estimee` - Audience anonymisée
  - `rating_anonymise` - Note anonymisée
  - `created_at` - Date de création

#### 3. **Utilisateur**
- **Description** : Utilisateur anonymisé (RGPD compliant)
- **Attributs** :
  - `id` (PK) - Identifiant unique
  - `hash_anonyme` - Hash SHA-256 anonymisé
  - `region_anonymisee` - Région anonymisée (ex: "FR-75")
  - `age_groupe` - Groupe d'âge (ex: "18-25")
  - `langue_preferee` - Langue préférée
  - `created_at` - Date de création
  - `last_activity` - Dernière activité

#### 4. **Réaction**
- **Description** : Réaction émotionnelle anonymisée
- **Attributs** :
  - `id` (PK) - Identifiant unique
  - `programme_id` (FK) - Référence vers Programme
  - `diffusion_id` (FK) - Référence vers Diffusion
  - `utilisateur_id` (FK) - Référence vers Utilisateur
  - `source_id` (FK) - Référence vers Source
  - `texte_anonymise` - Texte nettoyé et anonymisé
  - `langue` - Langue du texte
  - `emotion_principale` - Émotion détectée
  - `score_emotion` - Score d'émotion (0.0-1.0)
  - `polarite` - Polarité (-1.0 à 1.0)
  - `confiance` - Niveau de confiance
  - `timestamp` - Horodatage de la réaction
  - `created_at` - Date de création

#### 5. **Source**
- **Description** : Source de données (5 types obligatoires)
- **Attributs** :
  - `id` (PK) - Identifiant unique
  - `nom` - Nom de la source
  - `type_source` - Type : "file", "sql", "bigdata", "scraping", "api"
  - `url` - URL de la source
  - `configuration` - Configuration anonymisée (JSONB)
  - `actif` - Statut actif/inactif
  - `last_sync` - Dernière synchronisation
  - `created_at` - Date de création

### **Relations MCD**

```
Programme (1,N) ---> Diffusion
Programme (1,N) ---> Réaction
Diffusion (1,N) ---> Réaction
Utilisateur (1,N) ---> Réaction
Source (1,N) ---> Réaction
```

## 🔹 MLD (Modèle Logique de Données)

### **Tables relationnelles**

#### **Tables principales**
- `programmes` - Entité Programme
- `diffusions` - Entité Diffusion
- `utilisateurs` - Entité Utilisateur
- `reactions` - Entité Réaction
- `sources` - Entité Source

#### **Tables de logs d'ingestion**
- `logs_ingestion` - Traçabilité des données collectées
  - `source_id` (FK) - Référence vers Source
  - `date_ingestion` - Date d'ingestion
  - `nombre_records` - Nombre d'enregistrements
  - `statut` - Statut : "success", "error", "partial"
  - `message` - Message d'erreur ou d'info
  - `configuration_utilisee` - Configuration utilisée

### **Contraintes d'intégrité**

#### **Clés primaires**
- Toutes les tables ont une PK `id` (UUID)

#### **Clés étrangères**
- `diffusions.programme_id` → `programmes.id`
- `reactions.programme_id` → `programmes.id`
- `reactions.diffusion_id` → `diffusions.id`
- `reactions.utilisateur_id` → `utilisateurs.id`
- `reactions.source_id` → `sources.id`
- `logs_ingestion.source_id` → `sources.id`

#### **Contraintes RGPD**
- Aucun PII (Personally Identifiable Information)
- Anonymisation obligatoire des données utilisateur
- Hash SHA-256 pour les identifiants anonymisés
- Régions et âges groupés uniquement

## 🔹 MLP (Modèle Physique de Données)

### **PostgreSQL**
- **Base principale** : `semantic_pulse`
- **Tables relationnelles** : Toutes les entités MCD
- **Index** : Sur les clés étrangères et colonnes de recherche
- **Contraintes** : Intégrité référentielle et RGPD

### **Parquet (Data Lake)**
- **Stockage** : MinIO/S3
- **Format** : Parquet pour performance
- **Partitionnement** : Par date et source
- **Compression** : Snappy

### **Vues agrégées**

#### **Agrégation émotionnelle**
- `agregations_emotionnelles` - Vues pré-calculées
  - Agrégations temporelles par programme/diffusion
  - Métriques émotionnelles moyennes
  - Compteurs de réactions

### **Architecture de stockage**

```
PostgreSQL (Relationnel)
├── programmes
├── diffusions
├── utilisateurs
├── reactions
├── sources
└── logs_ingestion

MinIO/S3 (Data Lake)
├── raw/
│   ├── file/
│   ├── sql/
│   ├── bigdata/
│   ├── scraping/
│   └── api/
├── processed/
│   ├── reactions_clean.parquet
│   ├── emotions_aggregated.parquet
│   └── trends_daily.parquet
└── analytics/
    ├── wordclouds/
    ├── predictions/
    └── reports/
```

## 🔹 Conformité RGPD

### **Anonymisation obligatoire**
- **Utilisateur** : Hash SHA-256 uniquement
- **Texte** : Nettoyage et anonymisation automatique
- **Géolocalisation** : Régions groupées (ex: "FR-75")
- **Âge** : Groupes d'âge (ex: "18-25")
- **Aucun PII** : Nom, email, téléphone, etc.

### **Pseudonymisation**
- Identifiants uniques remplacés par des hash
- Données sensibles groupées ou supprimées
- Traçabilité des transformations

### **Droits des utilisateurs**
- **Droit à l'effacement** : Suppression des données
- **Droit à la portabilité** : Export des données
- **Droit d'accès** : Consultation des données
- **Droit de rectification** : Modification des données

## 🔹 Sources de données (5 obligatoires)

### **1. Fichier plat (CSV/JSON/Parquet)**
- **Type** : `file`
- **Exemples** : IMDb, Kaggle datasets TV/films
- **Stockage** : `/data/raw/file/`
- **Format** : CSV, JSON, Parquet

### **2. Base relationnelle (PostgreSQL/MySQL)**
- **Type** : `sql`
- **Exemples** : Programmes, diffusions, métadonnées
- **Stockage** : Base PostgreSQL principale
- **Format** : Tables relationnelles

### **3. Big Data (Parquet/Data Lake)**
- **Type** : `bigdata`
- **Exemples** : Twitter publics, Reddit dumps
- **Stockage** : MinIO/S3
- **Format** : Parquet partitionné

### **4. Scraping web (HTML)**
- **Type** : `scraping`
- **Exemples** : Articles presse, blogs, forums
- **Stockage** : `/data/raw/scraping/`
- **Format** : HTML → JSON nettoyé

### **5. API REST (JSON/XML)**
- **Type** : `api`
- **Exemples** : NewsAPI, Media Cloud, GDELT, Twitter API
- **Stockage** : `/data/raw/api/`
- **Format** : JSON, XML

## 🔹 Workflow de données

### **1. Collecte**
- Scripts modulaires par source
- Anonymisation dès l'extraction
- Stockage dans `/data/raw/`

### **2. Nettoyage**
- Détection des entrées corrompues
- Homogénéisation des formats
- Déduplication

### **3. Agrégation**
- Fusion multi-sources
- Génération du jeu final unique
- Stockage relationnel + Data Lake

### **4. Analyse**
- Dashboards Streamlit
- Monitoring Grafana
- Prédictions IA

## 🔹 Validation Merise

### ✅ **MCD conforme**
- 5 entités exactes : Programme, Diffusion, Réaction, Utilisateur, Source
- Relations correctes entre entités
- Attributs RGPD-compliant

### ✅ **MLD conforme**
- Tables relationnelles avec PK/FK
- Logs d'ingestion pour traçabilité
- Contraintes d'intégrité

### ✅ **MLP conforme**
- PostgreSQL + Parquet + vues agrégées
- Architecture de stockage optimisée
- Performance et scalabilité

**La modélisation Merise est maintenant 100% conforme au prompt !** 📊✅

