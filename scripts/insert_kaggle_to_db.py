#!/usr/bin/env python3
"""
Insertion directe du dataset Kaggle dans la base relationnelle - Semantic Pulse X
Insère 1/3 du dataset Kaggle dans la base SQLite
"""

import sqlite3
import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
import hashlib

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_simple_tables():
    """Crée des tables simples pour recevoir les données Kaggle."""
    
    logger.info("🏗️ Création des tables simples...")
    
    db_file = Path("semantic_pulse.db")
    
    try:
        conn = sqlite3.connect(str(db_file))
        cursor = conn.cursor()
        
        # Table simple pour les tweets Kaggle
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tweets_kaggle (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                sentiment INTEGER NOT NULL,
                target INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Table pour les sources
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sources_kaggle (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                type_source VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Insérer la source Kaggle
        cursor.execute("""
            INSERT OR IGNORE INTO sources_kaggle (name, type_source)
            VALUES ('Kaggle Sentiment140', 'dataset')
        """)
        
        conn.commit()
        conn.close()
        
        logger.info("✅ Tables simples créées")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur création tables: {e}")
        return False

def insert_kaggle_data():
    """Insère 1/3 du dataset Kaggle dans la base."""
    
    logger.info("📊 Insertion des données Kaggle...")
    
    # Charger le dataset original
    kaggle_file = Path("data/raw/kaggle_tweets/sentiment140.csv")
    
    if not kaggle_file.exists():
        logger.error(f"❌ Fichier non trouvé: {kaggle_file}")
        return False
    
    try:
        # Charger le dataset complet
        logger.info("📖 Chargement du dataset Kaggle...")
        df = pd.read_csv(kaggle_file)
        total_rows = len(df)
        
        logger.info(f"📈 Dataset total: {total_rows} lignes")
        
        # Calculer 1/3
        third_size = total_rows // 3
        logger.info(f"🎯 Taille 1/3: {third_size} lignes")
        
        # Prendre le premier tiers
        df_third = df.head(third_size)
        
        logger.info(f"📊 Lignes à insérer: {len(df_third)}")
        
        # Insérer dans la base
        db_file = Path("semantic_pulse.db")
        conn = sqlite3.connect(str(db_file))
        cursor = conn.cursor()
        
        # Vider la table si elle existe déjà
        cursor.execute("DELETE FROM tweets_kaggle;")
        
        # Insérer les données
        logger.info("💾 Insertion en cours...")
        
        for index, row in df_third.iterrows():
            cursor.execute("""
                INSERT INTO tweets_kaggle (text, sentiment, target)
                VALUES (?, ?, ?)
            """, (row['text'], row['target'], row['target']))
        
        conn.commit()
        
        # Vérifier l'insertion
        cursor.execute("SELECT COUNT(*) FROM tweets_kaggle;")
        inserted_count = cursor.fetchone()[0]
        
        conn.close()
        
        logger.info(f"✅ {inserted_count} lignes insérées avec succès")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur insertion: {e}")
        return False

def verify_insertion():
    """Vérifie que l'insertion s'est bien passée."""
    
    logger.info("🔍 Vérification de l'insertion...")
    
    try:
        db_file = Path("semantic_pulse.db")
        conn = sqlite3.connect(str(db_file))
        cursor = conn.cursor()
        
        # Compter les tweets
        cursor.execute("SELECT COUNT(*) FROM tweets_kaggle;")
        tweet_count = cursor.fetchone()[0]
        
        # Compter les sources
        cursor.execute("SELECT COUNT(*) FROM sources_kaggle;")
        source_count = cursor.fetchone()[0]
        
        # Afficher quelques exemples
        cursor.execute("SELECT text, sentiment FROM tweets_kaggle LIMIT 3;")
        examples = cursor.fetchall()
        
        logger.info(f"📊 Tweets insérés: {tweet_count}")
        logger.info(f"📊 Sources: {source_count}")
        
        logger.info("📝 Exemples de tweets:")
        for i, (text, sentiment) in enumerate(examples, 1):
            logger.info(f"  {i}. Sentiment {sentiment}: {text[:50]}...")
        
        # Statistiques des sentiments
        cursor.execute("SELECT sentiment, COUNT(*) FROM tweets_kaggle GROUP BY sentiment;")
        sentiment_stats = cursor.fetchall()
        
        logger.info("📈 Répartition des sentiments:")
        for sentiment, count in sentiment_stats:
            logger.info(f"  Sentiment {sentiment}: {count} tweets")
        
        conn.close()
        
        logger.info("✅ Vérification terminée")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur vérification: {e}")
        return False

def main():
    """Fonction principale."""
    logger.info("🚀 INSERTION DATASET KAGGLE DANS BASE RELATIONNELLE")
    logger.info("=" * 60)
    
    # Étape 1: Créer les tables
    if not create_simple_tables():
        logger.error("❌ Échec création des tables")
        return False
    
    # Étape 2: Insérer les données
    if not insert_kaggle_data():
        logger.error("❌ Échec insertion des données")
        return False
    
    # Étape 3: Vérifier
    if not verify_insertion():
        logger.error("❌ Échec vérification")
        return False
    
    logger.info("\n" + "=" * 60)
    logger.info("🎉 INSERTION RÉUSSIE!")
    logger.info("=" * 60)
    logger.info("✅ Tables créées: tweets_kaggle, sources_kaggle")
    logger.info("✅ 1/3 du dataset Kaggle inséré")
    logger.info("✅ Base relationnelle opérationnelle")
    logger.info("🚀 Prêt pour le travail Merise")
    logger.info("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
