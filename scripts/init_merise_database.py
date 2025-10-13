#!/usr/bin/env python3
"""
Initialisateur de base de données Merise - Semantic Pulse X
Crée toutes les tables selon le modèle Merise avec relations cardinales
"""

import sqlite3
import logging
from datetime import datetime
from pathlib import Path

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_merise_database():
    """Crée la base de données selon le modèle Merise."""
    
    db_file = Path("semantic_pulse.db")
    
    logger.info("🏗️ CRÉATION DE LA BASE DE DONNÉES MERISE")
    logger.info("=" * 60)
    
    try:
        conn = sqlite3.connect(str(db_file))
        cursor = conn.cursor()
        
        # Activer les clés étrangères
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # 1. TABLE SOURCES (Entité Source)
        logger.info("📊 Création de la table SOURCES...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom VARCHAR(100) NOT NULL,
                type_source VARCHAR(50) NOT NULL,
                url_base VARCHAR(255),
                description TEXT,
                actif BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 2. TABLE PROGRAMMES (Entité Programme)
        logger.info("📊 Création de la table PROGRAMMES...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS programmes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre VARCHAR(255) NOT NULL,
                description TEXT,
                genre VARCHAR(100),
                duree_minutes INTEGER,
                source_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (source_id) REFERENCES sources(id) ON DELETE CASCADE
            );
        """)
        
        # 3. TABLE DIFFUSIONS (Entité Diffusion)
        logger.info("📊 Création de la table DIFFUSIONS...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS diffusions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                programme_id INTEGER NOT NULL,
                date_diffusion TIMESTAMP NOT NULL,
                heure_debut TIME,
                heure_fin TIME,
                canal VARCHAR(100),
                audience_estimee INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (programme_id) REFERENCES programmes(id) ON DELETE CASCADE
            );
        """)
        
        # 4. TABLE UTILISATEURS (Entité Utilisateur - Anonymisé)
        logger.info("📊 Création de la table UTILISATEURS...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS utilisateurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hash_anonyme VARCHAR(64) NOT NULL UNIQUE,
                type_utilisateur VARCHAR(50) DEFAULT 'anonyme',
                localisation VARCHAR(100),
                age_range VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 5. TABLE REACTIONS (Entité Réaction)
        logger.info("📊 Création de la table REACTIONS...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                diffusion_id INTEGER NOT NULL,
                utilisateur_id INTEGER NOT NULL,
                contenu TEXT NOT NULL,
                sentiment VARCHAR(50),
                emotion VARCHAR(50),
                score_sentiment DECIMAL(3,2),
                timestamp_reaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                source_reaction VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (diffusion_id) REFERENCES diffusions(id) ON DELETE CASCADE,
                FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
            );
        """)
        
        # 6. TABLE LOG_INGESTION (MLD - Logs d'ingestion)
        logger.info("📋 Création de la table LOG_INGESTION...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS log_ingestion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_type VARCHAR(50) NOT NULL,
                fichier_source VARCHAR(255),
                nb_lignes_traitees INTEGER,
                nb_lignes_erreur INTEGER,
                status VARCHAR(20) DEFAULT 'success',
                message_erreur TEXT,
                timestamp_ingestion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                duree_traitement_sec INTEGER
            );
        """)
        
        # 7. TABLE AGREGATION_EMOTIONNELLE (MLD - Agrégations)
        logger.info("📋 Création de la table AGREGATION_EMOTIONNELLE...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agregation_emotionnelle (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                diffusion_id INTEGER NOT NULL,
                emotion VARCHAR(50) NOT NULL,
                nombre_reactions INTEGER DEFAULT 0,
                score_moyen DECIMAL(3,2),
                score_max DECIMAL(3,2),
                score_min DECIMAL(3,2),
                periode_debut TIMESTAMP,
                periode_fin TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (diffusion_id) REFERENCES diffusions(id) ON DELETE CASCADE
            );
        """)
        
        # 8. INDEX pour optimiser les performances
        logger.info("🔍 Création des index...")
        
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_programmes_source_id ON programmes(source_id);",
            "CREATE INDEX IF NOT EXISTS idx_diffusions_programme_id ON diffusions(programme_id);",
            "CREATE INDEX IF NOT EXISTS idx_diffusions_date ON diffusions(date_diffusion);",
            "CREATE INDEX IF NOT EXISTS idx_reactions_diffusion_id ON reactions(diffusion_id);",
            "CREATE INDEX IF NOT EXISTS idx_reactions_utilisateur_id ON reactions(utilisateur_id);",
            "CREATE INDEX IF NOT EXISTS idx_reactions_timestamp ON reactions(timestamp_reaction);",
            "CREATE INDEX IF NOT EXISTS idx_reactions_sentiment ON reactions(sentiment);",
            "CREATE INDEX IF NOT EXISTS idx_agregation_diffusion_id ON agregation_emotionnelle(diffusion_id);",
            "CREATE INDEX IF NOT EXISTS idx_agregation_emotion ON agregation_emotionnelle(emotion);"
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
        
        # 9. Insérer des données de test
        logger.info("📊 Insertion des données de test...")
        
        # Sources de test
        sources_data = [
            ('Twitter', 'social_media', 'https://twitter.com', 'Réseau social de microblogging'),
            ('YouTube', 'video_platform', 'https://youtube.com', 'Plateforme de vidéos'),
            ('Web Scraping', 'web_content', 'https://example.com', 'Contenu web scrapé'),
            ('Kaggle Dataset', 'dataset', 'https://kaggle.com', 'Dataset public anonymisé'),
            ('Base Relationnelle', 'database', 'localhost', 'Base de données relationnelle')
        ]
        
        for source in sources_data:
            cursor.execute("""
                INSERT OR IGNORE INTO sources (nom, type_source, url_base, description)
                VALUES (?, ?, ?, ?)
            """, source)
        
        # Programmes de test
        programmes_data = [
            ('Actualités du soir', 'Émission d\'actualités quotidienne', 'actualites', 30, 1),
            ('Débat politique', 'Débat sur les enjeux politiques', 'politique', 60, 1),
            ('Sport en direct', 'Retransmission sportive', 'sport', 90, 2),
            ('Culture et société', 'Magazine culturel', 'culture', 45, 3),
            ('Économie', 'Analyse économique', 'economie', 25, 4)
        ]
        
        for programme in programmes_data:
            cursor.execute("""
                INSERT OR IGNORE INTO programmes (titre, description, genre, duree_minutes, source_id)
                VALUES (?, ?, ?, ?, ?)
            """, programme)
        
        # Diffusions de test
        diffusions_data = [
            (1, '2025-01-15 20:00:00', '20:00', '20:30', 'TF1', 5000000),
            (2, '2025-01-15 21:00:00', '21:00', '22:00', 'France 2', 3000000),
            (3, '2025-01-15 19:00:00', '19:00', '20:30', 'Canal+', 1500000),
            (4, '2025-01-15 22:00:00', '22:00', '22:45', 'Arte', 800000),
            (5, '2025-01-15 18:00:00', '18:00', '18:25', 'BFM TV', 1200000)
        ]
        
        for diffusion in diffusions_data:
            cursor.execute("""
                INSERT OR IGNORE INTO diffusions (programme_id, date_diffusion, heure_debut, heure_fin, canal, audience_estimee)
                VALUES (?, ?, ?, ?, ?, ?)
            """, diffusion)
        
        # Utilisateurs anonymisés de test
        utilisateurs_data = [
            ('hash_user_001', 'anonyme', 'France', '25-34'),
            ('hash_user_002', 'anonyme', 'France', '35-44'),
            ('hash_user_003', 'anonyme', 'Belgique', '18-24'),
            ('hash_user_004', 'anonyme', 'Suisse', '45-54'),
            ('hash_user_005', 'anonyme', 'France', '55-64')
        ]
        
        for utilisateur in utilisateurs_data:
            cursor.execute("""
                INSERT OR IGNORE INTO utilisateurs (hash_anonyme, type_utilisateur, localisation, age_range)
                VALUES (?, ?, ?, ?)
            """, utilisateur)
        
        # Réactions de test
        reactions_data = [
            (1, 1, 'Excellente émission ce soir !', 'positif', 'joie', 0.8, '2025-01-15 20:15:00', 'twitter'),
            (1, 2, 'Très intéressant ce débat', 'positif', 'satisfaction', 0.7, '2025-01-15 20:20:00', 'youtube'),
            (2, 3, 'Je ne suis pas d\'accord avec cette analyse', 'negatif', 'colere', -0.6, '2025-01-15 21:10:00', 'web_scraping'),
            (3, 4, 'Super match !', 'positif', 'excitation', 0.9, '2025-01-15 19:30:00', 'twitter'),
            (4, 5, 'Culturellement enrichissant', 'positif', 'satisfaction', 0.8, '2025-01-15 22:15:00', 'youtube'),
            (5, 1, 'Analyse économique pertinente', 'positif', 'confiance', 0.7, '2025-01-15 18:10:00', 'database')
        ]
        
        for reaction in reactions_data:
            cursor.execute("""
                INSERT OR IGNORE INTO reactions (diffusion_id, utilisateur_id, contenu, sentiment, emotion, score_sentiment, timestamp_reaction, source_reaction)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, reaction)
        
        # Logs d'ingestion de test
        logs_data = [
            ('bigdata', 'tweets_sentiment140.parquet', 10000, 0, 'success', None, '2025-01-15 10:00:00', 45),
            ('youtube', 'youtube_data.json', 50, 2, 'success', None, '2025-01-15 11:00:00', 12),
            ('web_scraping', 'scraped_content.json', 15, 0, 'success', None, '2025-01-15 12:00:00', 8),
            ('csv', 'kaggle_dataset.csv', 1000, 5, 'success', None, '2025-01-15 13:00:00', 25)
        ]
        
        for log in logs_data:
            cursor.execute("""
                INSERT OR IGNORE INTO log_ingestion (source_type, fichier_source, nb_lignes_traitees, nb_lignes_erreur, status, message_erreur, timestamp_ingestion, duree_traitement_sec)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, log)
        
        # Agrégations émotionnelles de test
        aggregations_data = [
            (1, 'joie', 2, 0.75, 0.8, 0.7, '2025-01-15 20:00:00', '2025-01-15 20:30:00'),
            (2, 'colere', 1, -0.6, -0.6, -0.6, '2025-01-15 21:00:00', '2025-01-15 22:00:00'),
            (3, 'excitation', 1, 0.9, 0.9, 0.9, '2025-01-15 19:00:00', '2025-01-15 20:30:00'),
            (4, 'satisfaction', 1, 0.8, 0.8, 0.8, '2025-01-15 22:00:00', '2025-01-15 22:45:00'),
            (5, 'confiance', 1, 0.7, 0.7, 0.7, '2025-01-15 18:00:00', '2025-01-15 18:25:00')
        ]
        
        for aggregation in aggregations_data:
            cursor.execute("""
                INSERT OR IGNORE INTO agregation_emotionnelle (diffusion_id, emotion, nombre_reactions, score_moyen, score_max, score_min, periode_debut, periode_fin)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, aggregation)
        
        # Valider les changements
        conn.commit()
        
        # Vérifier la création
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        logger.info(f"✅ {len(tables)} tables créées avec succès")
        
        # Statistiques
        for table_name, in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            logger.info(f"  📊 {table_name}: {count} enregistrements")
        
        conn.close()
        
        logger.info("\n" + "=" * 60)
        logger.info("🎉 BASE DE DONNÉES MERISE CRÉÉE AVEC SUCCÈS!")
        logger.info("=" * 60)
        logger.info("✅ Entités Merise: programmes, diffusions, reactions, utilisateurs, sources")
        logger.info("✅ Relations cardinales: 1:N et N:1 implémentées")
        logger.info("✅ Tables MLD: log_ingestion, agregation_emotionnelle")
        logger.info("✅ Contraintes d'intégrité: Clés primaires et étrangères")
        logger.info("✅ Index de performance: Créés")
        logger.info("✅ Données de test: Insérées")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la création: {e}")
        return False

def main():
    """Fonction principale."""
    logger.info("🏗️ INITIALISATEUR DE BASE MERISE")
    
    success = create_merise_database()
    
    if success:
        logger.info("🎉 Base de données Merise initialisée!")
    else:
        logger.info("❌ Échec de l'initialisation")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)




