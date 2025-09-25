#!/usr/bin/env python3
"""
Script de démonstration ETL - Semantic Pulse X
Démonstration du pipeline ETL complet avec les 5 sources de données
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire racine au PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.backend.etl.pipeline import etl_pipeline
from app.backend.data_sources.data_source_manager import data_source_manager

def demo_etl_complete():
    """Démonstration complète du pipeline ETL"""
    print("🚀 DÉMONSTRATION ETL - Semantic Pulse X")
    print("=" * 60)
    
    print("\n📊 Étape 1: Collecte des données")
    print("-" * 40)
    
    # Test des sources de données
    sources = ["kaggle_tweets", "youtube", "instagram", "web_scraping"]
    
    for source_name in sources:
        print(f"🔄 Test de la source: {source_name}")
        try:
            source = data_source_manager.sources[source_name]
            if hasattr(source, '_create_sentiment140_data'):
                data_path = source._create_sentiment140_data()
                print(f"✅ {source_name}: Données créées - {data_path}")
            else:
                print(f"⚠️  {source_name}: Méthodes à implémenter")
        except Exception as e:
            print(f"❌ {source_name}: Erreur - {str(e)}")
    
    print("\n🔄 Étape 2: Pipeline ETL complet")
    print("-" * 40)
    
    try:
        # Exécution du pipeline ETL
        result = etl_pipeline.run_etl_pipeline()
        print("✅ Pipeline ETL exécuté avec succès")
        print(f"   Résultat: {result}")
    except Exception as e:
        print(f"❌ Erreur pipeline ETL: {str(e)}")
    
    print("\n🎯 Étape 3: Vérification des données")
    print("-" * 40)
    
    # Vérifier les fichiers générés
    data_dir = Path("data/raw")
    if data_dir.exists():
        print("📁 Fichiers générés dans data/raw/:")
        for file_path in data_dir.rglob("*"):
            if file_path.is_file():
                print(f"   - {file_path.relative_to(project_root)}")
    
    print("\n🎉 Démonstration ETL terminée !")

if __name__ == "__main__":
    demo_etl_complete()
