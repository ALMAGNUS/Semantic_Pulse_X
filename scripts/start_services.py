#!/usr/bin/env python3
"""
Script de démarrage progressif - Semantic Pulse X
Démarrage étape par étape des services Big Data
"""

import subprocess
import time
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_command(command: str, description: str) -> bool:
    """
    Exécute une commande avec gestion d'erreur
    
    Args:
        command: Commande à exécuter
        description: Description de l'action
        
    Returns:
        bool: True si succès
    """
    try:
        logger.info(f"🔄 {description}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info(f"✅ {description} - Succès")
            return True
        else:
            logger.error(f"❌ {description} - Erreur: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ {description} - Exception: {e}")
        return False

def check_service_running(port: int, service_name: str) -> bool:
    """
    Vérifie si un service est en cours d'exécution
    
    Args:
        port: Port du service
        service_name: Nom du service
        
    Returns:
        bool: True si le service est actif
    """
    try:
        result = subprocess.run(f"netstat -an | findstr :{port}", shell=True, capture_output=True, text=True)
        if result.returncode == 0 and str(port) in result.stdout:
            logger.info(f"✅ {service_name} actif sur le port {port}")
            return True
        else:
            logger.warning(f"⚠️ {service_name} non actif sur le port {port}")
            return False
    except Exception as e:
        logger.error(f"❌ Erreur vérification {service_name}: {e}")
        return False

def wait_for_service(port: int, service_name: str, max_wait: int = 30) -> bool:
    """
    Attend qu'un service soit disponible
    
    Args:
        port: Port du service
        service_name: Nom du service
        max_wait: Temps d'attente maximum en secondes
        
    Returns:
        bool: True si le service est disponible
    """
    logger.info(f"⏳ Attente de {service_name} sur le port {port}")
    
    for i in range(max_wait):
        if check_service_running(port, service_name):
            return True
        time.sleep(1)
    
    logger.error(f"❌ {service_name} non disponible après {max_wait}s")
    return False

def main():
    """Fonction principale de démarrage progressif"""
    logger.info("🚀 Démarrage progressif de Semantic Pulse X")
    
    # Vérification de Docker
    if not run_command("docker --version", "Vérification Docker"):
        logger.error("❌ Docker non installé ou non accessible")
        return False
    
    # Vérification de Docker Compose
    if not run_command("docker-compose --version", "Vérification Docker Compose"):
        logger.error("❌ Docker Compose non installé")
        return False
    
    # Arrêt des services existants
    logger.info("🛑 Arrêt des services existants")
    run_command("docker-compose down", "Arrêt des conteneurs")
    
    # Démarrage des services essentiels
    logger.info("🔄 Démarrage des services essentiels")
    
    # MinIO (Data Lake)
    if not run_command("docker-compose up -d minio", "Démarrage MinIO"):
        logger.error("❌ Impossible de démarrer MinIO")
        return False
    
    # Attente de MinIO
    if not wait_for_service(9000, "MinIO", 30):
        return False
    
    # PostgreSQL (Database)
    if not run_command("docker-compose up -d postgres", "Démarrage PostgreSQL"):
        logger.error("❌ Impossible de démarrer PostgreSQL")
        return False
    
    # Attente de PostgreSQL
    if not wait_for_service(5432, "PostgreSQL", 30):
        return False
    
    # Redis (Cache)
    if not run_command("docker-compose up -d redis", "Démarrage Redis"):
        logger.error("❌ Impossible de démarrer Redis")
        return False
    
    # Attente de Redis
    if not wait_for_service(6379, "Redis", 15):
        return False
    
    # Vérification finale
    logger.info("🔍 Vérification finale des services")
    services_status = {
        "MinIO": check_service_running(9000, "MinIO"),
        "PostgreSQL": check_service_running(5432, "PostgreSQL"),
        "Redis": check_service_running(6379, "Redis")
    }
    
    active_services = sum(services_status.values())
    total_services = len(services_status)
    
    logger.info(f"📊 Services actifs: {active_services}/{total_services}")
    
    if active_services == total_services:
        logger.info("🎉 Tous les services sont actifs!")
        logger.info("🌐 MinIO Console: http://localhost:9001")
        logger.info("🗄️ PostgreSQL: localhost:5432")
        logger.info("⚡ Redis: localhost:6379")
        return True
    else:
        logger.warning("⚠️ Certains services ne sont pas actifs")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

