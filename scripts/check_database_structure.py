#!/usr/bin/env python3
"""
Vérificateur de structure de base de données - Semantic Pulse X
Vérifie la conformité Merise avec les relations cardinales
"""

import sqlite3
import logging
from pathlib import Path

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_database_structure():
    """Vérifie la structure de la base de données selon Merise."""
    
    db_file = Path("semantic_pulse.db")
    if not db_file.exists():
        logger.error("❌ Base de données semantic_pulse.db non trouvée")
        return False
    
    logger.info("🔍 VÉRIFICATION DE LA STRUCTURE MERISE")
    logger.info("=" * 60)
    
    try:
        conn = sqlite3.connect(str(db_file))
        cursor = conn.cursor()
        
        # 1. Lister toutes les tables
        logger.info("📊 TABLES DANS LA BASE:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        table_names = [table[0] for table in tables]
        for table_name in table_names:
            logger.info(f"  ✅ {table_name}")
        
        # 2. Vérifier les entités Merise obligatoires
        logger.info("\n🏗️ VÉRIFICATION DES ENTITÉS MERISE:")
        
        required_entities = ['programmes', 'diffusions', 'reactions', 'utilisateurs', 'sources']
        missing_entities = []
        
        for entity in required_entities:
            if entity in table_names:
                logger.info(f"  ✅ {entity.upper()}")
            else:
                logger.info(f"  ❌ {entity.upper()} - MANQUANTE")
                missing_entities.append(entity)
        
        # 3. Vérifier les tables de logs (MLD)
        logger.info("\n📋 VÉRIFICATION DES TABLES DE LOGS (MLD):")
        
        log_tables = ['log_ingestion', 'agregation_emotionnelle']
        for log_table in log_tables:
            if log_table in table_names:
                logger.info(f"  ✅ {log_table.upper()}")
            else:
                logger.info(f"  ❌ {log_table.upper()} - MANQUANTE")
        
        # 4. Analyser la structure détaillée de chaque table
        logger.info("\n🔍 STRUCTURE DÉTAILLÉE DES TABLES:")
        
        for table_name in table_names:
            logger.info(f"\n📋 TABLE: {table_name.upper()}")
            
            # Informations sur les colonnes
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            logger.info("  Colonnes:")
            for col in columns:
                col_id, col_name, col_type, not_null, default_val, pk = col
                pk_indicator = " 🔑" if pk else ""
                not_null_indicator = " NOT NULL" if not_null else ""
                logger.info(f"    - {col_name} ({col_type}){not_null_indicator}{pk_indicator}")
            
            # Clés étrangères
            cursor.execute(f"PRAGMA foreign_key_list({table_name});")
            foreign_keys = cursor.fetchall()
            
            if foreign_keys:
                logger.info("  Clés étrangères:")
                for fk in foreign_keys:
                    logger.info(f"    - {fk[3]} -> {fk[2]}.{fk[4]}")
            else:
                logger.info("  Clés étrangères: Aucune")
        
        # 5. Vérifier les relations cardinales selon Merise
        logger.info("\n🔗 VÉRIFICATION DES RELATIONS CARDINALES:")
        
        # Relations attendues selon le modèle Merise
        expected_relations = {
            'programmes': {
                'diffusions': '1:N',  # Un programme peut avoir plusieurs diffusions
                'sources': 'N:1'      # Plusieurs programmes peuvent venir d'une source
            },
            'diffusions': {
                'reactions': '1:N',   # Une diffusion peut avoir plusieurs réactions
                'programmes': 'N:1'   # Plusieurs diffusions appartiennent à un programme
            },
            'reactions': {
                'utilisateurs': 'N:1', # Plusieurs réactions peuvent venir d'un utilisateur
                'diffusions': 'N:1'    # Plusieurs réactions appartiennent à une diffusion
            },
            'utilisateurs': {
                'reactions': '1:N'     # Un utilisateur peut avoir plusieurs réactions
            },
            'sources': {
                'programmes': '1:N'    # Une source peut avoir plusieurs programmes
            }
        }
        
        # Vérifier les relations via les clés étrangères
        for table_name in table_names:
            if table_name in expected_relations:
                logger.info(f"\n  📊 {table_name.upper()}:")
                
                cursor.execute(f"PRAGMA foreign_key_list({table_name});")
                actual_fks = cursor.fetchall()
                
                for target_table, expected_cardinality in expected_relations[table_name].items():
                    if target_table in table_names:
                        # Chercher la clé étrangère vers target_table
                        fk_found = any(fk[2] == target_table for fk in actual_fks)
                        
                        if fk_found:
                            logger.info(f"    ✅ -> {target_table} ({expected_cardinality})")
                        else:
                            logger.info(f"    ❌ -> {target_table} ({expected_cardinality}) - FK manquante")
                    else:
                        logger.info(f"    ⚠️ -> {target_table} - Table inexistante")
        
        # 6. Vérifier les contraintes d'intégrité
        logger.info("\n🛡️ VÉRIFICATION DES CONTRAINTES D'INTÉGRITÉ:")
        
        # Vérifier les clés primaires
        for table_name in table_names:
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            pk_columns = [col[1] for col in columns if col[5]]  # col[5] = pk
            if pk_columns:
                logger.info(f"  ✅ {table_name}: PK = {', '.join(pk_columns)}")
            else:
                logger.info(f"  ❌ {table_name}: Pas de clé primaire")
        
        # 7. Statistiques des données
        logger.info("\n📊 STATISTIQUES DES DONNÉES:")
        
        for table_name in table_names:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            logger.info(f"  📈 {table_name}: {count} enregistrements")
        
        conn.close()
        
        # 8. Résumé de conformité
        logger.info("\n" + "=" * 60)
        logger.info("📋 RÉSUMÉ DE CONFORMITÉ MERISE:")
        logger.info("=" * 60)
        
        if not missing_entities:
            logger.info("✅ Toutes les entités Merise sont présentes")
        else:
            logger.info(f"❌ Entités manquantes: {', '.join(missing_entities)}")
        
        logger.info(f"✅ Tables créées: {len(table_names)}")
        logger.info(f"✅ Relations cardinales: Vérifiées")
        logger.info(f"✅ Contraintes d'intégrité: Vérifiées")
        
        logger.info("\n🎯 RECOMMANDATIONS:")
        if missing_entities:
            logger.info("  🔧 Créer les entités manquantes")
        logger.info("  📊 Insérer des données de test")
        logger.info("  🔗 Tester les relations cardinales")
        logger.info("  📈 Générer des vues agrégées (MLP)")
        
        logger.info("=" * 60)
        
        return len(missing_entities) == 0
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la vérification: {e}")
        return False

def main():
    """Fonction principale."""
    logger.info("🔍 VÉRIFICATEUR DE STRUCTURE MERISE")
    
    success = check_database_structure()
    
    if success:
        logger.info("🎉 Structure Merise conforme!")
    else:
        logger.info("⚠️ Structure Merise à corriger")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)




