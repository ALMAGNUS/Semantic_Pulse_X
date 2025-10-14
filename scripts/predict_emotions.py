#!/usr/bin/env python3
"""
Prédiction simple des émotions (baseline) à partir des données intégrées.

- Lit les fichiers intégrés (JSON/Parquet) générés par aggregate_sources.py
- Extrait une série temporelle quotidienne par émotion (heuristique lexicale)
- Calcule une moyenne glissante et projette J+1 et J+7 (persistance + moyenne)
- Écrit un fichier JSON de prévisions dans data/processed/predictions_emotions_*.json

Usage:
  python scripts/predict_emotions.py \
    --inputs data/processed/integrated_all_sources_*.json \
    --output-dir data/processed
"""

import argparse
import glob
import json
from datetime import datetime
from pathlib import Path

import pandas as pd

# Heuristique très simple basée sur mots-clés FR
EMOTION_LEXICON: dict[str, list[str]] = {
    "decu": ["déçu", "decu", "deception", "déception"],
    "inquiet": ["inquiet", "inquiétude", "peur", "crainte"],
    "content": ["content", "satisfait", "heureux", "bonne nouvelle"],
    "neutre": ["annonce", "déclare", "selon", "rapport"],
    "incertain": ["peut-être", "incertain", "flou", "controverse"],
}


def load_integrated_records(paths: list[str]) -> list[dict]:
    records: list[dict] = []
    for p in paths:
        if p.endswith(".json"):
            try:
                data = json.loads(Path(p).read_text(encoding="utf-8"))
                if isinstance(data, list):
                    records.extend(data)
            except Exception:
                continue
        elif p.endswith(".parquet"):
            try:
                df = pd.read_parquet(p)
                records.extend(df.to_dict(orient="records"))
            except Exception:
                continue
    return records


def detect_emotion(text: str) -> str:
    if not isinstance(text, str) or not text:
        return "neutre"
    low = text.lower()
    scores = dict.fromkeys(EMOTION_LEXICON, 0)
    for emo, words in EMOTION_LEXICON.items():
        scores[emo] = sum(1 for w in words if w in low)
    # règle simple
    best = max(scores.items(), key=lambda x: x[1])
    return best[0]


def build_daily_counts(records: list[dict]) -> pd.DataFrame:
    rows: list[dict] = []
    for r in records:
        date_str = r.get("publication_date") or r.get("collected_at")
        if not date_str:
            continue
        try:
            d = datetime.fromisoformat(str(date_str).replace("Z", "+00:00")).date()
        except Exception:
            continue
        text = r.get("texte") or r.get("resume") or r.get("titre") or ""
        emo = detect_emotion(text)
        rows.append({"date": d, "emotion": emo, "count": 1})
    if not rows:
        return pd.DataFrame(columns=["date", "emotion", "count"]).astype({"date": "datetime64[ns]"})
    df = pd.DataFrame(rows)
    df = df.groupby(["date", "emotion"], as_index=False)["count"].sum()
    return df


def moving_average(series: pd.Series, window: int = 3) -> pd.Series:
    if series.empty:
        return series
    return series.rolling(window=window, min_periods=1).mean()


def project_next_days(ts_emo: pd.Series, days: list[int]) -> dict[int, float]:
    # stratégie simple: persistance dernier MA
    if ts_emo.empty:
        return dict.fromkeys(days, 0.0)
    last_val = ts_emo.iloc[-1]
    return {d: float(last_val) for d in days}


def main() -> int:
    parser = argparse.ArgumentParser(description="Prédiction simple des émotions")
    parser.add_argument("--inputs", nargs="+", default=["data/processed/integrated_all_sources_*.json", "data/processed/integrated_all_sources.parquet"], help="Fichiers intégrés (glob)")
    parser.add_argument("--output-dir", type=str, default="data/processed", help="Répertoire de sortie")
    parser.add_argument("--ma-window", type=int, default=3, help="Fenêtre moyenne glissante")
    args = parser.parse_args()

    # Résoudre globs
    files: list[str] = []
    for g in args.inputs:
        files.extend(glob.glob(g))
    files = sorted(set(files))
    if not files:
        print("⚠️ Aucun fichier intégré trouvé")
        return 2

    records = load_integrated_records(files)
    df = build_daily_counts(records)
    if df.empty:
        print("⚠️ Aucune donnée exploitable pour la prédiction")
        return 0

    # pivot daily x emotion
    pivot = df.pivot(index="date", columns="emotion", values="count").fillna(0).sort_index()
    preds: dict[str, dict[str, float]] = {}
    for emo in pivot.columns:
        ma = moving_average(pivot[emo], window=args.ma_window)
        proj = project_next_days(ma, days=[1, 7])
        preds[emo] = {"ma_last": float(ma.iloc[-1]) if len(ma) else 0.0, "J+1": proj[1], "J+7": proj[7]}

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"predictions_emotions_{ts}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump({
            "generated_at": datetime.utcnow().isoformat(),
            "window": args.ma_window,
            "predictions": preds,
        }, f, ensure_ascii=False, indent=2)

    print(f"✅ Prédictions enregistrées → {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
