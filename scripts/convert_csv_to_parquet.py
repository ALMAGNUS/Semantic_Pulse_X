#!/usr/bin/env python3
"""
Script de conversion CSV vers Parquet - Semantic Pulse X
Conversion progressive des données Kaggle tweets vers format Big Data
"""

import pandas as pd
import os
from pathlib import Path
import logging

# Configuration du logging pour suivre le processus
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def convert_csv_to_parquet(csv_path: str, parquet_path: str) -> bool:
    """
    Convertit un fichier CSV en Parquet de manière optimisée
    
    Args:
        csv_path: Chemin vers le fichier CSV source
        parquet_path: Chemin de destination pour le fichier Parquet
    
    Returns:
        bool: True si la conversion réussit, False sinon
    """
    try:
        logger.info(f"🔄 Début de conversion: {csv_path} -> {parquet_path}")
        
        # Lecture du CSV avec gestion mémoire optimisée
        df = pd.read_csv(csv_path, encoding='utf-8')
        logger.info(f"📊 Données chargées: {len(df)} lignes, {len(df.columns)} colonnes")
        
        # Création du dossier de destination si nécessaire
        os.makedirs(os.path.dirname(parquet_path), exist_ok=True)
        
        # Conversion vers Parquet avec compression
        df.to_parquet(parquet_path, compression='snappy', index=False)
        
        # Vérification de la taille des fichiers
        csv_size = os.path.getsize(csv_path) / (1024 * 1024)  # MB
        parquet_size = os.path.getsize(parquet_path) / (1024 * 1024)  # MB
        compression_ratio = (csv_size - parquet_size) / csv_size * 100
        
        logger.info(f"✅ Conversion réussie!")
        logger.info(f"📁 Taille CSV: {csv_size:.2f} MB")
        logger.info(f"📁 Taille Parquet: {parquet_size:.2f} MB")
        logger.info(f"🗜️ Compression: {compression_ratio:.1f}%")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la conversion: {e}")
        return False

def main():
    """Fonction principale de conversion"""
    logger.info("🚀 Démarrage de la conversion CSV vers Parquet")
    
    # Définition des chemins
    data_dir = Path("data/raw/kaggle_tweets")
    output_dir = Path("data/processed/bigdata")
    
    # Liste des fichiers à convertir
    files_to_convert = [
        ("db_source_tweets.csv", "tweets_db.parquet"),
        ("file_source_tweets.csv", "tweets_file.parquet"),
        ("sentiment140.csv", "tweets_sentiment140.parquet")
    ]
    
    success_count = 0
    total_files = len(files_to_convert)
    
    # Conversion de chaque fichier
    for csv_file, parquet_file in files_to_convert:
        csv_path = data_dir / csv_file
        parquet_path = output_dir / parquet_file
        
        if csv_path.exists():
            if convert_csv_to_parquet(str(csv_path), str(parquet_path)):
                success_count += 1
        else:
            logger.warning(f"⚠️ Fichier non trouvé: {csv_path}")
    
    # Résumé final
    logger.info(f"📊 Conversion terminée: {success_count}/{total_files} fichiers convertis")
    
    if success_count == total_files:
        logger.info("🎉 Toutes les conversions ont réussi!")
        return True
    else:
        logger.warning("⚠️ Certaines conversions ont échoué")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

