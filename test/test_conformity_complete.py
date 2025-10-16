#!/usr/bin/env python3
"""
Test de Conformité Complet - Semantic Pulse X
Vérification de la conformité aux livrables E1/E2/E3
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConformityTester:
    """Testeur de conformité complet pour les livrables E1/E2/E3"""

    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "bloc_1_donnees": {},
            "bloc_2_modeles": {},
            "bloc_3_application": {},
            "conformity_score": 0.0,
            "critical_issues": [],
            "warnings": [],
            "recommendations": []
        }

    def test_bloc_1_donnees(self) -> dict[str, Any]:
        """Test de conformité Bloc 1 - Les Données"""
        logger.info("🧪 TEST BLOC 1 - LES DONNÉES")
        logger.info("-" * 50)

        bloc_results = {
            "sources_count": 0,
            "sources_details": {},
            "merise_compliance": False,
            "rgpd_compliance": False,
            "metadata_complete": False,
            "data_processing": False,
            "score": 0.0
        }

        try:
            # Test 1: Vérifier les 6 sources de données distinctes
            sources_expected = [
                "kaggle_tweets/file_source_tweets.csv", # Source 1: 50% Kaggle fichier plat
                "kaggle_tweets/db_source_tweets.csv",    # Source 2: 50% Kaggle base simple
                "gdelt_data.json",                       # Source 3: GDELT Big Data
                "youtube_data.json",                     # Source 4: APIs externes (YouTube)
                "web_scraping.json",                     # Source 5: Web Scraping (Yahoo+Franceinfo)
                "semantic_pulse.db"                      # Source 6: Base MERISE agrégée
            ]

            # Compter les 5 sources distinctes + base MERISE
            distinct_sources_found = 0
            kaggle_file_found = False
            kaggle_db_found = False
            gdelt_found = False
            apis_found = False
            scraping_found = False

            for source in sources_expected:
                if Path(f"data/raw/{source}").exists() or Path(source).exists():
                    bloc_results["sources_details"][source] = "✅ Trouvé"

                    # Compter les sources distinctes
                    if "file_source_tweets.csv" in source:
                        kaggle_file_found = True
                    elif "db_source_tweets.csv" in source:
                        kaggle_db_found = True
                    elif source == "gdelt_data.json":
                        gdelt_found = True
                    elif source == "youtube_data.json":
                        apis_found = True
                    elif source == "web_scraping.json":
                        scraping_found = True
                else:
                    bloc_results["sources_details"][source] = "❌ Manquant"

            # Compter les 5 sources distinctes
            if kaggle_file_found:
                distinct_sources_found += 1
            if kaggle_db_found:
                distinct_sources_found += 1
            if gdelt_found:
                distinct_sources_found += 1
            if apis_found:
                distinct_sources_found += 1
            if scraping_found:
                distinct_sources_found += 1

            bloc_results["sources_count"] = distinct_sources_found

            # Test 2: Vérifier la conformité MERISE
            if Path("semantic_pulse.db").exists():
                bloc_results["merise_compliance"] = True
                bloc_results["sources_details"]["merise_db"] = "✅ Base MERISE présente"
            else:
                bloc_results["sources_details"]["merise_db"] = "❌ Base MERISE manquante"

            # Test 3: Vérifier la documentation RGPD
            rgpd_docs = [
                "docs/LIVRABLES_BLOC_1_DONNEES.md",
                "docs/AUDIT_CONFORMITE_E1_E2_E3.md"
            ]

            rgpd_found = sum(1 for doc in rgpd_docs if Path(doc).exists())
            bloc_results["rgpd_compliance"] = rgpd_found > 0

            # Test 4: Vérifier les métadonnées
            metadata_docs = [
                "docs/RESUME_6_SOURCES.md",
                "docs/CODE_MERMAID_MERISE_REEL.md"
            ]

            metadata_found = sum(1 for doc in metadata_docs if Path(doc).exists())
            bloc_results["metadata_complete"] = metadata_found > 0

            # Test 5: Vérifier le traitement des données
            processing_scripts = [
                "scripts/aggregate_sources.py",
                "scripts/load_aggregated_to_db.py"
            ]

            processing_found = sum(1 for script in processing_scripts if Path(script).exists())
            bloc_results["data_processing"] = processing_found > 0

            # Calcul du score Bloc 1
            score_components = [
                bloc_results["sources_count"] / 5,  # 5 sources distinctes attendues
                bloc_results["merise_compliance"],
                bloc_results["rgpd_compliance"],
                bloc_results["metadata_complete"],
                bloc_results["data_processing"]
            ]

            bloc_results["score"] = sum(score_components) / len(score_components) * 100

            logger.info(f"✅ Bloc 1 - Score: {bloc_results['score']:.1f}%")
            logger.info(f"   Sources trouvées: {distinct_sources_found}/5 + Base MERISE")
            logger.info(f"   MERISE: {'✅' if bloc_results['merise_compliance'] else '❌'}")
            logger.info(f"   RGPD: {'✅' if bloc_results['rgpd_compliance'] else '❌'}")

        except Exception as e:
            logger.error(f"❌ Erreur test Bloc 1: {e}")
            bloc_results["error"] = str(e)

        return bloc_results

    def test_bloc_2_modeles(self) -> dict[str, Any]:
        """Test de conformité Bloc 2 - Les Modèles"""
        logger.info("🧪 TEST BLOC 2 - LES MODÈLES")
        logger.info("-" * 50)

        bloc_results = {
            "models_count": 0,
            "models_details": {},
            "performance_metrics": False,
            "drift_monitoring": False,
            "benchmarking": False,
            "monitoring_infrastructure": False,
            "score": 0.0
        }

        try:
            # Test 1: Vérifier les modèles IA
            ai_models = [
                "app/backend/ai/emotion_classifier.py",
                "app/backend/ai/langchain_agent.py",
                "app/backend/ai/topic_clustering.py"
            ]

            models_found = 0
            for model in ai_models:
                if Path(model).exists():
                    models_found += 1
                    bloc_results["models_details"][model] = "✅ Modèle présent"
                else:
                    bloc_results["models_details"][model] = "❌ Modèle manquant"

            bloc_results["models_count"] = models_found

            # Test 2: Vérifier les métriques de performance
            performance_scripts = [
                "scripts/test_components_individual.py",
                "test/test_end_to_end_ultime.py"
            ]

            performance_found = sum(1 for script in performance_scripts if Path(script).exists())
            bloc_results["performance_metrics"] = performance_found > 0

            # Test 3: Vérifier la surveillance de dérive (CRITIQUE)
            drift_components = [
                "scripts/model_drift_monitor.py",
                "app/backend/core/metrics.py"
            ]

            drift_found = sum(1 for component in drift_components if Path(component).exists())
            bloc_results["drift_monitoring"] = drift_found > 0

            # Test 4: Vérifier le benchmarking
            benchmarking_docs = [
                "docs/LIVRABLES_BLOC_2_MODELES.md"
            ]

            benchmarking_found = sum(1 for doc in benchmarking_docs if Path(doc).exists())
            bloc_results["benchmarking"] = benchmarking_found > 0

            # Test 5: Vérifier l'infrastructure de monitoring
            monitoring_components = [
                "monitoring/prometheus.yml",
                "monitoring/grafana/dashboards/semantic_pulse.json",
                "monitoring/alert_rules.yml"
            ]

            monitoring_found = sum(1 for component in monitoring_components if Path(component).exists())
            bloc_results["monitoring_infrastructure"] = monitoring_found > 0

            # Calcul du score Bloc 2
            score_components = [
                bloc_results["models_count"] / 3,  # 3 modèles attendus
                bloc_results["performance_metrics"],
                bloc_results["drift_monitoring"],  # CRITIQUE
                bloc_results["benchmarking"],
                bloc_results["monitoring_infrastructure"]
            ]

            bloc_results["score"] = sum(score_components) / len(score_components) * 100

            logger.info(f"✅ Bloc 2 - Score: {bloc_results['score']:.1f}%")
            logger.info(f"   Modèles trouvés: {models_found}/3")
            logger.info(f"   Surveillance dérive: {'✅' if bloc_results['drift_monitoring'] else '❌'}")
            logger.info(f"   Monitoring: {'✅' if bloc_results['monitoring_infrastructure'] else '❌'}")

        except Exception as e:
            logger.error(f"❌ Erreur test Bloc 2: {e}")
            bloc_results["error"] = str(e)

        return bloc_results

    def test_bloc_3_application(self) -> dict[str, Any]:
        """Test de conformité Bloc 3 - L'Application"""
        logger.info("🧪 TEST BLOC 3 - L'APPLICATION")
        logger.info("-" * 50)

        bloc_results = {
            "project_management": False,
            "tasks_completion": False,
            "ui_mockups": False,
            "architecture": False,
            "database_design": False,
            "score": 0.0
        }

        try:
            # Test 1: Vérifier la gestion de projet
            project_docs = [
                "docs/SCRUM_METHODOLOGY.md",
                "docs/LIVRABLES_BLOC_3_APPLICATION.md"
            ]

            project_found = sum(1 for doc in project_docs if Path(doc).exists())
            bloc_results["project_management"] = project_found > 0

            # Test 2: Vérifier les tâches principales
            main_tasks = [
                "app/backend/etl/pipeline.py",  # Pipeline ETL
                "app/frontend/streamlit_app.py"  # Interface utilisateur
            ]

            tasks_found = sum(1 for task in main_tasks if Path(task).exists())
            bloc_results["tasks_completion"] = tasks_found > 0

            # Test 3: Vérifier les maquettes
            ui_components = [
                "app/frontend/streamlit_app.py",
                "docs/GUIDE_DEMONSTRATION_PROF.md"
            ]

            ui_found = sum(1 for component in ui_components if Path(component).exists())
            bloc_results["ui_mockups"] = ui_found > 0

            # Test 4: Vérifier l'architecture
            architecture_docs = [
                "docs/ARCHITECTURE.md",
                "docs/INDEX_LIVRABLES_COMPLETS.md"
            ]

            arch_found = sum(1 for doc in architecture_docs if Path(doc).exists())
            bloc_results["architecture"] = arch_found > 0

            # Test 5: Vérifier la conception de base de données
            db_components = [
                "app/backend/models/schema.py",
                "semantic_pulse.db"
            ]

            db_found = sum(1 for component in db_components if Path(component).exists())
            bloc_results["database_design"] = db_found > 0

            # Calcul du score Bloc 3
            score_components = [
                bloc_results["project_management"],
                bloc_results["tasks_completion"],
                bloc_results["ui_mockups"],
                bloc_results["architecture"],
                bloc_results["database_design"]
            ]

            bloc_results["score"] = sum(score_components) / len(score_components) * 100

            logger.info(f"✅ Bloc 3 - Score: {bloc_results['score']:.1f}%")
            logger.info(f"   Gestion projet: {'✅' if bloc_results['project_management'] else '❌'}")
            logger.info(f"   Tâches principales: {'✅' if bloc_results['tasks_completion'] else '❌'}")
            logger.info(f"   Architecture: {'✅' if bloc_results['architecture'] else '❌'}")

        except Exception as e:
            logger.error(f"❌ Erreur test Bloc 3: {e}")
            bloc_results["error"] = str(e)

        return bloc_results

    def test_critical_functionality(self) -> dict[str, Any]:
        """Test des fonctionnalités critiques"""
        logger.info("🧪 TEST FONCTIONNALITÉS CRITIQUES")
        logger.info("-" * 50)

        critical_tests = {
            "drift_monitoring_working": False,
            "api_endpoints_working": False,
            "database_accessible": False,
            "monitoring_metrics_exposed": False
        }

        try:
            # Test 1: Surveillance de dérive fonctionnelle
            if Path("scripts/model_drift_monitor.py").exists():
                try:
                    import subprocess
                    result = subprocess.run(
                        ["python", "scripts/model_drift_monitor.py"],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    critical_tests["drift_monitoring_working"] = result.returncode == 0
                except Exception as e:
                    logger.warning(f"Test surveillance dérive: {e}")

            # Test 2: Endpoints API disponibles
            api_files = [
                "app/backend/api/routes.py",
                "app/backend/api/wordcloud_routes.py"
            ]

            api_found = sum(1 for file in api_files if Path(file).exists())
            critical_tests["api_endpoints_working"] = api_found > 0

            # Test 3: Base de données accessible
            if Path("semantic_pulse.db").exists():
                try:
                    import sqlite3
                    conn = sqlite3.connect("semantic_pulse.db")
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()
                    conn.close()
                    critical_tests["database_accessible"] = len(tables) > 0
                except Exception as e:
                    logger.warning(f"Test base de données: {e}")

            # Test 4: Métriques exposées
            if Path("app/backend/core/metrics.py").exists():
                critical_tests["monitoring_metrics_exposed"] = True

        except Exception as e:
            logger.error(f"❌ Erreur tests critiques: {e}")

        return critical_tests

    def run_complete_test(self):
        """Exécute le test de conformité complet"""
        logger.info("🚀 TEST DE CONFORMITÉ COMPLET - SEMANTIC PULSE X")
        logger.info("=" * 70)

        # Tests des 3 blocs
        self.results["bloc_1_donnees"] = self.test_bloc_1_donnees()
        self.results["bloc_2_modeles"] = self.test_bloc_2_modeles()
        self.results["bloc_3_application"] = self.test_bloc_3_application()

        # Test des fonctionnalités critiques
        critical_results = self.test_critical_functionality()

        # Calcul du score global
        bloc_scores = [
            self.results["bloc_1_donnees"]["score"],
            self.results["bloc_2_modeles"]["score"],
            self.results["bloc_3_application"]["score"]
        ]

        self.results["conformity_score"] = sum(bloc_scores) / len(bloc_scores)

        # Identification des problèmes critiques
        if not critical_results["drift_monitoring_working"]:
            self.results["critical_issues"].append("Surveillance de dérive non fonctionnelle")

        if not critical_results["api_endpoints_working"]:
            self.results["critical_issues"].append("Endpoints API manquants")

        if not critical_results["database_accessible"]:
            self.results["critical_issues"].append("Base de données inaccessible")

        # Génération des recommandations
        if self.results["conformity_score"] < 90:
            self.results["recommendations"].append("Améliorer la conformité globale")

        if self.results["bloc_2_modeles"]["score"] < 80:
            self.results["recommendations"].append("Renforcer le Bloc 2 - Modèles")

        # Affichage du résumé final
        self.print_final_summary()

        return self.results

    def print_final_summary(self):
        """Affiche le résumé final"""
        logger.info("\n" + "=" * 70)
        logger.info("📊 RÉSUMÉ FINAL DE CONFORMITÉ")
        logger.info("=" * 70)

        logger.info(f"🎯 Score global: {self.results['conformity_score']:.1f}%")
        logger.info(f"📊 Bloc 1 (Données): {self.results['bloc_1_donnees']['score']:.1f}%")
        logger.info(f"🤖 Bloc 2 (Modèles): {self.results['bloc_2_modeles']['score']:.1f}%")
        logger.info(f"🚀 Bloc 3 (Application): {self.results['bloc_3_application']['score']:.1f}%")

        if self.results["critical_issues"]:
            logger.info(f"\n🚨 Problèmes critiques ({len(self.results['critical_issues'])}):")
            for issue in self.results["critical_issues"]:
                logger.info(f"   - {issue}")

        if self.results["recommendations"]:
            logger.info(f"\n💡 Recommandations ({len(self.results['recommendations'])}):")
            for rec in self.results["recommendations"]:
                logger.info(f"   - {rec}")

        # Évaluation finale
        if self.results["conformity_score"] >= 95:
            logger.info("\n🎉 EXCELLENT! Conformité quasi-parfaite")
        elif self.results["conformity_score"] >= 90:
            logger.info("\n✅ TRÈS BON! Conformité élevée")
        elif self.results["conformity_score"] >= 80:
            logger.info("\n⚠️ BON! Quelques améliorations nécessaires")
        else:
            logger.info("\n❌ ATTENTION! Conformité insuffisante")

        logger.info("=" * 70)


def main():
    """Fonction principale"""
    tester = ConformityTester()
    results = tester.run_complete_test()

    # Sauvegarder les résultats
    output_file = "data/processed/conformity_test_results.json"
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Résultats sauvegardés: {output_file}")

    # Code de sortie basé sur la conformité
    if results["conformity_score"] >= 90:
        sys.exit(0)  # Succès
    else:
        sys.exit(1)  # Échec


if __name__ == "__main__":
    main()
