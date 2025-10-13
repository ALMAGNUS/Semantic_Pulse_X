#!/usr/bin/env python3
"""
Vérificateur et correcteur de répartition des données - Semantic Pulse X
Vérifie la répartition 1/3 CSV, 1/3 Base relationnelle, 1/3 Big Data
"""

import sqlite3
import pandas as pd
import logging
from pathlib import Path

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_data_distribution():
    """Vérifie la répartition actuelle des données."""
    
    logger.info("🔍 VÉRIFICATION DE LA RÉPARTITION DES DONNÉES")
    logger.info("=" * 60)
    
    # 1. Vérifier la base de données
    logger.info("🗄️ VÉRIFICATION BASE DE DONNÉES:")
    db_file = Path("semantic_pulse.db")
    
    if db_file.exists():
        try:
            conn = sqlite3.connect(str(db_file))
            cursor = conn.cursor()
            
            # Lister les tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            if tables:
                logger.info(f"  ✅ Tables trouvées: {len(tables)}")
                for table_name, in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                    count = cursor.fetchone()[0]
                    logger.info(f"    📊 {table_name}: {count} enregistrements")
            else:
                logger.info("  ❌ Aucune table dans la base")
            
            conn.close()
            
        except Exception as e:
            logger.error(f"  ❌ Erreur base de données: {e}")
    else:
        logger.info("  ❌ Fichier semantic_pulse.db non trouvé")
    
    # 2. Vérifier les fichiers CSV
    logger.info("\n📄 VÉRIFICATION FICHIERS CSV:")
    csv_dir = Path("data/raw/kaggle_tweets")
    
    if csv_dir.exists():
        csv_files = list(csv_dir.glob("*.csv"))
        total_csv_rows = 0
        
        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file, nrows=5)  # Juste pour vérifier
                full_df = pd.read_csv(csv_file)
                total_csv_rows += len(full_df)
                logger.info(f"  ✅ {csv_file.name}: {len(full_df)} lignes")
            except Exception as e:
                logger.warning(f"  ⚠️ Erreur lecture {csv_file.name}: {e}")
        
        logger.info(f"  📊 Total CSV: {total_csv_rows} lignes")
    else:
        logger.info("  ❌ Dossier CSV non trouvé")
    
    # 3. Vérifier les fichiers Parquet (Big Data)
    logger.info("\n📊 VÉRIFICATION BIG DATA (PARQUET):")
    parquet_dir = Path("data/processed/bigdata")
    
    if parquet_dir.exists():
        parquet_files = list(parquet_dir.glob("*.parquet"))
        total_parquet_rows = 0
        
        for parquet_file in parquet_files:
            try:
                df = pd.read_parquet(parquet_file)
                total_parquet_rows += len(df)
                logger.info(f"  ✅ {parquet_file.name}: {len(df)} lignes")
            except Exception as e:
                logger.warning(f"  ⚠️ Erreur lecture {parquet_file.name}: {e}")
        
        logger.info(f"  📊 Total Parquet: {total_parquet_rows} lignes")
    else:
        logger.info("  ❌ Dossier Parquet non trouvé")
    
    # 4. Analyser la répartition
    logger.info("\n📊 ANALYSE DE LA RÉPARTITION:")
    
    # Compter le total des données Kaggle originales
    original_file = Path("data/raw/kaggle_tweets/sentiment140.csv")
    if original_file.exists():
        try:
            df_original = pd.read_csv(original_file)
            total_original = len(df_original)
            logger.info(f"  📈 Dataset original: {total_original} lignes")
            
            # Calculer les tiers attendus
            tier_size = total_original // 3
            logger.info(f"  🎯 Taille attendue par tiers: {tier_size} lignes")
            
            # Vérifier la répartition actuelle
            logger.info(f"  📄 CSV actuel: {total_csv_rows} lignes")
            logger.info(f"  🗄️ Base relationnelle: 0 lignes (à vérifier)")
            logger.info(f"  📊 Parquet actuel: {total_parquet_rows} lignes")
            
            # Diagnostiquer le problème
            logger.info("\n🔍 DIAGNOSTIC:")
            if total_parquet_rows > tier_size * 2:
                logger.warning("  ⚠️ PROBLÈME: Trop de données en Parquet")
                logger.info("  💡 Solution: Répartir équitablement en 3 tiers")
            elif total_csv_rows > tier_size:
                logger.warning("  ⚠️ PROBLÈME: Trop de données en CSV")
            else:
                logger.info("  ✅ Répartition CSV/Parquet correcte")
            
            logger.info("  ❌ PROBLÈME PRINCIPAL: Base relationnelle vide")
            logger.info("  💡 Solution: Créer les tables Merise et insérer 1/3 des données")
            
        except Exception as e:
            logger.error(f"  ❌ Erreur lecture fichier original: {e}")
    else:
        logger.info("  ❌ Fichier original sentiment140.csv non trouvé")
    
    logger.info("\n" + "=" * 60)
    logger.info("🎯 RECOMMANDATIONS:")
    logger.info("=" * 60)
    logger.info("1. 🏗️ Créer les tables Merise (programmes, diffusions, reactions, etc.)")
    logger.info("2. 📊 Diviser le dataset en 3 tiers égaux")
    logger.info("3. 🗄️ Insérer 1/3 dans la base relationnelle")
    logger.info("4. 📄 Garder 1/3 en CSV")
    logger.info("5. 📊 Garder 1/3 en Parquet")
    logger.info("6. 🔗 Tester les relations cardinales")
    logger.info("=" * 60)

def main():
    """Fonction principale."""
    logger.info("🔍 VÉRIFICATEUR DE RÉPARTITION DES DONNÉES")
    
    check_data_distribution()
    
    return True

if __name__ == "__main__":
    main()




