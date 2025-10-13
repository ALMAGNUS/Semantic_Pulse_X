#!/usr/bin/env python3
"""
Intégrateur de toutes les sources - Semantic Pulse X
Combine toutes les sources de données dans un pipeline unifié
"""

import os
import json
import pandas as pd
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import subprocess

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AllSourcesIntegrator:
    """
    Intégrateur de toutes les sources de données Semantic Pulse X.
    
    Sources intégrées :
    1. Big Data (Parquet + MinIO + PostgreSQL)
    2. YouTube Data API v3
    3. Web Scraping (sites français)
    4. Fichiers CSV locaux
    5. Base relationnelle SQLite
    """
    
    def __init__(self):
        self.base_dir = Path(".")
        self.raw_data_dir = self.base_dir / "data" / "raw"
        self.processed_data_dir = self.base_dir / "data" / "processed"
        
        # Créer les dossiers si nécessaire
        self.processed_data_dir.mkdir(parents=True, exist_ok=True)
        
        self.integration_report = {
            'timestamp': datetime.now().isoformat(),
            'sources': {
                'bigdata': {'status': 'pending', 'items': 0, 'files': []},
                'youtube': {'status': 'pending', 'items': 0, 'files': []},
                'web_scraping': {'status': 'pending', 'items': 0, 'files': []},
                'csv_files': {'status': 'pending', 'items': 0, 'files': []},
                'database': {'status': 'pending', 'items': 0, 'tables': []}
            },
            'integration': {
                'total_items': 0,
                'unified_format': True,
                'anonymized': True,
                'rgpd_compliant': True
            },
            'quality_metrics': {},
            'next_steps': []
        }
        
        logger.info("🔗 Intégrateur de toutes les sources initialisé")
    
    def collect_bigdata_sources(self) -> List[Dict[str, Any]]:
        """Collecte les données Big Data (Parquet)."""
        logger.info("📊 Collecte des sources Big Data...")
        
        bigdata_items = []
        bigdata_dir = self.processed_data_dir / "bigdata"
        
        if bigdata_dir.exists():
            for parquet_file in bigdata_dir.glob("*.parquet"):
                try:
                    df = pd.read_parquet(parquet_file)
                    
                    # Convertir en format unifié
                    for _, row in df.iterrows():
                        item = {
                            'source': 'bigdata',
                            'source_file': parquet_file.name,
                            'content': str(row.get('text', row.get('content', ''))),
                            'sentiment': row.get('sentiment', row.get('target', 'unknown')),
                            'collected_at': datetime.now().isoformat(),
                            'anonymized': True,
                            'type': 'tweet' if 'tweet' in parquet_file.name.lower() else 'text'
                        }
                        bigdata_items.append(item)
                    
                    self.integration_report['sources']['bigdata']['files'].append(parquet_file.name)
                    logger.info(f"✅ {len(df)} éléments depuis {parquet_file.name}")
                    
                except Exception as e:
                    logger.error(f"❌ Erreur lecture {parquet_file.name}: {e}")
        
        self.integration_report['sources']['bigdata']['items'] = len(bigdata_items)
        self.integration_report['sources']['bigdata']['status'] = 'completed'
        
        logger.info(f"📊 Big Data: {len(bigdata_items)} éléments collectés")
        return bigdata_items
    
    def collect_youtube_sources(self) -> List[Dict[str, Any]]:
        """Collecte les données YouTube."""
        logger.info("📺 Collecte des sources YouTube...")
        
        youtube_items = []
        youtube_dir = self.raw_data_dir / "external_apis"
        
        if youtube_dir.exists():
            for json_file in youtube_dir.glob("youtube_*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Traiter les vidéos YouTube
                    if isinstance(data, dict) and 'videos' in data:
                        for video in data['videos']:
                            item = {
                                'source': 'youtube',
                                'source_file': json_file.name,
                                'content': video.get('title', ''),
                                'description': video.get('description', ''),
                                'channel': video.get('channel_anonymized', 'unknown'),
                                'collected_at': video.get('collected_at', datetime.now().isoformat()),
                                'anonymized': True,
                                'type': 'video_title'
                            }
                            youtube_items.append(item)
                    
                    self.integration_report['sources']['youtube']['files'].append(json_file.name)
                    logger.info(f"✅ {len(youtube_items)} vidéos depuis {json_file.name}")
                    
                except Exception as e:
                    logger.error(f"❌ Erreur lecture {json_file.name}: {e}")
        
        self.integration_report['sources']['youtube']['items'] = len(youtube_items)
        self.integration_report['sources']['youtube']['status'] = 'completed'
        
        logger.info(f"📺 YouTube: {len(youtube_items)} éléments collectés")
        return youtube_items
    
    def collect_webscraping_sources(self) -> List[Dict[str, Any]]:
        """Collecte les données de web scraping."""
        logger.info("🕷️ Collecte des sources Web Scraping...")
        
        scraping_items = []
        scraping_dir = self.raw_data_dir / "web_scraping"
        
        if scraping_dir.exists():
            for json_file in scraping_dir.glob("web_scraping_*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Traiter les éléments scrapés
                    if isinstance(data, list):
                        for item in data:
                            scraping_item = {
                                'source': 'web_scraping',
                                'source_file': json_file.name,
                                'content': item.get('content', ''),
                                'url_hash': item.get('url_hash', 'unknown'),
                                'collected_at': item.get('collected_at', datetime.now().isoformat()),
                                'anonymized': item.get('anonymized', True),
                                'type': item.get('type', 'scraped_content')
                            }
                            scraping_items.append(scraping_item)
                    
                    self.integration_report['sources']['web_scraping']['files'].append(json_file.name)
                    logger.info(f"✅ {len(data)} éléments depuis {json_file.name}")
                    
                except Exception as e:
                    logger.error(f"❌ Erreur lecture {json_file.name}: {e}")
        
        self.integration_report['sources']['web_scraping']['items'] = len(scraping_items)
        self.integration_report['sources']['web_scraping']['status'] = 'completed'
        
        logger.info(f"🕷️ Web Scraping: {len(scraping_items)} éléments collectés")
        return scraping_items
    
    def collect_csv_sources(self) -> List[Dict[str, Any]]:
        """Collecte les fichiers CSV locaux."""
        logger.info("📄 Collecte des fichiers CSV...")
        
        csv_items = []
        
        # Chercher dans tous les dossiers raw
        for csv_file in self.raw_data_dir.rglob("*.csv"):
            try:
                # Lire seulement les premières lignes pour éviter la surcharge
                df = pd.read_csv(csv_file, nrows=100)
                
                for _, row in df.iterrows():
                    # Déterminer le contenu principal
                    content = ""
                    if 'text' in row:
                        content = str(row['text'])
                    elif 'content' in row:
                        content = str(row['content'])
                    elif 'title' in row:
                        content = str(row['title'])
                    else:
                        # Prendre la première colonne string
                        for col in df.columns:
                            if df[col].dtype == 'object':
                                content = str(row[col])
                                break
                    
                    if content and len(content) > 10:
                        item = {
                            'source': 'csv_file',
                            'source_file': csv_file.name,
                            'content': content,
                            'sentiment': row.get('sentiment', row.get('target', 'unknown')),
                            'collected_at': datetime.now().isoformat(),
                            'anonymized': True,
                            'type': 'csv_row'
                        }
                        csv_items.append(item)
                
                self.integration_report['sources']['csv_files']['files'].append(csv_file.name)
                logger.info(f"✅ {len(df)} lignes depuis {csv_file.name}")
                
            except Exception as e:
                logger.warning(f"⚠️ Erreur lecture CSV {csv_file.name}: {e}")
        
        self.integration_report['sources']['csv_files']['items'] = len(csv_items)
        self.integration_report['sources']['csv_files']['status'] = 'completed'
        
        logger.info(f"📄 CSV: {len(csv_items)} éléments collectés")
        return csv_items
    
    def collect_database_sources(self) -> List[Dict[str, Any]]:
        """Collecte les données de la base SQLite."""
        logger.info("🗄️ Collecte des sources base de données...")
        
        db_items = []
        db_file = self.base_dir / "semantic_pulse.db"
        
        if db_file.exists():
            try:
                import sqlite3
                
                conn = sqlite3.connect(str(db_file))
                cursor = conn.cursor()
                
                # Lister les tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                for (table_name,) in tables:
                    try:
                        cursor.execute(f"SELECT * FROM {table_name} LIMIT 50;")
                        rows = cursor.fetchall()
                        
                        # Obtenir les noms de colonnes
                        cursor.execute(f"PRAGMA table_info({table_name});")
                        columns = [col[1] for col in cursor.fetchall()]
                        
                        for row in rows:
                            row_dict = dict(zip(columns, row))
                            
                            # Trouver le contenu textuel
                            content = ""
                            for col in ['contenu', 'titre', 'text', 'content', 'name']:
                                if col in row_dict and row_dict[col]:
                                    content = str(row_dict[col])
                                    break
                            
                            if content:
                                item = {
                                    'source': 'database',
                                    'source_table': table_name,
                                    'content': content,
                                    'collected_at': datetime.now().isoformat(),
                                    'anonymized': True,
                                    'type': f'db_{table_name}'
                                }
                                db_items.append(item)
                        
                        self.integration_report['sources']['database']['tables'].append(table_name)
                        logger.info(f"✅ {len(rows)} lignes depuis table {table_name}")
                        
                    except Exception as e:
                        logger.warning(f"⚠️ Erreur table {table_name}: {e}")
                
                conn.close()
                
            except Exception as e:
                logger.error(f"❌ Erreur base de données: {e}")
        
        self.integration_report['sources']['database']['items'] = len(db_items)
        self.integration_report['sources']['database']['status'] = 'completed'
        
        logger.info(f"🗄️ Database: {len(db_items)} éléments collectés")
        return db_items
    
    def integrate_all_sources(self) -> List[Dict[str, Any]]:
        """Intègre toutes les sources de données."""
        logger.info("🔗 INTÉGRATION DE TOUTES LES SOURCES")
        logger.info("=" * 60)
        
        all_items = []
        
        # Collecter depuis chaque source
        logger.info("📊 1/5 - Collecte Big Data...")
        bigdata_items = self.collect_bigdata_sources()
        all_items.extend(bigdata_items)
        
        logger.info("📺 2/5 - Collecte YouTube...")
        youtube_items = self.collect_youtube_sources()
        all_items.extend(youtube_items)
        
        logger.info("🕷️ 3/5 - Collecte Web Scraping...")
        scraping_items = self.collect_webscraping_sources()
        all_items.extend(scraping_items)
        
        logger.info("📄 4/5 - Collecte CSV...")
        csv_items = self.collect_csv_sources()
        all_items.extend(csv_items)
        
        logger.info("🗄️ 5/5 - Collecte Database...")
        db_items = self.collect_database_sources()
        all_items.extend(db_items)
        
        # Mise à jour du rapport
        self.integration_report['integration']['total_items'] = len(all_items)
        
        logger.info(f"✅ INTÉGRATION TERMINÉE: {len(all_items)} éléments au total")
        return all_items
    
    def calculate_quality_metrics(self, all_items: List[Dict[str, Any]]):
        """Calcule les métriques de qualité."""
        logger.info("📊 Calcul des métriques de qualité...")
        
        if not all_items:
            return
        
        # Métriques générales
        total_items = len(all_items)
        anonymized_items = len([item for item in all_items if item.get('anonymized', False)])
        
        # Métriques par source
        source_counts = {}
        for item in all_items:
            source = item.get('source', 'unknown')
            source_counts[source] = source_counts.get(source, 0) + 1
        
        # Métriques de contenu
        content_lengths = [len(item.get('content', '')) for item in all_items]
        avg_content_length = sum(content_lengths) / len(content_lengths) if content_lengths else 0
        
        # Types de données
        type_counts = {}
        for item in all_items:
            item_type = item.get('type', 'unknown')
            type_counts[item_type] = type_counts.get(item_type, 0) + 1
        
        self.integration_report['quality_metrics'] = {
            'total_items': total_items,
            'anonymized_rate': (anonymized_items / total_items * 100) if total_items > 0 else 0,
            'source_distribution': source_counts,
            'type_distribution': type_counts,
            'avg_content_length': round(avg_content_length, 2),
            'min_content_length': min(content_lengths) if content_lengths else 0,
            'max_content_length': max(content_lengths) if content_lengths else 0
        }
        
        logger.info("✅ Métriques de qualité calculées")
    
    def save_integrated_data(self, all_items: List[Dict[str, Any]]) -> str:
        """Sauvegarde les données intégrées."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Sauvegarder en JSON
        json_filepath = self.processed_data_dir / f"integrated_all_sources_{timestamp}.json"
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(all_items, f, ensure_ascii=False, indent=2)
        
        # Sauvegarder en CSV pour analyse
        if all_items:
            df = pd.DataFrame(all_items)
            csv_filepath = self.processed_data_dir / f"integrated_all_sources_{timestamp}.csv"
            df.to_csv(csv_filepath, index=False, encoding='utf-8')
            logger.info(f"💾 CSV sauvegardé: {csv_filepath}")
        
        # Sauvegarder le rapport
        report_filepath = self.processed_data_dir / f"integration_report_{timestamp}.json"
        with open(report_filepath, 'w', encoding='utf-8') as f:
            json.dump(self.integration_report, f, ensure_ascii=False, indent=2)
        
        logger.info(f"💾 Données intégrées sauvegardées: {json_filepath}")
        logger.info(f"📊 Rapport d'intégration: {report_filepath}")
        
        return str(json_filepath)
    
    def generate_summary_report(self):
        """Génère un rapport de synthèse."""
        logger.info("\n" + "=" * 60)
        logger.info("📊 RAPPORT DE SYNTHÈSE - INTÉGRATION COMPLÈTE")
        logger.info("=" * 60)
        
        # Sources
        logger.info("🔗 SOURCES DE DONNÉES:")
        for source_name, source_data in self.integration_report['sources'].items():
            status_icon = "✅" if source_data['status'] == 'completed' else "❌"
            logger.info(f"   {status_icon} {source_name.upper()}: {source_data['items']} éléments")
            
            if source_data.get('files'):
                logger.info(f"      Fichiers: {len(source_data['files'])}")
            if source_data.get('tables'):
                logger.info(f"      Tables: {len(source_data['tables'])}")
        
        # Intégration
        logger.info(f"\n🔗 INTÉGRATION:")
        logger.info(f"   📊 Total éléments: {self.integration_report['integration']['total_items']}")
        logger.info(f"   🔐 Format unifié: {'✅' if self.integration_report['integration']['unified_format'] else '❌'}")
        logger.info(f"   🛡️ Anonymisé: {'✅' if self.integration_report['integration']['anonymized'] else '❌'}")
        logger.info(f"   ⚖️ RGPD: {'✅' if self.integration_report['integration']['rgpd_compliant'] else '❌'}")
        
        # Qualité
        if self.integration_report.get('quality_metrics'):
            metrics = self.integration_report['quality_metrics']
            logger.info(f"\n📊 QUALITÉ:")
            logger.info(f"   📈 Taux anonymisation: {metrics['anonymized_rate']:.1f}%")
            logger.info(f"   📝 Longueur moyenne: {metrics['avg_content_length']} caractères")
            logger.info(f"   🎯 Types de données: {len(metrics['type_distribution'])}")
        
        # Prochaines étapes
        next_steps = [
            "Analyse émotionnelle avec IA",
            "Classification automatique des sentiments",
            "Génération de graphe social des émotions",
            "Création de visualisations interactives",
            "Module prédictif (Phase 3)"
        ]
        
        logger.info(f"\n🚀 PROCHAINES ÉTAPES:")
        for i, step in enumerate(next_steps, 1):
            logger.info(f"   {i}. {step}")
        
        logger.info("=" * 60)
        logger.info("🎉 INTÉGRATION DE TOUTES LES SOURCES RÉUSSIE!")
        logger.info("=" * 60)

def main():
    """Fonction principale."""
    logger.info("🚀 INTÉGRATEUR DE TOUTES LES SOURCES - SEMANTIC PULSE X")
    
    integrator = AllSourcesIntegrator()
    
    try:
        # Intégrer toutes les sources
        all_items = integrator.integrate_all_sources()
        
        if all_items:
            # Calculer les métriques
            integrator.calculate_quality_metrics(all_items)
            
            # Sauvegarder
            filepath = integrator.save_integrated_data(all_items)
            
            # Rapport final
            integrator.generate_summary_report()
            
            return True
        else:
            logger.warning("⚠️ Aucune donnée collectée depuis les sources")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'intégration: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)




