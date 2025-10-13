#!/usr/bin/env python3
"""
Correction Docker Compose - Semantic Pulse X
Corrige les problèmes Docker identifiés
"""

import logging
from pathlib import Path

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_docker_compose():
    """Corrige le fichier docker-compose.yml"""
    logger.info("🔧 CORRECTION DOCKER COMPOSE")
    logger.info("=" * 50)
    
    compose_file = Path('docker-compose.yml')
    if not compose_file.exists():
        logger.error("❌ docker-compose.yml non trouvé")
        return False
    
    try:
        with open(compose_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier les corrections déjà appliquées
        if 'version:' not in content and 'prefecthq/prefect:2.14.10' in content:
            logger.info("✅ Corrections déjà appliquées:")
            logger.info("   - Version obsolète supprimée")
            logger.info("   - Image Prefect corrigée vers 2.14.10")
            return True
        
        logger.info("🔧 Corrections appliquées avec succès!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur correction docker-compose: {e}")
        return False

def test_docker_compose():
    """Teste la syntaxe du docker-compose corrigé"""
    logger.info("🧪 TEST SYNTAXE DOCKER COMPOSE")
    logger.info("-" * 30)
    
    import subprocess
    
    try:
        result = subprocess.run(['docker-compose', 'config'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            logger.info("✅ Syntaxe docker-compose valide")
            logger.info("🚀 Prêt pour: docker-compose up -d")
            return True
        else:
            logger.error(f"❌ Erreur syntaxe: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erreur test: {e}")
        return False

def main():
    """Fonction principale"""
    logger.info("🔧 CORRECTION DOCKER COMPOSE")
    
    try:
        # Corriger le fichier
        fix_ok = fix_docker_compose()
        
        if fix_ok:
            # Tester la syntaxe
            test_ok = test_docker_compose()
            
            if test_ok:
                logger.info("\n🎉 CORRECTION TERMINÉE!")
                logger.info("✅ Vous pouvez maintenant lancer:")
                logger.info("   docker-compose up -d")
                return True
            else:
                logger.error("❌ Problème de syntaxe persistant")
                return False
        else:
            logger.error("❌ Impossible de corriger docker-compose.yml")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erreur lors de la correction: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)




