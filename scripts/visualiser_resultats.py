#!/usr/bin/env python3
"""
Visualisation des résultats du data engineering - Semantic Pulse X
Montre toutes les étapes du traitement des données avec des détails concrets
"""

import os
import json
import pandas as pd
import logging
from datetime import datetime
from pathlib import Path

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def visualiser_etapes_data_engineering():
    """Visualise toutes les étapes du data engineering avec des détails concrets."""
    logger.info("🔍 VISUALISATION COMPLÈTE DU DATA ENGINEERING")
    logger.info("=" * 80)
    
    # Étape 1: Sources de données
    logger.info("\n📊 ÉTAPE 1: SOURCES DE DONNÉES")
    logger.info("-" * 50)
    
    sources_dir = "data/raw"
    if os.path.exists(sources_dir):
        for root, dirs, files in os.walk(sources_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                logger.info(f"📄 {file_path}")
                logger.info(f"   💾 Taille: {file_size:.3f} MB")
                
                # Analyser le contenu si c'est un CSV
                if file.endswith('.csv'):
                    try:
                        df = pd.read_csv(file_path, nrows=5)  # Lire seulement les 5 premières lignes
                        logger.info(f"   📊 Colonnes: {list(df.columns)}")
                        logger.info(f"   📈 Échantillon de données:")
                        for i, row in df.iterrows():
                            logger.info(f"      Ligne {i+1}: {dict(row)}")
                    except Exception as e:
                        logger.warning(f"   ⚠️ Impossible de lire le CSV: {e}")
    
    # Étape 2: Données traitées
    logger.info("\n🔄 ÉTAPE 2: DONNÉES TRAITÉES")
    logger.info("-" * 50)
    
    processed_dir = "data/processed"
    if os.path.exists(processed_dir):
        for root, dirs, files in os.walk(processed_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                logger.info(f"📄 {file_path}")
                logger.info(f"   💾 Taille: {file_size:.3f} MB")
                
                # Analyser le contenu selon le type
                if file.endswith('.parquet'):
                    try:
                        df = pd.read_parquet(file_path)
                        logger.info(f"   📊 Lignes: {len(df):,}")
                        logger.info(f"   📋 Colonnes: {len(df.columns)}")
                        logger.info(f"   🏷️ Colonnes: {list(df.columns)}")
                        
                        # Statistiques de base
                        logger.info(f"   📈 Statistiques:")
                        for col in df.columns:
                            if df[col].dtype in ['int64', 'float64']:
                                logger.info(f"      {col}: min={df[col].min()}, max={df[col].max()}, moyenne={df[col].mean():.2f}")
                            else:
                                unique_count = df[col].nunique()
                                logger.info(f"      {col}: {unique_count} valeurs uniques")
                    except Exception as e:
                        logger.warning(f"   ⚠️ Impossible de lire le Parquet: {e}")
                
                elif file.endswith('.json'):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        logger.info(f"   📊 Type: {type(data).__name__}")
                        if isinstance(data, list):
                            logger.info(f"   📈 Éléments: {len(data)}")
                            if data:
                                logger.info(f"   🏷️ Clés du premier élément: {list(data[0].keys()) if isinstance(data[0], dict) else 'N/A'}")
                        elif isinstance(data, dict):
                            logger.info(f"   🏷️ Clés: {list(data.keys())}")
                    except Exception as e:
                        logger.warning(f"   ⚠️ Impossible de lire le JSON: {e}")
    
    # Étape 3: Analyse de qualité
    logger.info("\n🔍 ÉTAPE 3: ANALYSE DE QUALITÉ")
    logger.info("-" * 50)
    
    # Analyser les fichiers Parquet
    parquet_files = []
    for root, dirs, files in os.walk(processed_dir):
        for file in files:
            if file.endswith('.parquet'):
                parquet_files.append(os.path.join(root, file))
    
    total_rows = 0
    total_size = 0
    
    for parquet_file in parquet_files:
        try:
            df = pd.read_parquet(parquet_file)
            file_size = os.path.getsize(parquet_file) / (1024 * 1024)
            
            logger.info(f"📊 {os.path.basename(parquet_file)}:")
            logger.info(f"   📈 Lignes: {len(df):,}")
            logger.info(f"   💾 Taille: {file_size:.3f} MB")
            
            # Qualité des données
            missing_data = df.isnull().sum()
            if missing_data.sum() > 0:
                logger.info(f"   ⚠️ Données manquantes:")
                for col, missing in missing_data.items():
                    if missing > 0:
                        logger.info(f"      {col}: {missing} ({missing/len(df)*100:.1f}%)")
            else:
                logger.info(f"   ✅ Aucune donnée manquante")
            
            # Types de données
            logger.info(f"   🏷️ Types de données:")
            for col, dtype in df.dtypes.items():
                logger.info(f"      {col}: {dtype}")
            
            total_rows += len(df)
            total_size += file_size
            
        except Exception as e:
            logger.error(f"❌ Erreur analyse {parquet_file}: {e}")
    
    logger.info(f"\n📊 RÉSUMÉ GLOBAL:")
    logger.info(f"   📈 Total lignes: {total_rows:,}")
    logger.info(f"   💾 Taille totale: {total_size:.3f} MB")
    
    # Étape 4: Métriques de performance
    logger.info("\n⚡ ÉTAPE 4: MÉTRIQUES DE PERFORMANCE")
    logger.info("-" * 50)
    
    # Calculer la compression
    raw_size = 0
    for root, dirs, files in os.walk(sources_dir):
        for file in files:
            if file.endswith('.csv'):
                raw_size += os.path.getsize(os.path.join(root, file)) / (1024 * 1024)
    
    if raw_size > 0:
        compression_ratio = (1 - (total_size / raw_size)) * 100
        logger.info(f"🗜️ Compression CSV → Parquet: {compression_ratio:.1f}%")
        logger.info(f"📊 Taille originale CSV: {raw_size:.3f} MB")
        logger.info(f"📊 Taille compressée Parquet: {total_size:.3f} MB")
        logger.info(f"💰 Économie d'espace: {raw_size - total_size:.3f} MB")
    
    # Étape 5: Traçabilité
    logger.info("\n🔍 ÉTAPE 5: TRAÇABILITÉ")
    logger.info("-" * 50)
    
    # Vérifier les logs et rapports
    log_files = []
    for root, dirs, files in os.walk(processed_dir):
        for file in files:
            if 'report' in file.lower() or 'log' in file.lower():
                log_files.append(os.path.join(root, file))
    
    for log_file in log_files:
        logger.info(f"📋 {os.path.basename(log_file)}")
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.info(f"   📄 Taille: {len(content)} caractères")
            logger.info(f"   📅 Dernière modification: {datetime.fromtimestamp(os.path.getmtime(log_file))}")
        except Exception as e:
            logger.warning(f"   ⚠️ Impossible de lire: {e}")
    
    logger.info("\n" + "=" * 80)
    logger.info("✅ VISUALISATION COMPLÈTE TERMINÉE")
    logger.info("=" * 80)

def analyser_pipeline_etl():
    """Analyse le pipeline ETL en détail."""
    logger.info("\n🔄 ANALYSE DÉTAILLÉE DU PIPELINE ETL")
    logger.info("=" * 60)
    
    # Vérifier les étapes du pipeline
    pipeline_steps = [
        ("Extraction", "data/raw"),
        ("Transformation", "data/processed"),
        ("Chargement", "data/processed/bigdata")
    ]
    
    for step_name, step_dir in pipeline_steps:
        logger.info(f"\n📊 {step_name.upper()}:")
        logger.info("-" * 30)
        
        if os.path.exists(step_dir):
            files = []
            total_size = 0
            
            for root, dirs, filenames in os.walk(step_dir):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    file_size = os.path.getsize(file_path) / (1024 * 1024)
                    files.append((filename, file_size))
                    total_size += file_size
            
            logger.info(f"   📁 Fichiers: {len(files)}")
            logger.info(f"   💾 Taille totale: {total_size:.3f} MB")
            
            for filename, size in files:
                logger.info(f"      📄 {filename}: {size:.3f} MB")
        else:
            logger.warning(f"   ⚠️ Répertoire {step_dir} non trouvé")

def generer_rapport_complet():
    """Génère un rapport complet du data engineering."""
    logger.info("\n📋 GÉNÉRATION DU RAPPORT COMPLET")
    logger.info("=" * 50)
    
    rapport = {
        "timestamp": datetime.now().isoformat(),
        "data_engineering_summary": {
            "sources": [],
            "processed_files": [],
            "quality_metrics": {},
            "performance_metrics": {}
        }
    }
    
    # Analyser les sources
    sources_dir = "data/raw"
    if os.path.exists(sources_dir):
        for root, dirs, files in os.walk(sources_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path) / (1024 * 1024)
                rapport["data_engineering_summary"]["sources"].append({
                    "file": file_path,
                    "size_mb": round(file_size, 3)
                })
    
    # Analyser les fichiers traités
    processed_dir = "data/processed"
    if os.path.exists(processed_dir):
        for root, dirs, files in os.walk(processed_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path) / (1024 * 1024)
                rapport["data_engineering_summary"]["processed_files"].append({
                    "file": file_path,
                    "size_mb": round(file_size, 3)
                })
    
    # Sauvegarder le rapport
    rapport_file = "data/processed/rapport_data_engineering_complet.json"
    os.makedirs(os.path.dirname(rapport_file), exist_ok=True)
    
    with open(rapport_file, 'w', encoding='utf-8') as f:
        json.dump(rapport, f, ensure_ascii=False, indent=2)
    
    logger.info(f"💾 Rapport sauvegardé: {rapport_file}")
    return rapport

def main():
    """Fonction principale."""
    logger.info("🔍 VISUALISATION DES RÉSULTATS - DATA ENGINEERING")
    logger.info("=" * 80)
    logger.info("📊 Analyse complète de toutes les étapes du traitement des données")
    logger.info("🔍 Détails concrets pour démonstration")
    logger.info("=" * 80)
    
    # Visualiser toutes les étapes
    visualiser_etapes_data_engineering()
    
    # Analyser le pipeline ETL
    analyser_pipeline_etl()
    
    # Générer le rapport complet
    rapport = generer_rapport_complet()
    
    logger.info("\n" + "=" * 80)
    logger.info("🎉 VISUALISATION TERMINÉE")
    logger.info("=" * 80)
    logger.info("📊 Toutes les étapes du data engineering ont été analysées")
    logger.info("🔍 Détails concrets disponibles pour démonstration")
    logger.info("📋 Rapport complet généré")
    logger.info("=" * 80)

if __name__ == "__main__":
    main()
