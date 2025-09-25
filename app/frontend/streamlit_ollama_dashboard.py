"""
Dashboard Ollama - Semantic Pulse X
Interface de gestion des modèles IA locaux
"""

import streamlit as st
import requests
import json
from typing import List, Dict, Any
from datetime import datetime
import time

from app.backend.ai.ollama_client import ollama_client


def show_ollama_dashboard():
    """Affiche le dashboard Ollama"""
    st.header("🤖 Dashboard Ollama - Modèles IA Locaux")
    
    # Vérifier le statut d'Ollama
    if not ollama_client.is_available():
        st.error("❌ Ollama n'est pas disponible!")
        st.info("💡 Démarrez Ollama avec: `docker-compose -f docker-compose.ollama.yml up -d`")
        return
    
    # Statut général
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Statut Ollama", "🟢 Actif")
    
    with col2:
        models = ollama_client.get_available_models()
        st.metric("Modèles disponibles", len(models))
    
    with col3:
        st.metric("Modèle par défaut", "mistral:7b")
    
    # Onglets
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Modèles", 
        "🧪 Test", 
        "💬 Chat", 
        "⚙️ Configuration"
    ])
    
    with tab1:
        show_models_tab()
    
    with tab2:
        show_test_tab()
    
    with tab3:
        show_chat_tab()
    
    with tab4:
        show_config_tab()


def show_models_tab():
    """Onglet des modèles"""
    st.subheader("📋 Modèles disponibles")
    
    models = ollama_client.get_available_models()
    
    if not models:
        st.warning("Aucun modèle disponible")
        return
    
    # Liste des modèles
    for model in models:
        with st.expander(f"🤖 {model}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Nom:** {model}")
                st.write(f"**Statut:** ✅ Disponible")
            
            with col2:
                if st.button(f"Tester {model}", key=f"test_{model}"):
                    test_model(model)
    
    # Recommandations
    st.subheader("💡 Recommandations")
    
    recommended_models = [
        {"name": "mistral:7b", "description": "Excellent pour le français, recommandé pour Semantic Pulse"},
        {"name": "llama2:7b", "description": "Polyvalent et performant, bon pour l'anglais"},
        {"name": "codellama:7b", "description": "Spécialisé dans la génération de code"},
        {"name": "phi3:3.8b", "description": "Léger et rapide, idéal pour les tests"}
    ]
    
    for rec in recommended_models:
        status = "✅" if rec["name"] in models else "❌"
        st.write(f"{status} **{rec['name']}** - {rec['description']}")


def show_test_tab():
    """Onglet de test"""
    st.subheader("🧪 Test des modèles")
    
    models = ollama_client.get_available_models()
    
    if not models:
        st.warning("Aucun modèle disponible pour les tests")
        return
    
    # Sélection du modèle
    selected_model = st.selectbox("Sélectionner un modèle", models)
    
    # Prompt de test
    test_prompt = st.text_area(
        "Prompt de test",
        value="Analysez les tendances émotionnelles dans les médias et fournissez des insights.",
        height=100
    )
    
    # Paramètres
    col1, col2 = st.columns(2)
    
    with col1:
        temperature = st.slider("Température", 0.0, 1.0, 0.7, 0.1)
    
    with col2:
        max_tokens = st.slider("Max tokens", 100, 2000, 1000, 100)
    
    # Bouton de test
    if st.button("🚀 Tester le modèle", type="primary"):
        with st.spinner("Test en cours..."):
            start_time = time.time()
            
            try:
                response = ollama_client.generate_text(
                    prompt=test_prompt,
                    model=selected_model,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                
                end_time = time.time()
                duration = end_time - start_time
                
                # Afficher les résultats
                st.success(f"✅ Test réussi en {duration:.2f}s")
                
                st.subheader("📝 Réponse du modèle:")
                st.write(response)
                
                # Métriques
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Durée", f"{duration:.2f}s")
                with col2:
                    st.metric("Tokens générés", len(response.split()))
                with col3:
                    st.metric("Modèle", selected_model)
                
            except Exception as e:
                st.error(f"❌ Erreur lors du test: {e}")


def show_chat_tab():
    """Onglet de chat"""
    st.subheader("💬 Chat avec l'IA")
    
    models = ollama_client.get_available_models()
    
    if not models:
        st.warning("Aucun modèle disponible pour le chat")
        return
    
    # Sélection du modèle
    selected_model = st.selectbox("Modèle de chat", models, key="chat_model")
    
    # Initialiser l'historique de chat
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Afficher l'historique
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Input utilisateur
    user_input = st.chat_input("Posez une question à l'IA...")
    
    if user_input:
        # Ajouter le message utilisateur
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Générer la réponse
        with st.spinner("L'IA réfléchit..."):
            try:
                response = ollama_client.generate_text(
                    prompt=user_input,
                    model=selected_model,
                    temperature=0.7
                )
                
                # Ajouter la réponse
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                # Afficher la réponse
                with st.chat_message("assistant"):
                    st.write(response)
                    
            except Exception as e:
                error_msg = f"Erreur: {str(e)}"
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
                
                with st.chat_message("assistant"):
                    st.write(error_msg)
    
    # Bouton pour effacer l'historique
    if st.button("🗑️ Effacer l'historique"):
        st.session_state.chat_history = []
        st.rerun()


def show_config_tab():
    """Onglet de configuration"""
    st.subheader("⚙️ Configuration Ollama")
    
    # Informations système
    st.subheader("📊 Informations système")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("URL Ollama", "http://localhost:11434")
        st.metric("Modèles disponibles", len(ollama_client.get_available_models()))
    
    with col2:
        st.metric("Statut", "🟢 Connecté")
        st.metric("Dernière vérification", datetime.now().strftime("%H:%M:%S"))
    
    # Configuration des modèles
    st.subheader("🔧 Configuration des modèles")
    
    st.info("💡 Pour installer de nouveaux modèles, utilisez le script: `python scripts/setup_ollama.py`")
    
    # Boutons d'action
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Actualiser les modèles"):
            st.rerun()
    
    with col2:
        if st.button("🧪 Test rapide"):
            test_quick()
    
    with col3:
        if st.button("📊 Rapport de statut"):
            generate_status_report()


def test_model(model_name: str):
    """Teste un modèle spécifique"""
    with st.spinner(f"Test de {model_name}..."):
        try:
            response = ollama_client.generate_text(
                prompt="Bonjour, comment allez-vous?",
                model=model_name,
                temperature=0.7
            )
            
            st.success(f"✅ {model_name} fonctionne correctement!")
            st.write(f"**Réponse:** {response}")
            
        except Exception as e:
            st.error(f"❌ Erreur avec {model_name}: {e}")


def test_quick():
    """Test rapide de tous les modèles"""
    models = ollama_client.get_available_models()
    
    if not models:
        st.warning("Aucun modèle disponible")
        return
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = []
    
    for i, model in enumerate(models):
        status_text.text(f"Test de {model}...")
        
        try:
            response = ollama_client.generate_text(
                prompt="Test rapide",
                model=model,
                temperature=0.1
            )
            results.append({"model": model, "status": "✅ OK", "response": response[:50] + "..."})
        except Exception as e:
            results.append({"model": model, "status": "❌ Erreur", "response": str(e)[:50] + "..."})
        
        progress_bar.progress((i + 1) / len(models))
    
    status_text.text("Test terminé!")
    
    # Afficher les résultats
    st.subheader("📊 Résultats du test rapide")
    
    for result in results:
        st.write(f"{result['status']} **{result['model']}** - {result['response']}")


def generate_status_report():
    """Génère un rapport de statut"""
    models = ollama_client.get_available_models()
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "ollama_status": "connected" if ollama_client.is_available() else "disconnected",
        "available_models": models,
        "total_models": len(models)
    }
    
    st.subheader("📊 Rapport de statut")
    st.json(report)
    
    # Bouton de téléchargement
    st.download_button(
        label="💾 Télécharger le rapport",
        data=json.dumps(report, indent=2, ensure_ascii=False),
        file_name=f"ollama_status_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )


if __name__ == "__main__":
    st.set_page_config(
        page_title="Ollama Dashboard",
        page_icon="🤖",
        layout="wide"
    )
    
    show_ollama_dashboard()
