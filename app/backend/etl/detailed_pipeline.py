"""
Pipeline ETL Détaillé - Semantic Pulse X
Implémentation complète des techniques de Data Engineering
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import hashlib
import json
import re
from pathlib import Path
import logging

from sqlalchemy import create_engine, text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import SequenceMatcher
from fuzzywuzzy import fuzz, process

from app.backend.core.config import settings
from app.backend.core.anonymization import anonymizer

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DetailedETLPipeline:
    """
    Pipeline ETL détaillé pour traitement complet des données
    """
    
    def __init__(self):
        self.pipeline_results = {
            'start_time': datetime.now(),
            'steps_completed': [],
            'errors': [],
            'metrics': {},
            'final_records': 0
        }
    
    def run_complete_pipeline(self) -> Dict[str, Any]:
        """
        Exécution du pipeline ETL complet
        """
        logger.info("🚀 Démarrage du pipeline ETL détaillé...")
        
        try:
            # ÉTAPE 1: Extraction
            self._step_1_extraction()
            
            # ÉTAPE 2: Nettoyage
            self._step_2_cleaning()
            
            # ÉTAPE 3: Dédoublonnage
            self._step_3_deduplication()
            
            # ÉTAPE 4: Homogénéisation
            self._step_4_homogenization()
            
            # ÉTAPE 5: Agrégation multi-sources
            self._step_5_aggregation()
            
            # ÉTAPE 6: Jointures
            self._step_6_joins()
            
            # ÉTAPE 7: Chargement
            self._step_7_loading()
            
            # Monitoring final
            self._final_monitoring()
            
        except Exception as e:
            error_msg = f"Erreur critique dans le pipeline: {str(e)}"
            logger.error(error_msg)
            self.pipeline_results['errors'].append(error_msg)
        
        return self.pipeline_results
    
    def _step_1_extraction(self):
        """ÉTAPE 1: Extraction des données"""
        logger.info("="*50)
        logger.info("ÉTAPE 1: EXTRACTION DES DONNÉES")
        logger.info("="*50)
        
        sources_data = {}
        
        # Extraction de chaque source
        sources_data['file'] = self._extract_csv_data()
        sources_data['sql'] = self._extract_sql_data()
        sources_data['bigdata'] = self._extract_parquet_data()
        sources_data['scraping'] = self._extract_scraping_data()
        sources_data['api'] = self._extract_api_data()
        
        # Validation des extractions
        total_records = sum(len(df) for df in sources_data.values())
        logger.info(f"📊 Total extrait: {total_records} enregistrements")
        
        self.pipeline_results['sources_data'] = sources_data
        self.pipeline_results['steps_completed'].append('extraction')
        self.pipeline_results['metrics']['extraction_records'] = total_records
    
    def _step_2_cleaning(self):
        """ÉTAPE 2: Nettoyage des données"""
        logger.info("="*50)
        logger.info("ÉTAPE 2: NETTOYAGE DES DONNÉES")
        logger.info("="*50)
        
        cleaned_data = {}
        corruption_reports = {}
        
        for source_name, df in self.pipeline_results['sources_data'].items():
            if df.empty:
                continue
            
            logger.info(f"--- Nettoyage {source_name} ---")
            
            # Détection des données corrompues
            corruption_report = self._detect_corrupted_data(df)
            corruption_reports[source_name] = corruption_report
            
            # Nettoyage des textes
            df_clean = self._clean_text_data(df)
            
            # Nettoyage des timestamps
            df_clean = self._clean_timestamp_data(df_clean)
            
            # Standardisation des types
            df_clean = self._standardize_data_types(df_clean)
            
            cleaned_data[source_name] = df_clean
            
            logger.info(f"✅ {source_name}: {len(df_clean)} lignes nettoyées")
        
        self.pipeline_results['cleaned_data'] = cleaned_data
        self.pipeline_results['corruption_reports'] = corruption_reports
        self.pipeline_results['steps_completed'].append('cleaning')
    
    def _step_3_deduplication(self):
        """ÉTAPE 3: Dédoublonnage"""
        logger.info("="*50)
        logger.info("ÉTAPE 3: DÉDOUBLONNAGE")
        logger.info("="*50)
        
        deduplicated_data = {}
        deduplication_stats = {}
        
        for source_name, df in self.pipeline_results['cleaned_data'].items():
            if df.empty:
                continue
            
            logger.info(f"--- Dédoublonnage {source_name} ---")
            
            initial_count = len(df)
            
            # Suppression des doublons exacts
            df_dedup = self._remove_exact_duplicates(df)
            exact_duplicates = initial_count - len(df_dedup)
            
            # Détection des doublons sémantiques
            df_dedup = self._detect_semantic_duplicates(df_dedup)
            semantic_duplicates = len(df) - len(df_dedup) - exact_duplicates
            
            # Détection des doublons temporels
            df_dedup = self._detect_temporal_duplicates(df_dedup)
            temporal_duplicates = len(df) - len(df_dedup) - exact_duplicates - semantic_duplicates
            
            deduplicated_data[source_name] = df_dedup
            deduplication_stats[source_name] = {
                'initial': initial_count,
                'final': len(df_dedup),
                'exact_duplicates': exact_duplicates,
                'semantic_duplicates': semantic_duplicates,
                'temporal_duplicates': temporal_duplicates,
                'total_removed': initial_count - len(df_dedup)
            }
            
            logger.info(f"✅ {source_name}: {deduplication_stats[source_name]['total_removed']} doublons supprimés")
        
        self.pipeline_results['deduplicated_data'] = deduplicated_data
        self.pipeline_results['deduplication_stats'] = deduplication_stats
        self.pipeline_results['steps_completed'].append('deduplication')
    
    def _step_4_homogenization(self):
        """ÉTAPE 4: Homogénéisation"""
        logger.info("="*50)
        logger.info("ÉTAPE 4: HOMOGÉNÉISATION")
        logger.info("="*50)
        
        homogenized_data = {}
        
        for source_name, df in self.pipeline_results['deduplicated_data'].items():
            if df.empty:
                continue
            
            logger.info(f"--- Homogénéisation {source_name} ---")
            
            # Normalisation des émotions
            df_homo = self._normalize_emotions(df)
            
            # Standardisation des langues
            df_homo = self._standardize_languages(df_homo)
            
            # Mapping vers schéma unifié
            df_homo = self._map_to_unified_schema(df_homo, source_name)
            
            homogenized_data[source_name] = df_homo
            
            logger.info(f"✅ {source_name}: {len(df_homo)} lignes homogénéisées")
        
        self.pipeline_results['homogenized_data'] = homogenized_data
        self.pipeline_results['steps_completed'].append('homogenization')
    
    def _step_5_aggregation(self):
        """ÉTAPE 5: Agrégation multi-sources"""
        logger.info("="*50)
        logger.info("ÉTAPE 5: AGRÉGATION MULTI-SOURCES")
        logger.info("="*50)
        
        # Fusion des sources
        merged_data = self._merge_data_sources(self.pipeline_results['homogenized_data'])
        
        if not merged_data.empty:
            # Création des agrégations temporelles
            aggregations = self._create_temporal_aggregations(merged_data)
            
            # Création des agrégations par émotion
            emotion_aggregations = self._create_emotion_aggregations(merged_data)
            
            self.pipeline_results['merged_data'] = merged_data
            self.pipeline_results['temporal_aggregations'] = aggregations
            self.pipeline_results['emotion_aggregations'] = emotion_aggregations
            
            logger.info(f"✅ Fusion: {len(merged_data)} enregistrements")
            logger.info(f"✅ Agrégations temporelles: {len(aggregations)} enregistrements")
            logger.info(f"✅ Agrégations émotions: {len(emotion_aggregations)} enregistrements")
        
        self.pipeline_results['steps_completed'].append('aggregation')
    
    def _step_6_joins(self):
        """ÉTAPE 6: Jointures"""
        logger.info("="*50)
        logger.info("ÉTAPE 6: JOINTURES")
        logger.info("="*50)
        
        # Chargement des tables de référence
        programmes_df = self._load_programmes_table()
        utilisateurs_df = self._load_utilisateurs_table()
        sources_df = self._load_sources_table()
        
        # Jointures
        final_data = self.pipeline_results['merged_data'].copy()
        
        # Jointure avec les programmes
        final_data = self._join_with_programmes(final_data, programmes_df)
        
        # Jointure avec les utilisateurs
        final_data = self._join_with_utilisateurs(final_data, utilisateurs_df)
        
        # Jointure avec les sources
        final_data = self._join_with_sources(final_data, sources_df)
        
        self.pipeline_results['final_data'] = final_data
        self.pipeline_results['steps_completed'].append('joins')
        
        logger.info(f"✅ Jointures terminées: {len(final_data)} enregistrements finaux")
    
    def _step_7_loading(self):
        """ÉTAPE 7: Chargement"""
        logger.info("="*50)
        logger.info("ÉTAPE 7: CHARGEMENT")
        logger.info("="*50)
        
        final_data = self.pipeline_results['final_data']
        
        # Sauvegarde en PostgreSQL
        self._save_to_postgresql(final_data, 'reactions')
        
        # Sauvegarde en Parquet
        self._save_to_parquet(final_data, 'data/processed/final_data.parquet')
        
        # Sauvegarde des agrégations
        if 'temporal_aggregations' in self.pipeline_results:
            self._save_to_postgresql(
                self.pipeline_results['temporal_aggregations'], 
                'agregations_emotionnelles'
            )
        
        self.pipeline_results['final_records'] = len(final_data)
        self.pipeline_results['steps_completed'].append('loading')
        
        logger.info(f"✅ Chargement terminé: {len(final_data)} enregistrements sauvegardés")
    
    def _final_monitoring(self):
        """Monitoring final du pipeline"""
        logger.info("="*50)
        logger.info("MONITORING FINAL")
        logger.info("="*50)
        
        self.pipeline_results['end_time'] = datetime.now()
        self.pipeline_results['duration'] = (
            self.pipeline_results['end_time'] - self.pipeline_results['start_time']
        )
        
        # Métriques de performance
        duration = self.pipeline_results['duration']
        records = self.pipeline_results['final_records']
        
        logger.info(f"⏱️ Durée totale: {duration}")
        logger.info(f"📊 Enregistrements traités: {records}")
        logger.info(f"⚡ Vitesse: {records / duration.total_seconds():.2f} records/sec")
        
        # Étapes complétées
        logger.info(f"✅ Étapes complétées: {len(self.pipeline_results['steps_completed'])}/7")
        for step in self.pipeline_results['steps_completed']:
            logger.info(f"  - {step}")
        
        # Erreurs
        if self.pipeline_results['errors']:
            logger.error(f"❌ Erreurs: {len(self.pipeline_results['errors'])}")
            for error in self.pipeline_results['errors']:
                logger.error(f"  - {error}")
        else:
            logger.info("✅ Aucune erreur détectée")
        
        # Sauvegarde du rapport
        self._save_pipeline_report()
    
    # Méthodes d'extraction
    def _extract_csv_data(self) -> pd.DataFrame:
        """Extraction des données CSV"""
        try:
            # Simulation de données CSV
            data = {
                'text': [
                    'Super émission hier soir !',
                    'Très décevant, je m\'attendais à mieux',
                    'Excellent travail de l\'équipe',
                    'Pas mal mais peut mieux faire'
                ],
                'timestamp': [
                    '2024-01-15 20:30:00',
                    '2024-01-15 21:00:00',
                    '2024-01-15 21:30:00',
                    '2024-01-15 22:00:00'
                ],
                'emotion': ['joie', 'tristesse', 'joie', 'neutre'],
                'source': ['twitter', 'facebook', 'instagram', 'youtube']
            }
            return pd.DataFrame(data)
        except Exception as e:
            logger.error(f"Erreur extraction CSV: {e}")
            return pd.DataFrame()
    
    def _extract_sql_data(self) -> pd.DataFrame:
        """Extraction des données SQL"""
        try:
            # Simulation de données SQL
            data = {
                'contenu': [
                    'Émission très intéressante',
                    'Contenu décevant',
                    'Bravo pour cette émission'
                ],
                'date_creation': [
                    '2024-01-15 20:45:00',
                    '2024-01-15 21:15:00',
                    '2024-01-15 21:45:00'
                ],
                'emotion_detectee': ['joie', 'colere', 'joie']
            }
            return pd.DataFrame(data)
        except Exception as e:
            logger.error(f"Erreur extraction SQL: {e}")
            return pd.DataFrame()
    
    def _extract_parquet_data(self) -> pd.DataFrame:
        """Extraction des données Parquet"""
        try:
            # Simulation de données Parquet
            data = {
                'tweet_text': [
                    'Great show tonight!',
                    'Disappointed with the content',
                    'Amazing performance'
                ],
                'created_at': [
                    '2024-01-15 20:50:00',
                    '2024-01-15 21:20:00',
                    '2024-01-15 21:50:00'
                ],
                'sentiment': ['positive', 'negative', 'positive']
            }
            return pd.DataFrame(data)
        except Exception as e:
            logger.error(f"Erreur extraction Parquet: {e}")
            return pd.DataFrame()
    
    def _extract_scraping_data(self) -> pd.DataFrame:
        """Extraction des données de scraping"""
        try:
            # Simulation de données de scraping
            data = {
                'article_text': [
                    'Article très informatif',
                    'Contenu peu intéressant',
                    'Excellent article'
                ],
                'publication_date': [
                    '2024-01-15 20:55:00',
                    '2024-01-15 21:25:00',
                    '2024-01-15 21:55:00'
                ],
                'tone': ['positive', 'negative', 'positive']
            }
            return pd.DataFrame(data)
        except Exception as e:
            logger.error(f"Erreur extraction scraping: {e}")
            return pd.DataFrame()
    
    def _extract_api_data(self) -> pd.DataFrame:
        """Extraction des données API"""
        try:
            # Simulation de données API
            data = {
                'description': [
                    'News article about the show',
                    'Critical review of the program',
                    'Positive feedback on the content'
                ],
                'publishedAt': [
                    '2024-01-15T21:00:00Z',
                    '2024-01-15T21:30:00Z',
                    '2024-01-15T22:00:00Z'
                ],
                'mood': ['positive', 'negative', 'positive']
            }
            return pd.DataFrame(data)
        except Exception as e:
            logger.error(f"Erreur extraction API: {e}")
            return pd.DataFrame()
    
    # Méthodes de nettoyage
    def _detect_corrupted_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Détection des données corrompues"""
        corruption_report = {
            'total_rows': len(df),
            'corrupted_rows': 0,
            'issues': []
        }
        
        # Valeurs manquantes critiques
        critical_columns = ['text', 'timestamp']
        for col in critical_columns:
            if col in df.columns:
                missing_count = df[col].isna().sum()
                if missing_count > 0:
                    corruption_report['issues'].append({
                        'type': 'missing_values',
                        'column': col,
                        'count': missing_count,
                        'percentage': (missing_count / len(df)) * 100
                    })
        
        # Textes vides
        if 'text' in df.columns:
            empty_texts = df['text'].fillna('').str.strip().str.len() < 3
            empty_count = empty_texts.sum()
            if empty_count > 0:
                corruption_report['issues'].append({
                    'type': 'empty_text',
                    'count': empty_count,
                    'percentage': (empty_count / len(df)) * 100
                })
        
        corruption_report['corrupted_rows'] = sum(issue['count'] for issue in corruption_report['issues'])
        
        return corruption_report
    
    def _clean_text_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Nettoyage des données textuelles"""
        df_clean = df.copy()
        
        if 'text' not in df_clean.columns:
            return df_clean
        
        # Nettoyage des textes
        text_col = 'text'
        if text_col in df_clean.columns:
            df_clean[text_col] = df_clean[text_col].fillna('').astype(str)
            
            # Suppression des caractères de contrôle
            df_clean[text_col] = df_clean[text_col].str.replace(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', regex=True)
            
            # Normalisation Unicode
            df_clean[text_col] = df_clean[text_col].str.normalize('NFKD')
            
            # Suppression des espaces multiples
            df_clean[text_col] = df_clean[text_col].str.replace(r'\s+', ' ', regex=True)
            
            # Suppression des URLs
            df_clean[text_col] = df_clean[text_col].str.replace(r'https?://\S+', '[URL]', regex=True)
            
            # Suppression des emails
            df_clean[text_col] = df_clean[text_col].str.replace(r'\S+@\S+\.\S+', '[EMAIL]', regex=True)
            
            # Suppression des numéros de téléphone
            df_clean[text_col] = df_clean[text_col].str.replace(r'\+?[0-9]{10,15}', '[PHONE]', regex=True)
            
            # Suppression des mentions @
            df_clean[text_col] = df_clean[text_col].str.replace(r'@\w+', '[MENTION]', regex=True)
            
            # Trim des espaces
            df_clean[text_col] = df_clean[text_col].str.strip()
            
            # Suppression des textes trop courts
            df_clean = df_clean[df_clean[text_col].str.len() >= 3]
        
        return df_clean
    
    def _clean_timestamp_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Nettoyage des timestamps"""
        df_clean = df.copy()
        
        if 'timestamp' not in df_clean.columns:
            return df_clean
        
        # Conversion en datetime
        df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'], errors='coerce')
        
        # Suppression des timestamps invalides
        initial_count = len(df_clean)
        df_clean = df_clean.dropna(subset=['timestamp'])
        removed_count = initial_count - len(df_clean)
        
        if removed_count > 0:
            logger.warning(f"⚠️ {removed_count} timestamps invalides supprimés")
        
        return df_clean
    
    def _standardize_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardisation des types de données"""
        df_std = df.copy()
        
        # Standardisation des colonnes textuelles
        text_columns = ['text', 'emotion_principale', 'langue', 'source']
        for col in text_columns:
            if col in df_std.columns:
                df_std[col] = df_std[col].astype(str).str.strip()
        
        # Standardisation des colonnes numériques
        numeric_columns = ['score_emotion', 'polarite', 'confiance']
        for col in numeric_columns:
            if col in df_std.columns:
                df_std[col] = pd.to_numeric(df_std[col], errors='coerce')
                if col == 'score_emotion':
                    df_std[col] = df_std[col].clip(0, 1)
                elif col == 'polarite':
                    df_std[col] = df_std[col].clip(-1, 1)
                elif col == 'confiance':
                    df_std[col] = df_std[col].clip(0, 1)
        
        return df_std
    
    # Méthodes de dédoublonnage
    def _remove_exact_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Suppression des doublons exacts"""
        return df.drop_duplicates()
    
    def _detect_semantic_duplicates(self, df: pd.DataFrame, threshold: float = 0.85) -> pd.DataFrame:
        """Détection des doublons sémantiques"""
        if 'text' not in df.columns or len(df) < 2:
            return df
        
        # Vectorisation TF-IDF
        texts = df['text'].fillna('').astype(str).tolist()
        vectorizer = TfidfVectorizer(max_features=1000, stop_words='french')
        tfidf_matrix = vectorizer.fit_transform(texts)
        
        # Calcul de la similarité cosinus
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        # Détection des paires similaires
        indices_to_remove = set()
        for i in range(len(similarity_matrix)):
            for j in range(i + 1, len(similarity_matrix)):
                if similarity_matrix[i][j] > threshold:
                    if i not in indices_to_remove and j not in indices_to_remove:
                        indices_to_remove.add(j)
        
        return df.drop(df.index[list(indices_to_remove)])
    
    def _detect_temporal_duplicates(self, df: pd.DataFrame, time_window: str = '1H') -> pd.DataFrame:
        """Détection des doublons temporels"""
        if 'timestamp' not in df.columns or 'text' not in df.columns:
            return df
        
        # Tri par timestamp
        df_sorted = df.sort_values('timestamp').reset_index(drop=True)
        df_sorted['time_window'] = df_sorted['timestamp'].dt.floor(time_window)
        
        # Détection des doublons dans chaque fenêtre
        duplicates_to_remove = []
        
        for time_group, group in df_sorted.groupby('time_window'):
            if len(group) > 1:
                texts = group['text'].fillna('').astype(str).tolist()
                
                if len(texts) > 1:
                    for i in range(len(texts)):
                        for j in range(i + 1, len(texts)):
                            similarity = SequenceMatcher(None, texts[i], texts[j]).ratio()
                            if similarity > 0.8:
                                original_index = group.iloc[j].name
                                duplicates_to_remove.append(original_index)
        
        return df_sorted.drop(duplicates_to_remove)
    
    # Méthodes d'homogénéisation
    def _normalize_emotions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalisation des émotions"""
        df_norm = df.copy()
        
        if 'emotion_principale' not in df_norm.columns:
            return df_norm
        
        # Mapping des émotions
        emotion_mapping = {
            'joy': 'joie', 'happy': 'joie', 'happiness': 'joie',
            'anger': 'colere', 'angry': 'colere', 'mad': 'colere',
            'sadness': 'tristesse', 'sad': 'tristesse',
            'fear': 'peur', 'afraid': 'peur', 'scared': 'peur',
            'surprise': 'surprise', 'surprised': 'surprise',
            'neutral': 'neutre', 'indifferent': 'neutre'
        }
        
        df_norm['emotion_principale'] = df_norm['emotion_principale'].str.lower().map(
            emotion_mapping
        ).fillna(df_norm['emotion_principale'])
        
        # Gestion des émotions non reconnues
        valid_emotions = ['joie', 'colere', 'tristesse', 'peur', 'surprise', 'neutre']
        df_norm['emotion_principale'] = df_norm['emotion_principale'].apply(
            lambda x: x if x in valid_emotions else 'neutre'
        )
        
        return df_norm
    
    def _standardize_languages(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardisation des langues"""
        df_std = df.copy()
        
        if 'langue' not in df_std.columns:
            return df_std
        
        language_mapping = {
            'french': 'fr', 'français': 'fr', 'francais': 'fr',
            'english': 'en', 'anglais': 'en',
            'spanish': 'es', 'espagnol': 'es'
        }
        
        df_std['langue'] = df_std['langue'].str.lower().map(
            language_mapping
        ).fillna(df_std['langue'])
        
        df_std['langue'] = df_std['langue'].fillna('fr')
        
        return df_std
    
    def _map_to_unified_schema(self, df: pd.DataFrame, source_name: str) -> pd.DataFrame:
        """Mapping vers le schéma unifié"""
        schema_mapping = {
            'file': {'text': 'content', 'timestamp': 'created_at', 'emotion': 'sentiment'},
            'sql': {'contenu': 'text', 'date_creation': 'timestamp', 'emotion_detectee': 'emotion_principale'},
            'bigdata': {'tweet_text': 'text', 'created_at': 'timestamp', 'sentiment': 'emotion_principale'},
            'scraping': {'article_text': 'text', 'publication_date': 'timestamp', 'tone': 'emotion_principale'},
            'api': {'description': 'text', 'publishedAt': 'timestamp', 'mood': 'emotion_principale'}
        }
        
        df_mapped = df.copy()
        
        if source_name in schema_mapping:
            mapping = schema_mapping[source_name]
            df_mapped = df_mapped.rename(columns=mapping)
        
        # Ajout des colonnes manquantes
        required_columns = ['text', 'timestamp', 'emotion_principale', 'source_id']
        for col in required_columns:
            if col not in df_mapped.columns:
                if col == 'source_id':
                    df_mapped[col] = source_name
                else:
                    df_mapped[col] = None
        
        return df_mapped
    
    # Méthodes d'agrégation
    def _merge_data_sources(self, sources_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Fusion des sources de données"""
        merged_data = []
        
        for source_name, df in sources_data.items():
            if df.empty:
                continue
            
            df['source_name'] = source_name
            merged_data.append(df)
        
        if not merged_data:
            return pd.DataFrame()
        
        return pd.concat(merged_data, ignore_index=True, sort=False)
    
    def _create_temporal_aggregations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Création d'agrégations temporelles"""
        if 'timestamp' not in df.columns:
            return pd.DataFrame()
        
        # Agrégation par heure
        df['hour'] = df['timestamp'].dt.floor('H')
        hourly_agg = df.groupby(['hour', 'emotion_principale']).agg({
            'text': 'count',
            'score_emotion': 'mean',
            'polarite': 'mean'
        }).reset_index()
        
        hourly_agg.columns = ['timestamp', 'emotion', 'count', 'avg_score', 'avg_polarity']
        hourly_agg['aggregation_level'] = 'hourly'
        
        return hourly_agg
    
    def _create_emotion_aggregations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Création d'agrégations par émotion"""
        if 'emotion_principale' not in df.columns:
            return pd.DataFrame()
        
        emotion_agg = df.groupby('emotion_principale').agg({
            'text': 'count',
            'score_emotion': 'mean',
            'polarite': 'mean',
            'confiance': 'mean'
        }).reset_index()
        
        emotion_agg.columns = ['emotion', 'count', 'avg_score', 'avg_polarity', 'avg_confidence']
        
        return emotion_agg
    
    # Méthodes de jointures
    def _load_programmes_table(self) -> pd.DataFrame:
        """Chargement de la table des programmes"""
        # Simulation de données
        data = {
            'id': ['prog1', 'prog2', 'prog3'],
            'titre': ['Journal de 20h', 'Le Grand Journal', 'Quotidien'],
            'chaine': ['TF1', 'Canal+', 'TMC'],
            'genre': ['actualite', 'actualite', 'divertissement']
        }
        return pd.DataFrame(data)
    
    def _load_utilisateurs_table(self) -> pd.DataFrame:
        """Chargement de la table des utilisateurs"""
        # Simulation de données
        data = {
            'id': ['user1', 'user2', 'user3'],
            'hash_anonyme': ['hash1', 'hash2', 'hash3'],
            'region_anonymisee': ['FR-75', 'FR-69', 'FR-13'],
            'age_groupe': ['25-35', '18-25', '35-45']
        }
        return pd.DataFrame(data)
    
    def _load_sources_table(self) -> pd.DataFrame:
        """Chargement de la table des sources"""
        # Simulation de données
        data = {
            'id': ['source1', 'source2', 'source3', 'source4', 'source5'],
            'nom': ['Kaggle Tweets', 'PostgreSQL DB', 'Twitter Stream', 'News Scraping', 'NewsAPI'],
            'type_source': ['file', 'sql', 'bigdata', 'scraping', 'api']
        }
        return pd.DataFrame(data)
    
    def _join_with_programmes(self, df: pd.DataFrame, programmes_df: pd.DataFrame) -> pd.DataFrame:
        """Jointure avec les programmes"""
        # Simulation de jointure simple
        df['programme_id'] = 'prog1'  # Simulation
        return df.merge(programmes_df, left_on='programme_id', right_on='id', how='left')
    
    def _join_with_utilisateurs(self, df: pd.DataFrame, utilisateurs_df: pd.DataFrame) -> pd.DataFrame:
        """Jointure avec les utilisateurs"""
        # Simulation de jointure simple
        df['utilisateur_id'] = 'user1'  # Simulation
        return df.merge(utilisateurs_df, left_on='utilisateur_id', right_on='id', how='left')
    
    def _join_with_sources(self, df: pd.DataFrame, sources_df: pd.DataFrame) -> pd.DataFrame:
        """Jointure avec les sources"""
        return df.merge(sources_df, left_on='source_name', right_on='nom', how='left')
    
    # Méthodes de chargement
    def _save_to_postgresql(self, df: pd.DataFrame, table_name: str):
        """Sauvegarde en PostgreSQL"""
        try:
            engine = create_engine(settings.database_url)
            df.to_sql(table_name, engine, if_exists='append', index=False)
            logger.info(f"✅ Données sauvegardées en PostgreSQL: {table_name}")
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde PostgreSQL: {e}")
    
    def _save_to_parquet(self, df: pd.DataFrame, file_path: str):
        """Sauvegarde en Parquet"""
        try:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            df.to_parquet(file_path, index=False)
            logger.info(f"✅ Données sauvegardées en Parquet: {file_path}")
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde Parquet: {e}")
    
    def _save_pipeline_report(self):
        """Sauvegarde du rapport du pipeline"""
        try:
            report_path = f"data/reports/etl_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            Path(report_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(report_path, 'w') as f:
                json.dump(self.pipeline_results, f, indent=2, default=str)
            
            logger.info(f"📄 Rapport sauvegardé: {report_path}")
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde rapport: {e}")


# Instance globale
detailed_etl_pipeline = DetailedETLPipeline()
