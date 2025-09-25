"""
Sources de données - Semantic Pulse X
5 sources RGPD-compliant pour collecte de données
"""

import pandas as pd
import requests
import json
import sqlite3
from typing import List, Dict, Any, Optional, Iterator
from datetime import datetime, timedelta
import os
from pathlib import Path

from app.backend.core.config import settings
from app.backend.core.anonymization import anonymizer


class DataSourceBase:
    """Classe de base pour les sources de données"""
    
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.data_dir = Path("data/raw")
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def fetch_data(self) -> List[Dict[str, Any]]:
        """Méthode abstraite pour récupérer les données"""
        raise NotImplementedError
    
    def _anonymize_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Anonymise les données"""
        anonymized_data = []
        for item in data:
            anonymized_item = anonymizer.anonymize_reaction(item)
            anonymized_data.append(anonymized_item)
        return anonymized_data
    
    def _save_data(self, data: List[Dict[str, Any]], filename: str):
        """Sauvegarde les données"""
        filepath = self.data_dir / filename
        df = pd.DataFrame(data)
        df.to_parquet(filepath, index=False)
        print(f"✅ Données sauvegardées: {filepath}")


class FileDataSource(DataSourceBase):
    """Source 1: Fichiers plats (CSV/JSON/Parquet)"""
    
    def __init__(self):
        super().__init__("file_source")
        self.sample_data = self._generate_sample_data()
    
    def fetch_data(self) -> List[Dict[str, Any]]:
        """Récupère les données depuis des fichiers"""
        # Simulation de données IMDb/Kaggle anonymisées
        data = self.sample_data.copy()
        
        # Anonymiser
        anonymized_data = self._anonymize_data(data)
        
        # Sauvegarder
        self._save_data(anonymized_data, "file_source_data.parquet")
        
        return anonymized_data
    
    def _generate_sample_data(self) -> List[Dict[str, Any]]:
        """Génère des données d'exemple"""
        programmes = [
            "Koh Lanta", "Les Marseillais", "TPMP", "Quotidien", "C dans l'air",
            "Le 20h", "Journal de 13h", "Complément d'enquête", "Envoyé spécial"
        ]
        
        emotions = ["joie", "colere", "tristesse", "surprise", "peur", "neutre"]
        
        data = []
        for i in range(100):
            data.append({
                "programme": programmes[i % len(programmes)],
                "texte": f"Réaction anonyme {i+1} sur {programmes[i % len(programmes)]}",
                "emotion": emotions[i % len(emotions)],
                "polarite": (i % 3 - 1) * 0.5,
                "timestamp": datetime.now() - timedelta(hours=i),
                "source": "file_imdb"
            })
        
        return data


class DatabaseDataSource(DataSourceBase):
    """Source 2: Base de données relationnelle"""
    
    def __init__(self):
        super().__init__("database_source")
        self.db_path = "data/sample.db"
        self._create_sample_db()
    
    def fetch_data(self) -> List[Dict[str, Any]]:
        """Récupère les données depuis la base"""
        conn = sqlite3.connect(self.db_path)
        
        query = """
        SELECT p.titre, p.chaine, p.genre, d.date_debut, d.audience_estimee,
               r.texte, r.emotion, r.polarite, r.timestamp
        FROM programmes p
        JOIN diffusions d ON p.id = d.programme_id
        JOIN reactions r ON d.id = r.diffusion_id
        ORDER BY r.timestamp DESC
        LIMIT 50
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # Convertir en format standard
        data = []
        for _, row in df.iterrows():
            data.append({
                "programme": row["titre"],
                "chaine": row["chaine"],
                "genre": row["genre"],
                "texte": row["texte"],
                "emotion": row["emotion"],
                "polarite": row["polarite"],
                "timestamp": row["timestamp"],
                "audience": row["audience_estimee"],
                "source": "database"
            })
        
        # Anonymiser
        anonymized_data = self._anonymize_data(data)
        
        # Sauvegarder
        self._save_data(anonymized_data, "database_source_data.parquet")
        
        return anonymized_data
    
    def _create_sample_db(self):
        """Crée une base de données d'exemple"""
        conn = sqlite3.connect(self.db_path)
        
        # Créer les tables
        conn.execute("""
        CREATE TABLE IF NOT EXISTS programmes (
            id INTEGER PRIMARY KEY,
            titre TEXT,
            chaine TEXT,
            genre TEXT
        )
        """)
        
        conn.execute("""
        CREATE TABLE IF NOT EXISTS diffusions (
            id INTEGER PRIMARY KEY,
            programme_id INTEGER,
            date_debut TEXT,
            audience_estimee INTEGER,
            FOREIGN KEY (programme_id) REFERENCES programmes(id)
        )
        """)
        
        conn.execute("""
        CREATE TABLE IF NOT EXISTS reactions (
            id INTEGER PRIMARY KEY,
            diffusion_id INTEGER,
            texte TEXT,
            emotion TEXT,
            polarite REAL,
            timestamp TEXT,
            FOREIGN KEY (diffusion_id) REFERENCES diffusions(id)
        )
        """)
        
        # Insérer des données d'exemple
        programmes = [
            (1, "Koh Lanta", "TF1", "Reality"),
            (2, "TPMP", "C8", "Talk-show"),
            (3, "Le 20h", "TF1", "Journal")
        ]
        
        conn.executemany("INSERT OR IGNORE INTO programmes VALUES (?, ?, ?, ?)", programmes)
        
        diffusions = [
            (1, 1, "2024-01-15 20:00:00", 5000000),
            (2, 2, "2024-01-15 18:00:00", 800000),
            (3, 3, "2024-01-15 20:00:00", 3000000)
        ]
        
        conn.executemany("INSERT OR IGNORE INTO diffusions VALUES (?, ?, ?, ?)", diffusions)
        
        reactions = [
            (1, 1, "Super épisode !", "joie", 0.8, "2024-01-15 21:30:00"),
            (2, 1, "Bof, pas terrible", "tristesse", -0.3, "2024-01-15 21:45:00"),
            (3, 2, "C'est n'importe quoi !", "colere", -0.7, "2024-01-15 19:00:00"),
            (4, 3, "Info importante", "neutre", 0.0, "2024-01-15 20:30:00")
        ]
        
        conn.executemany("INSERT OR IGNORE INTO reactions VALUES (?, ?, ?, ?, ?, ?)", reactions)
        
        conn.commit()
        conn.close()


class BigDataDataSource(DataSourceBase):
    """Source 3: Big Data (Parquet/Data Lake)"""
    
    def __init__(self):
        super().__init__("bigdata_source")
    
    def fetch_data(self) -> List[Dict[str, Any]]:
        """Récupère les données depuis le Data Lake"""
        # Simulation de données Twitter/Reddit anonymisées
        data = self._generate_big_data()
        
        # Anonymiser
        anonymized_data = self._anonymize_data(data)
        
        # Sauvegarder
        self._save_data(anonymized_data, "bigdata_source_data.parquet")
        
        return anonymized_data
    
    def _generate_big_data(self) -> List[Dict[str, Any]]:
        """Génère des données volumineuses d'exemple"""
        hashtags = ["#KohLanta", "#TPMP", "#CNews", "#France2", "#TF1"]
        emotions = ["joie", "colere", "tristesse", "surprise", "peur", "neutre"]
        
        data = []
        for i in range(200):
            data.append({
                "texte": f"Tweet anonyme {i+1} {hashtags[i % len(hashtags)]}",
                "emotion": emotions[i % len(emotions)],
                "polarite": (i % 5 - 2) * 0.3,
                "timestamp": datetime.now() - timedelta(minutes=i*30),
                "hashtags": [hashtags[i % len(hashtags)]],
                "source": "twitter_anonymized"
            })
        
        return data


class WebScrapingDataSource(DataSourceBase):
    """Source 4: Scraping web"""
    
    def __init__(self):
        super().__init__("scraping_source")
    
    def fetch_data(self) -> List[Dict[str, Any]]:
        """Récupère les données via scraping"""
        # Simulation de données scrapées
        data = self._simulate_scraping()
        
        # Anonymiser
        anonymized_data = self._anonymize_data(data)
        
        # Sauvegarder
        self._save_data(anonymized_data, "scraping_source_data.parquet")
        
        return anonymized_data
    
    def _simulate_scraping(self) -> List[Dict[str, Any]]:
        """Simule le scraping de sites web"""
        sites = ["allocine.fr", "purepeople.com", "voici.fr"]
        emotions = ["joie", "colere", "tristesse", "surprise", "peur", "neutre"]
        
        data = []
        for i in range(75):
            data.append({
                "texte": f"Commentaire anonyme {i+1} depuis {sites[i % len(sites)]}",
                "emotion": emotions[i % len(emotions)],
                "polarite": (i % 3 - 1) * 0.4,
                "timestamp": datetime.now() - timedelta(hours=i*2),
                "site": sites[i % len(sites)],
                "source": "web_scraping"
            })
        
        return data


class APIDataSource(DataSourceBase):
    """Source 5: API REST"""
    
    def __init__(self):
        super().__init__("api_source")
    
    def fetch_data(self) -> List[Dict[str, Any]]:
        """Récupère les données via API"""
        # Simulation de données API
        data = self._simulate_api_data()
        
        # Anonymiser
        anonymized_data = self._anonymize_data(data)
        
        # Sauvegarder
        self._save_data(anonymized_data, "api_source_data.parquet")
        
        return anonymized_data
    
    def _simulate_api_data(self) -> List[Dict[str, Any]]:
        """Simule les données d'API"""
        emotions = ["joie", "colere", "tristesse", "surprise", "peur", "neutre"]
        
        data = []
        for i in range(100):
            data.append({
                "texte": f"Article anonyme {i+1} sur l'actualité TV",
                "emotion": emotions[i % len(emotions)],
                "polarite": (i % 4 - 1.5) * 0.3,
                "timestamp": datetime.now() - timedelta(hours=i*3),
                "api_source": "newsapi_simulated",
                "source": "api_rest"
            })
        
        return data


class DataSourceManager:
    """Gestionnaire des sources de données"""
    
    def __init__(self):
        self.sources = {
            "file": FileDataSource(),
            "database": DatabaseDataSource(),
            "bigdata": BigDataDataSource(),
            "scraping": WebScrapingDataSource(),
            "api": APIDataSource()
        }
    
    def fetch_all_sources(self) -> Dict[str, List[Dict[str, Any]]]:
        """Récupère les données de toutes les sources"""
        all_data = {}
        
        for source_name, source in self.sources.items():
            try:
                print(f"🔄 Récupération des données depuis {source_name}...")
                data = source.fetch_data()
                all_data[source_name] = data
                print(f"✅ {len(data)} enregistrements récupérés depuis {source_name}")
            except Exception as e:
                print(f"❌ Erreur source {source_name}: {e}")
                all_data[source_name] = []
        
        return all_data
    
    def get_source_stats(self) -> Dict[str, Dict[str, Any]]:
        """Retourne les statistiques des sources"""
        stats = {}
        
        for source_name, source in self.sources.items():
            try:
                data = source.fetch_data()
                stats[source_name] = {
                    "count": len(data),
                    "status": "active",
                    "last_update": datetime.now().isoformat()
                }
            except Exception as e:
                stats[source_name] = {
                    "count": 0,
                    "status": "error",
                    "error": str(e),
                    "last_update": datetime.now().isoformat()
                }
        
        return stats


# Instance globale
data_source_manager = DataSourceManager()
