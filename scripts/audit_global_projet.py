#!/usr/bin/env python3
"""
Audit global du projet - Semantic Pulse X
Identification de toutes les imperfections avant test Docker complet
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
import subprocess
import sys

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProjectAuditor:
    """Auditeur global du projet Semantic Pulse X"""
    
    def __init__(self):
        self.audit_report = {
            'timestamp': datetime.now().isoformat(),
            'project_status': 'AUDIT_EN_COURS',
            'imperfections': [],
            'corrections_needed': [],
            'docker_readiness': False,
            'components_status': {}
        }
        
    def audit_1_project_structure(self):
        """Audit de la structure du projet"""
        logger.info("\n🏗️ AUDIT 1: STRUCTURE DU PROJET")
        logger.info("-" * 50)
        
        required_structure = {
            'app/backend/': ['main.py', 'core/', 'ai/', 'etl/', 'models/', 'api/'],
            'app/frontend/': ['streamlit_app.py', 'visualization/'],
            'scripts/': ['test_', 'collect_', 'demo_'],  # Patterns simplifiés
            'docs/': ['ARCHITECTURE.md', 'README.md'],  # Fichiers spécifiques
            'data/': ['raw/', 'processed/'],
            'docker-compose.yml': True,
            'requirements.txt': True,
            '.env': True
        }
        
        issues = []
        
        for path, requirements in required_structure.items():
            if isinstance(requirements, bool):
                if not Path(path).exists():
                    issues.append(f"❌ {path} manquant")
                else:
                    logger.info(f"✅ {path} présent")
            else:
                base_path = Path(path)
                if not base_path.exists():
                    issues.append(f"❌ {path} dossier manquant")
                else:
                    for req in requirements:
                        if req.endswith('/'):
                            # Dossier
                            req_path = base_path / req
                            if not req_path.exists():
                                issues.append(f"❌ {path}{req} manquant")
                            else:
                                logger.info(f"✅ {path}{req} présent")
                        elif req.endswith('_'):
                            # Pattern de fichiers
                            matching_files = list(base_path.glob(f"{req}*"))
                            if not matching_files:
                                issues.append(f"❌ {path}{req}* fichiers manquants")
                            else:
                                logger.info(f"✅ {path}{req}*: {len(matching_files)} fichiers")
                        else:
                            # Fichier spécifique
                            req_path = base_path / req
                            if not req_path.exists():
                                issues.append(f"❌ {path}{req} manquant")
                            else:
                                logger.info(f"✅ {path}{req} présent")
        
        self.audit_report['imperfections'].extend(issues)
        logger.info(f"📊 Structure: {len(issues)} problèmes identifiés")
        
    def audit_2_imports_and_dependencies(self):
        """Audit des imports et dépendances"""
        logger.info("\n📦 AUDIT 2: IMPORTS ET DÉPENDANCES")
        logger.info("-" * 50)
        
        issues = []
        
        # Vérifier les imports dans les fichiers principaux
        main_files = [
            'app/backend/main.py',
            'app/frontend/streamlit_app.py',
            'app/backend/core/config.py'
        ]
        
        for file_path in main_files:
            if Path(file_path).exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Vérifier les imports problématiques
                    if 'from app.' in content and 'sys.path' not in content:
                        issues.append(f"⚠️ {file_path}: Import 'app.' sans sys.path")
                    
                    if 'import app.' in content:
                        issues.append(f"⚠️ {file_path}: Import 'app.' direct")
                        
                except Exception as e:
                    issues.append(f"❌ {file_path}: Erreur lecture - {e}")
        
        # Vérifier requirements.txt
        if Path('requirements.txt').exists():
            try:
                with open('requirements.txt', 'r') as f:
                    requirements = f.read()
                
                critical_deps = ['fastapi', 'streamlit', 'langchain', 'pandas', 'sqlalchemy']
                missing_deps = []
                
                for dep in critical_deps:
                    if dep not in requirements.lower():
                        missing_deps.append(dep)
                
                if missing_deps:
                    issues.append(f"❌ requirements.txt: Dépendances manquantes - {missing_deps}")
                else:
                    logger.info("✅ requirements.txt: Dépendances critiques présentes")
                    
            except Exception as e:
                issues.append(f"❌ requirements.txt: Erreur lecture - {e}")
        
        self.audit_report['imperfections'].extend(issues)
        logger.info(f"📊 Dépendances: {len(issues)} problèmes identifiés")
        
    def audit_3_docker_configuration(self):
        """Audit de la configuration Docker"""
        logger.info("\n🐳 AUDIT 3: CONFIGURATION DOCKER")
        logger.info("-" * 50)
        
        issues = []
        
        # Vérifier docker-compose.yml
        if Path('docker-compose.yml').exists():
            try:
                with open('docker-compose.yml', 'r', encoding='utf-8') as f:
                    docker_content = f.read()
                
                required_services = ['postgres', 'minio', 'redis', 'app']
                missing_services = []
                
                for service in required_services:
                    if service not in docker_content:
                        missing_services.append(service)
                
                if missing_services:
                    issues.append(f"❌ docker-compose.yml: Services manquants - {missing_services}")
                else:
                    logger.info("✅ docker-compose.yml: Services requis présents")
                
                # Vérifier les volumes
                if 'volumes:' not in docker_content:
                    issues.append("⚠️ docker-compose.yml: Pas de volumes définis")
                
                # Vérifier les ports
                if 'ports:' not in docker_content:
                    issues.append("⚠️ docker-compose.yml: Pas de ports exposés")
                    
            except Exception as e:
                issues.append(f"❌ docker-compose.yml: Erreur lecture - {e}")
        else:
            issues.append("❌ docker-compose.yml manquant")
        
        # Vérifier Dockerfile
        if not Path('Dockerfile').exists():
            issues.append("⚠️ Dockerfile manquant (optionnel si docker-compose suffisant)")
        
        self.audit_report['imperfections'].extend(issues)
        logger.info(f"📊 Docker: {len(issues)} problèmes identifiés")
        
    def audit_4_database_schema(self):
        """Audit du schéma de base de données"""
        logger.info("\n🗄️ AUDIT 4: SCHÉMA BASE DE DONNÉES")
        logger.info("-" * 50)
        
        issues = []
        
        # Vérifier la base SQLite
        if Path('semantic_pulse.db').exists():
            try:
                import sqlite3
                conn = sqlite3.connect('semantic_pulse.db')
                cursor = conn.cursor()
                
                # Lister les tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in cursor.fetchall()]
                
                required_tables = ['tweets_kaggle', 'sources_kaggle']
                missing_tables = [t for t in required_tables if t not in tables]
                
                if missing_tables:
                    issues.append(f"❌ Base de données: Tables manquantes - {missing_tables}")
                else:
                    logger.info("✅ Base de données: Tables requises présentes")
                
                # Vérifier les données
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table};")
                    count = cursor.fetchone()[0]
                    logger.info(f"   📊 {table}: {count} enregistrements")
                
                conn.close()
                
            except Exception as e:
                issues.append(f"❌ Base de données: Erreur accès - {e}")
        else:
            issues.append("❌ semantic_pulse.db manquant")
        
        self.audit_report['imperfections'].extend(issues)
        logger.info(f"📊 Base de données: {len(issues)} problèmes identifiés")
        
    def audit_5_data_sources(self):
        """Audit des sources de données"""
        logger.info("\n📊 AUDIT 5: SOURCES DE DONNÉES")
        logger.info("-" * 50)
        
        issues = []
        
        # Vérifier les 5 sources obligatoires
        sources = {
            'fichier_plat': 'data/raw/kaggle_tweets/sentiment140.csv',
            'base_relationnelle': 'semantic_pulse.db',
            'big_data': 'data/processed/bigdata',
            'web_scraping': 'data/raw/web_scraping',
            'api_rest': 'data/raw/external_apis'
        }
        
        for source_name, source_path in sources.items():
            if Path(source_path).exists():
                logger.info(f"✅ {source_name}: {source_path}")
            else:
                issues.append(f"❌ {source_name}: {source_path} manquant")
        
        # Vérifier les données récentes
        api_dir = Path('data/raw/external_apis')
        if api_dir.exists():
            recent_files = list(api_dir.glob('*hugo*'))
            if recent_files:
                logger.info(f"✅ Données Hugo récentes: {len(recent_files)} fichiers")
            else:
                issues.append("⚠️ Aucune donnée Hugo récente trouvée")
        
        self.audit_report['imperfections'].extend(issues)
        logger.info(f"📊 Sources de données: {len(issues)} problèmes identifiés")
        
    def audit_6_ai_modules(self):
        """Audit des modules IA"""
        logger.info("\n🧠 AUDIT 6: MODULES IA")
        logger.info("-" * 50)
        
        issues = []
        
        ai_dir = Path('app/backend/ai')
        if ai_dir.exists():
            ai_files = list(ai_dir.glob('*.py'))
            logger.info(f"✅ Modules IA: {len(ai_files)} fichiers")
            
            for ai_file in ai_files:
                logger.info(f"   📄 {ai_file.name}")
            
            # Vérifier les modules critiques
            critical_modules = ['emotion_classifier.py', 'embeddings.py', 'social_graph.py']
            missing_modules = [m for m in critical_modules if not (ai_dir / m).exists()]
            
            if missing_modules:
                issues.append(f"❌ Modules IA critiques manquants: {missing_modules}")
        else:
            issues.append("❌ Dossier app/backend/ai manquant")
        
        self.audit_report['imperfections'].extend(issues)
        logger.info(f"📊 Modules IA: {len(issues)} problèmes identifiés")
        
    def audit_7_environment_configuration(self):
        """Audit de la configuration d'environnement"""
        logger.info("\n⚙️ AUDIT 7: CONFIGURATION ENVIRONNEMENT")
        logger.info("-" * 50)
        
        issues = []
        
        # Vérifier .env
        if Path('.env').exists():
            try:
                with open('.env', 'r', encoding='utf-8') as f:
                    env_content = f.read()
                
                # Vérifier les variables critiques
                critical_vars = ['DATABASE_URL', 'YOUTUBE_API_KEY']
                missing_vars = []
                
                for var in critical_vars:
                    if f"{var}=" not in env_content:
                        missing_vars.append(var)
                
                if missing_vars:
                    issues.append(f"⚠️ .env: Variables manquantes - {missing_vars}")
                else:
                    logger.info("✅ .env: Variables critiques présentes")
                
                # Vérifier les clés API
                if 'your_youtube_api_key_here' in env_content:
                    issues.append("⚠️ .env: Clé YouTube non configurée (valeur par défaut)")
                
            except Exception as e:
                issues.append(f"❌ .env: Erreur lecture - {e}")
        else:
            issues.append("❌ Fichier .env manquant")
        
        self.audit_report['imperfections'].extend(issues)
        logger.info(f"📊 Configuration: {len(issues)} problèmes identifiés")
        
    def generate_corrections_plan(self):
        """Génère un plan de corrections"""
        logger.info("\n🔧 PLAN DE CORRECTIONS")
        logger.info("-" * 50)
        
        corrections = []
        
        for issue in self.audit_report['imperfections']:
            if 'manquant' in issue:
                if 'docker-compose.yml' in issue:
                    corrections.append("1. Créer docker-compose.yml complet")
                elif '.env' in issue:
                    corrections.append("2. Créer fichier .env avec toutes les variables")
                elif 'Base de données' in issue:
                    corrections.append("3. Initialiser la base de données")
                elif 'Dossier' in issue:
                    corrections.append("4. Créer les dossiers manquants")
            
            elif 'non configurée' in issue:
                corrections.append("5. Configurer les clés API dans .env")
            
            elif 'Import' in issue:
                corrections.append("6. Corriger les imports Python")
        
        # Dédupliquer et numéroter
        unique_corrections = list(set(corrections))
        self.audit_report['corrections_needed'] = unique_corrections
        
        for i, correction in enumerate(unique_corrections, 1):
            logger.info(f"   {i}. {correction}")
        
    def run_complete_audit(self):
        """Exécute l'audit complet"""
        logger.info("🔍 AUDIT GLOBAL DU PROJET SEMANTIC PULSE X")
        logger.info("=" * 70)
        
        # Exécuter tous les audits
        self.audit_1_project_structure()
        self.audit_2_imports_and_dependencies()
        self.audit_3_docker_configuration()
        self.audit_4_database_schema()
        self.audit_5_data_sources()
        self.audit_6_ai_modules()
        self.audit_7_environment_configuration()
        
        # Générer le plan de corrections
        self.generate_corrections_plan()
        
        # Résumé final
        total_issues = len(self.audit_report['imperfections'])
        logger.info("\n" + "=" * 70)
        logger.info("📊 RÉSUMÉ DE L'AUDIT GLOBAL")
        logger.info("=" * 70)
        logger.info(f"🔍 Total des problèmes identifiés: {total_issues}")
        logger.info(f"🔧 Corrections nécessaires: {len(self.audit_report['corrections_needed'])}")
        
        if total_issues == 0:
            logger.info("🎉 PROJET PARFAIT! Prêt pour Docker")
            self.audit_report['docker_readiness'] = True
        elif total_issues <= 3:
            logger.info("✅ PROJET TRÈS BON! Quelques ajustements mineurs")
            self.audit_report['docker_readiness'] = True
        elif total_issues <= 7:
            logger.info("⚠️ PROJET MOYEN! Plusieurs corrections nécessaires")
            self.audit_report['docker_readiness'] = False
        else:
            logger.info("❌ PROJET PROBLÉMATIQUE! Remise en ordre majeure")
            self.audit_report['docker_readiness'] = False
        
        logger.info("=" * 70)
        
        # Sauvegarder le rapport
        report_file = Path("data/processed/audit_global_projet.json")
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.audit_report, f, ensure_ascii=False, indent=2)
        
        logger.info(f"📊 Rapport d'audit sauvegardé: {report_file}")
        
        return self.audit_report

def main():
    """Fonction principale"""
    logger.info("🔍 AUDIT GLOBAL DU PROJET")
    
    auditor = ProjectAuditor()
    
    try:
        report = auditor.run_complete_audit()
        return report['docker_readiness']
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'audit: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
