#!/usr/bin/env python3
"""
Graphe Social des Émotions - Semantic Pulse X
Système de clustering thématique et mapping des relations émotionnelles
"""

import numpy as np
import pandas as pd
import networkx as nx
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime
import json
from collections import defaultdict, Counter
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SocialEmotionGraph:
    """
    Système de graphe social des émotions avec clustering thématique.
    
    Fonctionnalités :
    - Clustering des émotions par thèmes
    - Mapping des relations entre émotions
    - Analyse des communautés émotionnelles
    - Détection des influences émotionnelles
    """
    
    def __init__(self):
        self.graph = nx.Graph()
        self.emotion_clusters = {}
        self.theme_mapping = {}
        self.emotion_embeddings = {}
        self.influence_matrix = None
        self.community_structure = {}
        
        logger.info("🔗 Graphe Social des Émotions initialisé")
    
    def add_emotion_data(self, emotion_data: List[Dict]) -> None:
        """
        Ajoute des données émotionnelles au graphe.
        
        Args:
            emotion_data: Liste de dictionnaires contenant les données émotionnelles
        """
        logger.info(f"📊 Ajout de {len(emotion_data)} éléments émotionnels")
        
        for item in emotion_data:
            emotion = item.get('emotion', 'unknown')
            content = item.get('content', '')
            theme = item.get('theme', 'general')
            timestamp = item.get('timestamp', datetime.now().isoformat())
            source = item.get('source', 'unknown')
            
            # Ajouter le nœud émotion
            if not self.graph.has_node(emotion):
                self.graph.add_node(emotion, 
                                  emotion_type=emotion,
                                  frequency=0,
                                  themes=set(),
                                  sources=set())
            
            # Mettre à jour les attributs du nœud
            node_data = self.graph.nodes[emotion]
            node_data['frequency'] += 1
            node_data['themes'].add(theme)
            node_data['sources'].add(source)
            
            # Ajouter les relations avec les thèmes
            if not self.graph.has_node(theme):
                self.graph.add_node(theme, 
                                  node_type='theme',
                                  emotions=set(),
                                  frequency=0)
            
            theme_data = self.graph.nodes[theme]
            theme_data['emotions'].add(emotion)
            theme_data['frequency'] += 1
            
            # Créer une arête entre émotion et thème
            if not self.graph.has_edge(emotion, theme):
                self.graph.add_edge(emotion, theme, 
                                  weight=0,
                                  interactions=[])
            
            edge_data = self.graph.edges[emotion, theme]
            edge_data['weight'] += 1
            edge_data['interactions'].append({
                'timestamp': timestamp,
                'content': content[:100],  # Limiter la taille
                'source': source
            })
        
        logger.info(f"✅ Graphe mis à jour: {self.graph.number_of_nodes()} nœuds, {self.graph.number_of_edges()} arêtes")
    
    def perform_emotion_clustering(self, n_clusters: int = 5) -> Dict:
        """
        Effectue le clustering des émotions par similarité sémantique.
        
        Args:
            n_clusters: Nombre de clusters souhaités
            
        Returns:
            Dictionnaire contenant les clusters et leurs métriques
        """
        logger.info(f"🔍 Clustering des émotions en {n_clusters} groupes")
        
        # Extraire les émotions et leurs embeddings
        emotions = list(self.graph.nodes())
        emotion_nodes = [node for node in emotions if self.graph.nodes[node].get('emotion_type')]
        
        if len(emotion_nodes) < n_clusters:
            logger.warning(f"⚠️ Pas assez d'émotions pour {n_clusters} clusters")
            n_clusters = len(emotion_nodes)
        
        # Créer une matrice de similarité basée sur les thèmes partagés
        similarity_matrix = np.zeros((len(emotion_nodes), len(emotion_nodes)))
        
        for i, emotion1 in enumerate(emotion_nodes):
            for j, emotion2 in enumerate(emotion_nodes):
                if i != j:
                    # Calculer la similarité basée sur les thèmes partagés
                    themes1 = self.graph.nodes[emotion1].get('themes', set())
                    themes2 = self.graph.nodes[emotion2].get('themes', set())
                    
                    if themes1 and themes2:
                        intersection = len(themes1.intersection(themes2))
                        union = len(themes1.union(themes2))
                        similarity = intersection / union if union > 0 else 0
                        similarity_matrix[i][j] = similarity
        
        # Clustering avec KMeans
        if n_clusters > 1:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(similarity_matrix)
        else:
            cluster_labels = [0] * len(emotion_nodes)
        
        # Organiser les résultats
        clusters = defaultdict(list)
        for emotion, label in zip(emotion_nodes, cluster_labels):
            clusters[f"cluster_{label}"].append(emotion)
        
        # Calculer les métriques des clusters
        cluster_metrics = {}
        for cluster_name, emotions in clusters.items():
            cluster_metrics[cluster_name] = {
                'size': len(emotions),
                'emotions': emotions,
                'avg_frequency': np.mean([self.graph.nodes[e]['frequency'] for e in emotions]),
                'themes': set()
            }
            
            # Collecter tous les thèmes du cluster
            for emotion in emotions:
                cluster_metrics[cluster_name]['themes'].update(
                    self.graph.nodes[emotion].get('themes', set())
                )
        
        self.emotion_clusters = dict(clusters)
        
        logger.info(f"✅ Clustering terminé: {len(clusters)} clusters créés")
        for cluster_name, metrics in cluster_metrics.items():
            logger.info(f"   {cluster_name}: {metrics['size']} émotions, {len(metrics['themes'])} thèmes")
        
        return cluster_metrics
    
    def detect_emotion_communities(self) -> Dict:
        """
        Détecte les communautés d'émotions dans le graphe.
        
        Returns:
            Dictionnaire des communautés détectées
        """
        logger.info("🔍 Détection des communautés émotionnelles")
        
        # Utiliser l'algorithme de détection de communautés de NetworkX
        try:
            communities = nx.community.greedy_modularity_communities(self.graph)
        except:
            # Fallback si l'algorithme échoue
            communities = [list(self.graph.nodes())]
        
        community_structure = {}
        for i, community in enumerate(communities):
            community_name = f"community_{i}"
            community_structure[community_name] = {
                'nodes': list(community),
                'size': len(community),
                'emotions': [node for node in community if self.graph.nodes[node].get('emotion_type')],
                'themes': [node for node in community if self.graph.nodes[node].get('node_type') == 'theme']
            }
        
        self.community_structure = community_structure
        
        logger.info(f"✅ {len(communities)} communautés détectées")
        for name, structure in community_structure.items():
            logger.info(f"   {name}: {structure['size']} nœuds ({len(structure['emotions'])} émotions, {len(structure['themes'])} thèmes)")
        
        return community_structure
    
    def analyze_emotion_influence(self) -> Dict:
        """
        Analyse l'influence entre les émotions.
        
        Returns:
            Dictionnaire des influences émotionnelles
        """
        logger.info("📊 Analyse des influences émotionnelles")
        
        # Calculer la matrice d'influence basée sur les poids des arêtes
        emotion_nodes = [node for node in self.graph.nodes() 
                        if self.graph.nodes[node].get('emotion_type')]
        
        influence_matrix = np.zeros((len(emotion_nodes), len(emotion_nodes)))
        influence_dict = {}
        
        for i, emotion1 in enumerate(emotion_nodes):
            for j, emotion2 in enumerate(emotion_nodes):
                if i != j:
                    # Calculer l'influence basée sur les thèmes partagés
                    themes1 = self.graph.nodes[emotion1].get('themes', set())
                    themes2 = self.graph.nodes[emotion2].get('themes', set())
                    
                    if themes1 and themes2:
                        shared_themes = themes1.intersection(themes2)
                        influence = len(shared_themes) / len(themes1) if themes1 else 0
                        influence_matrix[i][j] = influence
                        
                        if influence > 0:
                            influence_dict[f"{emotion1}_to_{emotion2}"] = {
                                'influence_score': influence,
                                'shared_themes': list(shared_themes),
                                'source_frequency': self.graph.nodes[emotion1]['frequency'],
                                'target_frequency': self.graph.nodes[emotion2]['frequency']
                            }
        
        self.influence_matrix = influence_matrix
        
        # Identifier les émotions les plus influentes
        influence_scores = np.sum(influence_matrix, axis=1)
        most_influential = []
        
        for i, score in enumerate(influence_scores):
            if score > 0:
                most_influential.append({
                    'emotion': emotion_nodes[i],
                    'influence_score': score,
                    'frequency': self.graph.nodes[emotion_nodes[i]]['frequency']
                })
        
        most_influential.sort(key=lambda x: x['influence_score'], reverse=True)
        
        logger.info(f"✅ Analyse terminée: {len(influence_dict)} relations d'influence")
        logger.info("🏆 Top 3 émotions les plus influentes:")
        for i, emotion_data in enumerate(most_influential[:3]):
            logger.info(f"   {i+1}. {emotion_data['emotion']}: score {emotion_data['influence_score']:.3f}")
        
        return {
            'influence_matrix': influence_matrix.tolist(),
            'influence_relations': influence_dict,
            'most_influential': most_influential[:10],
            'emotion_nodes': emotion_nodes
        }
    
    def generate_theme_mapping(self) -> Dict:
        """
        Génère le mapping des thèmes vers les émotions.
        
        Returns:
            Dictionnaire du mapping thème-émotions
        """
        logger.info("🗺️ Génération du mapping thème-émotions")
        
        theme_mapping = {}
        
        for node in self.graph.nodes():
            if self.graph.nodes[node].get('node_type') == 'theme':
                emotions = self.graph.nodes[node].get('emotions', set())
                theme_mapping[node] = {
                    'emotions': list(emotions),
                    'emotion_count': len(emotions),
                    'frequency': self.graph.nodes[node]['frequency'],
                    'emotion_distribution': {}
                }
                
                # Calculer la distribution des émotions pour ce thème
                for emotion in emotions:
                    emotion_freq = self.graph.nodes[emotion]['frequency']
                    theme_mapping[node]['emotion_distribution'][emotion] = emotion_freq
        
        self.theme_mapping = theme_mapping
        
        logger.info(f"✅ Mapping généré pour {len(theme_mapping)} thèmes")
        for theme, data in theme_mapping.items():
            logger.info(f"   {theme}: {data['emotion_count']} émotions, fréquence {data['frequency']}")
        
        return theme_mapping
    
    def visualize_graph(self, output_path: str = "data/processed/social_emotion_graph.png") -> None:
        """
        Visualise le graphe social des émotions.
        
        Args:
            output_path: Chemin de sauvegarde de la visualisation
        """
        logger.info("📊 Génération de la visualisation du graphe")
        
        plt.figure(figsize=(15, 10))
        
        # Positionner les nœuds
        pos = nx.spring_layout(self.graph, k=3, iterations=50)
        
        # Séparer les nœuds par type
        emotion_nodes = [node for node in self.graph.nodes() 
                        if self.graph.nodes[node].get('emotion_type')]
        theme_nodes = [node for node in self.graph.nodes() 
                      if self.graph.nodes[node].get('node_type') == 'theme']
        
        # Dessiner le graphe
        nx.draw_networkx_nodes(self.graph, pos, 
                              nodelist=emotion_nodes,
                              node_color='lightblue',
                              node_size=500,
                              alpha=0.7,
                              label='Émotions')
        
        nx.draw_networkx_nodes(self.graph, pos,
                              nodelist=theme_nodes,
                              node_color='lightcoral',
                              node_size=300,
                              alpha=0.7,
                              label='Thèmes')
        
        # Dessiner les arêtes
        nx.draw_networkx_edges(self.graph, pos,
                              edge_color='gray',
                              alpha=0.5,
                              width=1)
        
        # Ajouter les labels
        nx.draw_networkx_labels(self.graph, pos,
                               font_size=8,
                               font_weight='bold')
        
        plt.title("Graphe Social des Émotions - Semantic Pulse X", fontsize=16, fontweight='bold')
        plt.legend()
        plt.axis('off')
        
        # Sauvegarder
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"✅ Visualisation sauvegardée: {output_path}")
    
    def export_graph_data(self, output_path: str = "data/processed/social_graph_data.json") -> Dict:
        """
        Exporte les données du graphe social.
        
        Args:
            output_path: Chemin de sauvegarde des données
            
        Returns:
            Dictionnaire contenant toutes les données du graphe
        """
        logger.info("💾 Export des données du graphe social")
        
        graph_data = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_nodes': self.graph.number_of_nodes(),
                'total_edges': self.graph.number_of_edges(),
                'emotion_nodes': len([n for n in self.graph.nodes() if self.graph.nodes[n].get('emotion_type')]),
                'theme_nodes': len([n for n in self.graph.nodes() if self.graph.nodes[n].get('node_type') == 'theme'])
            },
            'nodes': dict(self.graph.nodes(data=True)),
            'edges': list(self.graph.edges(data=True)),
            'emotion_clusters': self.emotion_clusters,
            'community_structure': self.community_structure,
            'theme_mapping': self.theme_mapping,
            'influence_analysis': self.analyze_emotion_influence() if self.influence_matrix is None else {
                'influence_matrix': self.influence_matrix.tolist(),
                'most_influential': []
            }
        }
        
        # Convertir les sets en listes pour la sérialisation JSON
        for node_data in graph_data['nodes'].values():
            if 'themes' in node_data:
                node_data['themes'] = list(node_data['themes'])
            if 'sources' in node_data:
                node_data['sources'] = list(node_data['sources'])
            if 'emotions' in node_data:
                node_data['emotions'] = list(node_data['emotions'])
        
        # Sauvegarder
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ Données exportées: {output_path}")
        return graph_data
    
    def get_graph_statistics(self) -> Dict:
        """
        Calcule les statistiques du graphe social.
        
        Returns:
            Dictionnaire des statistiques
        """
        logger.info("📊 Calcul des statistiques du graphe")
        
        emotion_nodes = [n for n in self.graph.nodes() if self.graph.nodes[n].get('emotion_type')]
        theme_nodes = [n for n in self.graph.nodes() if self.graph.nodes[n].get('node_type') == 'theme']
        
        stats = {
            'basic_metrics': {
                'total_nodes': self.graph.number_of_nodes(),
                'total_edges': self.graph.number_of_edges(),
                'emotion_nodes': len(emotion_nodes),
                'theme_nodes': len(theme_nodes),
                'density': nx.density(self.graph),
                'average_clustering': nx.average_clustering(self.graph)
            },
            'centrality_measures': {},
            'community_metrics': {},
            'clustering_metrics': {}
        }
        
        if len(emotion_nodes) > 0:
            # Mesures de centralité
            degree_centrality = nx.degree_centrality(self.graph)
            betweenness_centrality = nx.betweenness_centrality(self.graph)
            
            stats['centrality_measures'] = {
                'top_degree_centrality': sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5],
                'top_betweenness_centrality': sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
            }
        
        # Métriques des communautés
        if self.community_structure:
            stats['community_metrics'] = {
                'total_communities': len(self.community_structure),
                'community_sizes': [structure['size'] for structure in self.community_structure.values()],
                'average_community_size': np.mean([structure['size'] for structure in self.community_structure.values()])
            }
        
        # Métriques de clustering
        if self.emotion_clusters:
            stats['clustering_metrics'] = {
                'total_clusters': len(self.emotion_clusters),
                'cluster_sizes': [len(emotions) for emotions in self.emotion_clusters.values()],
                'average_cluster_size': np.mean([len(emotions) for emotions in self.emotion_clusters.values()])
            }
        
        logger.info("✅ Statistiques calculées")
        logger.info(f"   📊 Densité: {stats['basic_metrics']['density']:.3f}")
        logger.info(f"   🔗 Clustering moyen: {stats['basic_metrics']['average_clustering']:.3f}")
        
        return stats

def create_sample_emotion_data() -> List[Dict]:
    """
    Crée des données émotionnelles d'exemple pour les tests.
    
    Returns:
        Liste de données émotionnelles d'exemple
    """
    sample_data = [
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
    
    return sample_data

if __name__ == "__main__":
    # Test du système de graphe social
    logger.info("🚀 TEST DU GRAPHE SOCIAL DES ÉMOTIONS")
    logger.info("=" * 60)
    
    # Créer le graphe
    social_graph = SocialEmotionGraph()
    
    # Ajouter des données d'exemple
    sample_data = create_sample_emotion_data()
    social_graph.add_emotion_data(sample_data)
    
    # Effectuer le clustering
    cluster_metrics = social_graph.perform_emotion_clustering(n_clusters=3)
    
    # Détecter les communautés
    communities = social_graph.detect_emotion_communities()
    
    # Analyser les influences
    influence_analysis = social_graph.analyze_emotion_influence()
    
    # Générer le mapping des thèmes
    theme_mapping = social_graph.generate_theme_mapping()
    
    # Calculer les statistiques
    stats = social_graph.get_graph_statistics()
    
    # Visualiser le graphe
    social_graph.visualize_graph()
    
    # Exporter les données
    graph_data = social_graph.export_graph_data()
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ TEST TERMINÉ AVEC SUCCÈS")
    logger.info("=" * 60)
    logger.info(f"📊 Graphe créé: {social_graph.graph.number_of_nodes()} nœuds, {social_graph.graph.number_of_edges()} arêtes")
    logger.info(f"🔍 Clusters: {len(cluster_metrics)}")
    logger.info(f"👥 Communautés: {len(communities)}")
    logger.info(f"📈 Relations d'influence: {len(influence_analysis['influence_relations'])}")
    logger.info(f"🗺️ Thèmes mappés: {len(theme_mapping)}")
    logger.info("=" * 60)




