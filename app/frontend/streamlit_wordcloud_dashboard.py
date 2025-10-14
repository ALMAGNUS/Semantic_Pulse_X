"""
Dashboard Nuages de Mots - Semantic Pulse X
Interface de visualisation des vagues émotionnelles
"""


import pandas as pd
import plotly.express as px
import streamlit as st

from app.frontend.visualization.wordcloud_generator import wordcloud_generator


def show_wordcloud_dashboard():
    """Affiche le dashboard des nuages de mots"""
    st.header("☁️ Nuages de Mots - Vagues Émotionnelles")

    # Charger les données
    data = load_processed_data()
    if data.empty:
        st.warning("⚠️ Aucune donnée disponible. Exécutez d'abord le pipeline ETL.")
        return

    # Sidebar pour les contrôles
    with st.sidebar:
        st.subheader("🎛️ Contrôles")

        # Sélection de l'émotion
        emotions = data['emotion'].unique().tolist()
        selected_emotion = st.selectbox(
            "Sélectionner une émotion",
            ["Toutes"] + emotions,
            index=0
        )

        # Paramètres du nuage
        st.subheader("⚙️ Paramètres")

        max_words = st.slider("Nombre max de mots", 20, 200, 100)
        width = st.slider("Largeur", 400, 1200, 800)
        height = st.slider("Hauteur", 300, 800, 400)

        # Fenêtre temporelle
        time_window = st.selectbox(
            "Fenêtre temporelle",
            ["hour", "day", "week"],
            index=1
        )

        # Bouton de génération
        if st.button("🔄 Générer les nuages", type="primary"):
            st.session_state.regenerate_wordclouds = True

    # Onglets principaux
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "☁️ Nuage Principal",
        "📊 Comparaison Émotions",
        "⏰ Évolution Temporelle",
        "📈 Tendances",
        "🎯 Interactif"
    ])

    with tab1:
        show_main_wordcloud(data, selected_emotion, max_words, width, height)

    with tab2:
        show_emotion_comparison(data, max_words, width, height)

    with tab3:
        show_temporal_evolution(data, time_window, max_words)

    with tab4:
        show_trending_words(data, max_words)

    with tab5:
        show_interactive_wordcloud(data, selected_emotion)


def show_main_wordcloud(data: pd.DataFrame, emotion: str, max_words: int, width: int, height: int):
    """Affiche le nuage de mots principal"""
    st.subheader(f"☁️ Nuage de mots - {emotion if emotion != 'Toutes' else 'Toutes les émotions'}")

    # Préparer les données
    if emotion != "Toutes":
        filtered_data = data[data['emotion'] == emotion]
    else:
        filtered_data = data

    if filtered_data.empty:
        st.warning(f"Aucune donnée pour l'émotion '{emotion}'")
        return

    # Générer le nuage de mots
    with st.spinner("Génération du nuage de mots..."):
        texts = filtered_data['text'].tolist()
        emotions = filtered_data['emotion'].tolist()

        wordcloud_data = wordcloud_generator.generate_emotion_wordcloud(
            texts, emotions,
            emotion_filter=emotion if emotion != "Toutes" else None,
            max_words=max_words,
            width=width,
            height=height
        )

    # Afficher le nuage
    if wordcloud_data['image']:
        st.image(f"data:image/png;base64,{wordcloud_data['image']}", use_column_width=True)
    else:
        st.warning("Impossible de générer le nuage de mots")

    # Statistiques
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total mots", wordcloud_data['total_words'])

    with col2:
        st.metric("Mots uniques", wordcloud_data['unique_words'])

    with col3:
        st.metric("Textes analysés", len(filtered_data))

    with col4:
        st.metric("Émotion", wordcloud_data['emotion'])

    # Top mots
    if wordcloud_data['word_frequencies']:
        st.subheader("📝 Top mots")

        word_freq_df = pd.DataFrame(
            list(wordcloud_data['word_frequencies'].items()),
            columns=['Mot', 'Fréquence']
        )

        st.dataframe(word_freq_df, use_container_width=True)


def show_emotion_comparison(data: pd.DataFrame, max_words: int, width: int, height: int):
    """Affiche la comparaison des émotions"""
    st.subheader("📊 Comparaison des émotions")

    # Générer les nuages de comparaison
    with st.spinner("Génération des nuages de comparaison..."):
        emotions = data['emotion'].unique().tolist()
        comparison_data = wordcloud_generator.generate_emotion_comparison_wordclouds(
            data.to_dict('records'), emotions, max_words
        )

    if not comparison_data:
        st.warning("Aucune donnée disponible pour la comparaison")
        return

    # Afficher les nuages par émotion
    for emotion, emotion_data in comparison_data.items():
        st.subheader(f"😊 {emotion.title()} ({emotion_data['count']} textes - {emotion_data['percentage']:.1f}%)")

        col1, col2 = st.columns([2, 1])

        with col1:
            if emotion_data['wordcloud']['image']:
                st.image(f"data:image/png;base64,{emotion_data['wordcloud']['image']}", use_column_width=True)

        with col2:
            # Top mots pour cette émotion
            word_freq = emotion_data['wordcloud']['word_frequencies']
            if word_freq:
                st.write("**Top mots:**")
                for word, freq in list(word_freq.items())[:10]:
                    st.write(f"• {word} ({freq})")

        st.divider()


def show_temporal_evolution(data: pd.DataFrame, time_window: str, max_words: int):
    """Affiche l'évolution temporelle"""
    st.subheader("⏰ Évolution temporelle des mots")

    # Générer les nuages temporels
    with st.spinner("Génération des nuages temporels..."):
        temporal_wordclouds = wordcloud_generator.generate_temporal_wordclouds(
            data.to_dict('records'), time_window, max_words
        )

    if not temporal_wordclouds:
        st.warning("Aucune donnée temporelle disponible")
        return

    # Afficher les nuages par période
    for i, wordcloud_data in enumerate(temporal_wordclouds):
        time_group = wordcloud_data['time_group']
        count = wordcloud_data['count']

        st.subheader(f"📅 {time_group} ({count} textes)")

        col1, col2 = st.columns([2, 1])

        with col1:
            if wordcloud_data['image']:
                st.image(f"data:image/png;base64,{wordcloud_data['image']}", use_column_width=True)

        with col2:
            # Statistiques
            st.metric("Mots totaux", wordcloud_data['total_words'])
            st.metric("Mots uniques", wordcloud_data['unique_words'])

            # Top mots
            if wordcloud_data['word_frequencies']:
                st.write("**Top mots:**")
                for word, freq in list(wordcloud_data['word_frequencies'].items())[:5]:
                    st.write(f"• {word} ({freq})")

        if i < len(temporal_wordclouds) - 1:
            st.divider()


def show_trending_words(data: pd.DataFrame, max_words: int):
    """Affiche les mots en tendance"""
    st.subheader("📈 Mots en tendance")

    # Générer le nuage de tendances
    with st.spinner("Analyse des tendances..."):
        trending_data = wordcloud_generator.generate_trending_words_cloud(
            data.to_dict('records'), time_periods=3, max_words=max_words
        )

    if not trending_data or not trending_data['image']:
        st.warning("Impossible de générer l'analyse des tendances")
        return

    # Afficher le nuage de tendances
    st.image(f"data:image/png;base64,{trending_data['image']}", use_column_width=True)

    # Statistiques des tendances
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Mots en tendance")
        if trending_data['trending_words']:
            trending_df = pd.DataFrame(
                list(trending_data['trending_words'].items()),
                columns=['Mot', 'Score de tendance']
            )
            st.dataframe(trending_df, use_container_width=True)

    with col2:
        st.subheader("📈 Scores de tendance")
        if trending_data['trending_scores']:
            scores_df = pd.DataFrame(
                list(trending_data['trending_scores'].items()),
                columns=['Mot', 'Score']
            )
            scores_df = scores_df.sort_values('Score', ascending=False)
            st.dataframe(scores_df, use_container_width=True)


def show_interactive_wordcloud(data: pd.DataFrame, emotion: str):
    """Affiche le nuage de mots interactif"""
    st.subheader("🎯 Nuage de mots interactif")

    # Préparer les données
    if emotion != "Toutes":
        filtered_data = data[data['emotion'] == emotion]
    else:
        filtered_data = data

    if filtered_data.empty:
        st.warning(f"Aucune donnée pour l'émotion '{emotion}'")
        return

    # Générer le graphique interactif
    with st.spinner("Génération du graphique interactif..."):
        fig = wordcloud_generator.generate_interactive_wordcloud(
            filtered_data.to_dict('records'),
            emotion if emotion != "Toutes" else None
        )

    # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True)

    # Statistiques détaillées
    st.subheader("📊 Statistiques détaillées")

    filtered_data['text'].tolist()
    stats = wordcloud_generator.get_word_statistics(filtered_data.to_dict('records'))

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Mots totaux", stats.get('total_words', 0))

    with col2:
        st.metric("Mots uniques", stats.get('unique_words', 0))

    with col3:
        st.metric("Longueur moyenne", f"{stats.get('average_word_length', 0):.1f}")

    with col4:
        st.metric("Richesse vocabulaire", f"{stats.get('vocabulary_richness', 0):.2f}")

    # Graphique de fréquence
    if stats.get('most_common'):
        st.subheader("📈 Fréquence des mots")

        most_common = stats['most_common']
        words = list(most_common.keys())[:20]
        frequencies = list(most_common.values())[:20]

        fig_freq = px.bar(
            x=frequencies,
            y=words,
            orientation='h',
            title="Top 20 des mots les plus fréquents",
            labels={'x': 'Fréquence', 'y': 'Mots'}
        )

        fig_freq.update_layout(height=600)
        st.plotly_chart(fig_freq, use_container_width=True)


def load_processed_data() -> pd.DataFrame:
    """Charge les données traitées"""
    try:
        from pathlib import Path
        data_path = Path("data/processed/final_data.parquet")
        if data_path.exists():
            return pd.read_parquet(data_path)
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
        return pd.DataFrame()


def show_wordcloud_controls():
    """Affiche les contrôles avancés"""
    st.subheader("🎛️ Contrôles avancés")

    # Paramètres de génération
    col1, col2 = st.columns(2)

    with col1:
        st.number_input("Seuil de fréquence minimum", min_value=1, value=2)
        st.selectbox("Couleur de fond", ["blanc", "noir", "transparent"])

    with col2:
        st.selectbox("Police", ["Arial", "Times New Roman", "Courier New"])
        st.slider("Opacité", 0.0, 1.0, 0.8)

    # Filtres avancés
    st.subheader("🔍 Filtres avancés")

    col1, col2 = st.columns(2)

    with col1:
        st.text_input("Mots à exclure (séparés par des virgules)")
        st.text_input("Mots à inclure uniquement")

    with col2:
        st.number_input("Longueur minimum des mots", min_value=1, value=3)
        st.number_input("Longueur maximum des mots", min_value=1, value=20)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Nuages de Mots - Semantic Pulse X",
        page_icon="☁️",
        layout="wide"
    )

    show_wordcloud_dashboard()
