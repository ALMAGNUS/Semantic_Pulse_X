"""
Script pour charger les données Kaggle dans la base SQLite
"""

import sqlite3
from pathlib import Path

import pandas as pd


def load_kaggle_data():
    """Charge les données Kaggle dans la base SQLite"""

    # Chemin vers le fichier Kaggle (50% pour base simple)
    kaggle_file = Path("data/raw/kaggle_tweets/db_source_tweets.csv")

    if not kaggle_file.exists():
        print("❌ Fichier Kaggle non trouvé")
        return

    print("📊 Chargement des données Kaggle...")

    # Lire le CSV (premiers 1000 tweets pour éviter la surcharge)
    df = pd.read_csv(kaggle_file, nrows=1000)
    print(f"✅ {len(df)} tweets chargés")

    # Connexion à la base
    conn = sqlite3.connect('semantic_pulse.db')
    cursor = conn.cursor()

    # Vider la table existante
    cursor.execute("DELETE FROM tweets_kaggle")

    # Insérer les données
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO tweets_kaggle (text, sentiment, target, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            row['text'],
            row['target'],
            row['target'],
            '2025-01-01 00:00:00'
        ))

    conn.commit()

    # Vérifier le résultat
    cursor.execute("SELECT COUNT(*) FROM tweets_kaggle")
    count = cursor.fetchone()[0]
    print(f"✅ {count} tweets insérés dans la base")

    conn.close()

if __name__ == "__main__":
    load_kaggle_data()
