#!/usr/bin/env python3
"""
Script de configuration des sources de données - Semantic Pulse X
Configure et collecte les données de toutes les sources
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.append(str(Path(__file__).parent.parent))

from app.backend.data_sources.data_source_manager import data_source_manager


def main():
    """Fonction principale de configuration"""
    print("🚀 Configuration des sources de données Semantic Pulse X")
    print("=" * 60)
    
    try:
        # Collecter les données de toutes les sources
        print("\n📊 Démarrage de la collecte complète...")
        all_data = data_source_manager.collect_all_sources()
        
        if "error" in all_data:
            print(f"❌ Erreur: {all_data['error']}")
            return 1
        
        # Afficher le rapport
        report = all_data.get("report", {})
        print(f"\n📈 Rapport de collecte:")
        print(f"   - Sources configurées: {report.get('total_sources', 0)}")
        print(f"   - Statut des sources: {report.get('sources_status', {})}")
        
        # Afficher le résumé des données
        data_summary = report.get("data_summary", {})
        print(f"\n📊 Résumé des données collectées:")
        for source, summary in data_summary.items():
            print(f"   - {source}: {summary.get('total_items', 0)} éléments")
        
        # Afficher les recommandations
        recommendations = report.get("recommendations", [])
        if recommendations:
            print(f"\n💡 Recommandations:")
            for rec in recommendations:
                print(f"   - {rec}")
        
        print(f"\n✅ Configuration terminée avec succès!")
        print(f"📁 Données sauvegardées dans: data/raw/")
        
        return 0
        
    except Exception as e:
        print(f"❌ Erreur lors de la configuration: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
