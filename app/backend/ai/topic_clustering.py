"""
Clustering thématique - Semantic Pulse X
Regroupement sémantique des sujets avec BERTopic
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from bertopic import BERTopic
from sklearn.cluster import HDBSCAN
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from collections import Counter

from app.backend.ai.embeddings import embedding_engine


class TopicClusteringEngine:
    """Moteur de clustering thématique"""
    
    def __init__(self):
        self.bertopic_model = None
        self.topics = {}
        self.topic_embeddings = {}
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialise le modèle BERTopic"""
        try:
            # Configuration HDBSCAN pour clustering
            hdbscan_model = HDBSCAN(
                min_cluster_size=5,
                min_samples=3,
                metric='euclidean',
                cluster_selection_method='eom'
            )
            
            # Modèle BERTopic
            self.bertopic_model = BERTopic(
                hdbscan_model=hdbscan_model,
                embedding_model=embedding_engine.model,
                verbose=True
            )
            
            print("✅ Modèle BERTopic initialisé")
        except Exception as e:
            print(f"❌ Erreur initialisation BERTopic: {e}")
            self.bertopic_model = None
    
    def fit_topics(self, texts: List[str]) -> Dict[str, Any]:
        """Entraîne le modèle sur les textes"""
        if not texts or not self.bertopic_model:
            return {"error": "Modèle non disponible"}
        
        try:
            # Nettoyer les textes
            cleaned_texts = [self._clean_text(text) for text in texts]
            cleaned_texts = [text for text in cleaned_texts if text]
            
            if not cleaned_texts:
                return {"error": "Aucun texte valide"}
            
            # Entraîner le modèle
            topics, probs = self.bertopic_model.fit_transform(cleaned_texts)
            
            # Analyser les résultats
            topic_info = self.bertopic_model.get_topic_info()
            
            # Créer le mapping des topics
            self.topics = {
                int(row['Topic']): {
                    'name': row['Name'],
                    'count': int(row['Count']),
                    'words': self._get_topic_words(int(row['Topic']))
                }
                for _, row in topic_info.iterrows()
            }
            
            return {
                "success": True,
                "num_topics": len(topic_info),
                "topics": self.topics,
                "topic_assignments": topics.tolist()
            }
            
        except Exception as e:
            print(f"❌ Erreur fit topics: {e}")
            return {"error": str(e)}
    
    def predict_topics(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Prédit les topics pour de nouveaux textes"""
        if not texts or not self.bertopic_model:
            return []
        
        try:
            # Nettoyer les textes
            cleaned_texts = [self._clean_text(text) for text in texts]
            cleaned_texts = [text for text in cleaned_texts if text]
            
            if not cleaned_texts:
                return []
            
            # Prédire les topics
            topics, probs = self.bertopic_model.transform(cleaned_texts)
            
            results = []
            for i, (topic, prob) in enumerate(zip(topics, probs)):
                topic_info = self.topics.get(topic, {
                    'name': f'Topic_{topic}',
                    'count': 0,
                    'words': []
                })
                
                results.append({
                    'text': texts[i],
                    'topic_id': int(topic),
                    'topic_name': topic_info['name'],
                    'confidence': float(prob[0]) if len(prob) > 0 else 0.0,
                    'topic_words': topic_info['words']
                })
            
            return results
            
        except Exception as e:
            print(f"❌ Erreur prédiction topics: {e}")
            return []
    
    def get_topic_evolution(self, texts_with_timestamps: List[Tuple[str, str]]) -> Dict[str, Any]:
        """Analyse l'évolution des topics dans le temps"""
        if not texts_with_timestamps:
            return {}
        
        try:
            # Séparer textes et timestamps
            texts = [item[0] for item in texts_with_timestamps]
            timestamps = [item[1] for item in texts_with_timestamps]
            
            # Prédire les topics
            topic_predictions = self.predict_topics(texts)
            
            # Grouper par timestamp
            from collections import defaultdict
            time_topics = defaultdict(list)
            
            for i, prediction in enumerate(topic_predictions):
                timestamp = timestamps[i]
                time_topics[timestamp].append(prediction)
            
            # Analyser l'évolution
            evolution = {}
            for timestamp, predictions in time_topics.items():
                topic_counts = Counter([p['topic_id'] for p in predictions])
                evolution[timestamp] = dict(topic_counts)
            
            return {
                "evolution": evolution,
                "top_topics": self._get_top_topics(evolution),
                "trending_topics": self._get_trending_topics(evolution)
            }
            
        except Exception as e:
            print(f"❌ Erreur évolution topics: {e}")
            return {}
    
    def find_similar_topics(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Trouve les topics similaires à une requête"""
        if not self.topics or not self.bertopic_model:
            return []
        
        try:
            # Encoder la requête
            query_embedding = embedding_engine.encode_text(query)
            
            # Calculer les similarités avec tous les topics
            similarities = []
            for topic_id, topic_info in self.topics.items():
                if topic_id == -1:  # Skip noise topic
                    continue
                
                # Obtenir les mots du topic
                topic_words = topic_info.get('words', [])
                if not topic_words:
                    continue
                
                # Créer une représentation du topic
                topic_text = ' '.join([word for word, _ in topic_words[:5]])
                topic_embedding = embedding_engine.encode_text(topic_text)
                
                # Calculer la similarité
                similarity = cosine_similarity(
                    query_embedding.reshape(1, -1),
                    topic_embedding.reshape(1, -1)
                )[0][0]
                
                similarities.append({
                    'topic_id': topic_id,
                    'topic_name': topic_info['name'],
                    'similarity': float(similarity),
                    'words': topic_words
                })
            
            # Trier par similarité
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            return similarities[:top_k]
            
        except Exception as e:
            print(f"❌ Erreur similarité topics: {e}")
            return []
    
    def _clean_text(self, text: str) -> str:
        """Nettoie un texte pour le clustering"""
        if not text:
            return ""
        
        import re
        # Supprimer les URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Supprimer les mentions
        text = re.sub(r'@\w+', '', text)
        
        # Supprimer les caractères spéciaux
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def _get_topic_words(self, topic_id: int) -> List[Tuple[str, float]]:
        """Récupère les mots d'un topic"""
        try:
            words = self.bertopic_model.get_topic(topic_id)
            return [(word, score) for word, score in words]
        except:
            return []
    
    def _get_top_topics(self, evolution: Dict[str, Dict[int, int]]) -> List[Dict[str, Any]]:
        """Identifie les topics les plus fréquents"""
        topic_totals = {}
        for timestamp, topics in evolution.items():
            for topic_id, count in topics.items():
                topic_totals[topic_id] = topic_totals.get(topic_id, 0) + count
        
        # Trier par fréquence
        sorted_topics = sorted(topic_totals.items(), key=lambda x: x[1], reverse=True)
        
        top_topics = []
        for topic_id, count in sorted_topics[:10]:
            topic_info = self.topics.get(topic_id, {})
            top_topics.append({
                'topic_id': topic_id,
                'topic_name': topic_info.get('name', f'Topic_{topic_id}'),
                'total_count': count,
                'words': topic_info.get('words', [])
            })
        
        return top_topics
    
    def _get_trending_topics(self, evolution: Dict[str, Dict[int, int]]) -> List[Dict[str, Any]]:
        """Identifie les topics en tendance"""
        if len(evolution) < 2:
            return []
        
        # Calculer la croissance des topics
        topic_growth = {}
        timestamps = sorted(evolution.keys())
        
        for topic_id in set().union(*evolution.values()):
            recent_count = evolution[timestamps[-1]].get(topic_id, 0)
            older_count = evolution[timestamps[0]].get(topic_id, 0)
            
            if older_count > 0:
                growth = (recent_count - older_count) / older_count
                topic_growth[topic_id] = growth
        
        # Trier par croissance
        trending = sorted(topic_growth.items(), key=lambda x: x[1], reverse=True)
        
        trending_topics = []
        for topic_id, growth in trending[:5]:
            topic_info = self.topics.get(topic_id, {})
            trending_topics.append({
                'topic_id': topic_id,
                'topic_name': topic_info.get('name', f'Topic_{topic_id}'),
                'growth_rate': growth,
                'words': topic_info.get('words', [])
            })
        
        return trending_topics


# Instance globale
topic_clustering = TopicClusteringEngine()
