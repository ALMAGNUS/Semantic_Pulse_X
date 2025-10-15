#!/usr/bin/env python3
"""
TEST END-TO-END ULTIME - Semantic Pulse X
Test complet du pipeline ETL avec vérification des 5 sources
"""

import json
import os
import sqlite3
import sys
from pathlib import Path
from typing import Any

import pandas as pd

# Ajouter le chemin du projet
sys.path.insert(0, str(Path(__file__).parent.parent))

class EndToEndTester:
    """Testeur end-to-end du pipeline Semantic Pulse X"""

    def __init__(self):
        self.results = {
            "sources": {},
            "etl_pipeline": {},
            "database": {},
            "integration": {},
            "errors": []
        }
        self.project_root = Path(__file__).parent.parent

    def test_source_1_kaggle(self) -> dict[str, Any]:
        """Test Source 1: Kaggle CSV (Fichier plat)"""
        print("\n📊 TEST SOURCE 1: KAGGLE CSV")
        print("-" * 40)

        result = {"status": "FAIL", "files": [], "records": 0, "issues": []}

        # Chercher les fichiers Kaggle
        kaggle_paths = [
            "data/raw/kaggle_tweets/sentiment140.csv",
            "data/raw/kaggle_tweets.csv",
            "data/raw/sentiment140.csv"
        ]

        for path in kaggle_paths:
            if os.path.exists(path):
                result["files"].append(path)
                try:
                    df = pd.read_csv(path)
                    result["records"] = len(df)
                    print(f"✅ Fichier trouvé: {path} ({len(df)} enregistrements)")

                    # Vérifier les colonnes essentielles
                    required_cols = ["text", "sentiment", "target"]
                    missing_cols = [col for col in required_cols if col not in df.columns]
                    if missing_cols:
                        result["issues"].append(f"Colonnes manquantes: {missing_cols}")
                        print(f"❌ Colonnes manquantes: {missing_cols}")
                    else:
                        print(f"✅ Colonnes OK: {required_cols}")
                        result["status"] = "PASS"

                except Exception as e:
                    result["issues"].append(f"Erreur lecture: {e}")
                    print(f"❌ Erreur lecture: {e}")

        if not result["files"]:
            result["issues"].append("Aucun fichier Kaggle trouvé")
            print("❌ Aucun fichier Kaggle trouvé")

        return result

    def test_source_2_youtube(self) -> dict[str, Any]:
        """Test Source 2: YouTube API"""
        print("\n🎥 TEST SOURCE 2: YOUTUBE API")
        print("-" * 40)

        result = {"status": "FAIL", "files": [], "records": 0, "issues": []}

        # Chercher les fichiers YouTube
        youtube_paths = [
            "data/raw/youtube",
            "data/raw/external_apis",
            "data/processed"
        ]

        for base_path in youtube_paths:
            if os.path.exists(base_path):
                for file_path in Path(base_path).rglob("*youtube*"):
                    if file_path.suffix in ['.json', '.csv']:
                        result["files"].append(str(file_path))
                        try:
                            if file_path.suffix == '.json':
                                with open(file_path, encoding='utf-8') as f:
                                    data = json.load(f)
                                if isinstance(data, list):
                                    result["records"] += len(data)
                                else:
                                    result["records"] += 1
                            else:
                                df = pd.read_csv(file_path)
                                result["records"] += len(df)

                            print(f"✅ Fichier YouTube: {file_path.name}")

                        except Exception as e:
                            result["issues"].append(f"Erreur {file_path}: {e}")
                            print(f"❌ Erreur {file_path}: {e}")

        # Vérifier le contenu des vidéos
        if result["files"]:
            print(f"📊 Total fichiers YouTube: {len(result['files'])}")
            print(f"📊 Total enregistrements: {result['records']}")

            # Vérifier si on a le texte des vidéos
            has_video_text = False
            for file_path in result["files"]:
                try:
                    if file_path.endswith('.json'):
                        with open(file_path, encoding='utf-8') as f:
                            data = json.load(f)
                        if isinstance(data, list) and len(data) > 0:
                            sample = data[0]
                            if 'description' in sample or 'transcript' in sample or 'texte' in sample:
                                has_video_text = True
                                break
                except:
                    continue

            if has_video_text:
                print("✅ Texte des vidéos présent")
                result["status"] = "PASS"
            else:
                result["issues"].append("Pas de texte/description des vidéos")
                print("❌ Pas de texte/description des vidéos")
        else:
            result["issues"].append("Aucun fichier YouTube trouvé")
            print("❌ Aucun fichier YouTube trouvé")

        return result

    def test_source_3_web_scraping(self) -> dict[str, Any]:
        """Test Source 3: Web Scraping"""
        print("\n🕷️ TEST SOURCE 3: WEB SCRAPING")
        print("-" * 40)

        result = {"status": "FAIL", "files": [], "records": 0, "issues": []}

        # Chercher les fichiers de web scraping
        scraping_paths = [
            "data/raw/web_scraping",
            "data/processed"
        ]

        for base_path in scraping_paths:
            if os.path.exists(base_path):
                for file_path in Path(base_path).rglob("*"):
                    if file_path.suffix in ['.json', '.csv'] and any(keyword in file_path.name.lower() for keyword in ['yahoo', 'franceinfo', 'scraping', 'web']):
                        result["files"].append(str(file_path))
                        try:
                            if file_path.suffix == '.json':
                                with open(file_path, encoding='utf-8') as f:
                                    data = json.load(f)
                                if isinstance(data, list):
                                    result["records"] += len(data)
                                else:
                                    result["records"] += 1
                            else:
                                df = pd.read_csv(file_path)
                                result["records"] += len(df)

                            print(f"✅ Fichier scraping: {file_path.name}")

                        except Exception as e:
                            result["issues"].append(f"Erreur {file_path}: {e}")
                            print(f"❌ Erreur {file_path}: {e}")

        if result["files"]:
            print(f"📊 Total fichiers scraping: {len(result['files'])}")
            print(f"📊 Total enregistrements: {result['records']}")
            result["status"] = "PASS"
        else:
            result["issues"].append("Aucun fichier de web scraping trouvé")
            print("❌ Aucun fichier de web scraping trouvé")

        return result

    def test_source_4_gdelt(self) -> dict[str, Any]:
        """Test Source 4: GDELT (Big Data)"""
        print("\n🌍 TEST SOURCE 4: GDELT BIG DATA")
        print("-" * 40)

        result = {"status": "FAIL", "files": [], "records": 0, "issues": []}

        # Chercher les fichiers GDELT
        gdelt_paths = [
            "data/processed/bigdata",
            "data/raw/bigdata"
        ]

        for base_path in gdelt_paths:
            if os.path.exists(base_path):
                for file_path in Path(base_path).rglob("*gdelt*"):
                    if file_path.suffix in ['.parquet', '.json', '.csv']:
                        result["files"].append(str(file_path))
                        try:
                            if file_path.suffix == '.parquet':
                                df = pd.read_parquet(file_path)
                                result["records"] += len(df)
                            elif file_path.suffix == '.json':
                                with open(file_path, encoding='utf-8') as f:
                                    data = json.load(f)
                                if isinstance(data, list):
                                    result["records"] += len(data)
                                else:
                                    result["records"] += 1
                            else:
                                df = pd.read_csv(file_path)
                                result["records"] += len(df)

                            print(f"✅ Fichier GDELT: {file_path.name}")

                        except Exception as e:
                            result["issues"].append(f"Erreur {file_path}: {e}")
                            print(f"❌ Erreur {file_path}: {e}")

        if result["files"]:
            print(f"📊 Total fichiers GDELT: {len(result['files'])}")
            print(f"📊 Total enregistrements: {result['records']}")
            result["status"] = "PASS"
        else:
            result["issues"].append("Aucun fichier GDELT trouvé")
            print("❌ Aucun fichier GDELT trouvé")

        return result

    def test_source_5_newsapi(self) -> dict[str, Any]:
        """Test Source 5: NewsAPI"""
        print("\n📰 TEST SOURCE 5: NEWSAPI")
        print("-" * 40)

        result = {"status": "FAIL", "files": [], "records": 0, "issues": []}

        # Chercher les fichiers NewsAPI
        newsapi_paths = [
            "data/raw/newsapi",
            "data/raw/external_apis",
            "data/processed"
        ]

        for base_path in newsapi_paths:
            if os.path.exists(base_path):
                for file_path in Path(base_path).rglob("*newsapi*"):
                    if file_path.suffix in ['.json', '.csv']:
                        result["files"].append(str(file_path))
                        try:
                            if file_path.suffix == '.json':
                                with open(file_path, encoding='utf-8') as f:
                                    data = json.load(f)
                                if isinstance(data, list):
                                    result["records"] += len(data)
                                else:
                                    result["records"] += 1
                            else:
                                df = pd.read_csv(file_path)
                                result["records"] += len(df)

                            print(f"✅ Fichier NewsAPI: {file_path.name}")

                        except Exception as e:
                            result["issues"].append(f"Erreur {file_path}: {e}")
                            print(f"❌ Erreur {file_path}: {e}")

        if result["files"]:
            print(f"📊 Total fichiers NewsAPI: {len(result['files'])}")
            print(f"📊 Total enregistrements: {result['records']}")
            result["status"] = "PASS"
        else:
            result["issues"].append("Aucun fichier NewsAPI trouvé")
            print("❌ Aucun fichier NewsAPI trouvé")

        return result

    def test_etl_pipeline(self) -> dict[str, Any]:
        """Test du pipeline ETL"""
        print("\n⚙️ TEST PIPELINE ETL")
        print("-" * 40)

        result = {"status": "FAIL", "scripts": [], "issues": []}

        # Vérifier les scripts ETL essentiels
        etl_scripts = [
            "scripts/aggregate_sources.py",
            "scripts/load_aggregated_to_db.py",
            "scripts/load_kaggle_to_db.py"
        ]

        for script in etl_scripts:
            if os.path.exists(script):
                result["scripts"].append(script)
                print(f"✅ Script ETL: {script}")
            else:
                result["issues"].append(f"Script manquant: {script}")
                print(f"❌ Script manquant: {script}")

        # Vérifier les fichiers intégrés
        integrated_files = list(Path("data/processed").glob("*integrated*"))
        if integrated_files:
            print(f"✅ Fichiers intégrés: {len(integrated_files)}")
            result["status"] = "PASS"
        else:
            result["issues"].append("Aucun fichier intégré trouvé")
            print("❌ Aucun fichier intégré trouvé")

        return result

    def test_database_integration(self) -> dict[str, Any]:
        """Test de l'intégration en base de données"""
        print("\n🗄️ TEST INTÉGRATION BASE DE DONNÉES")
        print("-" * 40)

        result = {"status": "FAIL", "tables": {}, "issues": []}

        # Test base MERISE principale
        db_path = "semantic_pulse.db"
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                # Lister les tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]

                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    result["tables"][table] = count
                    print(f"✅ Table {table}: {count} enregistrements")

                conn.close()
                result["status"] = "PASS"

            except Exception as e:
                result["issues"].append(f"Erreur DB: {e}")
                print(f"❌ Erreur DB: {e}")
        else:
            result["issues"].append("Base de données manquante")
            print("❌ Base de données manquante")

        return result

    def test_end_to_end_integration(self) -> dict[str, Any]:
        """Test d'intégration end-to-end"""
        print("\n🔄 TEST INTÉGRATION END-TO-END")
        print("-" * 40)

        result = {"status": "FAIL", "sources_connected": 0, "issues": []}

        # Vérifier que les données des sources sont bien dans la DB
        db_path = "semantic_pulse.db"
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                # Vérifier les sources dans la table sources
                cursor.execute("SELECT nom, type, COUNT(*) as count FROM sources GROUP BY nom, type")
                sources = cursor.fetchall()

                print("📊 Sources dans la base:")
                for source_name, source_type, count in sources:
                    print(f"  ✅ {source_name} ({source_type}): {count} enregistrements")
                    result["sources_connected"] += 1

                # Vérifier les contenus
                cursor.execute("SELECT COUNT(*) FROM contenus")
                total_contenus = cursor.fetchone()[0]
                print(f"📊 Total contenus: {total_contenus}")

                if total_contenus > 0:
                    result["status"] = "PASS"
                else:
                    result["issues"].append("Aucun contenu dans la base")

                conn.close()

            except Exception as e:
                result["issues"].append(f"Erreur intégration: {e}")
                print(f"❌ Erreur intégration: {e}")

        return result

    def run_complete_test(self):
        """Lance le test complet end-to-end"""
        print("🧪 TEST END-TO-END ULTIME - SEMANTIC PULSE X")
        print("=" * 60)

        # Test des 5 sources
        self.results["sources"]["kaggle"] = self.test_source_1_kaggle()
        self.results["sources"]["youtube"] = self.test_source_2_youtube()
        self.results["sources"]["web_scraping"] = self.test_source_3_web_scraping()
        self.results["sources"]["gdelt"] = self.test_source_4_gdelt()
        self.results["sources"]["newsapi"] = self.test_source_5_newsapi()

        # Test du pipeline ETL
        self.results["etl_pipeline"] = self.test_etl_pipeline()

        # Test de l'intégration DB
        self.results["database"] = self.test_database_integration()

        # Test end-to-end
        self.results["integration"] = self.test_end_to_end_integration()

        # Résumé final
        self.print_final_summary()

    def print_final_summary(self):
        """Affiche le résumé final"""
        print("\n" + "=" * 60)
        print("📋 RÉSUMÉ FINAL DU TEST END-TO-END")
        print("=" * 60)

        # Compter les succès
        sources_passed = sum(1 for source in self.results["sources"].values() if source["status"] == "PASS")
        total_sources = len(self.results["sources"])

        etl_passed = self.results["etl_pipeline"]["status"] == "PASS"
        db_passed = self.results["database"]["status"] == "PASS"
        integration_passed = self.results["integration"]["status"] == "PASS"

        print("\n📊 RÉSULTATS:")
        print(f"  Sources de données: {sources_passed}/{total_sources}")
        print(f"  Pipeline ETL: {'✅' if etl_passed else '❌'}")
        print(f"  Base de données: {'✅' if db_passed else '❌'}")
        print(f"  Intégration end-to-end: {'✅' if integration_passed else '❌'}")

        # Score global
        total_tests = 4  # sources + etl + db + integration
        passed_tests = sources_passed + (1 if etl_passed else 0) + (1 if db_passed else 0) + (1 if integration_passed else 0)
        score = (passed_tests / total_tests) * 100

        print(f"\n🎯 SCORE GLOBAL: {score:.1f}%")

        if score >= 90:
            print("🏆 EXCELLENT - Pipeline end-to-end fonctionnel !")
        elif score >= 75:
            print("⚠️ BON - Quelques améliorations nécessaires")
        else:
            print("❌ CRITIQUE - Corrections majeures requises")

        # Lister les problèmes
        all_issues = []
        for source_name, source_data in self.results["sources"].items():
            all_issues.extend([f"{source_name}: {issue}" for issue in source_data["issues"]])
        all_issues.extend(self.results["etl_pipeline"]["issues"])
        all_issues.extend(self.results["database"]["issues"])
        all_issues.extend(self.results["integration"]["issues"])

        if all_issues:
            print("\n❌ PROBLÈMES IDENTIFIÉS:")
            for issue in all_issues:
                print(f"  • {issue}")

        # Sauvegarder le rapport
        self.save_report()

    def save_report(self):
        """Sauvegarde le rapport de test"""
        report_path = "test/end_to_end_test_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2, default=str)
        print(f"\n📄 Rapport sauvegardé: {report_path}")

def main():
    """Fonction principale"""
    tester = EndToEndTester()
    tester.run_complete_test()

if __name__ == "__main__":
    main()

