# ☁️ Guide des Nuages de Mots - Semantic Pulse X

## 🎯 Vue d'ensemble

Les nuages de mots sont la **visualisation parfaite** pour représenter les vagues émotionnelles dans Semantic Pulse X. Ils permettent de :

- **Visualiser instantanément** les mots-clés dominants
- **Identifier les tendances** émotionnelles en temps réel
- **Comparer les émotions** de manière intuitive
- **Suivre l'évolution** temporelle des sujets

## 🚀 Fonctionnalités

### 1. **Nuage Principal** ☁️
- **Filtrage par émotion** - Visualisez les mots spécifiques à chaque émotion
- **Paramètres personnalisables** - Taille, couleur, nombre de mots
- **Statistiques en temps réel** - Fréquence, mots uniques, textes analysés

### 2. **Comparaison des Émotions** 📊
- **Nuages côte à côte** - Comparez les mots entre différentes émotions
- **Pourcentages de répartition** - Visualisez la dominance de chaque émotion
- **Top mots par émotion** - Identifiez les mots-clés spécifiques

### 3. **Évolution Temporelle** ⏰
- **Nuages par période** - Heure, jour, semaine
- **Chronologie des tendances** - Suivez l'évolution des sujets
- **Détection des changements** - Identifiez les nouveaux mots-clés

### 4. **Mots en Tendance** 📈
- **Analyse des tendances** - Détection des mots émergents
- **Scores de croissance** - Mesure de l'évolution des mots
- **Visualisation des pics** - Identification des moments clés

### 5. **Nuage Interactif** 🎯
- **Graphique Plotly** - Interaction avec les données
- **Zoom et filtrage** - Exploration détaillée
- **Statistiques avancées** - Métriques de richesse vocabulaire

## 🎛️ Interface Utilisateur

### **Onglet "☁️ Nuages de Mots"**
- **URL** : http://localhost:8501
- **Accès** : Onglet principal dans Streamlit

### **Contrôles Sidebar**
- **Sélection d'émotion** - Filtre par émotion spécifique
- **Paramètres du nuage** - Nombre de mots, dimensions
- **Fenêtre temporelle** - Heure, jour, semaine
- **Bouton de régénération** - Actualise les nuages

## 🔧 API REST

### **Endpoints disponibles**

#### **Génération de nuage**
```http
GET /api/v1/wordcloud/generate
?emotion=joie&max_words=100&width=800&height=400
```

#### **Comparaison d'émotions**
```http
GET /api/v1/wordcloud/emotions/comparison
?emotions=joie,colere,tristesse&max_words=50
```

#### **Évolution temporelle**
```http
GET /api/v1/wordcloud/temporal
?time_window=day&max_words=50
```

#### **Mots en tendance**
```http
GET /api/v1/wordcloud/trending
?time_periods=3&max_words=30
```

#### **Nuage interactif**
```http
GET /api/v1/wordcloud/interactive
?emotion=joie&max_words=50
```

#### **Statistiques**
```http
GET /api/v1/wordcloud/statistics
?emotion=joie
```

## 🎨 Personnalisation

### **Couleurs par émotion**
```python
emotion_colors = {
    'joie': '#FFD700',      # Or
    'colere': '#FF4500',    # Rouge-orange
    'tristesse': '#4169E1', # Bleu royal
    'peur': '#8B0000',      # Rouge foncé
    'surprise': '#FF69B4',  # Rose vif
    'amour': '#FF1493',     # Rose profond
    'neutre': '#808080',    # Gris
    'positif': '#32CD32',   # Vert lime
    'negatif': '#DC143C'    # Rouge cramoisi
}
```

### **Paramètres de génération**
- **max_words** : 10-500 mots
- **width** : 400-1200 pixels
- **height** : 300-800 pixels
- **temperature** : 0.0-1.0 (couleurs)

### **Filtres avancés**
- **Stop words** - Mots à exclure automatiquement
- **Longueur minimale** - Filtre les mots courts
- **Seuil de fréquence** - Élimine les mots rares

## 📊 Métriques et Statistiques

### **Métriques de base**
- **Total mots** - Nombre total de mots analysés
- **Mots uniques** - Vocabulaire distinct
- **Textes analysés** - Nombre de textes traités
- **Émotion dominante** - Émotion la plus fréquente

### **Métriques avancées**
- **Richesse vocabulaire** - Ratio mots uniques / total
- **Longueur moyenne** - Taille moyenne des mots
- **Score de tendance** - Évolution des mots dans le temps
- **Densité émotionnelle** - Concentration des émotions

## 🔄 Intégration avec l'IA

### **Ollama Integration**
- **Génération de descriptions** - IA pour décrire les nuages
- **Analyse des tendances** - Insights automatiques
- **Détection d'anomalies** - Mots inattendus

### **LangChain Integration**
- **Résumés intelligents** - Synthèse des patterns
- **Recommandations** - Actions suggérées
- **Alertes contextuelles** - Notifications pertinentes

## 🛠️ Configuration Technique

### **Dépendances**
```python
wordcloud==1.9.2
matplotlib==3.7.2
Pillow==10.0.0
plotly==5.17.0
```

### **Paramètres de performance**
- **Cache des nuages** - Évite la régénération
- **Traitement par lots** - Optimise les gros volumes
- **Compression d'images** - Réduit la taille des fichiers

### **Optimisations**
- **Stop words français** - Filtrage intelligent
- **Anonymisation** - Protection RGPD
- **Mise en cache** - Performance améliorée

## 📈 Cas d'usage

### **1. Analyse de sentiment**
- **Détection des mots-clés** émotionnels
- **Identification des sujets** sensibles
- **Surveillance des tendances** négatives

### **2. Veille médiatique**
- **Suivi des sujets** émergents
- **Comparaison temporelle** des discours
- **Détection des changements** de ton

### **3. Analyse de contenu**
- **Extraction de thématiques** dominantes
- **Identification des mots-clés** pertinents
- **Visualisation des patterns** linguistiques

### **4. Reporting**
- **Génération automatique** de rapports
- **Visualisations exportables** (PNG, SVG)
- **Métriques intégrées** dans les dashboards

## 🚀 Utilisation Avancée

### **Scripts personnalisés**
```python
from app.visualization.wordcloud_generator import wordcloud_generator

# Générer un nuage personnalisé
wordcloud_data = wordcloud_generator.generate_emotion_wordcloud(
    texts=texts,
    emotions=emotions,
    emotion_filter="joie",
    max_words=100,
    width=800,
    height=400
)
```

### **Intégration dans les workflows**
```python
# Dans un pipeline ETL
def process_emotion_data(data):
    # Classification des émotions
    emotions = emotion_classifier.classify_batch(data['texts'])
    
    # Génération des nuages
    wordclouds = wordcloud_generator.generate_temporal_wordclouds(
        data, time_window='day'
    )
    
    return wordclouds
```

## 🎯 Prochaines étapes

1. **Installer les dépendances** - `pip install -r requirements.txt`
2. **Démarrer l'application** - `docker-compose up -d`
3. **Accéder à l'interface** - http://localhost:8501
4. **Explorer les nuages** - Onglet "☁️ Nuages de Mots"

**Les nuages de mots sont maintenant parfaitement intégrés dans Semantic Pulse X !** ☁️✨

