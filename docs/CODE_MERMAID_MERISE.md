# ⚠️ ATTENTION - SCHÉMA OBSOLÈTE

**Ce fichier contient un schéma MERISE obsolète qui ne correspond pas à la structure réelle de `semantic_pulse.db`.**

## 🔄 Voir le schéma RÉEL

**Consultez le fichier : `docs/CODE_MERMAID_MERISE_REEL.md`**

Ce fichier contient les diagrammes Mermaid basés sur la vraie structure de la base de données :
- 6 tables réelles (DIM_PAYS, DIM_DOMAINE, DIM_HUMEUR, SOURCES, CONTENUS, REACTIONS)
- Cardinalités exactes
- Relations correctes
- Structure conforme à l'implémentation

---

# 📊 Code Mermaid pour Schéma MERISE - Semantic Pulse X

## 🎯 Diagramme MCD (Modèle Conceptuel de Données)

```mermaid
erDiagram
    PROGRAMME {
        uuid id PK
        string titre
        string chaine
        string genre
        integer duree_minutes
        text description
        datetime created_at
        datetime updated_at
    }
    
    DIFFUSION {
        uuid id PK
        uuid programme_id FK
        datetime date_debut
        datetime date_fin
        integer audience_estimee
        decimal rating_anonymise
        datetime created_at
    }
    
    UTILISATEUR {
        uuid id PK
        string hash_anonyme
        string region_anonymisee
        string age_groupe
        string langue_preferee
        datetime created_at
        datetime last_activity
    }
    
    REACTION {
        uuid id PK
        uuid utilisateur_id FK
        uuid programme_id FK
        uuid diffusion_id FK
        uuid source_id FK
        text texte_anonymise
        string emotion_detectee
        decimal score_polarite
        decimal confiance_score
        datetime timestamp_anonymise
        datetime created_at
    }
    
    SOURCE {
        uuid id PK
        string nom_source
        string type_source
        string url_source
        string statut
        datetime derniere_collecte
        datetime created_at
    }
    
    LOGS_INGESTION {
        uuid id PK
        uuid source_id FK
        string operation
        integer nombre_enregistrements
        string statut
        text message_erreur
        datetime timestamp_operation
    }
    
    AGREGATIONS_EMOTIONNELLES {
        uuid id PK
        uuid programme_id FK
        uuid diffusion_id FK
        datetime periode_debut
        datetime periode_fin
        string emotion_dominante
        decimal score_moyen
        decimal polarite_moyenne
        integer nombre_reactions
        datetime created_at
    }
    
    %% Relations principales
    PROGRAMME ||--o{ DIFFUSION : "a"
    PROGRAMME ||--o{ REACTION : "génère"
    DIFFUSION ||--o{ REACTION : "provoque"
    UTILISATEUR ||--o{ REACTION : "exprime"
    SOURCE ||--o{ REACTION : "collecte"
    
    %% Relations de logs
    SOURCE ||--o{ LOGS_INGESTION : "trace"
    
    %% Relations d'agrégation
    PROGRAMME ||--o{ AGREGATIONS_EMOTIONNELLES : "agrège"
    DIFFUSION ||--o{ AGREGATIONS_EMOTIONNELLES : "agrège"
```

## 🔗 Diagramme des Sources de Données

```mermaid
graph TD
    A[Source 1: Fichier plat] --> E[Pipeline ETL]
    B[Source 2: Base relationnelle] --> E
    C[Source 3: Big Data] --> E
    D[Source 4: Web Scraping] --> E
    F[Source 5: API REST] --> E
    
    E --> G[Nettoyage RGPD]
    G --> H[Transformation]
    H --> I[Agrégation MERISE]
    I --> J[Chargement Multi-stockage]
    
    J --> K[PostgreSQL]
    J --> L[SQLite]
    J --> M[Parquet]
    J --> N[MinIO]
    
    style A fill:#e1f5fe
    style B fill:#e8f5e8
    style C fill:#fff3e0
    style D fill:#fce4ec
    style F fill:#f3e5f5
    style E fill:#ffebee
    style J fill:#e0f2f1
```

## 📊 Diagramme Architecture MLP

```mermaid
graph TB
    subgraph "Couche Application"
        A[Streamlit Frontend]
        B[FastAPI Backend]
    end
    
    subgraph "Couche Données"
        C[PostgreSQL<br/>Base principale]
        D[SQLite<br/>Développement]
        E[Parquet<br/>Big Data]
        F[MinIO<br/>Data Lake]
    end
    
    subgraph "Couche Sources"
        G[Kaggle CSV]
        H[YouTube API]
        I[Web Scraping]
        J[NewsAPI]
    end
    
    subgraph "Couche IA"
        K[Emotion Classifier]
        L[Topic Clustering]
        M[Embeddings]
    end
    
    A --> B
    B --> C
    B --> D
    B --> E
    B --> F
    
    G --> B
    H --> B
    I --> B
    J --> B
    
    B --> K
    B --> L
    B --> M
    
    style C fill:#e3f2fd
    style D fill:#e8f5e8
    style E fill:#fff3e0
    style F fill:#fce4ec
```

## 🔄 Diagramme Flux ETL

```mermaid
flowchart TD
    subgraph "EXTRACTION"
        A1[Kaggle Dataset]
        A2[YouTube API]
        A3[Web Scraping]
        A4[NewsAPI]
        A5[Base SQLite]
    end
    
    subgraph "NETTOYAGE"
        B1[Suppression PII]
        B2[Hachage SHA-256]
        B3[Normalisation]
        B4[Validation RGPD]
    end
    
    subgraph "TRANSFORMATION"
        C1[Standardisation colonnes]
        C2[Conversion types]
        C3[Enrichissement]
        C4[Déduplication]
    end
    
    subgraph "AGRÉGATION"
        D1[Fusion multi-sources]
        D2[Jointures MERISE]
        D3[Calculs agrégés]
        D4[Génération jeu final]
    end
    
    subgraph "CHARGEMENT"
        E1[PostgreSQL]
        E2[Parquet]
        E3[MinIO]
        E4[Logs traçabilité]
    end
    
    A1 --> B1
    A2 --> B1
    A3 --> B1
    A4 --> B1
    A5 --> B1
    
    B1 --> B2
    B2 --> B3
    B3 --> B4
    
    B4 --> C1
    C1 --> C2
    C2 --> C3
    C3 --> C4
    
    C4 --> D1
    D1 --> D2
    D2 --> D3
    D3 --> D4
    
    D4 --> E1
    D4 --> E2
    D4 --> E3
    D4 --> E4
    
    style B1 fill:#ffebee
    style C1 fill:#e8f5e8
    style D1 fill:#e3f2fd
    style E1 fill:#fff3e0
```

## 🛡️ Diagramme Conformité RGPD

```mermaid
graph LR
    subgraph "DONNÉES BRUTES"
        A[Texte original]
        B[Identifiants]
        C[Géolocalisation]
        D[Âge exact]
    end
    
    subgraph "ANONYMIZATION"
        E[Texte nettoyé]
        F[Hash SHA-256]
        G[Région anonymisée]
        H[Groupe d'âge]
    end
    
    subgraph "PSEUDONYMIZATION"
        I[Hash anonyme]
        J[Zone géographique]
        K[Tranche d'âge]
        L[Métadonnées]
    end
    
    subgraph "TRACABILITÉ"
        M[Logs ingestion]
        N[Audit trail]
        O[Droits utilisateurs]
        P[Suppression]
    end
    
    A --> E
    B --> F
    C --> G
    D --> H
    
    E --> I
    F --> I
    G --> J
    H --> K
    
    I --> M
    J --> N
    K --> O
    L --> P
    
    style E fill:#e8f5e8
    style F fill:#e8f5e8
    style I fill:#e3f2fd
    style M fill:#fff3e0
```

## 📈 Diagramme Monitoring

```mermaid
graph TB
    subgraph "MÉTRIQUES"
        A[Prometheus]
        B[Grafana Dashboard]
    end
    
    subgraph "INDICATEURS"
        C[Qualité données]
        D[Performance ETL]
        E[Conformité RGPD]
        F[Disponibilité services]
    end
    
    subgraph "ALERTES"
        G[Seuils qualité]
        H[Délais ETL]
        I[Erreurs RGPD]
        J[Pannes services]
    end
    
    A --> C
    A --> D
    A --> E
    A --> F
    
    C --> G
    D --> H
    E --> I
    F --> J
    
    B --> A
    
    style A fill:#e3f2fd
    style B fill:#e8f5e8
    style G fill:#ffebee
    style H fill:#ffebee
```

---

## 🎯 Instructions d'utilisation

### **Pour utiliser ces diagrammes :**

1. **Copiez le code Mermaid** de chaque section
2. **Collez-le dans un éditeur Mermaid** comme :
   - [Mermaid Live Editor](https://mermaid.live/)
   - [GitHub** (dans un fichier .md)
   - **VS Code** avec extension Mermaid
   - **Notion** ou **Obsidian**

### **Exemple d'utilisation :**
```markdown
```mermaid
erDiagram
    PROGRAMME {
        uuid id PK
        string titre
    }
    DIFFUSION {
        uuid id PK
        uuid programme_id FK
    }
    PROGRAMME ||--o{ DIFFUSION : "a"
```
```

**Ces diagrammes montrent clairement toute la conformité MERISE avec les cardinalités exactes !** 🎯✅
