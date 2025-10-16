#!/usr/bin/env python3
"""
Chargement des données agrégées dans la base relationnelle
- Respecte le cahier des charges (5 sources + base unique)
- Utilise le schéma SQLAlchemy mis à jour avec GDELT

Usage:
  python scripts/load_aggregated_to_db.py --input data/processed/integrated_all_sources_*.json
"""

import argparse
import json

# Import du schéma mis à jour
import sys
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(str(Path(__file__).parent.parent))
from app.backend.models.schema import (
    Base,
    Contenu,
    DimDomaine,
    DimHumeur,
    DimPays,
    Source,
)


def get_or_create_dimension(session, model_class, name_field: str, name_value: str, **kwargs):
    """Récupère ou crée une entrée de dimension"""
    instance = session.query(model_class).filter(getattr(model_class, name_field) == name_value).first()
    if not instance:
        instance = model_class(**{name_field: name_value, **kwargs})
        session.add(instance)
        session.flush()  # Pour obtenir l'ID
    return instance


def load_aggregated_data(input_file: Path) -> int:
    """Charge les données agrégées dans la base relationnelle"""

    # Connexion à la base
    engine = create_engine("sqlite:///semantic_pulse.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Charger les données JSON
        with input_file.open("r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"LOADING: Chargement de {len(data)} enregistrements")

        # Statistiques par source
        source_stats = {}
        sentiment_stats = {}

        for record in data:
            # Récupérer ou créer les dimensions
            pays = get_or_create_dimension(session, DimPays, "nom", record.get("pays", "FR"),
                                         code_iso=record.get("pays", "FR"))

            domaine = get_or_create_dimension(session, DimDomaine, "nom", record.get("domaine", "inconnu"))

            sentiment = record.get("sentiment", "neutre") or "neutre"
            get_or_create_dimension(session, DimHumeur, "nom", sentiment)

            # Récupérer ou créer la source
            source_name = record.get("source", "Unknown")
            source_type = record.get("source_type", "web")
            source = get_or_create_dimension(session, Source, "nom", source_name,
                                           type=source_type, url_base="")

            # Vérifier si l'enregistrement existe déjà
            existing = session.query(Contenu).filter_by(
                url=record.get("url", ""),
                titre=record.get("titre", "")
            ).first()

            if existing:
                print(f"WARNING: Enregistrement existant ignoré: {record.get('titre', '')[:50]}...")
                continue

            # Créer le contenu
            contenu = Contenu(
                source_id=source.id,
                pays_id=pays.id,
                domaine_id=domaine.id,
                url=record.get("url", ""),
                titre=record.get("titre", ""),
                resume=record.get("resume", ""),
                texte=record.get("texte", ""),
                publication_date=datetime.fromisoformat(record.get("publication_date", "").replace("Z", "+00:00")) if record.get("publication_date") and record.get("publication_date") != "None" else datetime.now(UTC),
                auteur=record.get("auteur", ""),
                langue=record.get("langue", "fr"),
                collected_at=datetime.fromisoformat(record.get("collected_at", "").replace("Z", "+00:00")) if record.get("collected_at") and record.get("collected_at") != "None" else datetime.now(UTC),
                # Champs GDELT
                sentiment=sentiment,
                confidence=record.get("confidence", 0.0),
                themes=record.get("themes", ""),
                source_type=source_type
            )

            session.add(contenu)

            # Statistiques
            source_stats[source_name] = source_stats.get(source_name, 0) + 1
            sentiment_stats[sentiment] = sentiment_stats.get(sentiment, 0) + 1

        # Commit des changements
        session.commit()

        print(f"SUCCESS: {len(data)} enregistrements chargés avec succès")

        # Afficher les statistiques
        print("\nSTATS par source:")
        for source, count in sorted(source_stats.items()):
            print(f"   • {source}: {count} enregistrements")

        print("\nDISTRIBUTION des sentiments:")
        for sentiment, count in sorted(sentiment_stats.items()):
            percentage = (count / len(data)) * 100
            print(f"   • {sentiment}: {count} ({percentage:.1f}%)")

        # Vérifier les données en base
        total_contenus = session.query(Contenu).count()
        print(f"\nDATABASE: Total en base: {total_contenus} contenus")

        return 0

    except Exception as e:
        session.rollback()
        print(f"ERROR: Erreur lors du chargement: {e}")
        return 1
    finally:
        session.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Chargement données agrégées en base")
    parser.add_argument("--input", required=True, help="Fichier JSON agrégé")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: Fichier introuvable: {input_path}")
        return 1

    return load_aggregated_data(input_path)


if __name__ == "__main__":
    exit(main())
