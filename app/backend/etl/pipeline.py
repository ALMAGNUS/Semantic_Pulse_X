"""
Pipeline ETL - Semantic Pulse X
Orchestration et traitement des données
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from app.backend.ai.embeddings import embedding_engine
from app.backend.ai.emotion_classifier import emotion_classifier
from app.backend.ai.topic_clustering import topic_clustering
from app.backend.etl.data_sources import data_source_manager

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ETLPipeline:
    """Pipeline ETL principal"""

    def __init__(self):
        self.data_dir = Path("data")
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        self.models_dir = self.data_dir / "models"

        # Créer les répertoires
        for dir_path in [self.raw_dir, self.processed_dir, self.models_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    def run_full_pipeline(self) -> dict[str, Any]:
        """Exécute le pipeline ETL complet"""
        logger.info("🚀 Démarrage du pipeline ETL")

        try:
            # 1. Extraction
            logger.info("📥 Phase d'extraction...")
            raw_data = self._extract_data()

            # 2. Transformation
            logger.info("🔄 Phase de transformation...")
            processed_data = self._transform_data(raw_data)

            # 3. Chargement
            logger.info("💾 Phase de chargement...")
            self._load_data(processed_data)

            # 4. Analyse IA
            logger.info("🧠 Phase d'analyse IA...")
            ai_results = self._run_ai_analysis(processed_data)

            # 5. Génération du rapport
            logger.info("📊 Génération du rapport...")
            report = self._generate_report(raw_data, processed_data, ai_results)

            logger.info("✅ Pipeline ETL terminé avec succès")
            return report

        except Exception as e:
            logger.error(f"❌ Erreur pipeline ETL: {e}")
            return {"error": str(e), "success": False}

    def _extract_data(self) -> dict[str, list[dict[str, Any]]]:
        """Extrait les données de toutes les sources"""
        return data_source_manager.fetch_all_sources()

    def _transform_data(self, raw_data: dict[str, list[dict[str, Any]]]) -> pd.DataFrame:
        """Transforme et nettoie les données"""
        all_data = []

        for source_name, data in raw_data.items():
            if not data:
                continue

            # Convertir en DataFrame
            df = pd.DataFrame(data)

            # Ajouter la source
            df['source_type'] = source_name

            # Standardiser les colonnes
            df = self._standardize_columns(df)

            # Nettoyer les données
            df = self._clean_data(df)

            all_data.append(df)

        if not all_data:
            return pd.DataFrame()

        # Concaténer tous les DataFrames
        combined_df = pd.concat(all_data, ignore_index=True)

        # Dédupliquer
        combined_df = self._deduplicate_data(combined_df)

        # Sauvegarder
        output_path = self.processed_dir / "processed_data.parquet"
        combined_df.to_parquet(output_path, index=False)
        logger.info(f"✅ Données transformées sauvegardées: {output_path}")

        return combined_df

    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardise les colonnes"""
        # Mapping des colonnes
        column_mapping = {
            'texte': 'text',
            'emotion': 'emotion',
            'polarite': 'polarity',
            'timestamp': 'timestamp',
            'programme': 'program',
            'chaine': 'channel',
            'genre': 'genre'
        }

        # Renommer les colonnes
        df = df.rename(columns=column_mapping)

        # Ajouter des colonnes manquantes
        if 'text' not in df.columns:
            df['text'] = ''
        if 'emotion' not in df.columns:
            df['emotion'] = 'neutre'
        if 'polarity' not in df.columns:
            df['polarity'] = 0.0
        if 'timestamp' not in df.columns:
            df['timestamp'] = datetime.now()

        return df

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Nettoie les données"""
        # Supprimer les lignes vides
        df = df.dropna(subset=['text'])

        # Nettoyer le texte
        df['text'] = df['text'].astype(str).str.strip()
        df = df[df['text'].str.len() > 0]

        # Convertir les timestamps
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])

        # Nettoyer les émotions
        valid_emotions = ['joie', 'colere', 'tristesse', 'surprise', 'peur', 'neutre', 'positif', 'negatif']
        df['emotion'] = df['emotion'].apply(
            lambda x: x if x in valid_emotions else 'neutre'
        )

        # Nettoyer la polarité
        df['polarity'] = pd.to_numeric(df['polarity'], errors='coerce')
        df['polarity'] = df['polarity'].fillna(0.0)
        df['polarity'] = df['polarity'].clip(-1.0, 1.0)

        return df

    def _deduplicate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Supprime les doublons"""
        # Dédupliquer basé sur le texte et le timestamp
        df = df.drop_duplicates(subset=['text', 'timestamp'], keep='first')

        # Supprimer les textes trop similaires (basé sur les embeddings)
        df = self._remove_similar_texts(df)

        return df

    def _remove_similar_texts(self, df: pd.DataFrame, similarity_threshold: float = 0.9) -> pd.DataFrame:
        """Supprime les textes trop similaires"""
        if len(df) < 2:
            return df

        # Échantillonner pour éviter les calculs trop lourds
        sample_size = min(1000, len(df))
        df_sample = df.sample(n=sample_size, random_state=42)

        # Calculer les similarités
        texts = df_sample['text'].tolist()
        embeddings = embedding_engine.encode_batch(texts)

        if len(embeddings) == 0:
            return df

        # Matrice de similarité
        similarity_matrix = np.dot(embeddings, embeddings.T)

        # Trouver les paires similaires
        similar_pairs = []
        for i in range(len(similarity_matrix)):
            for j in range(i+1, len(similarity_matrix)):
                if similarity_matrix[i][j] > similarity_threshold:
                    similar_pairs.append((i, j))

        # Supprimer les doublons
        indices_to_remove = set()
        for _i, j in similar_pairs:
            indices_to_remove.add(j)  # Garder le premier, supprimer le second

        # Filtrer
        df_sample = df_sample.drop(df_sample.index[list(indices_to_remove)])

        return df_sample

    def _load_data(self, df: pd.DataFrame) -> dict[str, Any]:
        """Charge les données dans la base"""
        if df.empty:
            return {"error": "Aucune donnée à charger"}

        # Sauvegarder les données finales
        final_path = self.processed_dir / "final_data.parquet"
        df.to_parquet(final_path, index=False)

        # Générer des statistiques
        stats = {
            "total_records": len(df),
            "sources": df['source_type'].value_counts().to_dict(),
            "emotions": df['emotion'].value_counts().to_dict(),
            "date_range": {
                "start": df['timestamp'].min().isoformat(),
                "end": df['timestamp'].max().isoformat()
            },
            "avg_polarity": df['polarity'].mean(),
            "file_path": str(final_path)
        }

        logger.info(f"✅ {len(df)} enregistrements chargés")
        return stats

    def _run_ai_analysis(self, df: pd.DataFrame) -> dict[str, Any]:
        """Exécute l'analyse IA"""
        if df.empty:
            return {"error": "Aucune donnée à analyser"}

        results = {}

        try:
            # Classification émotionnelle
            logger.info("🎭 Classification émotionnelle...")
            texts = df['text'].tolist()
            emotion_results = emotion_classifier.classify_batch(texts)

            # Mettre à jour les données avec les résultats IA
            df['ai_emotion'] = [r['emotion_principale'] for r in emotion_results]
            df['ai_polarity'] = [r['polarite'] for r in emotion_results]
            df['ai_confidence'] = [r['confiance'] for r in emotion_results]

            results['emotion_classification'] = {
                "total_processed": len(emotion_results),
                "emotion_distribution": emotion_classifier.get_emotion_distribution(texts)
            }

            # Clustering thématique
            logger.info("📊 Clustering thématique...")
            topic_results = topic_clustering.fit_topics(texts)
            results['topic_clustering'] = topic_results

            # Sauvegarder les résultats IA
            ai_path = self.processed_dir / "ai_analysis_results.parquet"
            df.to_parquet(ai_path, index=False)

            logger.info("✅ Analyse IA terminée")

        except Exception as e:
            logger.error(f"❌ Erreur analyse IA: {e}")
            results['error'] = str(e)

        return results

    def _generate_report(self, raw_data: dict, processed_data: pd.DataFrame, ai_results: dict) -> dict[str, Any]:
        """Génère un rapport final"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "pipeline_status": "completed",
            "raw_data_stats": {
                source: len(data) for source, data in raw_data.items()
            },
            "processed_data_stats": {
                "total_records": len(processed_data),
                "columns": list(processed_data.columns),
                "memory_usage": processed_data.memory_usage(deep=True).sum()
            },
            "ai_analysis": ai_results,
            "data_quality": {
                "missing_values": processed_data.isnull().sum().to_dict(),
                "duplicate_rate": processed_data.duplicated().sum() / len(processed_data),
                "text_length_stats": {
                    "mean": processed_data['text'].str.len().mean(),
                    "std": processed_data['text'].str.len().std(),
                    "min": processed_data['text'].str.len().min(),
                    "max": processed_data['text'].str.len().max()
                }
            }
        }

        # Sauvegarder le rapport
        report_path = self.processed_dir / "pipeline_report.json"
        import json
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)

        logger.info(f"✅ Rapport généré: {report_path}")
        return report


# Instance globale
etl_pipeline = ETLPipeline()
