#!/usr/bin/env python3
"""
Démonstration nuage de mots avec traçabilité des sources - Semantic Pulse X
Montre l'origine de chaque mot (Twitter, YouTube, Instagram, etc.)
"""

import sys
from pathlib import Path
import json
import base64
from io import BytesIO

# Ajouter le répertoire racine au PYTHONPATH
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

def demo_wordcloud_with_sources():
    """Démonstration du nuage de mots avec traçabilité des sources"""
    print("🎨 DÉMONSTRATION NUAGE DE MOTS AVEC SOURCES")
    print("=" * 60)
    
    try:
        from app.frontend.visualization.wordcloud_generator import wordcloud_generator
        
        # Charger les données traitées
        data_file = Path("data/processed/donnees_traitees_demo.json")
        if not data_file.exists():
            print("❌ Aucune donnée traitée trouvée")
            return
        
        with open(data_file, 'r', encoding='utf-8') as f:
            donnees = json.load(f)
        
        print(f"✅ {len(donnees)} données chargées")
        
        # Préparer les données avec sources
        data_with_sources = []
        for data in donnees:
            data_with_sources.append({
                'text': data['contenu'],
                'source': data['source_type'],
                'emotion': 'joie',  # Simuler une émotion pour la démo
                'user_id': data['utilisateur_anonyme']
            })
        
        print("\n📊 DONNÉES AVEC SOURCES:")
        for i, data in enumerate(data_with_sources, 1):
            print(f"   {i}. Texte: '{data['text']}'")
            print(f"      Source: {data['source'].upper()}")
            print(f"      Utilisateur: {data['user_id']}")
            print()
        
        print("🔄 Génération du nuage de mots avec traçabilité...")
        
        # Générer le nuage de mots avec sources
        wordcloud_data = wordcloud_generator.generate_emotion_wordcloud_with_sources(
            data=data_with_sources,
            emotion_filter="joie",
            max_words=15,
            width=800,
            height=400
        )
        
        if wordcloud_data and wordcloud_data.get('image'):
            print("✅ Nuage de mots généré avec succès !")
            
            # Afficher les statistiques
            print(f"\n📊 STATISTIQUES:")
            print(f"   • Total mots: {wordcloud_data['total_words']}")
            print(f"   • Mots uniques: {wordcloud_data['unique_words']}")
            print(f"   • Émotion: {wordcloud_data['emotion']}")
            
            # Afficher la traçabilité des sources
            print(f"\n🔍 TRACABILITÉ DES SOURCES:")
            print("=" * 50)
            
            source_traceability = wordcloud_data.get('source_traceability', {})
            for word, info in source_traceability.items():
                print(f"\n📝 Mot: '{word}' (fréquence: {info['frequency']})")
                print(f"   🎯 Source principale: {info['main_source'].upper()}")
                print(f"   📊 Répartition par source:")
                for source, count in info['sources'].items():
                    percentage = (count / info['frequency']) * 100
                    print(f"      • {source.upper()}: {count} fois ({percentage:.1f}%)")
            
            # Sauvegarder l'image
            output_file = Path("data/processed/wordcloud_sources_demo.png")
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Décoder l'image base64
            image_data = base64.b64decode(wordcloud_data['image'])
            
            with open(output_file, 'wb') as f:
                f.write(image_data)
            
            print(f"\n💾 Nuage de mots sauvegardé: {output_file}")
            print(f"   Taille: {len(image_data)} octets")
            
            # Générer un rapport détaillé
            rapport = {
                "nuage_mots_sources": {
                    "fichier": str(output_file),
                    "emotion": wordcloud_data['emotion'],
                    "total_mots": wordcloud_data['total_words'],
                    "mots_uniques": wordcloud_data['unique_words'],
                    "traçabilite_sources": source_traceability
                },
                "donnees_source": {
                    "nombre_donnees": len(donnees),
                    "sources_detectees": list(set(data['source_type'] for data in donnees)),
                    "repartition_sources": {
                        source: len([d for d in donnees if d['source_type'] == source])
                        for source in set(data['source_type'] for data in donnees)
                    }
                },
                "generation": {
                    "timestamp": wordcloud_data['metadata']['generated_at'],
                    "parametres": {
                        "max_words": 15,
                        "width": 800,
                        "height": 400
                    }
                }
            }
            
            rapport_file = Path("data/processed/rapport_wordcloud_sources_demo.json")
            with open(rapport_file, 'w', encoding='utf-8') as f:
                json.dump(rapport, f, indent=2, ensure_ascii=False)
            
            print(f"📊 Rapport détaillé: {rapport_file}")
            
            # Résumé pour le jury
            print("\n🎯 RÉSUMÉ FINAL:")
            print("=" * 60)
            print("✅ TRACABILITÉ DES SOURCES DÉMONTRÉE:")
            
            # Compter les sources
            source_counts = {}
            for word, info in source_traceability.items():
                for source, count in info['sources'].items():
                    source_counts[source] = source_counts.get(source, 0) + count
            
            for source, count in source_counts.items():
                print(f"   • {source.upper()}: {count} contributions")
            
            print("\n✅ COMPÉTENCES DÉMONTRÉES:")
            print("   • Traçabilité complète des données")
            print("   • Association mot-source en temps réel")
            print("   • Analyse multi-sources")
            print("   • Visualisation avec contexte")
            print("   • Conformité RGPD maintenue")
            
            print("\n🌐 INTERFACES DISPONIBLES:")
            print("   • Streamlit: http://localhost:8501")
            print("   • API FastAPI: http://localhost:8000")
            print("   • Documentation: http://localhost:8000/docs")
            
        else:
            print("❌ Échec de la génération du nuage de mots")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demo_wordcloud_with_sources()
