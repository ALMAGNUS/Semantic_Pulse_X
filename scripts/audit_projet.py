#!/usr/bin/env python3
"""
Audit complet du projet Semantic Pulse X
Revue de code et vérification de conformité
"""

import os
import sys
from pathlib import Path
import json
import ast
import importlib.util

def audit_projet():
    """Audit complet du projet"""
    print("🔍 AUDIT COMPLET - SEMANTIC PULSE X")
    print("=" * 70)
    
    project_root = Path(".")
    
    # 1. STRUCTURE DU PROJET
    print("\n📁 STRUCTURE DU PROJET")
    print("-" * 50)
    
    structure_attendue = {
        "app/": ["backend/", "frontend/"],
        "app/backend/": ["ai/", "api/", "core/", "data_sources/", "etl/", "models/", "orchestration/"],
        "app/frontend/": ["visualization/"],
        "docs/": [],
        "scripts/": [],
        "monitoring/": ["grafana/", "prometheus/"],
        "data/": ["raw/", "processed/"]
    }
    
    structure_ok = True
    for dossier, sous_dossiers in structure_attendue.items():
        if Path(dossier).exists():
            print(f"✅ {dossier}")
            for sous_dossier in sous_dossiers:
                if Path(dossier + sous_dossier).exists():
                    print(f"   ✅ {sous_dossier}")
                else:
                    print(f"   ❌ {sous_dossier} - MANQUANT")
                    structure_ok = False
        else:
            print(f"❌ {dossier} - MANQUANT")
            structure_ok = False
    
    # 2. FICHIERS CRITIQUES
    print("\n📄 FICHIERS CRITIQUES")
    print("-" * 50)
    
    fichiers_critiques = [
        "README.md",
        "requirements.txt",
        "docker-compose.yml",
        "Dockerfile",
        "app/backend/main.py",
        "app/frontend/streamlit_app.py",
        "app/backend/core/config.py",
        "app/backend/core/database.py",
        "app/backend/models/entities.py",
        "app/backend/ai/emotion_classifier.py",
        "app/backend/ai/embeddings.py",
        "app/backend/etl/pipeline.py",
        "app/backend/core/anonymization.py"
    ]
    
    fichiers_ok = True
    for fichier in fichiers_critiques:
        if Path(fichier).exists():
            print(f"✅ {fichier}")
        else:
            print(f"❌ {fichier} - MANQUANT")
            fichiers_ok = False
    
    # 3. CONFORMITÉ RGPD
    print("\n🔒 CONFORMITÉ RGPD")
    print("-" * 50)
    
    # Vérifier le module d'anonymisation
    try:
        sys.path.append(str(project_root))
        from app.backend.core.anonymization import anonymizer
        
        # Test d'anonymisation
        test_id = "test_user_123"
        anonymized = anonymizer.anonymize_user_id(test_id)
        hashed = anonymizer.hash_text("test text")
        
        print("✅ Module d'anonymisation fonctionnel")
        print(f"   • Test anonymisation: {test_id} → {anonymized}")
        print(f"   • Test hachage: 'test text' → {hashed[:20]}...")
        
        # Vérifier que les données personnelles ne sont pas stockées
        if "email" not in str(anonymizer.__dict__):
            print("✅ Aucune donnée personnelle stockée dans le module")
        else:
            print("❌ Données personnelles détectées dans le module")
            
    except Exception as e:
        print(f"❌ Erreur module anonymisation: {e}")
    
    # 4. MODÈLES DE DONNÉES
    print("\n🗄️ MODÈLES DE DONNÉES")
    print("-" * 50)
    
    try:
        from app.backend.models.entities import Base, Programme, Diffusion, Reaction, Utilisateur, Source
        
        print("✅ Modèles Merise implémentés")
        print("   • Programme")
        print("   • Diffusion") 
        print("   • Reaction")
        print("   • Utilisateur (anonymisé)")
        print("   • Source")
        
        # Vérifier les relations
        if hasattr(Programme, 'diffusions'):
            print("✅ Relations entre entités définies")
        else:
            print("❌ Relations manquantes")
            
    except Exception as e:
        print(f"❌ Erreur modèles de données: {e}")
    
    # 5. SOURCES DE DONNÉES
    print("\n📊 SOURCES DE DONNÉES")
    print("-" * 50)
    
    sources_attendues = [
        "app/backend/data_sources/kaggle_tweets.py",
        "app/backend/data_sources/youtube_api.py", 
        "app/backend/data_sources/instagram_api.py",
        "app/backend/data_sources/web_scraping.py",
        "app/backend/etl/data_sources.py"
    ]
    
    sources_ok = True
    for source in sources_attendues:
        if Path(source).exists():
            print(f"✅ {source}")
        else:
            print(f"❌ {source} - MANQUANT")
            sources_ok = False
    
    # 6. IA ET MODÈLES
    print("\n🤖 IA ET MODÈLES")
    print("-" * 50)
    
    modules_ia = [
        "app/backend/ai/emotion_classifier.py",
        "app/backend/ai/embeddings.py",
        "app/backend/ai/topic_clustering.py",
        "app/backend/ai/langchain_agent.py",
        "app/backend/ai/ollama_client.py"
    ]
    
    ia_ok = True
    for module in modules_ia:
        if Path(module).exists():
            print(f"✅ {module}")
        else:
            print(f"❌ {module} - MANQUANT")
            ia_ok = False
    
    # 7. API ET ENDPOINTS
    print("\n🌐 API ET ENDPOINTS")
    print("-" * 50)
    
    try:
        from app.backend.main import app
        
        routes = [route.path for route in app.routes if hasattr(route, 'path')]
        print(f"✅ {len(routes)} routes API configurées")
        
        endpoints_attendus = [
            "/",
            "/health",
            "/api/v1/emotions/",
            "/api/v1/sources/",
            "/api/v1/wordcloud/generate"
        ]
        
        for endpoint in endpoints_attendus:
            if any(endpoint in route for route in routes):
                print(f"   ✅ {endpoint}")
            else:
                print(f"   ❌ {endpoint} - MANQUANT")
                
    except Exception as e:
        print(f"❌ Erreur API: {e}")
    
    # 8. DASHBOARD STREAMLIT
    print("\n🎨 DASHBOARD STREAMLIT")
    print("-" * 50)
    
    if Path("app/frontend/streamlit_app.py").exists():
        print("✅ Application Streamlit principale")
        
        dashboards = [
            "app/frontend/streamlit_ollama_dashboard.py",
            "app/frontend/streamlit_wordcloud_dashboard.py"
        ]
        
        for dashboard in dashboards:
            if Path(dashboard).exists():
                print(f"   ✅ {dashboard}")
            else:
                print(f"   ❌ {dashboard} - MANQUANT")
    else:
        print("❌ Application Streamlit manquante")
    
    # 9. DOCKER ET DÉPLOIEMENT
    print("\n🐳 DOCKER ET DÉPLOIEMENT")
    print("-" * 50)
    
    docker_files = [
        "Dockerfile",
        "docker-compose.yml"
    ]
    
    for docker_file in docker_files:
        if Path(docker_file).exists():
            print(f"✅ {docker_file}")
        else:
            print(f"❌ {docker_file} - MANQUANT")
    
    # 10. MONITORING
    print("\n📊 MONITORING")
    print("-" * 50)
    
    monitoring_files = [
        "monitoring/prometheus.yml",
        "monitoring/grafana/dashboards/semantic_pulse.json",
        "monitoring/grafana/datasources/prometheus.yml"
    ]
    
    for monitoring_file in monitoring_files:
        if Path(monitoring_file).exists():
            print(f"✅ {monitoring_file}")
        else:
            print(f"❌ {monitoring_file} - MANQUANT")
    
    # 11. DOCUMENTATION
    print("\n📚 DOCUMENTATION")
    print("-" * 50)
    
    docs_files = [
        "README.md",
        "docs/ARCHITECTURE.md",
        "docs/RGPD.md",
        "docs/MERISE_MODELING.md"
    ]
    
    for doc_file in docs_files:
        if Path(doc_file).exists():
            print(f"✅ {doc_file}")
        else:
            print(f"❌ {doc_file} - MANQUANT")
    
    # 12. TESTS ET SCRIPTS
    print("\n🧪 TESTS ET SCRIPTS")
    print("-" * 50)
    
    scripts_files = [
        "scripts/demo_data_engineering_simple.py",
        "scripts/visualiser_resultats.py",
        "scripts/setup_data_sources.py",
        "scripts/setup_ollama.py"
    ]
    
    for script_file in scripts_files:
        if Path(script_file).exists():
            print(f"✅ {script_file}")
        else:
            print(f"❌ {script_file} - MANQUANT")
    
    # 13. DONNÉES
    print("\n💾 DONNÉES")
    print("-" * 50)
    
    data_dirs = [
        "data/raw/kaggle_tweets",
        "data/processed"
    ]
    
    for data_dir in data_dirs:
        if Path(data_dir).exists():
            files = list(Path(data_dir).glob("*"))
            print(f"✅ {data_dir} ({len(files)} fichiers)")
            for file in files[:3]:  # Afficher les 3 premiers
                print(f"   • {file.name}")
        else:
            print(f"❌ {data_dir} - MANQUANT")
    
    # 14. RÉSUMÉ DE L'AUDIT
    print("\n🎯 RÉSUMÉ DE L'AUDIT")
    print("=" * 70)
    
    # Compter les éléments
    total_elements = 0
    elements_ok = 0
    
    # Structure
    total_elements += len(structure_attendue)
    if structure_ok:
        elements_ok += len(structure_attendue)
    
    # Fichiers critiques
    total_elements += len(fichiers_critiques)
    if fichiers_ok:
        elements_ok += len(fichiers_critiques)
    
    # Sources
    total_elements += len(sources_attendues)
    if sources_ok:
        elements_ok += len(sources_attendues)
    
    # IA
    total_elements += len(modules_ia)
    if ia_ok:
        elements_ok += len(modules_ia)
    
    score = (elements_ok / total_elements) * 100 if total_elements > 0 else 0
    
    print(f"📊 SCORE GLOBAL: {score:.1f}%")
    print(f"   • Éléments vérifiés: {total_elements}")
    print(f"   • Éléments conformes: {elements_ok}")
    print(f"   • Éléments manquants: {total_elements - elements_ok}")
    
    if score >= 90:
        print("🎉 EXCELLENT: Projet très bien structuré et conforme")
    elif score >= 80:
        print("✅ BON: Projet bien structuré avec quelques améliorations possibles")
    elif score >= 70:
        print("⚠️ MOYEN: Projet correct mais nécessite des améliorations")
    else:
        print("❌ INSUFFISANT: Projet nécessite des corrections importantes")
    
    print("\n🚀 RECOMMANDATIONS:")
    print("   • Lancer Streamlit pour tester l'interface")
    print("   • Vérifier les nuages de mots")
    print("   • Tester l'API FastAPI")
    print("   • Valider les données générées")
    
    return score >= 80

if __name__ == "__main__":
    audit_projet()
