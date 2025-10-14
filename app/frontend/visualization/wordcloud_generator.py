"""
Générateur de nuages de mots - Semantic Pulse X
Visualisation des vagues émotionnelles avec nuages de mots interactifs
"""

import base64
import io
import re
from collections import Counter
from datetime import datetime
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from wordcloud import WordCloud

from app.backend.core.anonymization import anonymizer


class WordCloudGenerator:
    """Générateur de nuages de mots pour les vagues émotionnelles"""

    def __init__(self):
        self.emotion_colors = {
            'joie': '#FFD700',      # Or
            'colere': '#FF4500',    # Rouge-orange
            'tristesse': '#4169E1', # Bleu royal
            'peur': '#8B0000',      # Rouge foncé
            'surprise': '#FF69B4',  # Rose vif
            'amour': '#FF1493',     # Rose profond
            'neutre': '#808080',    # Gris
            'positif': '#32CD32',   # Vert lime
            'negatif': '#DC143C'    # Rouge cramoisi
        }

        # Mots à exclure (stop words français + mots non-émotionnels)
        self.stop_words = {
            'le', 'la', 'les', 'de', 'du', 'des', 'un', 'une', 'et', 'ou', 'mais', 'donc', 'or', 'ni', 'car',
            'à', 'au', 'aux', 'avec', 'sans', 'pour', 'par', 'sur', 'sous', 'dans', 'entre', 'vers', 'chez',
            'ce', 'cette', 'ces', 'son', 'sa', 'ses', 'mon', 'ma', 'mes', 'ton', 'ta', 'tes', 'notre', 'nos',
            'votre', 'vos', 'leur', 'leurs', 'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles',
            'me', 'te', 'se', 'moi', 'toi', 'lui', 'eux',
            'est', 'sont', 'était', 'étaient', 'sera', 'seront', 'avoir', 'être', 'faire', 'dire', 'aller',
            'voir', 'savoir', 'pouvoir', 'falloir', 'vouloir', 'devoir', 'venir', 'prendre', 'donner',
            'que', 'qui', 'quoi', 'où', 'quand', 'comment', 'pourquoi', 'si', 'comme', 'aussi', 'très',
            'tout', 'tous', 'toute', 'toutes', 'plus', 'moins', 'bien', 'mal', 'grand', 'petit', 'bon',
            'mauvais', 'nouveau', 'ancien', 'premier', 'dernier', 'autre', 'même', 'seul', 'seule',
            # Mots non-émotionnels spécifiques
            'émission', 'épisode', 'suite', 'cest', 'jai', 'hâte'
        }

        # Mots émotionnels à privilégier
        self.emotion_words = {
            'adore', 'génial', 'super', 'nulle', 'déteste', 'excellent', 'fantastique', 'merveilleux',
            'terrible', 'horrible', 'magnifique', 'formidable', 'incroyable', 'extraordinaire',
            'amazing', 'awesome', 'awful', 'wonderful', 'fantastic', 'incredible',
            'love', 'hate', 'like', 'dislike', 'enjoy', 'suffer', 'happy', 'sad', 'angry', 'excited'
        }

    def generate_emotion_wordcloud_with_sources(self,
                                              data: list[dict[str, Any]],
                                              emotion_filter: str | None = None,
                                              max_words: int = 100,
                                              width: int = 800,
                                              height: int = 400) -> dict[str, Any]:
        """Génère un nuage de mots avec traçabilité des sources"""

        # Filtrer par émotion si spécifiée
        if emotion_filter:
            filtered_data = [item for item in data if item.get('emotion') == emotion_filter]
        else:
            filtered_data = data

        if not filtered_data:
            return self._empty_wordcloud()

        # Extraire les textes et sources
        texts = [item['text'] for item in filtered_data]
        sources = [item.get('source', 'unknown') for item in filtered_data]

        # Extraire et nettoyer les mots avec traçabilité
        words_with_sources = self._extract_words_with_sources(texts, sources)

        if not words_with_sources:
            return self._empty_wordcloud()

        # Calculer les fréquences par mot
        word_freq = Counter([word for word, _ in words_with_sources])

        # Créer le nuage de mots
        if emotion_filter and emotion_filter in self.emotion_colors:
            color = self.emotion_colors[emotion_filter]
        else:
            color = '#1f77b4'  # Bleu par défaut

        wordcloud = WordCloud(
            width=width,
            height=height,
            background_color='white',
            max_words=max_words,
            color_func=lambda *args, **kwargs: color,
            relative_scaling=0.5,
            random_state=42,
            colormap='viridis'
        ).generate_from_frequencies(word_freq)

        # Convertir en base64 pour Streamlit
        img_buffer = io.BytesIO()
        plt.figure(figsize=(width/100, height/100))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
        plt.close()

        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()

        # Créer la traçabilité des sources
        source_traceability = self._create_source_traceability(words_with_sources, word_freq)

        return {
            'image': img_base64,
            'word_frequencies': dict(word_freq.most_common(20)),
            'total_words': len(words_with_sources),
            'unique_words': len(word_freq),
            'emotion': emotion_filter or 'all',
            'source_traceability': source_traceability,
            'metadata': {
                'width': width,
                'height': height,
                'max_words': max_words,
                'generated_at': datetime.now().isoformat()
            }
        }

    def generate_emotion_wordcloud(self,
                                 texts: list[str],
                                 emotions: list[str],
                                 emotion_filter: str | None = None,
                                 max_words: int = 100,
                                 width: int = 800,
                                 height: int = 400) -> dict[str, Any]:
        """Génère un nuage de mots pour une émotion spécifique"""

        # Filtrer par émotion si spécifiée
        if emotion_filter:
            filtered_data = [(text, emotion) for text, emotion in zip(texts, emotions, strict=False)
                           if emotion == emotion_filter]
            if not filtered_data:
                return self._empty_wordcloud()
            texts, emotions = zip(*filtered_data, strict=False)

        # Extraire et nettoyer les mots
        words = self._extract_words(texts)

        if not words:
            return self._empty_wordcloud()

        # Calculer les fréquences
        word_freq = Counter(words)

        # Créer le nuage de mots
        if emotion_filter and emotion_filter in self.emotion_colors:
            color = self.emotion_colors[emotion_filter]
        else:
            color = '#1f77b4'  # Bleu par défaut

        wordcloud = WordCloud(
            width=width,
            height=height,
            background_color='white',
            max_words=max_words,
            color_func=lambda *args, **kwargs: color,
            relative_scaling=0.5,
            random_state=42,
            colormap='viridis'
        ).generate_from_frequencies(word_freq)

        # Convertir en base64 pour Streamlit
        img_buffer = io.BytesIO()
        plt.figure(figsize=(width/100, height/100))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
        plt.close()

        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()

        return {
            'image': img_base64,
            'word_frequencies': dict(word_freq.most_common(20)),
            'total_words': len(words),
            'unique_words': len(word_freq),
            'emotion': emotion_filter or 'all',
            'metadata': {
                'width': width,
                'height': height,
                'max_words': max_words,
                'generated_at': datetime.now().isoformat()
            }
        }

    def generate_temporal_wordclouds(self,
                                   data: list[dict[str, Any]],
                                   time_window: str = 'hour',
                                   max_words: int = 50) -> list[dict[str, Any]]:
        """Génère des nuages de mots temporels"""

        if not data:
            return []

        # Convertir en DataFrame
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Grouper par fenêtre temporelle
        if time_window == 'hour':
            df['time_group'] = df['timestamp'].dt.floor('H')
        elif time_window == 'day':
            df['time_group'] = df['timestamp'].dt.floor('D')
        elif time_window == 'week':
            df['time_group'] = df['timestamp'].dt.floor('W')
        else:
            df['time_group'] = df['timestamp'].dt.floor('H')

        # Générer un nuage par période
        wordclouds = []

        for time_group, group_data in df.groupby('time_group'):
            texts = group_data['text'].tolist()
            emotions = group_data.get('emotion', ['neutre'] * len(texts)).tolist()

            # Nuage global pour cette période
            wordcloud = self.generate_emotion_wordcloud(
                texts, emotions, max_words=max_words, width=600, height=300
            )

            wordcloud['time_group'] = time_group.isoformat()
            wordcloud['count'] = len(group_data)
            wordclouds.append(wordcloud)

        return sorted(wordclouds, key=lambda x: x['time_group'])

    def generate_emotion_comparison_wordclouds(self,
                                             data: list[dict[str, Any]],
                                             emotions: list[str],
                                             max_words: int = 50) -> dict[str, Any]:
        """Génère des nuages de mots pour comparer les émotions"""

        if not data:
            return {}

        df = pd.DataFrame(data)
        comparison = {}

        for emotion in emotions:
            emotion_data = df[df['emotion'] == emotion]

            if len(emotion_data) > 0:
                texts = emotion_data['text'].tolist()
                wordcloud = self.generate_emotion_wordcloud(
                    texts, [emotion] * len(texts),
                    emotion_filter=emotion,
                    max_words=max_words,
                    width=400,
                    height=300
                )

                comparison[emotion] = {
                    'wordcloud': wordcloud,
                    'count': len(emotion_data),
                    'percentage': (len(emotion_data) / len(df)) * 100
                }

        return comparison

    def generate_trending_words_cloud(self,
                                    data: list[dict[str, Any]],
                                    time_periods: int = 3,
                                    max_words: int = 30) -> dict[str, Any]:
        """Génère un nuage de mots des tendances"""

        if not data:
            return self._empty_wordcloud()

        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Diviser en périodes
        df = df.sort_values('timestamp')
        period_size = len(df) // time_periods

        trending_words = {}

        for i in range(time_periods):
            start_idx = i * period_size
            end_idx = (i + 1) * period_size if i < time_periods - 1 else len(df)

            period_data = df.iloc[start_idx:end_idx]
            texts = period_data['text'].tolist()

            # Extraire les mots
            words = self._extract_words(texts)
            word_freq = Counter(words)

            # Calculer les tendances
            for word, freq in word_freq.items():
                if word not in trending_words:
                    trending_words[word] = [0] * time_periods
                trending_words[word][i] = freq

        # Calculer les mots en tendance
        trending_scores = {}
        for word, frequencies in trending_words.items():
            if len(frequencies) >= 2:
                # Calculer la tendance (croissance)
                trend = (frequencies[-1] - frequencies[0]) / max(frequencies[0], 1)
                trending_scores[word] = trend

        # Prendre les mots les plus en tendance
        top_trending = dict(Counter(trending_scores).most_common(max_words))

        # Créer le nuage de mots
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            max_words=max_words,
            colormap='RdYlBu_r',  # Rouge-jaune-bleu pour les tendances
            relative_scaling=0.5,
            random_state=42
        ).generate_from_frequencies(top_trending)

        # Convertir en base64
        img_buffer = io.BytesIO()
        plt.figure(figsize=(8, 4))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Mots en tendance', fontsize=16, pad=20)
        plt.tight_layout(pad=0)
        plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
        plt.close()

        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()

        return {
            'image': img_base64,
            'trending_words': top_trending,
            'trending_scores': trending_scores,
            'metadata': {
                'time_periods': time_periods,
                'max_words': max_words,
                'generated_at': datetime.now().isoformat()
            }
        }

    def generate_interactive_wordcloud(self,
                                     data: list[dict[str, Any]],
                                     emotion: str | None = None) -> go.Figure:
        """Génère un nuage de mots interactif avec Plotly"""

        if not data:
            return self._empty_plotly_figure()

        # Filtrer par émotion si spécifiée
        if emotion:
            data = [item for item in data if item.get('emotion') == emotion]

        if not data:
            return self._empty_plotly_figure()

        # Extraire les mots
        texts = [item['text'] for item in data]
        words = self._extract_words(texts)
        word_freq = Counter(words)

        # Prendre les mots les plus fréquents
        top_words = dict(word_freq.most_common(50))

        # Créer les données pour le graphique
        words_list = list(top_words.keys())
        frequencies = list(top_words.values())

        # Créer le graphique en barres horizontales
        fig = go.Figure(data=[
            go.Bar(
                y=words_list,
                x=frequencies,
                orientation='h',
                marker={
                    'color': frequencies,
                    'colorscale': 'Viridis',
                    'showscale': True,
                    'colorbar': {'title': "Fréquence"}
                },
                text=frequencies,
                textposition='auto',
                hovertemplate='<b>%{y}</b><br>Fréquence: %{x}<extra></extra>'
            )
        ])

        fig.update_layout(
            title=f'Nuage de mots interactif - {emotion or "Toutes les émotions"}',
            xaxis_title='Fréquence',
            yaxis_title='Mots',
            height=600,
            showlegend=False,
            margin={'l': 100, 'r': 50, 't': 50, 'b': 50}
        )

        return fig

    def _extract_words_with_sources(self, texts: list[str], sources: list[str]) -> list[tuple[str, str]]:
        """Extrait et nettoie les mots avec traçabilité des sources"""
        words_with_sources = []

        for text, source in zip(texts, sources, strict=False):
            if not text:
                continue

            # Nettoyer le texte
            text = anonymizer.anonymize_text(text)
            text = text.lower()

            # Supprimer la ponctuation et extraire les mots
            words_in_text = re.findall(r'\b[a-zA-Zàâäéèêëïîôöùûüÿçñ]+\b', text)

            # Filtrer les stop words et mots courts, privilégier les mots émotionnels
            filtered_words = []
            for word in words_in_text:
                if (word not in self.stop_words
                    and len(word) > 2
                    and not word.isdigit()):
                    # Privilégier les mots émotionnels
                    if word in self.emotion_words:
                        filtered_words.extend([word] * 3)  # Poids x3 pour les mots émotionnels
                    else:
                        filtered_words.append(word)

            # Associer chaque mot à sa source
            for word in filtered_words:
                words_with_sources.append((word, source))

        return words_with_sources

    def _create_source_traceability(self, words_with_sources: list[tuple[str, str]], word_freq: Counter) -> dict[str, Any]:
        """Crée la traçabilité des sources pour chaque mot"""
        source_traceability = {}

        # Grouper les mots par fréquence
        for word, freq in word_freq.most_common(20):  # Top 20 mots
            # Trouver toutes les sources pour ce mot
            word_sources = [source for w, source in words_with_sources if w == word]
            source_counts = Counter(word_sources)

            source_traceability[word] = {
                'frequency': freq,
                'sources': dict(source_counts),
                'total_sources': len(source_counts),
                'main_source': source_counts.most_common(1)[0][0] if source_counts else 'unknown'
            }

        return source_traceability

    def _extract_words(self, texts: list[str]) -> list[str]:
        """Extrait et nettoie les mots des textes"""
        words = []

        for text in texts:
            if not text:
                continue

            # Nettoyer le texte
            text = anonymizer.anonymize_text(text)
            text = text.lower()

            # Supprimer la ponctuation et extraire les mots
            words_in_text = re.findall(r'\b[a-zA-Zàâäéèêëïîôöùûüÿçñ]+\b', text)

            # Filtrer les stop words et mots courts
            filtered_words = [
                word for word in words_in_text
                if word not in self.stop_words
                and len(word) > 2
                and not word.isdigit()
            ]

            words.extend(filtered_words)

        return words

    def _empty_wordcloud(self) -> dict[str, Any]:
        """Retourne un nuage de mots vide"""
        return {
            'image': '',
            'word_frequencies': {},
            'total_words': 0,
            'unique_words': 0,
            'emotion': 'none',
            'metadata': {
                'generated_at': datetime.now().isoformat()
            }
        }

    def _empty_plotly_figure(self) -> go.Figure:
        """Retourne une figure Plotly vide"""
        fig = go.Figure()
        fig.add_annotation(
            text="Aucune donnée disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font={'size': 16}
        )
        fig.update_layout(
            title="Nuage de mots interactif",
            height=400,
            showlegend=False
        )
        return fig

    def get_word_statistics(self, data: list[dict[str, Any]]) -> dict[str, Any]:
        """Retourne des statistiques sur les mots"""
        if not data:
            return {}

        texts = [item['text'] for item in data]
        words = self._extract_words(texts)
        word_freq = Counter(words)

        return {
            'total_words': len(words),
            'unique_words': len(word_freq),
            'most_common': dict(word_freq.most_common(20)),
            'average_word_length': np.mean([len(word) for word in words]),
            'vocabulary_richness': len(word_freq) / len(words) if words else 0
        }


# Instance globale
wordcloud_generator = WordCloudGenerator()
