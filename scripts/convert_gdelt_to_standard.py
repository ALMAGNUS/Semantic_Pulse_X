#!/usr/bin/env python3
"""
Conversion GDELT GKG vers format d'agrégation standard
- Convertit les données GDELT GKG en format compatible avec aggregate_sources.py
- Respecte le cahier des charges (5 sources + base relationnelle unique)

Usage:
  python scripts/convert_gdelt_to_standard.py --input data/processed/bigdata/gdelt_gkg_fr_*.json \
      --output data/raw/external_apis/gdelt_normalized.json
"""

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd


def convert_gdelt_record(gdelt_record: dict[str, Any]) -> dict[str, Any]:
    """Convertit un enregistrement GDELT vers le format standard"""

    # Extraction des données GDELT
    gkg_id = gdelt_record.get("gkg_id", "")
    source = gdelt_record.get("source", "GDELT")
    themes = gdelt_record.get("themes", "")
    locations = gdelt_record.get("locations", "")
    persons = gdelt_record.get("persons", "")
    organizations = gdelt_record.get("organizations", "")
    quotations = gdelt_record.get("quotations", "")
    sentiment = gdelt_record.get("sentiment", "neutre")
    confidence = gdelt_record.get("confidence", 0.0)
    date = gdelt_record.get("date", "")

    # Construction du contenu textuel
    text_parts = []
    if themes:
        text_parts.append(f"Thèmes: {themes}")
    if quotations:
        text_parts.append(f"Citations: {quotations}")
    if persons:
        text_parts.append(f"Personnes: {persons}")
    if organizations:
        text_parts.append(f"Organisations: {organizations}")

    combined_text = " | ".join(text_parts)

    # Construction du titre à partir des thèmes principaux
    title_parts = []
    if themes:
        theme_list = themes.split(";")[:3]  # Top 3 thèmes
        title_parts.extend([t.strip() for t in theme_list if t.strip()])

    title = " - ".join(title_parts) if title_parts else f"Article GDELT {gkg_id}"

    # Construction du résumé
    summary_parts = []
    if quotations:
        # Prendre la première citation comme résumé
        quotes = quotations.split(";")
        if quotes:
            summary_parts.append(quotes[0].strip())
    if locations:
        summary_parts.append(f"Localisation: {locations}")

    summary = " | ".join(summary_parts) if summary_parts else f"Analyse GDELT - Sentiment: {sentiment}"

    # Format standard
    standard_record = {
        "url": f"https://gdeltproject.org/data.html#{gkg_id}",
        "source": source,
        "pays": "FR",
        "domaine": "international",  # GDELT couvre l'international
        "titre": title,
        "resume": summary,
        "texte": combined_text,
        "publication_date": date.isoformat() if hasattr(date, 'isoformat') else str(date),
        "auteur": "GDELT Project",
        "langue": "fr",
        "collected_at": datetime.now(UTC).isoformat(),
        "sentiment": sentiment,
        "confidence": confidence,
        "themes": themes,
        "source_type": "gdelt_gkg"  # Métadonnée pour identification
    }

    return standard_record


def main() -> int:
    parser = argparse.ArgumentParser(description="Conversion GDELT vers format standard")
    parser.add_argument("--input", required=True, help="Fichier JSON GDELT GKG")
    parser.add_argument("--output", required=True, help="Fichier JSON de sortie normalisé")

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"❌ Fichier d'entrée introuvable: {input_path}")
        return 1

    # Charger les données GDELT
    try:
        with input_path.open("r", encoding="utf-8") as f:
            gdelt_data = json.load(f)

        if not isinstance(gdelt_data, list):
            print("❌ Format JSON invalide: attendu une liste")
            return 1

        print(f"📊 Chargement de {len(gdelt_data)} enregistrements GDELT")

    except Exception as e:
        print(f"❌ Erreur lecture fichier: {e}")
        return 1

    # Convertir chaque enregistrement
    converted_records = []
    for i, gdelt_record in enumerate(gdelt_data):
        try:
            standard_record = convert_gdelt_record(gdelt_record)
            converted_records.append(standard_record)
        except Exception as e:
            print(f"⚠️ Erreur conversion enregistrement {i}: {e}")
            continue

    print(f"✅ {len(converted_records)} enregistrements convertis")

    # Créer le dossier de sortie
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Sauvegarder au format standard
    try:
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(converted_records, f, ensure_ascii=False, indent=2)

        print(f"💾 Données sauvegardées: {output_path}")

        # Statistiques
        df = pd.DataFrame(converted_records)
        sentiment_dist = df['sentiment'].value_counts().to_dict()
        avg_confidence = df['confidence'].mean()

        print("\n📈 Statistiques:")
        print(f"   • Distribution sentiment: {sentiment_dist}")
        print(f"   • Confiance moyenne: {avg_confidence:.2%}")
        print(f"   • Sources: {df['source'].nunique()} sources uniques")

        return 0

    except Exception as e:
        print(f"❌ Erreur sauvegarde: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
