#!/usr/bin/env python3
"""
Script de test pour diagnostiquer le problème de nuage de mots
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import base64
import io
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def test_wordcloud_generation():
    """Test simple de génération de nuage de mots"""
    print("🔍 Test de génération de nuage de mots...")
    
    # Données de test
    text = "amour génial super excellent fantastique merveilleux terrible horrible nulle"
    word_freq = {"amour": 5, "génial": 4, "super": 3, "excellent": 2, "fantastique": 2, "merveilleux": 1, "terrible": 1, "horrible": 1, "nulle": 1}
    
    try:
        # Créer le nuage de mots
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            max_words=50,
            relative_scaling=0.5,
            random_state=42,
            colormap='viridis'
        ).generate_from_frequencies(word_freq)
        
        print("✅ Nuage de mots créé avec succès")
        
        # Convertir en base64
        img_buffer = io.BytesIO()
        plt.figure(figsize=(8, 4))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
        plt.close()
        
        print("✅ Image matplotlib créée avec succès")
        
        # Encoder en base64
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        print(f"✅ Base64 généré: {len(img_base64)} caractères")
        print(f"📝 Début du base64: {img_base64[:100]}...")
        
        # Tester le décodage
        try:
            decoded = base64.b64decode(img_base64)
            print(f"✅ Décodage base64 réussi: {len(decoded)} bytes")
            
            # Tester l'ouverture avec PIL
            from PIL import Image
            img = Image.open(io.BytesIO(decoded))
            print(f"✅ Image PIL ouverte: {img.size} pixels")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du décodage: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        return False

def test_streamlit_display():
    """Test d'affichage Streamlit"""
    print("\n🔍 Test d'affichage Streamlit...")
    
    try:
        import streamlit as st
        print("✅ Streamlit importé avec succès")
        
        # Test simple d'affichage
        text = "Test simple"
        st.write(text)
        print("✅ Streamlit fonctionne")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur Streamlit: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Démarrage des tests de diagnostic...")
    
    # Test 1: Génération de nuage de mots
    success1 = test_wordcloud_generation()
    
    # Test 2: Streamlit
    success2 = test_streamlit_display()
    
    print(f"\n📊 Résultats:")
    print(f"   Nuage de mots: {'✅' if success1 else '❌'}")
    print(f"   Streamlit: {'✅' if success2 else '❌'}")
    
    if success1 and success2:
        print("🎉 Tous les tests sont passés!")
    else:
        print("⚠️ Certains tests ont échoué")
