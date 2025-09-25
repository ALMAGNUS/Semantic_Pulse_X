# 📊 Schéma Mermaid - Base de Données Relationnelle

## 🗄️ Schéma complet avec les 5 sources

```mermaid
erDiagram
    %% Entités principales - MCD Merise
    PROGRAMMES {
        uuid id PK
        string titre
        string chaine
        string genre
        integer duree_minutes
        text description
        datetime created_at
        datetime updated_at
    }
    
    DIFFUSIONS {
        uuid id PK
        uuid programme_id FK
        datetime date_debut
        datetime date_fin
        integer audience_estimee
        float rating_anonymise
        datetime created_at
    }
    
    UTILISATEURS {
        uuid id PK
        string hash_anonyme UK
        string region_anonymisee
        string age_groupe
        string langue_preferee
        datetime created_at
        datetime last_activity
    }
    
    REACTIONS {
        uuid id PK
        uuid programme_id FK
        uuid diffusion_id FK
        uuid utilisateur_id FK
        uuid source_id FK
        text texte_anonymise
        string langue
        string emotion_principale
        float score_emotion
        float polarite
        float confiance
        datetime timestamp
        datetime created_at
    }
    
    SOURCES {
        uuid id PK
        string nom
        string type_source
        string url
        jsonb configuration
        boolean actif
        datetime last_sync
        datetime created_at
    }
    
    %% Tables de logs - MLD Merise
    LOGS_INGESTION {
        uuid id PK
        uuid source_id FK
        datetime date_ingestion
        integer nombre_records
        string statut
        text message
        jsonb configuration_utilisee
    }
    
    %% Tables d'agrégation - MLP Merise
    AGREGATIONS_EMOTIONNELLES {
        uuid id PK
        uuid programme_id FK
        uuid diffusion_id FK
        datetime periode_debut
        datetime periode_fin
        string emotion_dominante
        float score_moyen
        float polarite_moyenne
        integer nombre_reactions
        datetime created_at
    }
    
    %% Relations principales
    PROGRAMMES ||--o{ DIFFUSIONS : "a"
    PROGRAMMES ||--o{ REACTIONS : "génère"
    DIFFUSIONS ||--o{ REACTIONS : "provoque"
    UTILISATEURS ||--o{ REACTIONS : "exprime"
    SOURCES ||--o{ REACTIONS : "collecte"
    
    %% Relations de logs
    SOURCES ||--o{ LOGS_INGESTION : "trace"
    
    %% Relations d'agrégation
    PROGRAMMES ||--o{ AGREGATIONS_EMOTIONNELLES : "agrège"
    DIFFUSIONS ||--o{ AGREGATIONS_EMOTIONNELLES : "agrège"
```

## 🔗 Intégration des 5 sources de données

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

## 📊 Flux de données

```mermaid
graph TD
    A[Source 1: Fichier plat] --> E[Pipeline ETL]
    B[Source 2: Base SQL] --> E
    C[Source 3: Big Data] --> E
    D[Source 4: Scraping] --> E
    F[Source 5: API REST] --> E
    
    E --> G[Anonymisation RGPD]
    G --> H[PostgreSQL Relations]
    G --> I[MinIO/S3 Data Lake]
    
    H --> J[Dashboards Streamlit]
    H --> K[Monitoring Grafana]
    I --> L[Analytics IA]
```

## 🔒 Conformité RGPD

### **Anonymisation intégrée**
- **Utilisateur** : Hash SHA-256 uniquement
- **Texte** : Nettoyage et anonymisation automatique
- **Géolocalisation** : Régions groupées
- **Âge** : Groupes d'âge
- **Aucun PII** : Nom, email, téléphone, etc.

### **Traçabilité complète**
- **Logs d'ingestion** : Chaque source tracée
- **Configuration** : Paramètres sauvegardés
- **Audit trail** : Historique des opérations

## 🚀 Performance

### **Index optimisés**
- Clés étrangères
- Colonnes de recherche fréquente
- Index composites pour les requêtes complexes

### **Partitionnement**
- Par date pour les réactions
- Par source pour les logs
- Par émotion pour les agrégations

### **Archiving**
- Données anciennes archivées
- Compression des données historiques
- Nettoyage automatique

**Toutes les 5 sources sont maintenant intégrées dans la base de données relationnelle !** 🗄️✅
