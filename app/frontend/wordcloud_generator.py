"""
Générateur de nuages de mots pour Semantic Pulse X
"""

import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from wordcloud import WordCloud


def generate_wordcloud_from_data():
    """Génère un nuage de mots à partir des données collectées"""

    # Collecter tous les textes
    texts = []

    try:
        # Textes YouTube
        youtube_files = list(Path("data/raw/external_apis").glob("hugo_*.json"))
        for file in youtube_files:
            with open(file, encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        if 'title' in item:
                            texts.append(item['title'])
                        if 'description' in item:
                            texts.append(item['description'])

        # Textes Web Scraping
        scraping_files = list(Path("data/raw/web_scraping").glob("*.json"))
        for file in scraping_files:
            with open(file, encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        if 'title' in item:
                            texts.append(item['title'])
                        if 'content' in item:
                            texts.append(item['content'])

        # Textes Kaggle
        kaggle_file = Path("data/raw/kaggle_tweets/sentiment140.csv")
        if kaggle_file.exists():
            df = pd.read_csv(kaggle_file)
            texts.extend(df['text'].astype(str).tolist())

    except Exception as e:
        st.error(f"Erreur lors de la collecte des textes: {e}")
        return None

    if not texts:
        st.warning("Aucun texte trouvé pour générer le nuage de mots")
        return None

    # Normalisation & nettoyage
    all_text = " ".join(texts).lower()
    all_text = all_text.replace("aujourd hui", "aujourd'hui").replace("c '", "c'").replace("l '", "l'")
    all_text = re.sub(r"[^a-z0-9àâäéèêëîïôöùûüç'\s]", " ", all_text)
    all_text = re.sub(r"\s+", " ", all_text).strip()

    # Stopwords FR/EN élargis (auxiliaires, négations, pronoms, prépositions)
    stop_words = {
        'le','la','les','de','du','des','un','une','et','ou','mais','donc','or','ni','car','en','dans','sur','sous','chez','avec','sans','pour','par','plus','moins','tres','très','comme','quand','que','qui','quoi','où','afin','ainsi','alors','depuis','entre','vers','aux','au','ses','ces','mes','tes','nos','vos','leurs','son','sa','notre','votre','leur','ce','cet','cette','cela','ça','ca','c','l','d','n','m','t','se','y','on','nous','vous','ils','elles','je','tu','il','elle','me','te','toi','moi','lui','eux',
        'etre','est','suis','es','sommes','etes','êtes','sont','ete','été','avoir','ai','as','a','avons','avez','ont','avait','avaient','fait','faire','fais','faisons','faites','font','peut','peux','pouvoir','doit','dois','devoir','aller','vais','va','allons','allez','vont',
        'pas','non','ne','rien','jamais','toujours','ici','là','bien','mal','aussi','encore','deja','déjà','trop','peu','beaucoup','vraiment',
        'aujourd','hui','aujourd\'hui','demain','hier',
        # contractions courantes
        "c'","cest","c'est","n'","j'","l'","d'","qu'",
        'the','and','but','in','at','to','for','of','with','by','is','are','was','were','an','this','that','these','those','i','you','he','she','it','we','they','my','your','his','her','its','our','their','from','be'
    }

    raw_tokens = all_text.split()
    tokens = [
        tok for tok in raw_tokens
        if tok not in stop_words
        and not tok.startswith(("c'","n'","j'","l'","d'","qu'"))
        and len(tok) > 2 and not tok.isdigit()
    ]
    word_counts = Counter(tokens)

    # Ajouter quelques bigrammes fréquents pour contexte
    bigrams = []
    verbs_context = {"aime","adore","deteste","déteste","kiffe","apprécie","apprecie"}
    for _i, (w1, w2) in enumerate(zip(tokens, tokens[1:], strict=False)):
        if w1 in verbs_context and w2 not in stop_words and len(w2) > 2:
            # privilégier le contexte: "aime X"
            bigrams.append(f"{w1} {w2}")
            # option: diminuer le poids du verbe seul
            if word_counts[w1] > 0:
                word_counts[w1] -= 1
        elif w1 not in stop_words and w2 not in stop_words and all(len(w) > 2 for w in (w1, w2)):
            bigrams.append(f"{w1} {w2}")
    word_counts.update(Counter(bigrams).most_common(50))

    # Créer le nuage de mots
    if word_counts:
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap='viridis',
            max_words=100,
            relative_scaling=0.5,
            random_state=42,
            collocations=True,
            stopwords=stop_words
        ).generate_from_frequencies(word_counts)

        return wordcloud, word_counts
    else:
        return None, None

def generate_wordcloud_for_event(event_description: str):
    """Génère un nuage de mots spécifique pour un événement"""
    
    st.subheader(f"🎯 Nuage de Mots pour: {event_description}")
    
    # Debug
    st.info(f"🔍 Recherche de textes pour: '{event_description}'")
    
    # Rechercher des données liées à cet événement
    related_texts = search_texts_for_event(event_description)
    
    st.info(f"📊 {len(related_texts)} textes trouvés")
    
    if related_texts:
        # Générer le nuage spécifique
        wordcloud_fig = create_wordcloud_from_texts(related_texts, title=f"Mots-clés: {event_description}")
        if wordcloud_fig:
            st.pyplot(wordcloud_fig)
        else:
            st.error("❌ Erreur lors de la génération du nuage de mots")
        
        # Afficher les textes trouvés
        with st.expander(f"📄 Textes trouvés pour '{event_description}' ({len(related_texts)} textes)"):
            for i, text in enumerate(related_texts[:10], 1):  # Limiter à 10
                st.write(f"**{i}.** {text[:200]}...")
    else:
        st.warning(f"⚠️ Aucun texte trouvé pour l'événement '{event_description}'")
        st.write("**Conseil :** Lancez une collecte de données pour cet événement")
        
        # Fallback : utiliser le nuage général
        st.info("🔄 Génération du nuage de mots général...")
        wordcloud_fig = get_cached_wordcloud()
        if wordcloud_fig:
            st.pyplot(wordcloud_fig)

def search_texts_for_event(event_description: str):
    """Recherche des textes liés à un événement spécifique"""
    
    # Mots-clés de l'événement (plus intelligents)
    keywords = event_description.lower().split()
    
    # Ajouter des mots-clés politiques français
    political_keywords = [
        'gouvernement', 'ministre', 'président', 'assemblée', 'sénat',
        'réforme', 'loi', 'budget', 'retraite', 'chômage', 'économie',
        'écologie', 'santé', 'éducation', 'sécurité', 'immigration',
        'france', 'français', 'française', 'politique'
    ]
    
    # Combiner les mots-clés
    all_keywords = keywords + [kw for kw in political_keywords if any(kw in event_description.lower() for kw in political_keywords)]
    
    all_texts = collect_all_texts()
    related_texts = []
    
    if not all_texts:
        # Si pas de textes, utiliser les données de session temps réel
        if 'realtime_analysis' in st.session_state:
            realtime_data = st.session_state['realtime_analysis']
            return realtime_data.get('texts', [])
        return []
    
    for text in all_texts:
        text_lower = text.lower()
        # Vérifier si au moins un mot-clé est présent
        if any(keyword in text_lower for keyword in all_keywords):
            related_texts.append(text)
    
    # Si pas de textes trouvés, retourner tous les textes (fallback)
    if not related_texts and all_texts:
        related_texts = all_texts[:10]  # Limiter à 10 pour éviter les problèmes
    
    return related_texts

def create_wordcloud_from_texts(texts, title="Nuage de Mots"):
    """Crée un nuage de mots à partir d'une liste de textes"""
    
    if not texts:
        return None
    
    # Combiner tous les textes
    combined_text = " ".join(texts)
    
    # Générer le nuage de mots
    wordcloud = WordCloud(
        width=800, height=400,
        background_color='white',
        max_words=100,
        colormap='viridis'
    ).generate(combined_text)
    
    # Créer la figure
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(title, fontsize=16, pad=20)
    
    return fig

def show_wordcloud_dashboard():
    """Affiche le dashboard des nuages de mots"""

    st.header("☁️ Nuages de Mots")
    st.subheader("Analyse sémantique des données collectées")
    
    # Vérifier s'il y a une prédiction récente à analyser
    if 'generate_wordcloud_for' in st.session_state:
        st.info(f"🎯 **Analyse programmée pour :** {st.session_state['generate_wordcloud_for']}")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("**Recherche de données liées à cet événement...**")
        with col2:
            if st.button("🚀 Générer Maintenant", key="generate_now"):
                # Générer le nuage pour cet événement spécifique
                generate_wordcloud_for_event(st.session_state['generate_wordcloud_for'])
                del st.session_state['generate_wordcloud_for']  # Nettoyer
                st.rerun()
        
        st.divider()

    # Bouton de mise à jour
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Mettre à jour le nuage de mots", type="primary"):
            # Invalider le cache
            st.cache_data.clear()
            st.success("✅ Cache vidé ! Génération du nouveau nuage...")
            st.rerun()

    # Générer le nuage de mots avec cache intelligent
    @st.cache_data(ttl=300)  # Cache de 5 minutes
    def get_cached_wordcloud():
        return generate_wordcloud_from_data()
    
    with st.spinner("Génération du nuage de mots..."):
        wordcloud, word_counts = get_cached_wordcloud()

    if wordcloud and word_counts:
        # Afficher le nuage de mots
        st.subheader("📊 Nuage de mots global")

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('Mots-clés les plus fréquents', fontsize=16, pad=20)

        st.pyplot(fig)

        # Top mots
        st.subheader("🔝 Top 20 des mots les plus fréquents")

        top_words = word_counts.most_common(20)
        words_df = pd.DataFrame(top_words, columns=['Mot', 'Fréquence'])

        # Graphique en barres
        fig_bar = plt.figure(figsize=(10, 6))
        plt.barh(range(len(words_df)), words_df['Fréquence'])
        plt.yticks(range(len(words_df)), words_df['Mot'])
        plt.xlabel('Fréquence')
        plt.title('Top 20 des mots les plus fréquents')
        plt.gca().invert_yaxis()

        st.pyplot(fig_bar)

        # Tableau des mots
        st.subheader("📋 Détail des fréquences")
        st.dataframe(words_df, use_container_width=True)

        # Statistiques
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total de mots uniques", len(word_counts))

        with col2:
            st.metric("Mot le plus fréquent", f"{top_words[0][0]} ({top_words[0][1]})")

        with col3:
            total_words = sum(word_counts.values())
            st.metric("Total de mots", total_words)
        
        # Indicateur de dernière mise à jour
        st.info(f"🕒 Dernière mise à jour: {datetime.now().strftime('%H:%M:%S')}")

        # Analyse par source
        st.subheader("📊 Analyse par source de données")

        sources_analysis = {
            'YouTube': 0,
            'Web Scraping': 0,
            'Kaggle': 0
        }

        try:
            # Compter les fichiers YouTube
            youtube_files = list(Path("data/raw/external_apis").glob("hugo_*.json"))
            sources_analysis['YouTube'] = len(youtube_files) * 15

            # Compter les fichiers Web Scraping
            scraping_files = list(Path("data/raw/web_scraping").glob("*.json"))
            sources_analysis['Web Scraping'] = len(scraping_files) * 10

            # Compter les tweets Kaggle
            kaggle_file = Path("data/raw/kaggle_tweets/sentiment140.csv")
            if kaggle_file.exists():
                df = pd.read_csv(kaggle_file)
                sources_analysis['Kaggle'] = len(df)

        except Exception as e:
            st.warning(f"Erreur lors de l'analyse par source: {e}")

        # Graphique des sources
        sources_df = pd.DataFrame(list(sources_analysis.items()), columns=['Source', 'Volume'])

        fig_sources = plt.figure(figsize=(6, 6))
        # Dessiner le camembert sans labels pour éviter le chevauchement
        wedges, texts, autotexts = plt.pie(
            sources_df['Volume'],
            labels=None,
            autopct='%1.1f%%',
            pctdistance=0.8,
            labeldistance=1.15,
            startangle=90,
            textprops={'fontsize': 10}
        )
        plt.title('Répartition des données par source', fontsize=14, pad=12)
        plt.axis('equal')
        # Légende propre sur la droite
        plt.legend(
            wedges,
            sources_df['Source'],
            title='Sources',
            loc='center left',
            bbox_to_anchor=(1, 0.5),
            frameon=False
        )
        plt.tight_layout()
        st.pyplot(fig_sources)

    else:
        st.error("Impossible de générer le nuage de mots. Vérifiez que des données ont été collectées.")

        # Instructions
        st.info("""
        **Pour générer un nuage de mots :**
        1. Lancez une collecte YouTube : `python scripts/collect_hugo_youtube.py`
        2. Lancez une collecte Web Scraping : `python scripts/collect_web_scraping.py`
        3. Vérifiez que les fichiers Kaggle sont présents
        4. Rechargez cette page
        """)

if __name__ == "__main__":
    show_wordcloud_dashboard()
