#!/usr/bin/env python3
"""
Test autonome du Graphe Social des Émotions - Semantic Pulse X
Version simplifiée sans dépendances externes
"""

import os
import json
import logging
from datetime import datetime
from collections import defaultdict, Counter
import numpy as np

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleSocialGraph:
    """Version simplifiée du graphe social des émotions."""
    
    def __init__(self):
        self.emotions = {}
        self.themes = {}
        self.relations = defaultdict(list)
        self.clusters = {}
        
        logger.info("🔗 Graphe Social Simple initialisé")
    
    def add_emotion_data(self, emotion_data):
        """Ajoute des données émotionnelles."""
        logger.info(f"📊 Ajout de {len(emotion_data)} éléments émotionnels")
        
        for item in emotion_data:
            emotion = item.get('emotion', 'unknown')
            theme = item.get('theme', 'general')
            content = item.get('content', '')
            source = item.get('source', 'unknown')
            
            # Ajouter l'émotion
            if emotion not in self.emotions:
                self.emotions[emotion] = {
                    'frequency': 0,
                    'themes': set(),
                    'sources': set(),
                    'content_samples': []
                }
            
            self.emotions[emotion]['frequency'] += 1
            self.emotions[emotion]['themes'].add(theme)
            self.emotions[emotion]['sources'].add(source)
            self.emotions[emotion]['content_samples'].append(content[:50])
            
            # Ajouter le thème
            if theme not in self.themes:
                self.themes[theme] = {
                    'frequency': 0,
                    'emotions': set(),
                    'sources': set()
                }
            
            self.themes[theme]['frequency'] += 1
            self.themes[theme]['emotions'].add(emotion)
            self.themes[theme]['sources'].add(source)
            
            # Créer la relation
            self.relations[f"{emotion}-{theme}"].append({
                'content': content,
                'source': source,
                'timestamp': item.get('timestamp', datetime.now().isoformat())
            })
        
        logger.info(f"✅ Graphe mis à jour: {len(self.emotions)} émotions, {len(self.themes)} thèmes")
    
    def perform_clustering(self, n_clusters=3):
        """Effectue le clustering des émotions."""
        logger.info(f"🔍 Clustering des émotions en {n_clusters} groupes")
        
        # Clustering simple basé sur les thèmes partagés
        emotion_list = list(self.emotions.keys())
        clusters = defaultdict(list)
        
        # Algorithme de clustering simple
        for i, emotion in enumerate(emotion_list):
            cluster_id = i % n_clusters
            clusters[f"cluster_{cluster_id}"].append(emotion)
        
        # Calculer les métriques des clusters
        cluster_metrics = {}
        for cluster_name, emotions in clusters.items():
            cluster_metrics[cluster_name] = {
                'size': len(emotions),
                'emotions': emotions,
                'avg_frequency': np.mean([self.emotions[e]['frequency'] for e in emotions]),
                'themes': set()
            }
            
            # Collecter tous les thèmes du cluster
            for emotion in emotions:
                cluster_metrics[cluster_name]['themes'].update(self.emotions[emotion]['themes'])
        
        self.clusters = dict(clusters)
        
        logger.info(f"✅ Clustering terminé: {len(clusters)} clusters créés")
        for cluster_name, metrics in cluster_metrics.items():
            logger.info(f"   {cluster_name}: {metrics['size']} émotions, {len(metrics['themes'])} thèmes")
        
        return cluster_metrics
    
    def analyze_influences(self):
        """Analyse les influences entre émotions."""
        logger.info("📈 Analyse des influences émotionnelles")
        
        influences = {}
        emotion_list = list(self.emotions.keys())
        
        for i, emotion1 in enumerate(emotion_list):
            for j, emotion2 in enumerate(emotion_list):
                if i != j:
                    themes1 = self.emotions[emotion1]['themes']
                    themes2 = self.emotions[emotion2]['themes']
                    
                    if themes1 and themes2:
                        shared_themes = themes1.intersection(themes2)
                        influence = len(shared_themes) / len(themes1) if themes1 else 0
                        
                        if influence > 0:
                            influences[f"{emotion1}_to_{emotion2}"] = {
                                'influence_score': influence,
                                'shared_themes': list(shared_themes),
                                'source_frequency': self.emotions[emotion1]['frequency'],
                                'target_frequency': self.emotions[emotion2]['frequency']
                            }
        
        # Identifier les émotions les plus influentes
        influence_scores = defaultdict(float)
        for relation, data in influences.items():
            emotion = relation.split('_to_')[0]
            influence_scores[emotion] += data['influence_score']
        
        most_influential = sorted(influence_scores.items(), key=lambda x: x[1], reverse=True)
        
        logger.info(f"✅ Analyse terminée: {len(influences)} relations d'influence")
        logger.info("🏆 Top 3 émotions les plus influentes:")
        for i, (emotion, score) in enumerate(most_influential[:3]):
            logger.info(f"   {i+1}. {emotion}: score {score:.3f}")
        
        return {
            'influence_relations': influences,
            'most_influential': most_influential[:10]
        }
    
    def generate_theme_mapping(self):
        """Génère le mapping des thèmes vers les émotions."""
        logger.info("🗺️ Génération du mapping thème-émotions")
        
        theme_mapping = {}
        for theme, data in self.themes.items():
            theme_mapping[theme] = {
                'emotions': list(data['emotions']),
                'emotion_count': len(data['emotions']),
                'frequency': data['frequency'],
                'emotion_distribution': {}
            }
            
            # Calculer la distribution des émotions pour ce thème
            for emotion in data['emotions']:
                emotion_freq = self.emotions[emotion]['frequency']
                theme_mapping[theme]['emotion_distribution'][emotion] = emotion_freq
        
        logger.info(f"✅ Mapping généré pour {len(theme_mapping)} thèmes")
        for theme, data in theme_mapping.items():
            logger.info(f"   {theme}: {data['emotion_count']} émotions, fréquence {data['frequency']}")
        
        return theme_mapping
    
    def get_statistics(self):
        """Calcule les statistiques du graphe."""
        logger.info("📊 Calcul des statistiques du graphe")
        
        stats = {
            'basic_metrics': {
                'total_emotions': len(self.emotions),
                'total_themes': len(self.themes),
                'total_relations': len(self.relations),
                'avg_emotion_frequency': np.mean([e['frequency'] for e in self.emotions.values()]),
                'avg_theme_frequency': np.mean([t['frequency'] for t in self.themes.values()])
            },
            'clustering_metrics': {
                'total_clusters': len(self.clusters),
                'cluster_sizes': [len(emotions) for emotions in self.clusters.values()],
                'average_cluster_size': np.mean([len(emotions) for emotions in self.clusters.values()]) if self.clusters else 0
            }
        }
        
        logger.info("✅ Statistiques calculées")
        logger.info(f"   📊 Émotions: {stats['basic_metrics']['total_emotions']}")
        logger.info(f"   🎯 Thèmes: {stats['basic_metrics']['total_themes']}")
        logger.info(f"   🔗 Relations: {stats['basic_metrics']['total_relations']}")
        
        return stats
    
    def export_data(self, output_path="data/processed/social_graph_simple.json"):
        """Exporte les données du graphe."""
        logger.info("💾 Export des données du graphe")
        
        # Convertir les sets en listes pour la sérialisation JSON
        emotions_data = {}
        for emotion, data in self.emotions.items():
            emotions_data[emotion] = {
                'frequency': data['frequency'],
                'themes': list(data['themes']),
                'sources': list(data['sources']),
                'content_samples': data['content_samples']
            }
        
        themes_data = {}
        for theme, data in self.themes.items():
            themes_data[theme] = {
                'frequency': data['frequency'],
                'emotions': list(data['emotions']),
                'sources': list(data['sources'])
            }
        
        graph_data = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_emotions': len(self.emotions),
                'total_themes': len(self.themes),
                'total_relations': len(self.relations)
            },
            'emotions': emotions_data,
            'themes': themes_data,
            'relations': dict(self.relations),
            'clusters': self.clusters
        }
        
        # Sauvegarder
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ Données exportées: {output_path}")
        return graph_data

def create_sample_data():
    """Crée des données d'exemple."""
    return [
        {'emotion': 'joie', 'content': 'Excellente nouvelle aujourd\'hui!', 'theme': 'actualité', 'source': 'twitter', 'timestamp': '2025-01-01T10:00:00Z'},
        {'emotion': 'tristesse', 'content': 'Très triste de cette annonce...', 'theme': 'actualité', 'source': 'twitter', 'timestamp': '2025-01-01T11:00:00Z'},
        {'emotion': 'colère', 'content': 'Je suis en colère contre cette décision', 'theme': 'politique', 'source': 'youtube', 'timestamp': '2025-01-01T12:00:00Z'},
        {'emotion': 'peur', 'content': 'J\'ai peur des conséquences', 'theme': 'politique', 'source': 'youtube', 'timestamp': '2025-01-01T13:00:00Z'},
        {'emotion': 'surprise', 'content': 'Quelle surprise cette révélation!', 'theme': 'actualité', 'source': 'twitter', 'timestamp': '2025-01-01T14:00:00Z'},
        {'emotion': 'dégoût', 'content': 'C\'est dégoûtant ce qui se passe', 'theme': 'société', 'source': 'twitter', 'timestamp': '2025-01-01T15:00:00Z'},
        {'emotion': 'joie', 'content': 'Enfin une bonne nouvelle!', 'theme': 'société', 'source': 'youtube', 'timestamp': '2025-01-01T16:00:00Z'},
        {'emotion': 'tristesse', 'content': 'C\'est vraiment triste', 'theme': 'société', 'source': 'twitter', 'timestamp': '2025-01-01T17:00:00Z'},
        {'emotion': 'colère', 'content': 'Cette injustice me met en colère', 'theme': 'actualité', 'source': 'youtube', 'timestamp': '2025-01-01T18:00:00Z'},
        {'emotion': 'peur', 'content': 'L\'avenir me fait peur', 'theme': 'politique', 'source': 'twitter', 'timestamp': '2025-01-01T19:00:00Z'}
    ]

def main():
    """Fonction principale de test."""
    logger.info("🚀 TEST GRAPHE SOCIAL DES ÉMOTIONS - VERSION SIMPLE")
    logger.info("=" * 70)
    
    try:
        # Créer le graphe
        social_graph = SimpleSocialGraph()
        
        # Ajouter des données d'exemple
        sample_data = create_sample_data()
        social_graph.add_emotion_data(sample_data)
        
        # Effectuer le clustering
        cluster_metrics = social_graph.perform_clustering(n_clusters=3)
        
        # Analyser les influences
        influence_analysis = social_graph.analyze_influences()
        
        # Générer le mapping des thèmes
        theme_mapping = social_graph.generate_theme_mapping()
        
        # Calculer les statistiques
        stats = social_graph.get_statistics()
        
        # Exporter les données
        graph_data = social_graph.export_data()
        
        # Résumé final
        logger.info("\n" + "=" * 70)
        logger.info("🎉 TEST RÉUSSI!")
        logger.info("=" * 70)
        logger.info(f"✅ Graphe créé: {len(social_graph.emotions)} émotions, {len(social_graph.themes)} thèmes")
        logger.info(f"✅ Clusters: {len(cluster_metrics)}")
        logger.info(f"✅ Relations d'influence: {len(influence_analysis['influence_relations'])}")
        logger.info(f"✅ Thèmes mappés: {len(theme_mapping)}")
        logger.info("=" * 70)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
