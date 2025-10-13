#!/usr/bin/env python3
"""
Client MinIO simple - Semantic Pulse X
Upload progressif des données Parquet vers le Data Lake
"""

import os
import logging
from pathlib import Path
from minio import Minio
from minio.error import S3Error

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MinIOClient:
    """
    Client MinIO simplifié pour l'upload des données Big Data
    Approche progressive et commentée
    """
    
    def __init__(self, endpoint: str = "localhost:9000", 
                 access_key: str = "admin", 
                 secret_key: str = "admin123"):
        """
        Initialise le client MinIO
        
        Args:
            endpoint: Adresse du serveur MinIO
            access_key: Clé d'accès
            secret_key: Clé secrète
        """
        self.endpoint = endpoint
        self.client = Minio(endpoint, access_key, secret_key, secure=False)
        logger.info(f"🔗 Client MinIO initialisé: {endpoint}")
    
    def create_bucket_if_not_exists(self, bucket_name: str) -> bool:
        """
        Crée un bucket s'il n'existe pas
        
        Args:
            bucket_name: Nom du bucket à créer
            
        Returns:
            bool: True si le bucket existe ou a été créé
        """
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
                logger.info(f"🪣 Bucket créé: {bucket_name}")
            else:
                logger.info(f"✅ Bucket existe déjà: {bucket_name}")
            return True
        except S3Error as e:
            logger.error(f"❌ Erreur création bucket: {e}")
            return False
    
    def upload_file(self, file_path: str, bucket_name: str, object_name: str = None) -> bool:
        """
        Upload un fichier vers MinIO
        
        Args:
            file_path: Chemin local du fichier
            bucket_name: Nom du bucket de destination
            object_name: Nom de l'objet dans MinIO (optionnel)
            
        Returns:
            bool: True si l'upload réussit
        """
        try:
            if not object_name:
                object_name = os.path.basename(file_path)
            
            # Vérification de la taille du fichier
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            logger.info(f"📤 Upload: {file_path} -> {bucket_name}/{object_name} ({file_size:.2f} MB)")
            
            # Upload du fichier
            self.client.fput_object(bucket_name, object_name, file_path)
            
            logger.info(f"✅ Upload réussi: {object_name}")
            return True
            
        except S3Error as e:
            logger.error(f"❌ Erreur upload: {e}")
            return False
        except FileNotFoundError:
            logger.error(f"❌ Fichier non trouvé: {file_path}")
            return False
    
    def list_objects(self, bucket_name: str) -> list:
        """
        Liste les objets dans un bucket
        
        Args:
            bucket_name: Nom du bucket
            
        Returns:
            list: Liste des objets
        """
        try:
            objects = list(self.client.list_objects(bucket_name))
            logger.info(f"📋 {len(objects)} objets trouvés dans {bucket_name}")
            return objects
        except S3Error as e:
            logger.error(f"❌ Erreur listing: {e}")
            return []

def main():
    """Fonction principale d'upload vers MinIO"""
    logger.info("🚀 Démarrage de l'upload vers MinIO")
    
    # Initialisation du client
    minio_client = MinIOClient()
    
    # Configuration des buckets et fichiers
    bucket_name = "semantic-pulse-data"
    data_dir = Path("data/processed/bigdata")
    
    # Création du bucket
    if not minio_client.create_bucket_if_not_exists(bucket_name):
        logger.error("❌ Impossible de créer le bucket")
        return False
    
    # Upload des fichiers Parquet
    parquet_files = [
        "tweets_db.parquet",
        "tweets_file.parquet", 
        "tweets_sentiment140.parquet"
    ]
    
    success_count = 0
    total_files = len(parquet_files)
    
    for file_name in parquet_files:
        file_path = data_dir / file_name
        if file_path.exists():
            if minio_client.upload_file(str(file_path), bucket_name, file_name):
                success_count += 1
        else:
            logger.warning(f"⚠️ Fichier non trouvé: {file_path}")
    
    # Vérification finale
    objects = minio_client.list_objects(bucket_name)
    logger.info(f"📊 Upload terminé: {success_count}/{total_files} fichiers uploadés")
    logger.info(f"📋 Total objets dans le bucket: {len(objects)}")
    
    return success_count == total_files

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

