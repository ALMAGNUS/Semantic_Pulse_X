#!/usr/bin/env python3
"""
Audit complet du projet Semantic Pulse X
Diagnostic et plan de remise en ordre
"""

import os
import json
import pandas as pd
import sqlite3
import logging
from pathlib import Path
from datetime import datetime

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def audit_complet():
    """Audit complet du projet."""
    
    logger.info("🔍 AUDIT COMPLET DU PROJET SEMANTIC PULSE X")
    logger.info("=" * 70)
    
    audit_report = {
        'timestamp': datetime.now().isoformat(),
        'status': 'AUDIT_EN_COURS',
        'problemes': [],
        'recommandations': [],
        'sources_donnees': {},
        'architecture': {},
        'conformite_rgpd': {},
        'etat_actuel': {}
    }
    
    # 1. AUDIT DES 5 SOURCES DE DONNÉES OBLIGATOIRES
    logger.info("\n📊 AUDIT DES 5 SOURCES DE DONNÉES:")
    logger.info("-" * 50)
    
    sources_status = {
        'fichier_plat': {'status': 'unknown', 'details': {}},
        'base_relationnelle': {'status': 'unknown', 'details': {}},
        'big_data': {'status': 'unknown', 'details': {}},
        'web_scraping': {'status': 'unknown', 'details': {}},
        'api_rest': {'status': 'unknown', 'details': {}}
    }
    
    # Source 1: Fichier plat (CSV/JSON/Parquet)
    logger.info("1️⃣ FICHIER PLAT (CSV/JSON/Parquet):")
    csv_files = list(Path("data/raw").rglob("*.csv"))
    json_files = list(Path("data/raw").rglob("*.json"))
    parquet_files = list(Path("data/processed").rglob("*.parquet"))
    
    if csv_files or json_files or parquet_files:
        sources_status['fichier_plat']['status'] = 'OK'
        sources_status['fichier_plat']['details'] = {
            'csv': len(csv_files),
            'json': len(json_files),
            'parquet': len(parquet_files)
        }
        logger.info(f"  ✅ Trouvé: {len(csv_files)} CSV, {len(json_files)} JSON, {len(parquet_files)} Parquet")
    else:
        sources_status['fichier_plat']['status'] = 'MANQUANT'
        logger.info("  ❌ Aucun fichier plat trouvé")
    
    # Source 2: Base relationnelle
    logger.info("2️⃣ BASE RELATIONNELLE:")
    db_file = Path("semantic_pulse.db")
    if db_file.exists():
        try:
            conn = sqlite3.connect(str(db_file))
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            if tables:
                sources_status['base_relationnelle']['status'] = 'OK'
                sources_status['base_relationnelle']['details'] = {
                    'tables': len(tables),
                    'table_names': [t[0] for t in tables]
                }
                logger.info(f"  ✅ Base SQLite avec {len(tables)} tables")
                
                # Compter les données
                total_data = 0
                for table_name, in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                    count = cursor.fetchone()[0]
                    total_data += count
                    logger.info(f"    📊 {table_name}: {count} enregistrements")
                
                sources_status['base_relationnelle']['details']['total_data'] = total_data
            else:
                sources_status['base_relationnelle']['status'] = 'VIDE'
                logger.info("  ⚠️ Base vide (pas de tables)")
            
            conn.close()
        except Exception as e:
            sources_status['base_relationnelle']['status'] = 'ERREUR'
            logger.info(f"  ❌ Erreur base: {e}")
    else:
        sources_status['base_relationnelle']['status'] = 'MANQUANT'
        logger.info("  ❌ Fichier semantic_pulse.db non trouvé")
    
    # Source 3: Big Data
    logger.info("3️⃣ BIG DATA (Parquet/Data Lake):")
    bigdata_dir = Path("data/processed/bigdata")
    if bigdata_dir.exists():
        parquet_files = list(bigdata_dir.glob("*.parquet"))
        if parquet_files:
            sources_status['big_data']['status'] = 'OK'
            total_rows = 0
            for pf in parquet_files:
                try:
                    df = pd.read_parquet(pf)
                    total_rows += len(df)
                except:
                    pass
            
            sources_status['big_data']['details'] = {
                'files': len(parquet_files),
                'total_rows': total_rows
            }
            logger.info(f"  ✅ {len(parquet_files)} fichiers Parquet, {total_rows} lignes")
        else:
            sources_status['big_data']['status'] = 'VIDE'
            logger.info("  ⚠️ Dossier Big Data vide")
    else:
        sources_status['big_data']['status'] = 'MANQUANT'
        logger.info("  ❌ Dossier Big Data non trouvé")
    
    # Source 4: Web Scraping
    logger.info("4️⃣ WEB SCRAPING:")
    scraping_dir = Path("data/raw/web_scraping")
    if scraping_dir.exists():
        scraping_files = list(scraping_dir.glob("*.json"))
        if scraping_files:
            sources_status['web_scraping']['status'] = 'OK'
            sources_status['web_scraping']['details'] = {'files': len(scraping_files)}
            logger.info(f"  ✅ {len(scraping_files)} fichiers de scraping")
        else:
            sources_status['web_scraping']['status'] = 'VIDE'
            logger.info("  ⚠️ Dossier Web Scraping vide")
    else:
        sources_status['web_scraping']['status'] = 'MANQUANT'
        logger.info("  ❌ Dossier Web Scraping non trouvé")
    
    # Source 5: API REST
    logger.info("5️⃣ API REST:")
    api_dir = Path("data/raw/external_apis")
    if api_dir.exists():
        api_files = list(api_dir.glob("*.json"))
        if api_files:
            sources_status['api_rest']['status'] = 'OK'
            sources_status['api_rest']['details'] = {'files': len(api_files)}
            logger.info(f"  ✅ {len(api_files)} fichiers API")
        else:
            sources_status['api_rest']['status'] = 'VIDE'
            logger.info("  ⚠️ Dossier API vide")
    else:
        sources_status['api_rest']['status'] = 'MANQUANT'
        logger.info("  ❌ Dossier API non trouvé")
    
    # 2. AUDIT DE L'ARCHITECTURE
    logger.info("\n🏗️ AUDIT DE L'ARCHITECTURE:")
    logger.info("-" * 50)
    
    architecture_status = {
        'app_structure': 'unknown',
        'docker': 'unknown',
        'requirements': 'unknown',
        'documentation': 'unknown'
    }
    
    # Structure app/
    app_dir = Path("app")
    if app_dir.exists():
        backend_dir = app_dir / "backend"
        frontend_dir = app_dir / "frontend"
        
        if backend_dir.exists() and frontend_dir.exists():
            architecture_status['app_structure'] = 'OK'
            logger.info("  ✅ Structure app/backend/ et app/frontend/ présente")
        else:
            architecture_status['app_structure'] = 'PARTIEL'
            logger.info("  ⚠️ Structure app/ incomplète")
    else:
        architecture_status['app_structure'] = 'MANQUANT'
        logger.info("  ❌ Dossier app/ manquant")
    
    # Docker
    docker_file = Path("docker-compose.yml")
    if docker_file.exists():
        architecture_status['docker'] = 'OK'
        logger.info("  ✅ docker-compose.yml présent")
    else:
        architecture_status['docker'] = 'MANQUANT'
        logger.info("  ❌ docker-compose.yml manquant")
    
    # Requirements
    req_file = Path("requirements.txt")
    if req_file.exists():
        architecture_status['requirements'] = 'OK'
        logger.info("  ✅ requirements.txt présent")
    else:
        architecture_status['requirements'] = 'MANQUANT'
        logger.info("  ❌ requirements.txt manquant")
    
    # Documentation
    docs_dir = Path("docs")
    if docs_dir.exists():
        doc_files = list(docs_dir.glob("*.md"))
        architecture_status['documentation'] = 'OK'
        logger.info(f"  ✅ {len(doc_files)} fichiers de documentation")
    else:
        architecture_status['documentation'] = 'MANQUANT'
        logger.info("  ❌ Dossier docs/ manquant")
    
    # 3. AUDIT RGPD
    logger.info("\n🛡️ AUDIT CONFORMITÉ RGPD:")
    logger.info("-" * 50)
    
    rgpd_status = {
        'anonymisation': 'unknown',
        'pseudonymisation': 'unknown',
        'traçabilité': 'unknown'
    }
    
    # Chercher des traces d'anonymisation
    anonymization_files = list(Path(".").rglob("*anonym*"))
    if anonymization_files:
        rgpd_status['anonymisation'] = 'OK'
        logger.info(f"  ✅ {len(anonymization_files)} fichiers d'anonymisation")
    else:
        rgpd_status['anonymisation'] = 'MANQUANT'
        logger.info("  ❌ Aucun fichier d'anonymisation trouvé")
    
    # 4. DIAGNOSTIC DES PROBLÈMES
    logger.info("\n🚨 DIAGNOSTIC DES PROBLÈMES:")
    logger.info("-" * 50)
    
    problemes = []
    
    # Problème 1: Sources de données
    sources_ok = sum(1 for s in sources_status.values() if s['status'] == 'OK')
    if sources_ok < 5:
        problemes.append(f"Seulement {sources_ok}/5 sources de données opérationnelles")
    
    # Problème 2: Architecture
    arch_ok = sum(1 for a in architecture_status.values() if a == 'OK')
    if arch_ok < 4:
        problemes.append(f"Architecture incomplète: {arch_ok}/4 composants OK")
    
    # Problème 3: RGPD
    rgpd_ok = sum(1 for r in rgpd_status.values() if r == 'OK')
    if rgpd_ok < 3:
        problemes.append(f"Conformité RGPD incomplète: {rgpd_ok}/3 aspects OK")
    
    for i, probleme in enumerate(problemes, 1):
        logger.info(f"  {i}. ❌ {probleme}")
    
    # 5. RECOMMANDATIONS
    logger.info("\n💡 RECOMMANDATIONS:")
    logger.info("-" * 50)
    
    recommandations = [
        "1. 🔄 SIMPLIFIER le projet - revenir aux bases",
        "2. 📊 FOCALISER sur les 5 sources de données obligatoires",
        "3. 🏗️ CRÉER une architecture simple et fonctionnelle",
        "4. 🛡️ IMPLÉMENTER l'anonymisation RGPD de base",
        "5. 📝 DOCUMENTER chaque étape clairement",
        "6. 🧪 TESTER chaque composant individuellement",
        "7. 🔗 INTÉGRER progressivement les sources"
    ]
    
    for rec in recommandations:
        logger.info(f"  {rec}")
    
    # 6. PLAN DE REMISE EN ORDRE
    logger.info("\n🎯 PLAN DE REMISE EN ORDRE:")
    logger.info("-" * 50)
    
    plan = [
        "ÉTAPE 1: Nettoyer et réorganiser la structure",
        "ÉTAPE 2: Créer les 5 sources de données simples",
        "ÉTAPE 3: Implémenter l'anonymisation RGPD",
        "ÉTAPE 4: Créer un pipeline ETL basique",
        "ÉTAPE 5: Développer l'interface utilisateur",
        "ÉTAPE 6: Tester et documenter"
    ]
    
    for i, etape in enumerate(plan, 1):
        logger.info(f"  {i}. {etape}")
    
    # Sauvegarder le rapport
    audit_report.update({
        'sources_donnees': sources_status,
        'architecture': architecture_status,
        'conformite_rgpd': rgpd_status,
        'problemes': problemes,
        'recommandations': recommandations,
        'plan_remise_ordre': plan,
        'status': 'TERMINE'
    })
    
    report_file = Path("data/processed/audit_complet_projet.json")
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(audit_report, f, ensure_ascii=False, indent=2)
    
    logger.info(f"\n📊 Rapport d'audit sauvegardé: {report_file}")
    
    # 7. CONCLUSION
    logger.info("\n" + "=" * 70)
    logger.info("🎯 CONCLUSION DE L'AUDIT:")
    logger.info("=" * 70)
    
    if len(problemes) > 3:
        logger.info("❌ PROJET EN DIFFICULTÉ - Remise en ordre nécessaire")
        logger.info("💡 Recommandation: Repartir sur des bases simples")
    elif len(problemes) > 1:
        logger.info("⚠️ PROJET PARTIELLEMENT FONCTIONNEL - Corrections nécessaires")
        logger.info("💡 Recommandation: Corriger les problèmes identifiés")
    else:
        logger.info("✅ PROJET FONCTIONNEL - Optimisations possibles")
        logger.info("💡 Recommandation: Continuer le développement")
    
    logger.info("=" * 70)
    
    return audit_report

def main():
    """Fonction principale."""
    logger.info("🔍 AUDIT COMPLET DU PROJET SEMANTIC PULSE X")
    
    try:
        audit_report = audit_complet()
        return True
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'audit: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)




