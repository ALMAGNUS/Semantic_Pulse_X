#!/usr/bin/env python3
"""
Test du Graphe Social des Émotions - Semantic Pulse X
Démontre le clustering thématique et l'analyse des relations émotionnelles
"""

import os
import sys
import logging
import json
from datetime import datetime

# Ajouter le chemin du projet
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.backend.ai.social_graph import SocialEmotionGraph, create_sample_emotion_data

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_social_graph_basic():
    """Test basique du graphe social des émotions."""
    logger.info("🧪 TEST BASIQUE - GRAPHE SOCIAL DES ÉMOTIONS")
    logger.info("=" * 60)
    
    # Créer le graphe
    social_graph = SocialEmotionGraph()
    
    # Ajouter des données d'exemple
    sample_data = create_sample_emotion_data()
    logger.info(f"📊 Ajout de {len(sample_data)} éléments émotionnels d'exemple")
    
    social_graph.add_emotion_data(sample_data)
    
    # Vérifier la structure du graphe
    logger.info(f"✅ Graphe créé: {social_graph.graph.number_of_nodes()} nœuds, {social_graph.graph.number_of_edges()} arêtes")
    
    return social_graph

def test_emotion_clustering(social_graph):
    """Test du clustering des émotions."""
    logger.info("\n🔍 TEST CLUSTERING DES ÉMOTIONS")
    logger.info("-" * 40)
    
    # Effectuer le clustering
    cluster_metrics = social_graph.perform_emotion_clustering(n_clusters=3)
    
    logger.info("📊 Résultats du clustering:")
    for cluster_name, metrics in cluster_metrics.items():
        logger.info(f"   {cluster_name}:")
        logger.info(f"      📈 Taille: {metrics['size']} émotions")
        logger.info(f"      😊 Émotions: {', '.join(metrics['emotions'])}")
        logger.info(f"      🎯 Thèmes: {', '.join(metrics['themes'])}")
        logger.info(f"      📊 Fréquence moyenne: {metrics['avg_frequency']:.2f}")
    
    return cluster_metrics

def test_community_detection(social_graph):
    """Test de la détection de communautés."""
    logger.info("\n👥 TEST DÉTECTION DE COMMUNAUTÉS")
    logger.info("-" * 40)
    
    # Détecter les communautés
    communities = social_graph.detect_emotion_communities()
    
    logger.info("📊 Communautés détectées:")
    for community_name, structure in communities.items():
        logger.info(f"   {community_name}:")
        logger.info(f"      📈 Taille: {structure['size']} nœuds")
        logger.info(f"      😊 Émotions: {', '.join(structure['emotions'])}")
        logger.info(f"      🎯 Thèmes: {', '.join(structure['themes'])}")
    
    return communities

def test_influence_analysis(social_graph):
    """Test de l'analyse des influences."""
    logger.info("\n📈 TEST ANALYSE DES INFLUENCES")
    logger.info("-" * 40)
    
    # Analyser les influences
    influence_analysis = social_graph.analyze_emotion_influence()
    
    logger.info("📊 Relations d'influence détectées:")
    for relation, data in influence_analysis['influence_relations'].items():
        logger.info(f"   {relation}:")
        logger.info(f"      📊 Score: {data['influence_score']:.3f}")
        logger.info(f"      🎯 Thèmes partagés: {', '.join(data['shared_themes'])}")
    
    logger.info("\n🏆 Top 3 émotions les plus influentes:")
    for i, emotion_data in enumerate(influence_analysis['most_influential'][:3]):
        logger.info(f"   {i+1}. {emotion_data['emotion']}: score {emotion_data['influence_score']:.3f}")
    
    return influence_analysis

def test_theme_mapping(social_graph):
    """Test du mapping des thèmes."""
    logger.info("\n🗺️ TEST MAPPING DES THÈMES")
    logger.info("-" * 40)
    
    # Générer le mapping des thèmes
    theme_mapping = social_graph.generate_theme_mapping()
    
    logger.info("📊 Mapping thème-émotions:")
    for theme, data in theme_mapping.items():
        logger.info(f"   {theme}:")
        logger.info(f"      📈 {data['emotion_count']} émotions")
        logger.info(f"      😊 Émotions: {', '.join(data['emotions'])}")
        logger.info(f"      📊 Fréquence: {data['frequency']}")
        
        # Afficher la distribution des émotions
        logger.info(f"      📈 Distribution:")
        for emotion, freq in data['emotion_distribution'].items():
            logger.info(f"         {emotion}: {freq}")
    
    return theme_mapping

def test_graph_statistics(social_graph):
    """Test des statistiques du graphe."""
    logger.info("\n📊 TEST STATISTIQUES DU GRAPHE")
    logger.info("-" * 40)
    
    # Calculer les statistiques
    stats = social_graph.get_graph_statistics()
    
    logger.info("📊 Métriques de base:")
    for metric, value in stats['basic_metrics'].items():
        logger.info(f"   {metric}: {value}")
    
    if stats['centrality_measures']:
        logger.info("\n📈 Mesures de centralité:")
        logger.info("   Top centralité de degré:")
        for node, centrality in stats['centrality_measures']['top_degree_centrality']:
            logger.info(f"      {node}: {centrality:.3f}")
    
    if stats['community_metrics']:
        logger.info("\n👥 Métriques des communautés:")
        for metric, value in stats['community_metrics'].items():
            logger.info(f"   {metric}: {value}")
    
    if stats['clustering_metrics']:
        logger.info("\n🔍 Métriques de clustering:")
        for metric, value in stats['clustering_metrics'].items():
            logger.info(f"   {metric}: {value}")
    
    return stats

def test_visualization_and_export(social_graph):
    """Test de la visualisation et de l'export."""
    logger.info("\n📊 TEST VISUALISATION ET EXPORT")
    logger.info("-" * 40)
    
    # Créer le répertoire de sortie
    os.makedirs("data/processed", exist_ok=True)
    
    # Visualiser le graphe
    output_path = "data/processed/social_emotion_graph_test.png"
    social_graph.visualize_graph(output_path)
    logger.info(f"✅ Visualisation créée: {output_path}")
    
    # Exporter les données
    export_path = "data/processed/social_graph_test_data.json"
    graph_data = social_graph.export_graph_data(export_path)
    logger.info(f"✅ Données exportées: {export_path}")
    
    # Vérifier les fichiers créés
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path) / (1024 * 1024)
        logger.info(f"📊 Taille de l'image: {file_size:.3f} MB")
    
    if os.path.exists(export_path):
        file_size = os.path.getsize(export_path) / (1024 * 1024)
        logger.info(f"📊 Taille du JSON: {file_size:.3f} MB")
    
    return graph_data

def generate_test_report(social_graph, cluster_metrics, communities, influence_analysis, theme_mapping, stats):
    """Génère un rapport de test complet."""
    logger.info("\n📋 GÉNÉRATION DU RAPPORT DE TEST")
    logger.info("-" * 40)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "test_name": "Graphe Social des Émotions",
        "status": "SUCCESS",
        "summary": {
            "total_nodes": social_graph.graph.number_of_nodes(),
            "total_edges": social_graph.graph.number_of_edges(),
            "clusters_created": len(cluster_metrics),
            "communities_detected": len(communities),
            "influence_relations": len(influence_analysis['influence_relations']),
            "themes_mapped": len(theme_mapping)
        },
        "detailed_results": {
            "cluster_metrics": cluster_metrics,
            "community_structure": communities,
            "influence_analysis": influence_analysis,
            "theme_mapping": theme_mapping,
            "graph_statistics": stats
        }
    }
    
    # Sauvegarder le rapport
    report_path = "data/processed/social_graph_test_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    logger.info(f"✅ Rapport sauvegardé: {report_path}")
    return report

def main():
    """Fonction principale de test."""
    logger.info("🚀 TEST COMPLET - GRAPHE SOCIAL DES ÉMOTIONS")
    logger.info("=" * 80)
    logger.info("🔍 Clustering thématique des émotions")
    logger.info("👥 Détection de communautés émotionnelles")
    logger.info("📈 Analyse des influences entre émotions")
    logger.info("🗺️ Mapping thème-émotions")
    logger.info("📊 Visualisation et export des données")
    logger.info("=" * 80)
    
    try:
        # Test 1: Création du graphe
        social_graph = test_social_graph_basic()
        
        # Test 2: Clustering des émotions
        cluster_metrics = test_emotion_clustering(social_graph)
        
        # Test 3: Détection de communautés
        communities = test_community_detection(social_graph)
        
        # Test 4: Analyse des influences
        influence_analysis = test_influence_analysis(social_graph)
        
        # Test 5: Mapping des thèmes
        theme_mapping = test_theme_mapping(social_graph)
        
        # Test 6: Statistiques du graphe
        stats = test_graph_statistics(social_graph)
        
        # Test 7: Visualisation et export
        graph_data = test_visualization_and_export(social_graph)
        
        # Générer le rapport final
        report = generate_test_report(social_graph, cluster_metrics, communities, 
                                    influence_analysis, theme_mapping, stats)
        
        # Résumé final
        logger.info("\n" + "=" * 80)
        logger.info("🎉 TOUS LES TESTS RÉUSSIS!")
        logger.info("=" * 80)
        logger.info("✅ Graphe social des émotions opérationnel")
        logger.info("✅ Clustering thématique fonctionnel")
        logger.info("✅ Détection de communautés réussie")
        logger.info("✅ Analyse des influences complète")
        logger.info("✅ Mapping thème-émotions généré")
        logger.info("✅ Visualisation et export réussis")
        logger.info("=" * 80)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors des tests: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)




