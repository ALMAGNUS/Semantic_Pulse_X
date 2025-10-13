#!/usr/bin/env python3
"""
Test complet Phase 1 - Semantic Pulse X
Démonstration interactive de tous les composants Big Data
"""

import pandas as pd
import os
import logging
from pathlib import Path
import json
from datetime import datetime
from minio import Minio
from minio.error import S3Error
import psycopg2
from sqlalchemy import create_engine, text
import time

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Phase1Tester:
    """
    Testeur complet de la Phase 1 Big Data
    Approche progressive et détaillée
    """
    
    def __init__(self):
        """Initialise le testeur"""
        self.minio_client = Minio('localhost:9000', 'admin', 'admin123', secure=False)
        self.pg_engine = create_engine('postgresql://admin:admin123@localhost:5432/semantic_pulse')
        self.test_results = {}
        logger.info("🧪 Testeur Phase 1 initialisé")
    
    def test_1_parquet_files(self) -> bool:
        """Test 1: Vérification des fichiers Parquet"""
        logger.info("=" * 60)
        logger.info("📊 TEST 1: Vérification des fichiers Parquet")
        logger.info("=" * 60)
        
        parquet_dir = Path("data/processed/bigdata")
        if not parquet_dir.exists():
            logger.error("❌ Dossier Parquet non trouvé")
            return False
        
        parquet_files = list(parquet_dir.glob("*.parquet"))
        if not parquet_files:
            logger.error("❌ Aucun fichier Parquet trouvé")
            return False
        
        logger.info(f"📁 {len(parquet_files)} fichiers Parquet trouvés:")
        
        total_size = 0
        total_rows = 0
        
        for parquet_file in parquet_files:
            # Taille du fichier
            file_size = parquet_file.stat().st_size / (1024 * 1024)  # MB
            
            # Lecture des données
            df = pd.read_parquet(parquet_file)
            
            logger.info(f"   📄 {parquet_file.name}")
            logger.info(f"      💾 Taille: {file_size:.3f} MB")
            logger.info(f"      📊 Lignes: {len(df):,}")
            logger.info(f"      📋 Colonnes: {len(df.columns)}")
            logger.info(f"      🏷️ Colonnes: {list(df.columns)}")
            
            total_size += file_size
            total_rows += len(df)
        
        logger.info(f"📈 RÉSUMÉ:")
        logger.info(f"   📁 Total fichiers: {len(parquet_files)}")
        logger.info(f"   💾 Taille totale: {total_size:.3f} MB")
        logger.info(f"   📊 Total lignes: {total_rows:,}")
        
        self.test_results['parquet'] = {
            'files': len(parquet_files),
            'total_size_mb': total_size,
            'total_rows': total_rows
        }
        
        logger.info("✅ TEST 1 RÉUSSI: Fichiers Parquet OK")
        return True
    
    def test_2_minio_connection(self) -> bool:
        """Test 2: Connexion MinIO"""
        logger.info("=" * 60)
        logger.info("🗄️ TEST 2: Connexion MinIO Data Lake")
        logger.info("=" * 60)
        
        try:
            # Test de connexion
            buckets = list(self.minio_client.list_buckets())
            logger.info(f"✅ Connexion MinIO réussie")
            logger.info(f"📋 {len(buckets)} buckets trouvés:")
            
            for bucket in buckets:
                logger.info(f"   🪣 {bucket.name} (créé: {bucket.creation_date})")
            
            # Test du bucket principal
            bucket_name = 'semantic-pulse-data'
            if self.minio_client.bucket_exists(bucket_name):
                objects = list(self.minio_client.list_objects(bucket_name))
                logger.info(f"📄 {len(objects)} objets dans {bucket_name}:")
                
                total_size = 0
                for obj in objects:
                    size_mb = obj.size / (1024 * 1024)
                    total_size += size_mb
                    logger.info(f"   📄 {obj.object_name} ({size_mb:.3f} MB)")
                
                logger.info(f"📈 Taille totale dans MinIO: {total_size:.3f} MB")
                
                self.test_results['minio'] = {
                    'buckets': len(buckets),
                    'objects': len(objects),
                    'total_size_mb': total_size
                }
                
                logger.info("✅ TEST 2 RÉUSSI: MinIO Data Lake OK")
                return True
            else:
                logger.error(f"❌ Bucket {bucket_name} non trouvé")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur MinIO: {e}")
            return False
    
    def test_3_postgresql_connection(self) -> bool:
        """Test 3: Connexion PostgreSQL"""
        logger.info("=" * 60)
        logger.info("🐘 TEST 3: Connexion PostgreSQL")
        logger.info("=" * 60)
        
        try:
            # Test de connexion
            with self.pg_engine.connect() as conn:
                result = conn.execute(text("SELECT version()"))
                version = result.fetchone()[0]
                logger.info(f"✅ Connexion PostgreSQL réussie")
                logger.info(f"📋 Version: {version[:80]}...")
            
            # Test des tables
            with self.pg_engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT table_name, table_type 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """))
                tables = result.fetchall()
                
                logger.info(f"📊 {len(tables)} tables trouvées:")
                for table_name, table_type in tables:
                    logger.info(f"   📋 {table_name} ({table_type})")
                    
                    # Compter les lignes
                    count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                    count = count_result.fetchone()[0]
                    logger.info(f"      📈 {count:,} lignes")
            
            self.test_results['postgresql'] = {
                'tables': len(tables),
                'connected': True
            }
            
            logger.info("✅ TEST 3 RÉUSSI: PostgreSQL OK")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur PostgreSQL: {e}")
            return False
    
    def test_4_data_pipeline(self) -> bool:
        """Test 4: Pipeline de données complet"""
        logger.info("=" * 60)
        logger.info("🔄 TEST 4: Pipeline de données complet")
        logger.info("=" * 60)
        
        try:
            # 1. Téléchargement depuis MinIO
            logger.info("📥 Étape 1: Téléchargement depuis MinIO")
            bucket_name = 'semantic-pulse-data'
            objects = list(self.minio_client.list_objects(bucket_name))
            
            if not objects:
                logger.error("❌ Aucun objet dans MinIO")
                return False
            
            # Prendre le plus gros fichier
            largest_obj = max(objects, key=lambda x: x.size)
            temp_file = f"temp_{largest_obj.object_name}"
            
            self.minio_client.fget_object(bucket_name, largest_obj.object_name, temp_file)
            logger.info(f"✅ Téléchargé: {largest_obj.object_name} -> {temp_file}")
            
            # 2. Lecture Parquet
            logger.info("📖 Étape 2: Lecture du fichier Parquet")
            df = pd.read_parquet(temp_file)
            logger.info(f"✅ Lu: {len(df):,} lignes, {len(df.columns)} colonnes")
            
            # 3. Upload vers PostgreSQL
            logger.info("📤 Étape 3: Upload vers PostgreSQL")
            table_name = f"test_{largest_obj.object_name.replace('.parquet', '')}"
            df.to_sql(table_name, self.pg_engine, if_exists='replace', index=False)
            logger.info(f"✅ Uploadé vers table: {table_name}")
            
            # 4. Analyse des données
            logger.info("📊 Étape 4: Analyse des données")
            
            # Statistiques générales
            with self.pg_engine.connect() as conn:
                stats_query = text(f"""
                    SELECT 
                        COUNT(*) as total_rows,
                        COUNT(DISTINCT target) as unique_targets,
                        MIN(date) as earliest_date,
                        MAX(date) as latest_date
                    FROM {table_name}
                """)
                result = conn.execute(stats_query)
                stats = result.fetchone()
                
                logger.info(f"📈 Statistiques:")
                logger.info(f"   📊 Total lignes: {stats[0]:,}")
                logger.info(f"   🎯 Targets uniques: {stats[1]}")
                logger.info(f"   📅 Période: {stats[2]} à {stats[3]}")
            
            # Analyse des émotions
            if 'target' in df.columns:
                emotion_counts = df['target'].value_counts()
                logger.info(f"😊 Répartition des émotions:")
                for emotion, count in emotion_counts.items():
                    percentage = (count / len(df)) * 100
                    logger.info(f"   {emotion}: {count:,} ({percentage:.1f}%)")
            
            # 5. Nettoyage
            logger.info("🧹 Étape 5: Nettoyage")
            os.remove(temp_file)
            logger.info(f"✅ Fichier temporaire supprimé: {temp_file}")
            
            self.test_results['pipeline'] = {
                'downloaded_file': largest_obj.object_name,
                'rows_processed': len(df),
                'table_created': table_name
            }
            
            logger.info("✅ TEST 4 RÉUSSI: Pipeline complet OK")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur pipeline: {e}")
            return False
    
    def test_5_performance(self) -> bool:
        """Test 5: Tests de performance"""
        logger.info("=" * 60)
        logger.info("⚡ TEST 5: Tests de performance")
        logger.info("=" * 60)
        
        try:
            # Test de lecture Parquet
            parquet_dir = Path("data/processed/bigdata")
            parquet_files = list(parquet_dir.glob("*.parquet"))
            
            if not parquet_files:
                logger.error("❌ Aucun fichier Parquet pour le test")
                return False
            
            # Test sur le plus gros fichier
            largest_file = max(parquet_files, key=lambda f: f.stat().st_size)
            
            logger.info(f"📊 Test de performance sur: {largest_file.name}")
            
            # Lecture multiple pour moyenne
            read_times = []
            for i in range(3):
                start_time = time.time()
                df = pd.read_parquet(largest_file)
                read_time = time.time() - start_time
                read_times.append(read_time)
                logger.info(f"   Lecture {i+1}: {read_time:.3f}s")
            
            avg_read_time = sum(read_times) / len(read_times)
            file_size_mb = largest_file.stat().st_size / (1024 * 1024)
            
            logger.info(f"📈 Performance:")
            logger.info(f"   ⏱️ Temps moyen de lecture: {avg_read_time:.3f}s")
            logger.info(f"   💾 Taille fichier: {file_size_mb:.3f} MB")
            logger.info(f"   📊 Débit: {file_size_mb/avg_read_time:.1f} MB/s")
            logger.info(f"   📈 Lignes/s: {len(df)/avg_read_time:,.0f}")
            
            self.test_results['performance'] = {
                'avg_read_time': avg_read_time,
                'file_size_mb': file_size_mb,
                'throughput_mb_s': file_size_mb/avg_read_time,
                'rows_per_second': len(df)/avg_read_time
            }
            
            logger.info("✅ TEST 5 RÉUSSI: Performance OK")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur performance: {e}")
            return False
    
    def generate_report(self) -> dict:
        """Génère un rapport complet des tests"""
        logger.info("=" * 60)
        logger.info("📋 RAPPORT FINAL - PHASE 1")
        logger.info("=" * 60)
        
        # Résumé des tests
        total_tests = 5
        passed_tests = sum([
            'parquet' in self.test_results,
            'minio' in self.test_results,
            'postgresql' in self.test_results,
            'pipeline' in self.test_results,
            'performance' in self.test_results
        ])
        
        logger.info(f"📊 Tests exécutés: {passed_tests}/{total_tests}")
        
        if passed_tests == total_tests:
            logger.info("🎉 TOUS LES TESTS RÉUSSIS!")
            status = "SUCCESS"
        else:
            logger.info("⚠️ Certains tests ont échoué")
            status = "PARTIAL"
        
        # Détails par composant
        logger.info("🔍 Détails par composant:")
        
        if 'parquet' in self.test_results:
            p = self.test_results['parquet']
            logger.info(f"   📊 Parquet: {p['files']} fichiers, {p['total_size_mb']:.2f} MB, {p['total_rows']:,} lignes")
        
        if 'minio' in self.test_results:
            m = self.test_results['minio']
            logger.info(f"   🗄️ MinIO: {m['buckets']} buckets, {m['objects']} objets, {m['total_size_mb']:.2f} MB")
        
        if 'postgresql' in self.test_results:
            pg = self.test_results['postgresql']
            logger.info(f"   🐘 PostgreSQL: {pg['tables']} tables, connecté: {pg['connected']}")
        
        if 'pipeline' in self.test_results:
            pl = self.test_results['pipeline']
            logger.info(f"   🔄 Pipeline: {pl['rows_processed']:,} lignes traitées")
        
        if 'performance' in self.test_results:
            perf = self.test_results['performance']
            logger.info(f"   ⚡ Performance: {perf['throughput_mb_s']:.1f} MB/s, {perf['rows_per_second']:,.0f} lignes/s")
        
        # Sauvegarde du rapport
        report_file = "data/processed/phase1_test_report.json"
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'status': status,
            'tests_passed': passed_tests,
            'total_tests': total_tests,
            'results': self.test_results
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Rapport sauvegardé: {report_file}")
        
        return report_data

def main():
    """Fonction principale de test"""
    logger.info("🧪 DÉMARRAGE DES TESTS PHASE 1 - SEMANTIC PULSE X")
    logger.info("=" * 80)
    
    # Initialisation du testeur
    tester = Phase1Tester()
    
    # Exécution des tests
    tests = [
        ("Fichiers Parquet", tester.test_1_parquet_files),
        ("Connexion MinIO", tester.test_2_minio_connection),
        ("Connexion PostgreSQL", tester.test_3_postgresql_connection),
        ("Pipeline complet", tester.test_4_data_pipeline),
        ("Performance", tester.test_5_performance)
    ]
    
    for test_name, test_func in tests:
        logger.info(f"\n🚀 Exécution: {test_name}")
        try:
            success = test_func()
            if not success:
                logger.error(f"❌ Test échoué: {test_name}")
        except Exception as e:
            logger.error(f"❌ Erreur dans {test_name}: {e}")
    
    # Génération du rapport
    report = tester.generate_report()
    
    # Conclusion
    logger.info("\n" + "=" * 80)
    if report['status'] == 'SUCCESS':
        logger.info("🎉 PHASE 1 VALIDÉE AVEC SUCCÈS!")
        logger.info("✅ Tous les composants Big Data fonctionnent correctement")
        logger.info("🚀 Prêt pour la Phase 2: APIs externes")
    else:
        logger.info("⚠️ PHASE 1 PARTIELLEMENT VALIDÉE")
        logger.info("🔧 Certains composants nécessitent des corrections")
    
    logger.info("=" * 80)
    
    return report['status'] == 'SUCCESS'

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)




