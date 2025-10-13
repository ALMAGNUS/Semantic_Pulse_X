#!/usr/bin/env python3
"""
Correcteur automatique - Semantic Pulse X
Corrige les erreurs les plus courantes identifiées par l'audit
"""

import os
import logging
from pathlib import Path
from datetime import datetime

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProjectCorrector:
    """Correcteur automatique du projet"""
    
    def __init__(self):
        self.corrections_applied = []
        
    def fix_1_missing_directories(self):
        """Corrige les dossiers manquants"""
        logger.info("🔧 CORRECTION 1: Dossiers manquants")
        
        required_dirs = [
            'data/raw/kaggle_tweets',
            'data/raw/external_apis', 
            'data/raw/web_scraping',
            'data/processed/bigdata',
            'data/processed',
            'logs'
        ]
        
        for dir_path in required_dirs:
            path = Path(dir_path)
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
                logger.info(f"✅ Créé: {dir_path}")
                self.corrections_applied.append(f"Créé dossier: {dir_path}")
            else:
                logger.info(f"✅ Existe déjà: {dir_path}")
    
    def fix_2_docker_compose_completion(self):
        """Complète le docker-compose.yml"""
        logger.info("🔧 CORRECTION 2: Docker Compose")
        
        docker_file = Path('docker-compose.yml')
        if docker_file.exists():
            try:
                with open(docker_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Vérifier si tous les services sont présents
                required_services = ['postgres', 'minio', 'redis', 'app']
                missing_services = [s for s in required_services if s not in content]
                
                if missing_services:
                    logger.warning(f"⚠️ Services manquants dans docker-compose.yml: {missing_services}")
                    # Ici on pourrait ajouter les services manquants
                else:
                    logger.info("✅ docker-compose.yml: Tous les services présents")
                    
            except Exception as e:
                logger.error(f"❌ Erreur lecture docker-compose.yml: {e}")
        else:
            logger.error("❌ docker-compose.yml manquant")
    
    def fix_3_database_initialization(self):
        """Initialise la base de données si nécessaire"""
        logger.info("🔧 CORRECTION 3: Base de données")
        
        db_file = Path('semantic_pulse.db')
        if not db_file.exists():
            logger.info("📊 Initialisation de la base de données...")
            try:
                import sqlite3
                conn = sqlite3.connect('semantic_pulse.db')
                cursor = conn.cursor()
                
                # Créer les tables de base
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tweets_kaggle (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        text TEXT,
                        sentiment INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS sources_kaggle (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        source_name TEXT,
                        source_type TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Insérer des données de test
                cursor.execute("INSERT OR IGNORE INTO sources_kaggle (source_name, source_type) VALUES ('kaggle_tweets', 'csv')")
                cursor.execute("INSERT OR IGNORE INTO sources_kaggle (source_name, source_type) VALUES ('youtube_hugo', 'api')")
                
                conn.commit()
                conn.close()
                
                logger.info("✅ Base de données initialisée")
                self.corrections_applied.append("Base de données initialisée")
                
            except Exception as e:
                logger.error(f"❌ Erreur initialisation DB: {e}")
        else:
            logger.info("✅ Base de données existe déjà")
    
    def fix_4_import_corrections(self):
        """Corrige les imports problématiques"""
        logger.info("🔧 CORRECTION 4: Imports Python")
        
        # Fichiers à corriger
        files_to_fix = [
            'app/backend/main.py',
            'app/frontend/streamlit_app.py'
        ]
        
        for file_path in files_to_fix:
            if Path(file_path).exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Ajouter sys.path si nécessaire
                    if 'from app.' in content and 'import sys' not in content:
                        new_content = "import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).parent.parent.parent))\n\n" + content
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        logger.info(f"✅ Corrigé imports: {file_path}")
                        self.corrections_applied.append(f"Corrigé imports: {file_path}")
                    
                except Exception as e:
                    logger.error(f"❌ Erreur correction {file_path}: {e}")
    
    def fix_5_environment_variables(self):
        """Vérifie et complète le fichier .env"""
        logger.info("🔧 CORRECTION 5: Variables d'environnement")
        
        env_file = Path('.env')
        if env_file.exists():
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Vérifier les variables critiques
                critical_vars = {
                    'DATABASE_URL': 'sqlite:///./semantic_pulse.db',
                    'MINIO_ENDPOINT': 'localhost:9000',
                    'MINIO_ACCESS_KEY': 'admin',
                    'MINIO_SECRET_KEY': 'admin123',
                    'REDIS_URL': 'redis://localhost:6379',
                    'OLLAMA_HOST': 'localhost:11434'
                }
                
                missing_vars = []
                for var, default_value in critical_vars.items():
                    if f"{var}=" not in content:
                        missing_vars.append(f"{var}={default_value}")
                
                if missing_vars:
                    # Ajouter les variables manquantes
                    with open(env_file, 'a', encoding='utf-8') as f:
                        f.write('\n# Variables ajoutées automatiquement\n')
                        for var in missing_vars:
                            f.write(f"{var}\n")
                    
                    logger.info(f"✅ Ajouté {len(missing_vars)} variables manquantes")
                    self.corrections_applied.append(f"Ajouté {len(missing_vars)} variables .env")
                else:
                    logger.info("✅ Toutes les variables critiques présentes")
                    
            except Exception as e:
                logger.error(f"❌ Erreur .env: {e}")
        else:
            logger.warning("⚠️ Fichier .env manquant - utilisez le template")
    
    def fix_6_requirements_completion(self):
        """Vérifie et complète requirements.txt"""
        logger.info("🔧 CORRECTION 6: Requirements.txt")
        
        req_file = Path('requirements.txt')
        if req_file.exists():
            try:
                with open(req_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Vérifier les dépendances critiques
                critical_deps = [
                    'fastapi>=0.104.0',
                    'streamlit>=1.28.0',
                    'langchain>=0.1.0',
                    'pandas>=2.0.0',
                    'sqlalchemy>=2.0.0',
                    'python-dotenv>=1.0.0',
                    'requests>=2.31.0',
                    'pydantic>=2.0.0'
                ]
                
                missing_deps = []
                for dep in critical_deps:
                    dep_name = dep.split('>=')[0]
                    if dep_name not in content.lower():
                        missing_deps.append(dep)
                
                if missing_deps:
                    logger.warning(f"⚠️ Dépendances manquantes: {missing_deps}")
                    # Ici on pourrait les ajouter automatiquement
                else:
                    logger.info("✅ Toutes les dépendances critiques présentes")
                    
            except Exception as e:
                logger.error(f"❌ Erreur requirements.txt: {e}")
        else:
            logger.error("❌ requirements.txt manquant")
    
    def run_all_corrections(self):
        """Exécute toutes les corrections"""
        logger.info("🔧 CORRECTIONS AUTOMATIQUES - SEMANTIC PULSE X")
        logger.info("=" * 60)
        
        # Exécuter toutes les corrections
        self.fix_1_missing_directories()
        self.fix_2_docker_compose_completion()
        self.fix_3_database_initialization()
        self.fix_4_import_corrections()
        self.fix_5_environment_variables()
        self.fix_6_requirements_completion()
        
        # Résumé
        logger.info("\n" + "=" * 60)
        logger.info("📊 RÉSUMÉ DES CORRECTIONS")
        logger.info("=" * 60)
        logger.info(f"🔧 Corrections appliquées: {len(self.corrections_applied)}")
        
        for i, correction in enumerate(self.corrections_applied, 1):
            logger.info(f"   {i}. {correction}")
        
        if self.corrections_applied:
            logger.info("\n✅ Corrections terminées!")
            logger.info("🧪 Relancez l'audit pour vérifier les améliorations")
        else:
            logger.info("\n✅ Aucune correction nécessaire!")
        
        logger.info("=" * 60)
        
        return len(self.corrections_applied)

def main():
    """Fonction principale"""
    logger.info("🔧 CORRECTIONS AUTOMATIQUES")
    
    corrector = ProjectCorrector()
    
    try:
        corrections_count = corrector.run_all_corrections()
        return corrections_count > 0
    except Exception as e:
        logger.error(f"❌ Erreur lors des corrections: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)




