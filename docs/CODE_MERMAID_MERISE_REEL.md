# 📊 Code Mermaid pour Schéma MERISE RÉEL - Semantic Pulse X

## 🎯 Diagramme MCD (Modèle Conceptuel de Données) - STRUCTURE RÉELLE

```mermaid
erDiagram
    DIM_PAYS {
        integer id PK
        varchar nom
        varchar code_iso
    }
    
    DIM_DOMAINE {
        integer id PK
        varchar nom
        text description
    }
    
    DIM_HUMEUR {
        integer id PK
        varchar nom
        varchar couleur
        text description
    }
    
    SOURCES {
        integer id PK
        varchar nom "VARCHAR(100)"
        varchar type "VARCHAR(20)"
        varchar url_base "VARCHAR(500)"
        boolean actif
        datetime created_at
    }
    
    CONTENUS {
        integer id PK
        integer source_id FK
        integer pays_id FK
        integer domaine_id FK
        varchar url "VARCHAR(1000)"
        text titre
        text resume
        text texte
        datetime publication_date
        varchar auteur "VARCHAR(200)"
        varchar langue "VARCHAR(5)"
        datetime collected_at
        varchar sentiment "VARCHAR(30)"
        float confidence
        text themes
        varchar source_type "VARCHAR(50)"
    }
    
    REACTIONS {
        integer id PK
        integer contenu_id FK
        integer humeur_id FK
        float score
        float confidence
        datetime created_at
    }
    
    %% Relations avec cardinalités exactes
    DIM_PAYS ||--o{ CONTENUS : "localise"
    DIM_DOMAINE ||--o{ CONTENUS : "catégorise"
    DIM_HUMEUR ||--o{ REACTIONS : "définit"
    SOURCES ||--o{ CONTENUS : "produit"
    CONTENUS ||--o{ REACTIONS : "génère"
```

## 🔗 Diagramme des Sources de Données RÉELLES

```mermaid
graph TD
    A[Kaggle CSV<br/>1000 tweets] --> E[Pipeline ETL]
    B[YouTube API<br/>180 vidéos] --> E
    C[Web Scraping<br/>Yahoo + Franceinfo] --> E
    D[GDELT GKG<br/>Big Data] --> E
    F[NewsAPI<br/>Articles] --> E
    
    E --> G[aggregate_sources.py]
    G --> H[load_aggregated_to_db.py]
    H --> I[semantic_pulse.db]
    
    I --> J[DIM_PAYS: 1]
    I --> K[DIM_DOMAINE: 2]
    I --> L[DIM_HUMEUR: 3]
    I --> M[SOURCES: 487]
    I --> N[CONTENUS: 535]
    I --> O[REACTIONS: 0]
    
    style A fill:#e1f5fe
    style B fill:#e8f5e8
    style C fill:#fff3e0
    style D fill:#fce4ec
    style F fill:#f3e5f5
    style I fill:#e0f2f1
```

## 📊 Diagramme Architecture MLP RÉELLE

```mermaid
graph TB
    subgraph "Couche Application"
        A[Streamlit Frontend<br/>app/frontend/streamlit_app.py]
        B[FastAPI Backend<br/>app/backend/main.py]
    end
    
    subgraph "Couche Données MERISE"
        C[semantic_pulse.db<br/>Base principale]
        D[kaggle_tweets.db<br/>Base Kaggle]
        E[Parquet Files<br/>Big Data]
        F[MinIO<br/>Data Lake]
    end
    
    subgraph "Couche Sources"
        G[Kaggle CSV<br/>1000 tweets]
        H[YouTube API<br/>180 vidéos]
        I[Web Scraping<br/>Yahoo/Franceinfo]
        J[GDELT GKG<br/>Big Data]
        K[NewsAPI<br/>Articles]
    end
    
    subgraph "Couche IA"
        L[Emotion Classifier<br/>HuggingFace]
        M[Topic Clustering<br/>BERTopic]
        N[Embeddings<br/>SentenceTransformer]
        O[Ollama<br/>LLM Local]
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
    K --> B
    
    B --> L
    B --> M
    B --> N
    B --> O
    
    style C fill:#e3f2fd
    style D fill:#e8f5e8
    style E fill:#fff3e0
    style F fill:#fce4ec
```

## 🔄 Diagramme Flux ETL RÉEL

```mermaid
flowchart TD
    subgraph "EXTRACTION"
        A1[Kaggle CSV<br/>1000 tweets]
        A2[YouTube API<br/>180 vidéos]
        A3[Web Scraping<br/>Yahoo/Franceinfo]
        A4[GDELT GKG<br/>Big Data]
        A5[NewsAPI<br/>Articles]
    end
    
    subgraph "NETTOYAGE"
        B1[aggregate_sources.py<br/>Déduplication]
        B2[Anonymisation RGPD<br/>PII Removal]
        B3[Normalisation<br/>Standardisation]
        B4[Validation<br/>Qualité données]
    end
    
    subgraph "TRANSFORMATION"
        C1[Conversion types<br/>Datetime/String]
        C2[Enrichissement<br/>Sentiment/Confidence]
        C3[Mapping dimensions<br/>Pays/Domaine/Humeur]
        C4[Génération JSON<br/>Format standard]
    end
    
    subgraph "CHARGEMENT"
        D1[load_aggregated_to_db.py<br/>SQLite MERISE]
        D2[load_kaggle_to_db.py<br/>SQLite Kaggle]
        D3[Parquet Files<br/>Big Data]
        D4[MinIO Upload<br/>Data Lake]
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
    C4 --> D2
    C4 --> D3
    C4 --> D4
    
    style B1 fill:#ffebee
    style C1 fill:#e8f5e8
    style D1 fill:#e3f2fd
    style D2 fill:#e3f2fd
```

## 🛡️ Diagramme Conformité RGPD RÉELLE

```mermaid
graph LR
    subgraph "DONNÉES BRUTES"
        A[Texte original<br/>YouTube/Web]
        B[Identifiants<br/>URLs/IDs]
        C[Géolocalisation<br/>Pays exact]
        D[Dates précises<br/>Timestamps]
    end
    
    subgraph "ANONYMIZATION"
        E[Texte nettoyé<br/>PII Removal]
        F[URLs anonymisées<br/>Hash SHA-256]
        G[Pays généralisé<br/>FR/EN/etc]
        H[Dates anonymisées<br/>Périodes]
    end
    
    subgraph "PSEUDONYMIZATION"
        I[Hash anonyme<br/>Utilisateurs]
        J[Zone géographique<br/>Régions]
        K[Tranche temporelle<br/>Périodes]
        L[Métadonnées<br/>Sécurisées]
    end
    
    subgraph "TRACABILITÉ"
        M[Logs ingestion<br/>sources table]
        N[Audit trail<br/>collected_at]
        O[Droits utilisateurs<br/>RGPD compliant]
        P[Suppression<br/>Right to forget]
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

## 📈 Diagramme Monitoring RÉEL

```mermaid
graph TB
    subgraph "MÉTRIQUES"
        A[Prometheus<br/>Port 9090]
        B[Grafana Dashboard<br/>Port 3000]
    end
    
    subgraph "INDICATEURS"
        C[Qualité données<br/>535 contenus]
        D[Performance ETL<br/>5 sources]
        E[Conformité RGPD<br/>Anonymisation]
        F[Disponibilité services<br/>Docker Compose]
    end
    
    subgraph "ALERTES"
        G[Seuils qualité<br/>Confidence < 0.5]
        H[Délais ETL<br/>Timeout > 30s]
        I[Erreurs RGPD<br/>PII détecté]
        J[Pannes services<br/>Ports fermés]
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
   - **GitHub** (dans un fichier .md)
   - **VS Code** avec extension Mermaid
   - **Notion** ou **Obsidian**

### **Exemple d'utilisation :**
```markdown
```mermaid
erDiagram
    DIM_PAYS {
        integer id PK
        varchar nom
        varchar code_iso
    }
    CONTENUS {
        integer id PK
        integer pays_id FK
        text titre
    }
    DIM_PAYS ||--o{ CONTENUS : "localise"
```
```

**Ces diagrammes montrent la VRAIE structure MERISE avec les cardinalités exactes basées sur semantic_pulse.db !** 🎯✅

