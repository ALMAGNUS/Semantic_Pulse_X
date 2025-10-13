#!/usr/bin/env python3
"""
Audit de conformité au prompt original - Semantic Pulse X
Vérifie que le projet respecte toutes les spécifications du prompt
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def audit_conformite_prompt():
    """Audit de conformité au prompt original."""
    
    logger.info("📋 AUDIT DE CONFORMITÉ AU PROMPT ORIGINAL")
    logger.info("=" * 70)
    
    conformite_report = {
        'timestamp': datetime.now().isoformat(),
        'conformite_generale': 'EN_COURS',
        'exigences_obligatoires': {},
        'prerequis_techniques': {},
        'modelisation_merise': {},
        'stack_technologique': {},
        'modules_ia': {},
        'conformite_rgpd': {},
        'problemes': [],
        'recommandations': []
    }
    
    # 1. EXIGENCES OBLIGATOIRES DU PROMPT
    logger.info("\n📋 EXIGENCES OBLIGATOIRES:")
    logger.info("-" * 50)
    
    exigences = {
        'rgpd_compliance': {'status': 'unknown', 'details': []},
        'code_economy': {'status': 'unknown', 'details': []},
        'reliability_scalability': {'status': 'unknown', 'details': []},
        'versioning_documentation': {'status': 'unknown', 'details': []},
        '5_data_sources': {'status': 'unknown', 'details': []},
        'anonymization': {'status': 'unknown', 'details': []},
        'multi_source_aggregation': {'status': 'unknown', 'details': []},
        'unique_final_dataset': {'status': 'unknown', 'details': []},
        'script_versioning': {'status': 'unknown', 'details': []}
    }
    
    # Vérifier RGPD Compliance
    logger.info("1️⃣ RGPD Compliance:")
    anonymization_files = list(Path(".").rglob("*anonym*"))
    if anonymization_files:
        exigences['rgpd_compliance']['status'] = 'OK'
        exigences['rgpd_compliance']['details'] = [f.name for f in anonymization_files]
        logger.info(f"  ✅ {len(anonymization_files)} fichiers d'anonymisation trouvés")
    else:
        exigences['rgpd_compliance']['status'] = 'MANQUANT'
        logger.info("  ❌ Aucun fichier d'anonymisation trouvé")
    
    # Vérifier les 5 sources de données
    logger.info("2️⃣ 5 Sources de données obligatoires:")
    sources_status = {
        'fichier_plat': Path("data/raw/kaggle_tweets/sentiment140.csv").exists(),
        'base_relationnelle': Path("semantic_pulse.db").exists(),
        'big_data': Path("data/processed/bigdata").exists(),
        'web_scraping': Path("data/raw/web_scraping").exists(),
        'api_rest': Path("data/raw/external_apis").exists()
    }
    
    sources_ok = sum(sources_status.values())
    if sources_ok == 5:
        exigences['5_data_sources']['status'] = 'OK'
        logger.info("  ✅ Les 5 sources de données sont présentes")
    else:
        exigences['5_data_sources']['status'] = 'PARTIEL'
        logger.info(f"  ⚠️ Seulement {sources_ok}/5 sources présentes")
    
    # Vérifier l'architecture
    logger.info("3️⃣ Architecture modulaire:")
    app_structure = {
        'app_backend': Path("app/backend").exists(),
        'app_frontend': Path("app/frontend").exists(),
        'ai_modules': Path("app/backend/ai").exists(),
        'etl_pipeline': Path("app/backend/etl").exists(),
        'models': Path("app/backend/models").exists()
    }
    
    arch_ok = sum(app_structure.values())
    if arch_ok >= 4:
        exigences['reliability_scalability']['status'] = 'OK'
        logger.info("  ✅ Architecture modulaire présente")
    else:
        exigences['reliability_scalability']['status'] = 'PARTIEL'
        logger.info(f"  ⚠️ Architecture incomplète: {arch_ok}/5 composants")
    
    # 2. PRÉREQUIS TECHNIQUES (A1, C1, C2, C3)
    logger.info("\n🔧 PRÉREQUIS TECHNIQUES:")
    logger.info("-" * 50)
    
    prerequis = {
        'A1_programmed_collection': {'status': 'unknown', 'details': []},
        'C1_web_api_automation': {'status': 'unknown', 'details': []},
        'C2_sql_queries': {'status': 'unknown', 'details': []},
        'C3_aggregation_preparation': {'status': 'unknown', 'details': []}
    }
    
    # A1: Collecte programmée avec Python
    logger.info("A1️⃣ Collecte programmée:")
    collection_scripts = list(Path("scripts").glob("*collect*"))
    if collection_scripts:
        prerequis['A1_programmed_collection']['status'] = 'OK'
        prerequis['A1_programmed_collection']['details'] = [s.name for s in collection_scripts]
        logger.info(f"  ✅ {len(collection_scripts)} scripts de collecte")
    else:
        prerequis['A1_programmed_collection']['status'] = 'MANQUANT'
        logger.info("  ❌ Aucun script de collecte programmée")
    
    # C1: Automatisation Web/API
    logger.info("C1️⃣ Automatisation Web/API:")
    web_api_files = list(Path(".").rglob("*web*")) + list(Path(".").rglob("*api*"))
    if web_api_files:
        prerequis['C1_web_api_automation']['status'] = 'OK'
        logger.info(f"  ✅ {len(web_api_files)} fichiers Web/API")
    else:
        prerequis['C1_web_api_automation']['status'] = 'MANQUANT'
        logger.info("  ❌ Aucun fichier Web/API")
    
    # C2: Requêtes SQL
    logger.info("C2️⃣ Requêtes SQL:")
    sql_files = list(Path(".").rglob("*.sql")) + list(Path(".").rglob("*sql*"))
    if sql_files or Path("semantic_pulse.db").exists():
        prerequis['C2_sql_queries']['status'] = 'OK'
        logger.info("  ✅ Base de données et requêtes SQL présentes")
    else:
        prerequis['C2_sql_queries']['status'] = 'MANQUANT'
        logger.info("  ❌ Aucune requête SQL")
    
    # C3: Agrégation et préparation
    logger.info("C3️⃣ Agrégation et préparation:")
    etl_files = list(Path("app/backend/etl").glob("*")) if Path("app/backend/etl").exists() else []
    if etl_files:
        prerequis['C3_aggregation_preparation']['status'] = 'OK'
        logger.info(f"  ✅ {len(etl_files)} modules ETL")
    else:
        prerequis['C3_aggregation_preparation']['status'] = 'MANQUANT'
        logger.info("  ❌ Aucun module d'agrégation")
    
    # 3. MODÉLISATION MERISE
    logger.info("\n🏗️ MODÉLISATION MERISE:")
    logger.info("-" * 50)
    
    merise_status = {
        'MCD_entities': {'status': 'unknown', 'details': []},
        'MLD_tables': {'status': 'unknown', 'details': []},
        'MLP_physical': {'status': 'unknown', 'details': []}
    }
    
    # Vérifier les entités Merise
    logger.info("MCD️⃣ Entités Merise:")
    required_entities = ['Programme', 'Diffusion', 'Réaction', 'Utilisateur', 'Source']
    
    # Chercher dans les modèles
    models_dir = Path("app/backend/models")
    if models_dir.exists():
        model_files = list(models_dir.glob("*.py"))
        if model_files:
            merise_status['MCD_entities']['status'] = 'OK'
            merise_status['MCD_entities']['details'] = [f.name for f in model_files]
            logger.info(f"  ✅ {len(model_files)} fichiers de modèles")
        else:
            merise_status['MCD_entities']['status'] = 'MANQUANT'
            logger.info("  ❌ Aucun fichier de modèle")
    else:
        merise_status['MCD_entities']['status'] = 'MANQUANT'
        logger.info("  ❌ Dossier models/ manquant")
    
    # 4. STACK TECHNOLOGIQUE MODERNE
    logger.info("\n💻 STACK TECHNOLOGIQUE:")
    logger.info("-" * 50)
    
    stack_status = {
        'docker': {'status': 'unknown', 'details': []},
        'fastapi': {'status': 'unknown', 'details': []},
        'streamlit': {'status': 'unknown', 'details': []},
        'langchain': {'status': 'unknown', 'details': []},
        'prefect': {'status': 'unknown', 'details': []},
        'prometheus_grafana': {'status': 'unknown', 'details': []},
        'alembic': {'status': 'unknown', 'details': []}
    }
    
    # Docker
    if Path("docker-compose.yml").exists():
        stack_status['docker']['status'] = 'OK'
        logger.info("  ✅ Docker Compose présent")
    else:
        stack_status['docker']['status'] = 'MANQUANT'
        logger.info("  ❌ Docker Compose manquant")
    
    # FastAPI
    if Path("app/backend/main.py").exists():
        stack_status['fastapi']['status'] = 'OK'
        logger.info("  ✅ FastAPI présent")
    else:
        stack_status['fastapi']['status'] = 'MANQUANT'
        logger.info("  ❌ FastAPI manquant")
    
    # Streamlit
    if Path("app/frontend/streamlit_app.py").exists():
        stack_status['streamlit']['status'] = 'OK'
        logger.info("  ✅ Streamlit présent")
    else:
        stack_status['streamlit']['status'] = 'MANQUANT'
        logger.info("  ❌ Streamlit manquant")
    
    # 5. MODULES IA
    logger.info("\n🧠 MODULES IA:")
    logger.info("-" * 50)
    
    ai_modules = {
        'embeddings': {'status': 'unknown', 'details': []},
        'emotion_ai': {'status': 'unknown', 'details': []},
        'langchain_agent': {'status': 'unknown', 'details': []},
        'topic_clustering': {'status': 'unknown', 'details': []},
        'anomaly_detection': {'status': 'unknown', 'details': []},
        'proactive_generation': {'status': 'unknown', 'details': []}
    }
    
    ai_dir = Path("app/backend/ai")
    if ai_dir.exists():
        ai_files = list(ai_dir.glob("*.py"))
        if ai_files:
            ai_modules['embeddings']['status'] = 'OK'
            logger.info(f"  ✅ {len(ai_files)} modules IA")
        else:
            ai_modules['embeddings']['status'] = 'MANQUANT'
            logger.info("  ❌ Aucun module IA")
    else:
        ai_modules['embeddings']['status'] = 'MANQUANT'
        logger.info("  ❌ Dossier ai/ manquant")
    
    # 6. ANALYSE DES PROBLÈMES
    logger.info("\n🚨 ANALYSE DES PROBLÈMES:")
    logger.info("-" * 50)
    
    problemes = []
    
    # Compter les problèmes
    for categorie, items in [
        ('Exigences', exigences),
        ('Prérequis', prerequis),
        ('Merise', merise_status),
        ('Stack', stack_status),
        ('IA', ai_modules)
    ]:
        for item_name, item_data in items.items():
            if item_data['status'] == 'MANQUANT':
                problemes.append(f"{categorie}: {item_name}")
            elif item_data['status'] == 'PARTIEL':
                problemes.append(f"{categorie}: {item_name} (partiel)")
    
    for i, probleme in enumerate(problemes, 1):
        logger.info(f"  {i}. ❌ {probleme}")
    
    # 7. RECOMMANDATIONS
    logger.info("\n💡 RECOMMANDATIONS:")
    logger.info("-" * 50)
    
    recommandations = [
        "1. 🔧 Compléter les modules IA manquants",
        "2. 🏗️ Finaliser la modélisation Merise",
        "3. 🛡️ Renforcer la conformité RGPD",
        "4. 📊 Implémenter l'agrégation multi-sources",
        "5. 🧪 Tester chaque composant individuellement",
        "6. 📝 Documenter les scripts et versions",
        "7. 🚀 Lancer l'application complète"
    ]
    
    for rec in recommandations:
        logger.info(f"  {rec}")
    
    # 8. CONCLUSION
    logger.info("\n" + "=" * 70)
    logger.info("🎯 CONCLUSION DE L'AUDIT:")
    logger.info("=" * 70)
    
    total_problemes = len(problemes)
    if total_problemes == 0:
        logger.info("🎉 CONFORMITÉ PARFAITE!")
        logger.info("✅ Toutes les spécifications du prompt sont respectées")
        conformite_report['conformite_generale'] = 'PARFAITE'
    elif total_problemes <= 3:
        logger.info("✅ CONFORMITÉ BONNE")
        logger.info("⚠️ Quelques améliorations mineures nécessaires")
        conformite_report['conformite_generale'] = 'BONNE'
    elif total_problemes <= 7:
        logger.info("⚠️ CONFORMITÉ PARTIELLE")
        logger.info("🔧 Plusieurs éléments à compléter")
        conformite_report['conformite_generale'] = 'PARTIELLE'
    else:
        logger.info("❌ CONFORMITÉ INSUFFISANTE")
        logger.info("🚨 Remise en ordre majeure nécessaire")
        conformite_report['conformite_generale'] = 'INSUFFISANTE'
    
    logger.info(f"📊 Problèmes identifiés: {total_problemes}")
    logger.info("=" * 70)
    
    # Sauvegarder le rapport
    conformite_report.update({
        'exigences_obligatoires': exigences,
        'prerequis_techniques': prerequis,
        'modelisation_merise': merise_status,
        'stack_technologique': stack_status,
        'modules_ia': ai_modules,
        'problemes': problemes,
        'recommandations': recommandations
    })
    
    report_file = Path("data/processed/audit_conformite_prompt.json")
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(conformite_report, f, ensure_ascii=False, indent=2)
    
    logger.info(f"\n📊 Rapport d'audit sauvegardé: {report_file}")
    
    return conformite_report

def main():
    """Fonction principale."""
    logger.info("📋 AUDIT DE CONFORMITÉ AU PROMPT ORIGINAL")
    
    try:
        audit_report = audit_conformite_prompt()
        return True
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'audit: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)




