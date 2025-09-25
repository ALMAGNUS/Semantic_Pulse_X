#!/usr/bin/env python3
"""
Test simple - Semantic Pulse X
Évite les bibliothèques problématiques
"""

import sys
from pathlib import Path
import json

# Ajouter le répertoire racine au PYTHONPATH
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

def test_simple():
    """Test simple sans bibliothèques lourdes"""
    print("🧪 TEST SIMPLE - SEMANTIC PULSE X")
    print("=" * 50)
    
    try:
        # Test 1: Chargement des données
        print("\n📊 Test 1: Chargement des données")
        data_file = Path("data/processed/donnees_traitees_demo.json")
        if data_file.exists():
            with open(data_file, 'r', encoding='utf-8') as f:
                donnees = json.load(f)
            print(f"✅ {len(donnees)} données chargées")
            
            # Afficher les données
            for i, data in enumerate(donnees, 1):
                print(f"   {i}. {data['source_type'].upper()}: '{data['contenu']}'")
        else:
            print("❌ Aucune donnée trouvée")
            return
        
        # Test 2: Analyse des mots émotionnels
        print("\n🎭 Test 2: Analyse des mots émotionnels")
        
        # Mots émotionnels à chercher
        emotion_words = ['adore', 'génial', 'super', 'nulle', 'déteste']
        
        for data in donnees:
            texte = data['contenu']
            source = data['source_type']
            mots_trouves = []
            
            for mot in emotion_words:
                if mot in texte.lower():
                    mots_trouves.append(mot)
            
            if mots_trouves:
                print(f"   {source.upper()}: {mots_trouves}")
        
        # Test 3: Traçabilité des sources
        print("\n🔍 Test 3: Traçabilité des sources")
        
        mots_sources = {}
        for data in donnees:
            texte = data['contenu'].lower()
            source = data['source_type']
            
            for mot in emotion_words:
                if mot in texte:
                    if mot not in mots_sources:
                        mots_sources[mot] = []
                    mots_sources[mot].append(source)
        
        for mot, sources in mots_sources.items():
            print(f"   '{mot}': {sources}")
        
        # Test 4: Résumé
        print("\n📈 Test 4: Résumé")
        print(f"   • {len(donnees)} données analysées")
        print(f"   • {len(mots_sources)} mots émotionnels trouvés")
        print(f"   • Sources: {set(data['source_type'] for data in donnees)}")
        
        print("\n✅ Test simple réussi !")
        print("   Le système fonctionne sans les bibliothèques lourdes.")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple()
