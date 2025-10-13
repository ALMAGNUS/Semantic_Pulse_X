"""
Interface Streamlit - Semantic Pulse X
Dashboard interactif pour les analystes
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import json
from pathlib import Path

from app.backend.etl.pipeline import etl_pipeline
from app.backend.ai.emotion_classifier import emotion_classifier
from app.backend.ai.topic_clustering import topic_clustering
from app.backend.ai.langchain_agent import semantic_agent
from app.backend.orchestration.monitoring_dashboard import show_orchestration_dashboard
from app.frontend.streamlit_ollama_dashboard import show_ollama_dashboard
from app.frontend.streamlit_wordcloud_dashboard import show_wordcloud_dashboard


# Configuration de la page
st.set_page_config(
    page_title="Semantic Pulse X",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .emotion-positive { color: #2ca02c; }
    .emotion-negative { color: #d62728; }
    .emotion-neutral { color: #7f7f7f; }
</style>
""", unsafe_allow_html=True)


def main():
    """Fonction principale de l'application"""
    
    # Header
    st.markdown('<h1 class="main-header">🧠 Semantic Pulse X</h1>', unsafe_allow_html=True)
    st.markdown("### Cartographie dynamique des émotions médiatiques")
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Contrôles")
        
        # Sélection de la période
        st.subheader("📅 Période d'analyse")
        date_range = st.date_input(
            "Sélectionner la période",
            value=(datetime.now() - timedelta(days=7), datetime.now()),
            max_value=datetime.now()
        )
        
        # Sélection des sources
        st.subheader("📡 Sources de données")
        sources = st.multiselect(
            "Sélectionner les sources",
            ["file", "database", "bigdata", "scraping", "api"],
            default=["file", "database", "bigdata", "scraping", "api"]
        )
        
        # Bouton de mise à jour
        if st.button("🔄 Actualiser les données", type="primary"):
            with st.spinner("Traitement en cours..."):
                run_pipeline()
    
    # Onglets principaux
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📊 Vue d'ensemble", 
        "🎭 Analyse émotionnelle", 
        "📈 Tendances", 
        "🔍 Exploration", 
        "🤖 IA Assistant",
        "🎛️ Orchestration",
        "🤖 Ollama IA",
        "☁️ Nuages de Mots"
    ])
    
    with tab1:
        show_overview()
    
    with tab2:
        show_emotion_analysis()
    
    with tab3:
        show_trends()
    
    with tab4:
        show_exploration()
    
    with tab5:
        show_ai_assistant()
    
    with tab6:
        show_orchestration_dashboard()
    
    with tab7:
        show_ollama_dashboard()
    
    with tab8:
        show_wordcloud_dashboard()


def run_pipeline():
    """Exécute le pipeline ETL"""
    try:
        with st.spinner("🔄 Exécution du pipeline ETL..."):
            results = etl_pipeline.run_full_pipeline()
            
        if results.get("success", True):
            st.success("✅ Pipeline exécuté avec succès!")
            st.session_state.pipeline_results = results
        else:
            st.error(f"❌ Erreur: {results.get('error', 'Erreur inconnue')}")
            
    except Exception as e:
        st.error(f"❌ Erreur: {str(e)}")


def show_overview():
    """Affiche la vue d'ensemble"""
    st.header("📊 Vue d'ensemble")
    
    # Charger les données
    data = load_processed_data()
    if data.empty:
        st.warning("⚠️ Aucune donnée disponible. Exécutez d'abord le pipeline ETL.")
        return
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total réactions",
            f"{len(data):,}",
            delta=f"+{len(data)//10}" if len(data) > 0 else "0"
        )
    
    with col2:
        avg_polarity = data['polarity'].mean()
        st.metric(
            "Polarité moyenne",
            f"{avg_polarity:.2f}",
            delta=f"{avg_polarity:.2f}" if avg_polarity > 0 else f"{avg_polarity:.2f}"
        )
    
    with col3:
        unique_emotions = data['emotion'].nunique()
        st.metric(
            "Émotions détectées",
            unique_emotions,
            delta=f"+{unique_emotions//2}" if unique_emotions > 0 else "0"
        )
    
    with col4:
        sources_count = data['source_type'].nunique()
        st.metric(
            "Sources actives",
            sources_count,
            delta=f"+{sources_count//2}" if sources_count > 0 else "0"
        )
    
    # Graphiques principaux
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution des émotions
        emotion_counts = data['emotion'].value_counts()
        fig_emotions = px.pie(
            values=emotion_counts.values,
            names=emotion_counts.index,
            title="Distribution des émotions",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_emotions, use_container_width=True)
    
    with col2:
        # Distribution des sources
        source_counts = data['source_type'].value_counts()
        fig_sources = px.bar(
            x=source_counts.index,
            y=source_counts.values,
            title="Répartition par source",
            color=source_counts.values,
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig_sources, use_container_width=True)
    
    # Timeline des émotions
    st.subheader("📈 Évolution temporelle")
    
    # Grouper par heure
    data['hour'] = pd.to_datetime(data['timestamp']).dt.floor('H')
    hourly_emotions = data.groupby(['hour', 'emotion']).size().reset_index(name='count')
    
    fig_timeline = px.line(
        hourly_emotions,
        x='hour',
        y='count',
        color='emotion',
        title="Évolution des émotions dans le temps",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_timeline, use_container_width=True)


def show_emotion_analysis():
    """Affiche l'analyse émotionnelle détaillée"""
    st.header("🎭 Analyse émotionnelle")
    
    data = load_processed_data()
    if data.empty:
        st.warning("⚠️ Aucune donnée disponible.")
        return
    
    # Filtres
    col1, col2 = st.columns(2)
    
    with col1:
        selected_emotions = st.multiselect(
            "Sélectionner les émotions",
            data['emotion'].unique(),
            default=data['emotion'].unique()
        )
    
    with col2:
        selected_sources = st.multiselect(
            "Sélectionner les sources",
            data['source_type'].unique(),
            default=data['source_type'].unique()
        )
    
    # Filtrer les données
    filtered_data = data[
        (data['emotion'].isin(selected_emotions)) &
        (data['source_type'].isin(selected_sources))
    ]
    
    if filtered_data.empty:
        st.warning("⚠️ Aucune donnée correspondant aux filtres.")
        return
    
    # Analyse des émotions
    col1, col2 = st.columns(2)
    
    with col1:
        # Heatmap des émotions par source
        emotion_source = filtered_data.groupby(['emotion', 'source_type']).size().unstack(fill_value=0)
        
        fig_heatmap = px.imshow(
            emotion_source.values,
            x=emotion_source.columns,
            y=emotion_source.index,
            title="Heatmap émotions vs sources",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with col2:
        # Distribution de la polarité
        fig_polarity = px.histogram(
            filtered_data,
            x='polarity',
            nbins=20,
            title="Distribution de la polarité",
            color_discrete_sequence=['#1f77b4']
        )
        st.plotly_chart(fig_polarity, use_container_width=True)
    
    # Top textes par émotion
    st.subheader("📝 Top textes par émotion")
    
    for emotion in selected_emotions:
        emotion_data = filtered_data[filtered_data['emotion'] == emotion]
        if not emotion_data.empty:
            st.write(f"**{emotion.upper()}** ({len(emotion_data)} textes)")
            
            # Afficher les top textes
            top_texts = emotion_data.nlargest(5, 'polarity')['text'].tolist()
            for i, text in enumerate(top_texts, 1):
                st.write(f"{i}. {text[:100]}...")


def show_trends():
    """Affiche les tendances et prédictions"""
    st.header("📈 Tendances et prédictions")
    
    data = load_processed_data()
    if data.empty:
        st.warning("⚠️ Aucune donnée disponible.")
        return
    
    # Analyse des tendances
    st.subheader("🔍 Analyse des tendances")
    
    # Grouper par jour
    data['date'] = pd.to_datetime(data['timestamp']).dt.date
    daily_trends = data.groupby(['date', 'emotion']).size().reset_index(name='count')
    
    # Graphique des tendances
    fig_trends = px.line(
        daily_trends,
        x='date',
        y='count',
        color='emotion',
        title="Tendances quotidiennes des émotions",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_trends, use_container_width=True)
    
    # Analyse des corrélations
    st.subheader("🔗 Corrélations")
    
    # Matrice de corrélation
    numeric_data = data[['polarity', 'ai_confidence']].dropna()
    if not numeric_data.empty:
        corr_matrix = numeric_data.corr()
        
        fig_corr = px.imshow(
            corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            title="Matrice de corrélation",
            color_continuous_scale="RdBu",
            aspect="auto"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    
    # Prédictions (simulation)
    st.subheader("🔮 Prédictions")
    
    # Simuler des prédictions
    future_dates = pd.date_range(
        start=datetime.now(),
        periods=7,
        freq='D'
    )
    
    # Prédictions simulées
    predictions = []
    for date in future_dates:
        predictions.append({
            'date': date,
            'emotion': 'joie',
            'confidence': np.random.uniform(0.6, 0.9),
            'trend': 'positive'
        })
    
    pred_df = pd.DataFrame(predictions)
    
    fig_pred = px.line(
        pred_df,
        x='date',
        y='confidence',
        title="Prédictions de confiance",
        color_discrete_sequence=['#ff7f0e']
    )
    st.plotly_chart(fig_pred, use_container_width=True)


def show_exploration():
    """Affiche l'exploration interactive"""
    st.header("🔍 Exploration interactive")
    
    data = load_processed_data()
    if data.empty:
        st.warning("⚠️ Aucune donnée disponible.")
        return
    
    # Recherche de textes
    st.subheader("🔍 Recherche de textes")
    
    search_query = st.text_input("Rechercher dans les textes", "")
    
    if search_query:
        # Recherche simple
        filtered_data = data[data['text'].str.contains(search_query, case=False, na=False)]
        
        if not filtered_data.empty:
            st.write(f"**{len(filtered_data)} résultats trouvés**")
            
            # Afficher les résultats
            for idx, row in filtered_data.head(10).iterrows():
                with st.expander(f"Résultat {idx+1}: {row['text'][:50]}..."):
                    st.write(f"**Texte complet:** {row['text']}")
                    st.write(f"**Émotion:** {row['emotion']}")
                    st.write(f"**Polarité:** {row['polarity']:.2f}")
                    st.write(f"**Source:** {row['source_type']}")
                    st.write(f"**Timestamp:** {row['timestamp']}")
        else:
            st.info("Aucun résultat trouvé.")
    
    # Exploration des données
    st.subheader("📊 Exploration des données")
    
    # Sélection de colonnes
    columns_to_show = st.multiselect(
        "Sélectionner les colonnes à afficher",
        data.columns,
        default=['text', 'emotion', 'polarity', 'source_type', 'timestamp']
    )
    
    if columns_to_show:
        st.dataframe(data[columns_to_show].head(100))
    
    # Statistiques descriptives
    st.subheader("📈 Statistiques descriptives")
    
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    if not numeric_columns.empty:
        st.dataframe(data[numeric_columns].describe())


def show_ai_assistant():
    """Affiche l'assistant IA"""
    st.header("🤖 Assistant IA")
    
    # Chat interface
    st.subheader("💬 Chat avec l'IA")
    
    # Initialiser l'historique de chat
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Afficher l'historique
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Input utilisateur
    user_input = st.chat_input("Posez une question sur les données...")
    
    if user_input:
        # Ajouter le message utilisateur
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Générer la réponse IA
        with st.spinner("🤔 L'IA réfléchit..."):
            try:
                # Charger les données pour le contexte
                data = load_processed_data()
                context = {
                    "total_records": len(data),
                    "emotions": data['emotion'].value_counts().to_dict(),
                    "sources": data['source_type'].value_counts().to_dict(),
                    "avg_polarity": data['polarity'].mean()
                }
                
                # Générer la réponse
                response = semantic_agent.answer_question(user_input, context)
                
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


def load_processed_data():
    """Charge les données traitées"""
    try:
        data_path = Path("data/processed/final_data.parquet")
        if data_path.exists():
            return pd.read_parquet(data_path)
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
        return pd.DataFrame()


if __name__ == "__main__":
    main()
