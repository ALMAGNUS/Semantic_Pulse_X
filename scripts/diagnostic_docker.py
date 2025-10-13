#!/usr/bin/env python3
"""
Diagnostic Docker - Semantic Pulse X
Script pour diagnostiquer les problèmes Docker Compose
"""

import os
import subprocess
import sys
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_docker_installation():
    """Vérifie l'installation Docker"""
    logger.info("🐳 Vérification de l'installation Docker")
    
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"✅ Docker installé: {result.stdout.strip()}")
            return True
        else:
            logger.error(f"❌ Docker non installé: {result.stderr}")
            return False
    except FileNotFoundError:
        logger.error("❌ Docker non trouvé dans le PATH")
        return False

def check_docker_compose():
    """Vérifie Docker Compose"""
    logger.info("🐳 Vérification de Docker Compose")
    
    try:
        result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"✅ Docker Compose installé: {result.stdout.strip()}")
            return True
        else:
            logger.error(f"❌ Docker Compose non installé: {result.stderr}")
            return False
    except FileNotFoundError:
        logger.error("❌ Docker Compose non trouvé dans le PATH")
        return False

def check_docker_running():
    """Vérifie si Docker est en cours d'exécution"""
    logger.info("🐳 Vérification du statut Docker")
    
    try:
        result = subprocess.run(['docker', 'info'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("✅ Docker est en cours d'exécution")
            return True
        else:
            logger.error(f"❌ Docker n'est pas en cours d'exécution: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"❌ Erreur lors de la vérification Docker: {e}")
        return False

def check_docker_images():
    """Vérifie les images Docker disponibles"""
    logger.info("🐳 Vérification des images Docker")
    
    try:
        result = subprocess.run(['docker', 'images'], capture_output=True, text=True)
        if result.returncode == 0:
            images = result.stdout.strip().split('\n')[1:]  # Skip header
            logger.info(f"✅ {len(images)} image(s) Docker disponible(s)")
            
            # Vérifier les images spécifiques
            image_names = [line.split()[0] for line in images if line.strip()]
            
            required_images = ['redis', 'postgres', 'minio/minio', 'prom/prometheus', 'grafana/grafana']
            for img in required_images:
                if any(img in name for name in image_names):
                    logger.info(f"✅ Image {img} disponible")
                else:
                    logger.warning(f"⚠️ Image {img} non disponible")
            
            return True
        else:
            logger.error(f"❌ Erreur lors de la récupération des images: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"❌ Erreur lors de la vérification des images: {e}")
        return False

def check_docker_compose_config():
    """Vérifie la configuration Docker Compose"""
    logger.info("🐳 Vérification de la configuration Docker Compose")
    
    try:
        result = subprocess.run(['docker-compose', 'config'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("✅ Configuration Docker Compose valide")
            
            # Analyser la configuration
            config = result.stdout
            if 'prefecthq/prefect:2.14.10' in config:
                logger.warning("⚠️ Image Prefect trouvée dans la configuration")
            
            return True
        else:
            logger.error(f"❌ Configuration Docker Compose invalide: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"❌ Erreur lors de la vérification de la configuration: {e}")
        return False

def check_environment_variables():
    """Vérifie les variables d'environnement"""
    logger.info("🐳 Vérification des variables d'environnement")
    
    env_vars = [
        'DOCKER_BUILDKIT',
        'COMPOSE_PROJECT_NAME',
        'IMAGE',
        'DOCKER_HOST',
        'COMPOSE_FILE'
    ]
    
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            logger.info(f"✅ {var}={value}")
        else:
            logger.info(f"ℹ️ {var} non définie")

def check_docker_compose_file():
    """Vérifie le fichier docker-compose.yml"""
    logger.info("🐳 Vérification du fichier docker-compose.yml")
    
    if not os.path.exists('docker-compose.yml'):
        logger.error("❌ Fichier docker-compose.yml non trouvé")
        return False
    
    try:
        with open('docker-compose.yml', 'r', encoding='utf-8') as f:
            content = f.read()
        
        logger.info("✅ Fichier docker-compose.yml trouvé")
        
        # Vérifier les images
        if 'prefecthq/prefect:2.14.10' in content:
            logger.warning("⚠️ Image Prefect trouvée dans le fichier")
        
        # Compter les services
        services = content.count('image:')
        logger.info(f"ℹ️ {services} service(s) avec image définie")
        
        return True
    except Exception as e:
        logger.error(f"❌ Erreur lors de la lecture du fichier: {e}")
        return False

def main():
    """Fonction principale de diagnostic"""
    logger.info("🔍 DIAGNOSTIC DOCKER - SEMANTIC PULSE X")
    logger.info("=" * 50)
    
    checks = [
        check_docker_installation,
        check_docker_compose,
        check_docker_running,
        check_docker_images,
        check_docker_compose_config,
        check_environment_variables,
        check_docker_compose_file
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result if result is not None else False)
        except Exception as e:
            logger.error(f"❌ Erreur lors de {check.__name__}: {e}")
            results.append(False)
    
    # Résumé
    logger.info("\n" + "=" * 50)
    logger.info("📊 RÉSUMÉ DU DIAGNOSTIC")
    logger.info("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        logger.info("✅ Tous les tests sont passés")
        logger.info("🎉 Docker est correctement configuré")
    else:
        logger.error(f"❌ {total - passed} test(s) échoué(s)")
        logger.info("💡 Vérifiez les erreurs ci-dessus")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)