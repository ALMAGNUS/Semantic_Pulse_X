#!/usr/bin/env python3
"""
Streamlit simplifié - Semantic Pulse X
Focus sur les nuages de mots et visualisations
"""

import streamlit as st
import sys
import json
from pathlib import Path

# Ajouter le répertoire racine au PYTHONPATH
project_root = Path(__file__).parent.parent.parent.absolute()
sys.path.insert(0, str(project_root))

# Imports simplifiés
try:
    from app.backend.ai.emotion_classifier import emotion_classifier
    from app.backend.ai.topic_clustering import topic_clustering
    from app.backend.core.anonymization import anonymizer
    from app.frontend.visualization.wordcloud_generator import wordcloud_generator
except ImportError as e:
    st.error(f"Erreur d'import: {e}")
    st.stop()

def main():
    """Application Streamlit principale"""
    
    st.set_page_config(
        page_title="Semantic Pulse X - Nuages de Mots",
        page_icon="🌊",
        layout="wide"
    )
    
    st.title("🌊 Semantic Pulse X - Nuages de Mots")
    st.markdown("### Visualisation des vagues émotionnelles médiatiques")
    
    # Sidebar
    st.sidebar.title("🎛️ Configuration")
    
    # Paramètres des nuages de mots
    emotion = st.sidebar.selectbox(
        "Émotion à analyser",
        ["joy", "sadness", "anger", "fear", "surprise", "disgust"],
        index=0
    )
    
    max_words = st.sidebar.slider("Nombre maximum de mots", 10, 100, 30)
    
    colormap = st.sidebar.selectbox(
        "Palette de couleurs",
        ["viridis", "plasma", "inferno", "magma", "coolwarm", "RdYlBu"],
        index=0
    )
    
    # Bouton de génération
    if st.sidebar.button("🎨 Générer le nuage de mots", type="primary"):
        with st.spinner("Génération du nuage de mots..."):
            try:
                # Charger les données avec sources
                data_file = Path("data/processed/donnees_traitees_demo.json")
                if data_file.exists():
                    with open(data_file, 'r', encoding='utf-8') as f:
                        donnees = json.load(f)
                    
                    # Préparer les données avec sources
                    data_with_sources = []
                    for data in donnees:
                        data_with_sources.append({
                            'text': data['contenu'],
                            'source': data['source_type'],
                            'emotion': emotion,
                            'user_id': data['utilisateur_anonyme']
                        })
                    
                    # Générer le nuage de mots avec traçabilité
                    wordcloud_data = wordcloud_generator.generate_emotion_wordcloud_with_sources(
                        data=data_with_sources,
                        emotion_filter=emotion,
                        max_words=max_words,
                        width=800,
                        height=400
                    )
                else:
                    st.error("❌ Aucune donnée trouvée. Lancez d'abord le script de démonstration.")
                    st.stop()
                
                if wordcloud_data:
                    st.success("✅ Nuage de mots généré avec succès !")
                    
                    # Afficher le nuage de mots
                    st.image(wordcloud_data['image'], caption=f"Nuage de mots - Émotion: {emotion}", use_column_width=True)
                    
                    # Statistiques
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Émotion", emotion.title())
                    with col2:
                        st.metric("Mots max", max_words)
                    with col3:
                        st.metric("Palette", colormap)
                    
                    # Traçabilité des sources
                    if 'source_traceability' in wordcloud_data:
                        st.markdown("### 🔍 Traçabilité des Sources")
                        
                        source_traceability = wordcloud_data['source_traceability']
                        
                        # Afficher les mots les plus fréquents avec leurs sources
                        for word, info in list(source_traceability.items())[:10]:
                            with st.expander(f"📝 '{word}' (fréquence: {info['frequency']})"):
                                st.write(f"**Source principale:** {info['main_source'].upper()}")
                                st.write("**Répartition par source:**")
                                
                                for source, count in info['sources'].items():
                                    percentage = (count / info['frequency']) * 100
                                    st.write(f"• {source.upper()}: {count} fois ({percentage:.1f}%)")
                        
                else:
                    st.error("❌ Erreur lors de la génération du nuage de mots")
                    
            except Exception as e:
                st.error(f"❌ Erreur: {e}")
    
    # Section de démonstration
    st.markdown("---")
    st.markdown("## 📊 Démonstration Data Engineering")
    
    if st.button("🔍 Voir les résultats de traitement"):
        try:
            # Charger les données traitées
            data_file = Path("data/processed/donnees_traitees_demo.json")
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    donnees = json.load(f)
                
                st.success(f"✅ {len(donnees)} données traitées chargées")
                
                # Afficher les données
                for i, data in enumerate(donnees, 1):
                    with st.expander(f"Donnée {i}: {data['contenu'][:50]}..."):
                        st.write(f"**Texte:** {data['contenu']}")
                        st.write(f"**Utilisateur anonymisé:** {data['utilisateur_anonyme']}")
                        st.write(f"**Source:** {data['source_type']}")
                        st.write(f"**Mots:** {data['nombre_mots']}")
                        st.write(f"**Caractères:** {data['longueur_caracteres']}")
                        st.write(f"**Densité:** {data['densite_mots']}%")
            else:
                st.warning("⚠️ Aucune donnée traitée trouvée. Lancez d'abord le script de démonstration.")
                
        except Exception as e:
            st.error(f"❌ Erreur: {e}")
    
    # Section API
    st.markdown("---")
    st.markdown("## 🌐 API FastAPI")
    
    if st.button("🔗 Tester l'API"):
        try:
            import requests
            
            # Test de l'API
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                st.success("✅ API FastAPI accessible")
                st.json(response.json())
            else:
                st.error(f"❌ API non accessible: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ API FastAPI non lancée. Lancez: `python -m uvicorn app.backend.main:app --reload --port 8000`")
        except Exception as e:
            st.error(f"❌ Erreur: {e}")
    
    # Footer
    st.markdown("---")
    st.markdown("### 🎯 Semantic Pulse X - Pipeline de Data Engineering RGPD")
    st.markdown("**Compétences démontrées:** Nettoyage, Dédoublonnage, Anonymisation, Homogénéisation, Visualisation")

if __name__ == "__main__":
    main()
