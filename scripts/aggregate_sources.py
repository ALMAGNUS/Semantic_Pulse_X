#!/usr/bin/env python3
"""
Agrégation multi-sources (low-code, indépendante)

- Lit une ou plusieurs entrées JSON normalisées (listes d'objets)
  Champs attendus: url, source, pays, domaine, titre, resume, texte,
                   publication_date, auteur, langue, collected_at
- Déduplication par (url, titre)
- Gestion des manquants (pays/domaine/langue/auteur/publication_date)
- Écrit un JSON intégré + Parquet

Usage:
  python scripts/aggregate_sources.py --inputs data/raw/scraped/*.json \
      --output-dir data/processed
"""

import argparse
import glob
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd

REQUIRED_FIELDS = [
    "url",
    "source",
    "pays",
    "domaine",
    "titre",
    "resume",
    "texte",
    "publication_date",
    "auteur",
    "langue",
    "collected_at",
    "sentiment",  # Ajout pour GDELT
    "confidence", # Ajout pour GDELT
    "themes",     # Ajout pour GDELT
]


def load_json_list(path: Path) -> list[dict[str, Any]]:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except Exception:
        return []


def fill_missing(record: dict[str, Any]) -> dict[str, Any]:
    # Valeurs par défaut simples
    record.setdefault("pays", "FR")
    record.setdefault("domaine", "inconnu")
    record.setdefault("langue", "fr")
    record.setdefault("auteur", "")
    record.setdefault("sentiment", "neutre")  # Ajout pour GDELT
    record.setdefault("confidence", 0.0)      # Ajout pour GDELT
    record.setdefault("themes", "")           # Ajout pour GDELT

    # publication_date: si vide, fallback sur collected_at ou now UTC
    pub = (record.get("publication_date") or "").strip()
    if not pub:
        record["publication_date"] = (
            record.get("collected_at")
            or datetime.now(UTC).isoformat()
        )
    # Normalisation texte minimaliste
    for k in ["titre", "resume", "texte"]:
        val = record.get(k)
        if isinstance(val, str):
            record[k] = " ".join(val.split()).strip()
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description="Agrégation multi-sources")
    parser.add_argument(
        "--inputs", nargs="+", required=True, help="Glob(s) de fichiers JSON normalisés"
    )
    parser.add_argument(
        "--output-dir", type=str, default="data/processed", help="Dossier de sortie"
    )
    parser.add_argument(
        "--min-text-len", type=int, default=80, help="Longueur minimale du texte (défaut: 80)"
    )
    parser.add_argument(
        "--drop-empty-title", action="store_true", help="Supprimer les entrées sans titre"
    )
    args = parser.parse_args()

    # Résoudre globs
    files: list[str] = []
    for g in args.inputs:
        files.extend(glob.glob(g))
    files = sorted(set(files))
    if not files:
        print("⚠️ Aucun fichier en entrée")
        return 2

    records: list[dict[str, Any]] = []
    for fp in files:
        items = load_json_list(Path(fp))
        for it in items:
            # garder seulement les champs utiles
            norm: dict[str, Any] = {k: it.get(k) for k in REQUIRED_FIELDS}
            filled = fill_missing(norm)

            # Filtres qualité
            if args.drop_empty_title and not (filled.get("titre") or "").strip():
                continue
            texte = filled.get("texte", "") or ""
            if len(texte) < args.min_text_len:
                continue

            records.append(filled)

    if not records:
        print("⚠️ Aucune donnée après chargement")
        return 0

    print(f"✅ {len(records)} enregistrements chargés (après filtres qualité)")

    # Déduplication (url, titre)
    df = pd.DataFrame.from_records(records)
    df = df.drop_duplicates(subset=["url", "titre"], keep="first")

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    out_json = out_dir / f"integrated_all_sources_{ts}.json"
    out_parquet = out_dir / "integrated_all_sources.parquet"

    # Sauvegarde JSON
    data = df.to_dict(orient="records")
    with out_json.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Sauvegarde Parquet (append-overwrite simple: on réécrit un snapshot)
    df.to_parquet(out_parquet, index=False)

    print(
        f"✅ Agrégation: {len(records)} -> {len(df)} (dédupliqués).\n" \
        f"   Écrit: {out_json} et {out_parquet}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


