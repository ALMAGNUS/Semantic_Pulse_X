#!/usr/bin/env python3
"""
Ingestion minimale GDELT 2.0 (événements) -> Parquet

- Télécharge un fichier GDELT events (CSV) récent (ex: dernier jour)
- Filtre sur mentions France (France, FRA, French)
- Normalise colonnes clés
- Sauvegarde en Parquet dans data/processed/bigdata

Usage:
  python scripts/ingest_gdelt.py --days 1 --output-dir data/processed/bigdata

Note: Pour un vrai flux historique, il faudra itérer sur les archives GDELT.
"""

import argparse
import io
import zipfile
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pandas as pd
import requests

BASE_URL = "http://data.gdeltproject.org/events/"


def list_recent_files(days: int) -> list[str]:
    # GDELT events files are published every 15 minutes as CSV zip named like: 20251014000000.export.CSV.zip
    # For a minimal approach, we try the last N days at 00:00 UTC snapshots.
    files: list[str] = []
    now = datetime.now(UTC)
    for i in range(days):
        d = (now - timedelta(days=i)).strftime("%Y%m%d") + "000000"
        files.append(f"{d}.export.CSV.zip")
    return files


def download_zip(url: str) -> bytes:
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return r.content


def filter_france(df: pd.DataFrame) -> pd.DataFrame:
    # Columns documented at https://www.gdeltproject.org/data.html#documentation
    text_cols = [
        "Actor1Name", "Actor2Name", "Actor1CountryCode", "Actor2CountryCode",
        "ActionGeo_FullName", "ActionGeo_CountryCode", "SOURCEURL",
    ]
    mask = pd.Series(False, index=df.index)
    for c in text_cols:
        if c in df.columns:
            s = df[c].astype(str).str.lower()
            mask |= (s.str.contains("france") | s.str.contains("french") |
                    s.str.contains(" fra ") | s.str.contains("paris") |
                    s.str.contains("macron") | s.str.contains("lecornu") |
                    s.str.contains("europe") | s.str.contains("eu ") |
                    s.str.contains("nato") | s.str.contains("un ") |
                    s.str.contains("g7") | s.str.contains("g20"))
    return df[mask]


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    # Keep a minimal subset of columns for PoC
    keep = [
        "GLOBALEVENTID", "SQLDATE", "Actor1Name", "Actor2Name", "Actor1CountryCode",
        "Actor2CountryCode", "EventCode", "GoldsteinScale", "NumMentions",
        "AvgTone", "ActionGeo_FullName", "ActionGeo_CountryCode", "SOURCEURL",
    ]
    df = df[[c for c in keep if c in df.columns]].copy()
    # Parse date
    if "SQLDATE" in df.columns:
        df["date"] = pd.to_datetime(df["SQLDATE"], format="%Y%m%d", errors="coerce")
    else:
        df["date"] = pd.NaT
    df.rename(columns={
        "GLOBALEVENTID": "event_id",
        "Actor1Name": "acteur1",
        "Actor2Name": "acteur2",
        "ActionGeo_FullName": "lieu",
        "ActionGeo_CountryCode": "pays_code",
        "SOURCEURL": "url",
        "AvgTone": "tonalite",
    }, inplace=True)
    return df


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingestion minimale GDELT 2.0")
    parser.add_argument("--days", type=int, default=1, help="Nombre de jours à récupérer")
    parser.add_argument("--output-dir", type=str, default="data/processed/bigdata", help="Dossier de sortie")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    files = list_recent_files(args.days)
    total_rows = 0
    frames: list[pd.DataFrame] = []

    for fname in files:
        url = BASE_URL + fname
        try:
            content = download_zip(url)
        except Exception:
            continue
        try:
            with zipfile.ZipFile(io.BytesIO(content)) as zf:
                inner = [n for n in zf.namelist() if n.endswith(".CSV")]
                if not inner:
                    continue
                with zf.open(inner[0]) as f:
                    df = pd.read_csv(f, sep="\t", header=None, low_memory=False)
        except Exception:
            continue

        # Map columns from GDELT 2.0 Events schema (61 columns); here we assign names minimally
        # See schema: http://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf
        # We will use generic indices for the subset used in normalize.
        cols = list(range(df.shape[1]))
        df.columns = cols
        rename_map = {
            0: "GLOBALEVENTID",
            1: "SQLDATE",
            6: "Actor1Name",
            16: "Actor1CountryCode",
            26: "Actor2Name",
            36: "Actor2CountryCode",
            27: "EventCode",
            30: "GoldsteinScale",
            31: "NumMentions",
            34: "AvgTone",
            53: "ActionGeo_FullName",
            51: "ActionGeo_CountryCode",
            60: "SOURCEURL",
        }
        df = df.rename(columns=rename_map)
        df = filter_france(df)
        if df.empty:
            continue
        df = normalize(df)
        frames.append(df)
        total_rows += len(df)

    if not frames:
        print("⚠️ Aucun enregistrement FR trouvé dans la fenêtre demandée")
        return 0

    out_df = pd.concat(frames, ignore_index=True)
    ts = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"gdelt_fr_{ts}.parquet"
    out_df.to_parquet(out_path, index=False)
    print(f"✅ GDELT ingéré: {len(out_df)} lignes → {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
