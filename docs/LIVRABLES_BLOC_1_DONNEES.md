# 📋 LIVRABLES BLOC 1 - LES DONNÉES
## Certification E1/E2/E3 - Semantic Pulse X

---

## 🔗 **LIEN VERS DÉPÔT GITHUB**
```
https://github.com/ALMAGNUS/Semantic_Pulse_X
```

---

## 🤖 **LIEN POSSIBLE AVEC DE L'IA**

### **Comment utiliser ces données pour faire de l'IA**

**Les données collectées servent de base pour plusieurs types d'IA :**

#### **1. Classification d'Émotions**
- **Données d'entrée** : Textes des tweets, articles, commentaires YouTube
- **Type d'IA** : Classification supervisée (POSITIVE, NEGATIVE, NEUTRAL)
- **Modèles utilisés** : RoBERTa français, DialoGPT
- **Objectif** : Analyser le sentiment des Français en temps réel

#### **2. Prédiction de Tendances**
- **Données d'entrée** : Historique des émotions + données géopolitiques GDELT
- **Type d'IA** : Régression temporelle, moyennes mobiles
- **Modèles utilisés** : Système prédictif créatif
- **Objectif** : Anticiper les évolutions émotionnelles

#### **3. Analyse de Thèmes**
- **Données d'entrée** : Contenu textuel agrégé
- **Type d'IA** : Clustering, topic modeling
- **Modèles utilisés** : Word2Vec, LDA
- **Objectif** : Identifier les sujets qui influencent les émotions

#### **4. Génération de Réponses**
- **Données d'entrée** : Questions utilisateur + contexte émotionnel
- **Type d'IA** : Génération de texte conversationnel
- **Modèles utilisés** : DialoGPT français
- **Objectif** : Répondre aux questions sur les émotions

---

## 📊 **SOURCES DE DONNÉES**

### **Résumé des Sources**

**Semantic Pulse X** collecte des données depuis **5 sources distinctes** qui sont ensuite agrégées dans une **6ème source (base MERISE)** :

1. **📁 Fichier plat** : Dataset Kaggle Sentiment140
2. **🗄️ Base de données externe** : SQLite avec schéma MERISE
3. **🌐 API externe** : YouTube Data API v3 + NewsAPI
4. **🕷️ Web Scraping** : Yahoo Actualités FR + France Info
5. **📈 Système Big Data** : GDELT GKG (Global Knowledge Graph)
6. **🔄 Base agrégée** : `semantic_pulse.db` (base finale MERISE)

---

## 📁 **FICHIER**

### **Source : Dataset Kaggle Sentiment140**
- **Type** : Fichier CSV plat
- **Volume** : 1,600,000 tweets
- **Format** : Colonnes (sentiment, texte, id)
- **Acquisition** : Téléchargement direct depuis Kaggle
- **Utilisation** : Entraînement des modèles d'IA

### **Métadonnées**
- **Colonnes** : 3 colonnes principales
  - `sentiment` : 0 (négatif) ou 4 (positif)
  - `texte` : Contenu du tweet
  - `id` : Identifiant unique
- **Types** : INTEGER, TEXT, INTEGER
- **Encodage** : UTF-8
- **Séparateur** : Virgule

---

## 🗄️ **BASE DE DONNÉES**

### **Source : SQLite avec schéma MERISE**
- **Type** : Base de données relationnelle
- **Volume** : 535 contenus intégrés
- **Tables** : sources, contenus, reactions, dim_pays, dim_domaine, dim_humeur
- **Acquisition** : Génération automatique via ORM SQLAlchemy
- **Utilisation** : Stockage structuré des données analysées

### **Métadonnées**
- **Tables principales** :
  - `sources` : Informations sur les sources de données
  - `contenus` : Contenu textuel et métadonnées
  - `reactions` : Réactions et émotions associées
- **Tables dimensionnelles** :
  - `dim_pays` : Dimension géographique
  - `dim_domaine` : Dimension thématique
  - `dim_humeur` : Dimension émotionnelle

---

## 🌐 **API EXTERNE**

### **Source : YouTube Data API v3 + NewsAPI**
- **Type** : APIs REST externes
- **Volume** : 180 vidéos YouTube + articles NewsAPI
- **Format** : JSON avec métadonnées complètes
- **Acquisition** : Requêtes API automatisées
- **Utilisation** : Collecte temps réel de contenu

### **Métadonnées YouTube**
- **Colonnes** : titre, description, transcript, vues, likes, date
- **Types** : TEXT, TEXT, TEXT, INTEGER, INTEGER, TIMESTAMP
- **Filtres** : Langue française, chaînes politiques/actualités

### **Métadonnées NewsAPI**
- **Colonnes** : titre, contenu, source, auteur, date, url
- **Types** : TEXT, TEXT, TEXT, TEXT, TIMESTAMP, TEXT
- **Filtres** : France, actualités, politique

---

## 🕷️ **WEB SCRAPING**

### **Source : Yahoo Actualités FR + France Info**
- **Type** : Scraping HTML avec Selenium
- **Volume** : Articles français récents
- **Format** : JSON structuré avec contenu + métadonnées
- **Acquisition** : Scripts automatisés de scraping
- **Utilisation** : Collecte d'articles d'actualité

### **Métadonnées Web Scraping**
- **Colonnes** : titre, contenu, auteur, date, url, source
- **Types** : TEXT, TEXT, TEXT, TIMESTAMP, TEXT, TEXT
- **Technologies** : Selenium + BeautifulSoup
- **Filtres** : Sites français, actualités, politique

---

## 📈 **SYSTÈME BIG DATA**

### **Source : GDELT GKG (Global Knowledge Graph)**
- **Type** : Données géopolitiques mondiales
- **Volume** : 1,283 enregistrements français
- **Format** : Données structurées géopolitiques
- **Acquisition** : Pipeline automatisé GDELT
- **Utilisation** : Analyse géopolitique française

### **Métadonnées GDELT**
- **Colonnes** : date, source, acteur, action, lieu, thèmes, sentiment
- **Types** : TIMESTAMP, TEXT, TEXT, TEXT, TEXT, TEXT, FLOAT
- **Filtres** : France, événements géopolitiques
- **Mise à jour** : Quotidienne

---

## 🔄 **BASE AGRÉGÉE MERISE**

### **Source : semantic_pulse.db (Base finale)**
- **Type** : Base de données relationnelle agrégée
- **Volume** : 535 contenus analysés et intégrés
- **Format** : SQLite avec schéma MERISE complet
- **Acquisition** : Pipeline ETL d'agrégation
- **Utilisation** : Base finale pour l'application

---

## 📋 **EXPLICATION DES MÉTADONNÉES**

### **Résumé des Colonnes et Types**

#### **Table SOURCES**
- `id` : INTEGER PRIMARY KEY
- `nom` : VARCHAR(100) - Nom de la source
- `type` : VARCHAR(50) - Type de source (fichier, api, scraping, bigdata)
- `url` : VARCHAR(500) - URL de la source
- `created_at` : TIMESTAMP - Date de création

#### **Table CONTENUS**
- `id` : INTEGER PRIMARY KEY
- `source_id` : INTEGER FOREIGN KEY - Référence vers sources
- `titre` : TEXT - Titre du contenu
- `contenu` : TEXT - Contenu textuel principal
- `sentiment` : VARCHAR(50) - Sentiment détecté
- `confidence` : FLOAT - Niveau de confiance
- `created_at` : TIMESTAMP - Date de création

#### **Table REACTIONS**
- `id` : INTEGER PRIMARY KEY
- `contenu_id` : INTEGER FOREIGN KEY - Référence vers contenus
- `emotion` : VARCHAR(50) - Émotion spécifique
- `score` : FLOAT - Score de l'émotion
- `created_at` : TIMESTAMP - Date de création

---

## 🔒 **RGPD ET ASPECTS ÉTHIQUES - IA RESPONSABLE**

### **Résumé**

**Semantic Pulse X** respecte strictement le RGPD et les principes d'IA responsable :

#### **1. Anonymisation des Données**
- **Pseudonymisation** : Suppression des identifiants personnels
- **Hachage** : Chiffrement des données sensibles
- **Agrégation** : Données groupées pour préserver l'anonymat

#### **2. Consentement et Transparence**
- **Sources publiques** : Toutes les données proviennent de sources publiques
- **Transparence** : Documentation complète des traitements
- **Contrôle** : Possibilité de suppression des données

#### **3. Minimisation des Données**
- **Pertinence** : Seules les données nécessaires sont collectées
- **Limitation** : Conservation limitée dans le temps
- **Finalité** : Utilisation uniquement pour l'analyse de sentiment

#### **4. Sécurité des Données**
- **Chiffrement** : Données chiffrées en transit et au repos
- **Accès** : Contrôle d'accès strict
- **Audit** : Traçabilité complète des accès

#### **5. IA Responsable**
- **Biais** : Tests de biais sur les modèles
- **Équité** : Traitement équitable de tous les groupes
- **Explicabilité** : Modèles interprétables et explicables

---

## 🔧 **TRAITEMENT DES DONNÉES**

### **Préprocessing et Cleaning**

#### **1. Nettoyage des Données**
- **Suppression des doublons** : Élimination des contenus identiques
- **Normalisation** : Standardisation des formats de texte
- **Filtrage** : Suppression des contenus non pertinents
- **Validation** : Vérification de la cohérence des données

#### **2. Traitement du Texte**
- **Tokenisation** : Découpage en mots/tokens
- **Lemmatisation** : Réduction à la forme canonique
- **Suppression des stop words** : Élimination des mots vides
- **Normalisation** : Conversion en minuscules, suppression de la ponctuation

#### **3. Anonymisation**
- **Suppression des PII** : Élimination des données personnelles
- **Pseudonymisation** : Remplacement par des identifiants anonymes
- **Hachage** : Chiffrement des données sensibles
- **Agrégation** : Groupement pour préserver l'anonymat

#### **4. Équilibrage des Données**
- **Over-sampling** : Augmentation des classes minoritaires
- **Under-sampling** : Réduction des classes majoritaires
- **SMOTE** : Génération de données synthétiques
- **Validation croisée** : Évaluation robuste des modèles

---

## 🏗️ **MÉTHODE MERISE**

### **Résumé**

**Semantic Pulse X** utilise la méthode MERISE pour concevoir une base de données relationnelle robuste et conforme aux exigences E2.

#### **Avantages de MERISE**
- **Modélisation conceptuelle** : Vision métier claire
- **Normalisation** : Élimination des redondances
- **Intégrité** : Contraintes d'intégrité respectées
- **Évolutivité** : Architecture extensible
- **Maintenance** : Structure claire et documentée

---

## 📊 **MCD (Modèle Conceptuel de Données)**

### **Entités Principales**

```
SOURCES (1) ──── (N) CONTENUS (N) ──── (N) REACTIONS
    │                    │
    │                    │
    └─── DIM_PAYS        └─── DIM_DOMAINE
    └─── DIM_HUMEUR
```

### **Cardinalités**
- **SOURCES → CONTENUS** : 1:N (une source peut avoir plusieurs contenus)
- **CONTENUS → REACTIONS** : 1:N (un contenu peut avoir plusieurs réactions)
- **SOURCES → DIM_PAYS** : N:1 (plusieurs sources peuvent être du même pays)
- **CONTENUS → DIM_DOMAINE** : N:1 (plusieurs contenus peuvent être du même domaine)

---

## 🗄️ **MLD (Modèle Logique de Données)**

### **Tables et Relations**

```sql
-- Table principale des sources
CREATE TABLE sources (
    id INTEGER PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des contenus
CREATE TABLE contenus (
    id INTEGER PRIMARY KEY,
    source_id INTEGER REFERENCES sources(id),
    titre TEXT,
    contenu TEXT NOT NULL,
    sentiment VARCHAR(50),
    confidence FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des réactions
CREATE TABLE reactions (
    id INTEGER PRIMARY KEY,
    contenu_id INTEGER REFERENCES contenus(id),
    emotion VARCHAR(50),
    score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tables dimensionnelles
CREATE TABLE dim_pays (id INTEGER PRIMARY KEY, nom VARCHAR(100));
CREATE TABLE dim_domaine (id INTEGER PRIMARY KEY, nom VARCHAR(100));
CREATE TABLE dim_humeur (id INTEGER PRIMARY KEY, nom VARCHAR(100));
```

---

## ⚙️ **MPD (Modèle Physique de Données)**

### **Optimisations Physiques**

#### **1. Indexation**
```sql
-- Index sur les clés étrangères
CREATE INDEX idx_contenus_source_id ON contenus(source_id);
CREATE INDEX idx_reactions_contenu_id ON reactions(contenu_id);

-- Index sur les colonnes de recherche
CREATE INDEX idx_contenus_sentiment ON contenus(sentiment);
CREATE INDEX idx_contenus_created_at ON contenus(created_at);
```

#### **2. Contraintes d'Intégrité**
```sql
-- Contraintes de clés étrangères
ALTER TABLE contenus ADD CONSTRAINT fk_contenus_source 
    FOREIGN KEY (source_id) REFERENCES sources(id);

ALTER TABLE reactions ADD CONSTRAINT fk_reactions_contenu 
    FOREIGN KEY (contenu_id) REFERENCES contenus(id);
```

#### **3. Optimisations de Performance**
- **Partitionnement** : Par date pour les grandes tables
- **Compression** : Compression des données textuelles
- **Cache** : Mise en cache des requêtes fréquentes
- **VACUUM** : Maintenance automatique de la base

---

## 🎯 **CONCLUSION BLOC 1**

**Semantic Pulse X** respecte parfaitement les exigences du Bloc 1 :

- ✅ **5 sources distinctes** + base agrégée MERISE
- ✅ **Métadonnées complètes** et documentées
- ✅ **RGPD et IA responsable** respectés
- ✅ **Traitement des données** robuste
- ✅ **Méthode MERISE** complète (MCD/MLD/MPD)

**Prêt pour la certification E1/E2/E3 !** ✅

---

*Livrables Bloc 1 - Janvier 2025*
