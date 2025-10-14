#!/usr/bin/env python3
"""
Pipeline GDELT GKG + Sentiment FR complet
- Ingestion GDELT GKG (Global Knowledge Graph) - plus riche que Events
- Analyse sentiment française spécialisée
- Compatible Prefect, LangChain, Grafana
- Architecture modulaire et scalable

Usage:
  python scripts/gdelt_gkg_pipeline.py --days 7 --output-dir data/processed/bigdata
"""

import argparse
import io
import json
import zipfile
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from prefect import flow, get_run_logger, task

# Configuration
GDELT_GKG_BASE_URL = "http://data.gdeltproject.org/gkg/"
FRENCH_SENTIMENT_LEXICON = {
    "positif": ["bon", "excellent", "réussi", "succès", "victoire", "progrès", "amélioration", "espoir", "confiance"],
    "négatif": ["mauvais", "échec", "problème", "crise", "difficulté", "inquiétude", "peur", "déception", "échec"],
    "neutre": ["annonce", "déclare", "selon", "rapport", "information", "données", "résultat"],
    "inquiet": ["inquiet", "inquiétude", "préoccupation", "crainte", "anxiété", "souci", "alarme"],
    "content": ["content", "satisfait", "heureux", "réjoui", "satisfaction", "plaisir", "joie"],
    "déçu": ["déçu", "déception", "désillusion", "frustration", "regret", "amertume"],
    "sceptique": ["sceptique", "doute", "méfiance", "suspicion", "incrédulité", "réserve"],
    "incertain": ["incertain", "flou", "imprécis", "ambigu", "confus", "indécis"]
}


@task(name="download_gdelt_gkg")
def download_gdelt_gkg_file(date_str: str) -> bytes | None:
    """Télécharge un fichier GDELT GKG pour une date donnée"""
    logger = get_run_logger()

    url = f"{GDELT_GKG_BASE_URL}{date_str}.gkg.csv.zip"
    try:
        logger.info(f"Téléchargement GDELT GKG: {url}")
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        logger.info(f"✅ Fichier GKG téléchargé: {len(response.content)} bytes")
        return response.content
    except Exception as e:
        logger.warning(f"⚠️ Erreur téléchargement {url}: {e}")
        return None


@task(name="extract_gkg_data")
def extract_gkg_data(content: bytes) -> pd.DataFrame | None:
    """Extrait les données GKG du fichier ZIP"""
    logger = get_run_logger()

    try:
        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            csv_files = [f for f in zf.namelist() if f.endswith('.csv')]
            if not csv_files:
                logger.warning("Aucun fichier CSV trouvé dans le ZIP")
                return None

            with zf.open(csv_files[0]) as f:
                # GDELT GKG a 27 colonnes - on lit les premières colonnes importantes
                df = pd.read_csv(f, sep='\t', header=None, low_memory=False, nrows=10000)

                # Mapping des colonnes GKG principales
                gkg_columns = {
                    0: "GKGRECORDID",
                    1: "DATE",
                    2: "SourceCollectionIdentifier",
                    3: "SourceCommonName",
                    4: "DocumentIdentifier",
                    5: "Counts",
                    6: "V2Counts",
                    7: "Themes",
                    8: "V2Themes",
                    9: "Locations",
                    10: "V2Locations",
                    11: "Persons",
                    12: "V2Persons",
                    13: "Organizations",
                    14: "V2Organizations",
                    15: "V2Tone",
                    16: "V2Dates",
                    17: "V2GCAM",
                    18: "V2SharingImage",
                    19: "V2RelatedImages",
                    20: "V2SocialImageEmbeds",
                    21: "V2SocialVideoEmbeds",
                    22: "V2Quotations",
                    23: "V2AllNames",
                    24: "V2Amounts",
                    25: "V2TranslationInfo",
                    26: "V2Extras"
                }

                df = df.rename(columns=gkg_columns)
                logger.info(f"✅ Données GKG extraites: {len(df)} lignes")
                return df

    except Exception as e:
        logger.error(f"❌ Erreur extraction GKG: {e}")
        return None


@task(name="filter_french_content")
def filter_french_content(df: pd.DataFrame) -> pd.DataFrame:
    """Filtre le contenu français dans les données GKG"""
    logger = get_run_logger()

    if df.empty:
        return df

    # Colonnes à analyser pour le contenu français
    text_columns = ["SourceCommonName", "Themes", "V2Themes", "Locations", "V2Locations",
                   "Persons", "V2Persons", "Organizations", "V2Organizations", "V2Quotations"]

    french_keywords = [
        "france", "french", "français", "française", "paris", "macron", "lecornu",
        "europe", "eu ", "nato", "un ", "g7", "g20", "francophonie", "francophone"
    ]

    mask = pd.Series(False, index=df.index)

    for col in text_columns:
        if col in df.columns:
            text_data = df[col].astype(str).str.lower()
            for keyword in french_keywords:
                mask |= text_data.str.contains(keyword, na=False)

    filtered_df = df[mask]
    logger.info(f"✅ Contenu français filtré: {len(filtered_df)}/{len(df)} lignes")
    return filtered_df


@task(name="analyze_french_sentiment")
def analyze_french_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    """Analyse le sentiment français des données GKG"""
    logger = get_run_logger()

    if df.empty:
        return df

    def detect_sentiment(text: str) -> dict[str, Any]:
        if not isinstance(text, str) or not text:
            return {"sentiment": "neutre", "confidence": 0.0, "score": 0.0}

        text_lower = text.lower()
        sentiment_scores = {}

        for sentiment, keywords in FRENCH_SENTIMENT_LEXICON.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            sentiment_scores[sentiment] = score

        # Trouver le sentiment dominant
        dominant_sentiment = max(sentiment_scores, key=sentiment_scores.get)
        max_score = sentiment_scores[dominant_sentiment]

        # Calculer la confiance (normalisée)
        total_score = sum(sentiment_scores.values())
        confidence = max_score / max(total_score, 1)

        return {
            "sentiment": dominant_sentiment,
            "confidence": confidence,
            "score": max_score,
            "all_scores": sentiment_scores
        }

    # Analyser les colonnes textuelles
    text_columns = ["V2Themes", "V2Quotations", "SourceCommonName"]
    sentiment_results = []

    for _, row in df.iterrows():
        combined_text = " ".join([str(row.get(col, "")) for col in text_columns if col in row])
        sentiment_analysis = detect_sentiment(combined_text)
        sentiment_results.append(sentiment_analysis)

    # Ajouter les résultats au DataFrame
    sentiment_df = pd.DataFrame(sentiment_results)
    result_df = pd.concat([df.reset_index(drop=True), sentiment_df], axis=1)

    logger.info(f"✅ Sentiment analysé: {len(result_df)} enregistrements")
    return result_df


@task(name="normalize_gkg_data")
def normalize_gkg_data(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise les données GKG pour l'intégration"""
    logger = get_run_logger()

    if df.empty:
        return df

    # Sélectionner et renommer les colonnes importantes
    keep_columns = {
        "GKGRECORDID": "gkg_id",
        "DATE": "date",
        "SourceCommonName": "source",
        "V2Themes": "themes",
        "V2Locations": "locations",
        "V2Persons": "persons",
        "V2Organizations": "organizations",
        "V2Tone": "tone",
        "V2Quotations": "quotations",
        "sentiment": "sentiment",
        "confidence": "confidence",
        "score": "sentiment_score"
    }

    normalized_df = df[[col for col in keep_columns.keys() if col in df.columns]].copy()
    normalized_df = normalized_df.rename(columns=keep_columns)

    # Convertir la date
    if "date" in normalized_df.columns:
        normalized_df["date"] = pd.to_datetime(normalized_df["date"], format="%Y%m%d%H%M%S", errors="coerce")

    # Ajouter des métadonnées
    normalized_df["source_type"] = "gdelt_gkg"
    normalized_df["country"] = "FR"
    normalized_df["language"] = "fr"
    normalized_df["collected_at"] = datetime.now(UTC)

    logger.info(f"✅ Données GKG normalisées: {len(normalized_df)} lignes")
    return normalized_df


@task(name="save_gkg_data")
def save_gkg_data(df: pd.DataFrame, output_dir: Path) -> Path:
    """Sauvegarde les données GKG traitées"""
    logger = get_run_logger()

    if df.empty:
        logger.warning("Aucune donnée à sauvegarder")
        return None

    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")

    # Sauvegarde Parquet (Big Data)
    parquet_path = output_dir / f"gdelt_gkg_fr_{timestamp}.parquet"
    df.to_parquet(parquet_path, index=False)

    # Sauvegarde JSON (intégration)
    json_path = output_dir / f"gdelt_gkg_fr_{timestamp}.json"
    df.to_json(json_path, orient="records", date_format="iso", force_ascii=False, indent=2)

    logger.info("✅ Données GKG sauvegardées:")
    logger.info(f"   📊 Parquet: {parquet_path} ({len(df)} lignes)")
    logger.info(f"   📄 JSON: {json_path}")

    return parquet_path


@task(name="generate_sentiment_report")
def generate_sentiment_report(df: pd.DataFrame) -> dict[str, Any]:
    """Génère un rapport d'analyse sentiment"""
    logger = get_run_logger()

    if df.empty:
        return {"error": "Aucune donnée à analyser"}

    # Statistiques sentiment
    sentiment_counts = df["sentiment"].value_counts().to_dict()
    avg_confidence = df["confidence"].mean()

    # Top sources
    top_sources = df["source"].value_counts().head(10).to_dict()

    # Distribution temporelle
    if "date" in df.columns:
        df["date_only"] = df["date"].dt.date
        daily_counts = df["date_only"].value_counts().sort_index().to_dict()
    else:
        daily_counts = {}

    report = {
        "timestamp": datetime.now(UTC).isoformat(),
        "total_records": len(df),
        "sentiment_distribution": sentiment_counts,
        "average_confidence": float(avg_confidence),
        "top_sources": top_sources,
        "daily_distribution": daily_counts,
        "summary": f"Analyse de {len(df)} enregistrements GKG français avec {avg_confidence:.2%} de confiance moyenne"
    }

    logger.info(f"✅ Rapport sentiment généré: {report['summary']}")
    return report


@flow(name="gdelt_gkg_sentiment_pipeline")
def gdelt_gkg_sentiment_pipeline(days: int = 7, output_dir: str = "data/processed/bigdata") -> dict[str, Any]:
    """Pipeline complet GDELT GKG + Sentiment FR"""
    logger = get_run_logger()
    logger.info(f"🚀 Démarrage pipeline GDELT GKG + Sentiment FR ({days} jours)")

    output_path = Path(output_dir)
    all_dataframes = []

    # Générer les dates à traiter
    end_date = datetime.now(UTC)
    dates_to_process = []

    for i in range(days):
        date = end_date - timedelta(days=i)
        date_str = date.strftime("%Y%m%d")
        dates_to_process.append(date_str)

    logger.info(f"📅 Dates à traiter: {dates_to_process}")

    # Traiter chaque date
    for date_str in dates_to_process:
        logger.info(f"📊 Traitement date: {date_str}")

        # Télécharger le fichier GKG
        content = download_gdelt_gkg_file(date_str)
        if content is None:
            continue

        # Extraire les données
        df = extract_gkg_data(content)
        if df is None or df.empty:
            continue

        # Filtrer le contenu français
        french_df = filter_french_content(df)
        if french_df.empty:
            continue

        # Analyser le sentiment
        sentiment_df = analyze_french_sentiment(french_df)

        # Normaliser les données
        normalized_df = normalize_gkg_data(sentiment_df)

        all_dataframes.append(normalized_df)

    # Agréger toutes les données
    if all_dataframes:
        final_df = pd.concat(all_dataframes, ignore_index=True)
        logger.info(f"📊 Données agrégées: {len(final_df)} enregistrements")

        # Sauvegarder
        parquet_path = save_gkg_data(final_df, output_path)

        # Générer le rapport
        report = generate_sentiment_report(final_df)

        # Sauvegarder le rapport
        report_path = output_path / f"gdelt_sentiment_report_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.json"
        with report_path.open("w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        logger.info("✅ Pipeline terminé avec succès!")
        logger.info(f"📊 Total: {len(final_df)} enregistrements GKG français")
        logger.info(f"📄 Rapport: {report_path}")

        return {
            "success": True,
            "total_records": len(final_df),
            "parquet_path": str(parquet_path),
            "report_path": str(report_path),
            "sentiment_distribution": report["sentiment_distribution"]
        }
    else:
        logger.warning("⚠️ Aucune donnée GKG française trouvée")
        return {
            "success": False,
            "total_records": 0,
            "error": "Aucune donnée française trouvée dans la période"
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Pipeline GDELT GKG + Sentiment FR")
    parser.add_argument("--days", type=int, default=7, help="Nombre de jours à traiter")
    parser.add_argument("--output-dir", type=str, default="data/processed/bigdata", help="Dossier de sortie")
    args = parser.parse_args()

    # Exécuter le pipeline Prefect
    result = gdelt_gkg_sentiment_pipeline(days=args.days, output_dir=args.output_dir)

    if result["success"]:
        print("✅ Pipeline GDELT GKG terminé avec succès!")
        print(f"📊 {result['total_records']} enregistrements traités")
        print(f"📈 Distribution sentiment: {result['sentiment_distribution']}")
        return 0
    else:
        print(f"❌ Pipeline échoué: {result.get('error', 'Erreur inconnue')}")
        return 1


if __name__ == "__main__":
    exit(main())
