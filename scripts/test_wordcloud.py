#!/usr/bin/env python3
"""
Test des nuages de mots - Semantic Pulse X
"""

import sys
from pathlib import Path

# Ajouter le répertoire racine au PYTHONPATH
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

def test_wordcloud():
    """Test de génération de nuages de mots"""
    print("🎨 TEST DES NUAGES DE MOTS - Semantic Pulse X")
    print("=" * 60)
    
    try:
        from app.frontend.visualization.wordcloud_generator import wordcloud_generator
        
        print("✅ Module wordcloud_generator importé avec succès")
        
        # Test de génération
        print("\n🔄 Génération d'un nuage de mots...")
        
        # Créer des données de test
        test_texts = [
            "J'adore cette émission, c'est génial !",
            "Cette émission est nulle, je déteste !",
            "Super épisode, j'ai hâte de voir la suite !"
        ]
        test_emotions = ["joie", "colere", "joie"]
        
        wordcloud_data = wordcloud_generator.generate_emotion_wordcloud(
            texts=test_texts,
            emotions=test_emotions,
            emotion_filter="joie",
            max_words=20
        )
        
        if wordcloud_data:
            print("✅ Nuage de mots généré avec succès !")
            print(f"📊 Type de données: {type(wordcloud_data)}")
            print(f"📏 Taille: {len(wordcloud_data) if hasattr(wordcloud_data, '__len__') else 'N/A'}")
            
            # Sauvegarder le nuage de mots
            output_file = Path("data/processed/test_wordcloud.png")
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            if hasattr(wordcloud_data, 'save'):
                wordcloud_data.save(str(output_file))
                print(f"💾 Nuage de mots sauvegardé: {output_file}")
            else:
                print("⚠️ Impossible de sauvegarder le nuage de mots")
                
        else:
            print("❌ Échec de la génération du nuage de mots")
            
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

def test_emotion_classifier():
    """Test du classificateur d'émotions"""
    print("\n🤖 TEST DU CLASSIFICATEUR D'ÉMOTIONS")
    print("-" * 40)
    
    try:
        from app.backend.ai.emotion_classifier import emotion_classifier
        
        print("✅ Classificateur d'émotions importé")
        
        # Test de classification
        test_text = "J'adore cette émission, c'est génial !"
        print(f"📝 Texte de test: '{test_text}'")
        
        emotions = emotion_classifier.classify_batch([test_text])
        print(f"🎭 Émotions détectées: {emotions}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_data_processing():
    """Test du traitement de données"""
    print("\n📊 TEST DU TRAITEMENT DE DONNÉES")
    print("-" * 40)
    
    try:
        # Charger les données traitées
        data_file = Path("data/processed/donnees_traitees_demo.json")
        if data_file.exists():
            import json
            with open(data_file, 'r', encoding='utf-8') as f:
                donnees = json.load(f)
            
            print(f"✅ {len(donnees)} données chargées")
            
            # Afficher un échantillon
            for i, data in enumerate(donnees[:2], 1):
                print(f"\n📄 Donnée {i}:")
                print(f"   Texte: {data['contenu']}")
                print(f"   Utilisateur: {data['utilisateur_anonyme']}")
                print(f"   Source: {data['source_type']}")
                print(f"   Mots: {data['nombre_mots']}")
        else:
            print("❌ Aucune donnée traitée trouvée")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_wordcloud()
    test_emotion_classifier()
    test_data_processing()
    
    print("\n🎉 TESTS TERMINÉS")
    print("=" * 60)
    print("🌐 Streamlit disponible sur: http://localhost:8501")
    print("🔗 API FastAPI disponible sur: http://localhost:8000")
    print("📚 Documentation API: http://localhost:8000/docs")
