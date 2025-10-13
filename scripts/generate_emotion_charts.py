#!/usr/bin/env python3
"""
Visualisation des Graphiques Émotionnels - Semantic Pulse X
Crée des graphiques pour analyser les données du graphe social des émotions
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from collections import Counter
import logging
import os

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration matplotlib pour le français
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (12, 8)

def load_graph_data(file_path="data/processed/social_graph_simple.json"):
    """Charge les données du graphe social."""
    logger.info(f"📊 Chargement des données: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"✅ Données chargées: {data['metadata']['total_emotions']} émotions, {data['metadata']['total_themes']} thèmes")
        return data
    except Exception as e:
        logger.error(f"❌ Erreur lors du chargement: {e}")
        return None

def create_emotion_frequency_chart(data):
    """Crée un graphique des fréquences des émotions."""
    logger.info("📊 Création du graphique des fréquences émotionnelles")
    
    emotions = data['emotions']
    emotion_names = list(emotions.keys())
    frequencies = [emotions[emotion]['frequency'] for emotion in emotion_names]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(emotion_names, frequencies, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'])
    
    # Ajouter les valeurs sur les barres
    for bar, freq in zip(bars, frequencies):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                str(freq), ha='center', va='bottom', fontweight='bold')
    
    plt.title('Fréquence des Émotions - Graphe Social', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Émotions', fontsize=12, fontweight='bold')
    plt.ylabel('Fréquence', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45)
    plt.grid(axis='y', alpha=0.3)
    
    # Sauvegarder
    output_path = "data/processed/emotion_frequency_chart.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"✅ Graphique sauvegardé: {output_path}")
    return output_path

def create_theme_emotion_matrix(data):
    """Crée une matrice de chaleur émotion-thème."""
    logger.info("🔥 Création de la matrice émotion-thème")
    
    emotions = list(data['emotions'].keys())
    themes = list(data['themes'].keys())
    
    # Créer la matrice
    matrix = np.zeros((len(emotions), len(themes)))
    
    for i, emotion in enumerate(emotions):
        for j, theme in enumerate(themes):
            if theme in data['emotions'][emotion]['themes']:
                matrix[i][j] = data['emotions'][emotion]['frequency']
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(matrix, 
                xticklabels=themes, 
                yticklabels=emotions,
                annot=True, 
                fmt='.0f',
                cmap='YlOrRd',
                cbar_kws={'label': 'Fréquence'})
    
    plt.title('Matrice Émotion-Thème - Relations', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Thèmes', fontsize=12, fontweight='bold')
    plt.ylabel('Émotions', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    
    # Sauvegarder
    output_path = "data/processed/emotion_theme_matrix.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"✅ Matrice sauvegardée: {output_path}")
    return output_path

def create_source_distribution_chart(data):
    """Crée un graphique de la distribution par source."""
    logger.info("📱 Création du graphique de distribution par source")
    
    # Compter les émotions par source
    source_counts = Counter()
    for emotion_data in data['emotions'].values():
        for source in emotion_data['sources']:
            source_counts[source] += emotion_data['frequency']
    
    sources = list(source_counts.keys())
    counts = list(source_counts.values())
    
    plt.figure(figsize=(8, 8))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    wedges, texts, autotexts = plt.pie(counts, labels=sources, autopct='%1.1f%%', 
                                      colors=colors[:len(sources)], startangle=90)
    
    # Améliorer l'apparence
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    plt.title('Distribution des Émotions par Source', fontsize=16, fontweight='bold', pad=20)
    
    # Sauvegarder
    output_path = "data/processed/source_distribution_chart.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"✅ Graphique circulaire sauvegardé: {output_path}")
    return output_path

def create_cluster_visualization(data):
    """Crée une visualisation des clusters d'émotions."""
    logger.info("🔍 Création de la visualisation des clusters")
    
    clusters = data['clusters']
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Couleurs pour chaque cluster
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    y_pos = 0
    for i, (cluster_name, emotions) in enumerate(clusters.items()):
        # Créer un rectangle pour chaque cluster
        rect = plt.Rectangle((0, y_pos), 10, 1, 
                           facecolor=colors[i % len(colors)], 
                           alpha=0.7, 
                           edgecolor='black',
                           linewidth=2)
        ax.add_patch(rect)
        
        # Ajouter le nom du cluster
        ax.text(5, y_pos + 0.5, cluster_name.replace('_', ' ').title(), 
               ha='center', va='center', fontweight='bold', fontsize=12)
        
        # Ajouter les émotions
        emotion_text = ', '.join(emotions)
        ax.text(5, y_pos + 0.2, emotion_text, 
               ha='center', va='center', fontsize=10)
        
        y_pos += 1.5
    
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.5, y_pos - 0.5)
    ax.set_title('Clusters d\'Émotions - Groupement Thématique', 
                fontsize=16, fontweight='bold', pad=20)
    ax.axis('off')
    
    # Sauvegarder
    output_path = "data/processed/cluster_visualization.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"✅ Visualisation des clusters sauvegardée: {output_path}")
    return output_path

def create_timeline_chart(data):
    """Crée un graphique temporel des émotions."""
    logger.info("⏰ Création du graphique temporel")
    
    # Extraire les données temporelles
    timeline_data = []
    for relation, interactions in data['relations'].items():
        emotion = relation.split('-')[0]
        for interaction in interactions:
            timeline_data.append({
                'emotion': emotion,
                'timestamp': interaction['timestamp'],
                'source': interaction['source']
            })
    
    # Convertir en DataFrame
    df = pd.DataFrame(timeline_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    
    # Compter les émotions par heure
    emotion_hourly = df.groupby(['hour', 'emotion']).size().unstack(fill_value=0)
    
    plt.figure(figsize=(14, 8))
    emotion_hourly.plot(kind='bar', stacked=True, 
                       color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'])
    
    plt.title('Évolution Temporelle des Émotions', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Heure de la Journée', fontsize=12, fontweight='bold')
    plt.ylabel('Nombre d\'Occurrences', fontsize=12, fontweight='bold')
    plt.legend(title='Émotions', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.grid(axis='y', alpha=0.3)
    
    # Sauvegarder
    output_path = "data/processed/timeline_chart.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"✅ Graphique temporel sauvegardé: {output_path}")
    return output_path

def create_comprehensive_dashboard(data):
    """Crée un tableau de bord complet avec tous les graphiques."""
    logger.info("📊 Création du tableau de bord complet")
    
    fig = plt.figure(figsize=(20, 16))
    
    # Configuration de la grille
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # 1. Fréquences des émotions (en haut à gauche)
    ax1 = fig.add_subplot(gs[0, 0])
    emotions = list(data['emotions'].keys())
    frequencies = [data['emotions'][emotion]['frequency'] for emotion in emotions]
    bars = ax1.bar(emotions, frequencies, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'])
    ax1.set_title('Fréquences des Émotions', fontweight='bold')
    ax1.set_ylabel('Fréquence')
    ax1.tick_params(axis='x', rotation=45)
    
    # 2. Distribution par source (en haut au centre)
    ax2 = fig.add_subplot(gs[0, 1])
    source_counts = Counter()
    for emotion_data in data['emotions'].values():
        for source in emotion_data['sources']:
            source_counts[source] += emotion_data['frequency']
    ax2.pie(source_counts.values(), labels=source_counts.keys(), autopct='%1.1f%%')
    ax2.set_title('Distribution par Source', fontweight='bold')
    
    # 3. Matrice émotion-thème (en haut à droite)
    ax3 = fig.add_subplot(gs[0, 2])
    themes = list(data['themes'].keys())
    matrix = np.zeros((len(emotions), len(themes)))
    for i, emotion in enumerate(emotions):
        for j, theme in enumerate(themes):
            if theme in data['emotions'][emotion]['themes']:
                matrix[i][j] = data['emotions'][emotion]['frequency']
    im = ax3.imshow(matrix, cmap='YlOrRd')
    ax3.set_xticks(range(len(themes)))
    ax3.set_yticks(range(len(emotions)))
    ax3.set_xticklabels(themes, rotation=45)
    ax3.set_yticklabels(emotions)
    ax3.set_title('Matrice Émotion-Thème', fontweight='bold')
    
    # 4. Clusters (au milieu)
    ax4 = fig.add_subplot(gs[1, :])
    clusters = data['clusters']
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    y_pos = 0
    for i, (cluster_name, cluster_emotions) in enumerate(clusters.items()):
        rect = plt.Rectangle((0, y_pos), 10, 1, 
                           facecolor=colors[i % len(colors)], 
                           alpha=0.7, 
                           edgecolor='black')
        ax4.add_patch(rect)
        ax4.text(5, y_pos + 0.5, f"{cluster_name.replace('_', ' ').title()}: {', '.join(cluster_emotions)}", 
                ha='center', va='center', fontweight='bold')
        y_pos += 1.5
    ax4.set_xlim(0, 10)
    ax4.set_ylim(-0.5, y_pos - 0.5)
    ax4.set_title('Clusters d\'Émotions', fontweight='bold')
    ax4.axis('off')
    
    # 5. Statistiques textuelles (en bas)
    ax5 = fig.add_subplot(gs[2, :])
    ax5.axis('off')
    
    # Créer un résumé textuel
    summary_text = f"""
    📊 RÉSUMÉ DU GRAPHE SOCIAL DES ÉMOTIONS
    
    • Total Émotions: {data['metadata']['total_emotions']}
    • Total Thèmes: {data['metadata']['total_themes']}
    • Total Relations: {data['metadata']['total_relations']}
    • Clusters Créés: {len(data['clusters'])}
    
    🏆 ÉMOTIONS LES PLUS FRÉQUENTES:
    """
    
    emotion_freqs = [(emotion, data['emotions'][emotion]['frequency']) for emotion in emotions]
    emotion_freqs.sort(key=lambda x: x[1], reverse=True)
    
    for emotion, freq in emotion_freqs:
        summary_text += f"    • {emotion}: {freq} occurrences\n"
    
    ax5.text(0.1, 0.9, summary_text, transform=ax5.transAxes, fontsize=12,
            verticalalignment='top', fontfamily='monospace')
    
    plt.suptitle('TABLEAU DE BORD - GRAPHE SOCIAL DES ÉMOTIONS', 
                fontsize=20, fontweight='bold', y=0.98)
    
    # Sauvegarder
    output_path = "data/processed/comprehensive_dashboard.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"✅ Tableau de bord sauvegardé: {output_path}")
    return output_path

def main():
    """Fonction principale de visualisation."""
    logger.info("🎨 GÉNÉRATION DES GRAPHIQUES ÉMOTIONNELS")
    logger.info("=" * 60)
    
    # Charger les données
    data = load_graph_data()
    if not data:
        logger.error("❌ Impossible de charger les données")
        return False
    
    try:
        # Créer tous les graphiques
        charts = []
        
        logger.info("📊 Génération des graphiques individuels...")
        charts.append(create_emotion_frequency_chart(data))
        charts.append(create_theme_emotion_matrix(data))
        charts.append(create_source_distribution_chart(data))
        charts.append(create_cluster_visualization(data))
        charts.append(create_timeline_chart(data))
        
        logger.info("📊 Génération du tableau de bord complet...")
        charts.append(create_comprehensive_dashboard(data))
        
        # Résumé final
        logger.info("\n" + "=" * 60)
        logger.info("🎉 GRAPHIQUES GÉNÉRÉS AVEC SUCCÈS!")
        logger.info("=" * 60)
        logger.info("📊 Graphiques créés:")
        for i, chart in enumerate(charts, 1):
            logger.info(f"   {i}. {os.path.basename(chart)}")
        
        logger.info("\n📁 Tous les graphiques sont sauvegardés dans: data/processed/")
        logger.info("🎨 Vous pouvez maintenant visualiser les données émotionnelles!")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la génération des graphiques: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)




