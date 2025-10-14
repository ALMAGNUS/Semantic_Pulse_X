#!/usr/bin/env python3
"""
Données d'initialisation des tables de dimension
"""

from sqlalchemy.orm import Session

from .schema import DimDomaine, DimHumeur, DimPays, Source


def init_dimensions(db: Session) -> None:
    """Initialise les tables de dimension avec des données de base"""

    # Pays
    pays_data = [
        {"nom": "France", "code_iso": "FRA"},
        {"nom": "États-Unis", "code_iso": "USA"},
        {"nom": "Royaume-Uni", "code_iso": "GBR"},
        {"nom": "Allemagne", "code_iso": "DEU"},
        {"nom": "Espagne", "code_iso": "ESP"},
    ]

    for p in pays_data:
        existing = db.query(DimPays).filter(DimPays.nom == p["nom"]).first()
        if not existing:
            db.add(DimPays(**p))

    # Domaines
    domaines_data = [
        {"nom": "politique", "description": "Actualités politiques"},
        {"nom": "international", "description": "Actualités internationales"},
        {"nom": "économie", "description": "Actualités économiques"},
        {"nom": "sport", "description": "Actualités sportives"},
        {"nom": "culture", "description": "Actualités culturelles"},
        {"nom": "technologie", "description": "Actualités technologiques"},
        {"nom": "inconnu", "description": "Domaine non identifié"},
    ]

    for d in domaines_data:
        existing = db.query(DimDomaine).filter(DimDomaine.nom == d["nom"]).first()
        if not existing:
            db.add(DimDomaine(**d))

    # Humeurs
    humeurs_data = [
        {"nom": "positif", "couleur": "#4CAF50", "description": "Sentiment positif"},
        {"nom": "négatif", "couleur": "#F44336", "description": "Sentiment négatif"},
        {"nom": "neutre", "couleur": "#9E9E9E", "description": "Sentiment neutre"},
        {"nom": "inquiet", "couleur": "#FF9800", "description": "Inquiétude"},
        {"nom": "content", "couleur": "#2196F3", "description": "Satisfaction"},
        {"nom": "déçu", "couleur": "#795548", "description": "Déception"},
        {"nom": "sceptique", "couleur": "#607D8B", "description": "Scepticisme"},
        {"nom": "incertain", "couleur": "#E91E63", "description": "Incertitude"},
    ]

    for h in humeurs_data:
        existing = db.query(DimHumeur).filter(DimHumeur.nom == h["nom"]).first()
        if not existing:
            db.add(DimHumeur(**h))

    # Sources
    sources_data = [
        {"nom": "YouTube API", "type": "api", "url_base": "https://www.youtube.com/"},
        {"nom": "NewsAPI", "type": "api", "url_base": "https://newsapi.org/"},
        {"nom": "Yahoo Actualités", "type": "scraping", "url_base": "https://fr.news.yahoo.com/"},
        {"nom": "Franceinfo", "type": "scraping", "url_base": "https://www.francetvinfo.fr/"},
        {"nom": "Kaggle Tweets", "type": "file", "url_base": ""},
        {"nom": "GDELT 2.0", "type": "bigdata", "url_base": "https://www.gdeltproject.org/"},
    ]

    for s in sources_data:
        existing = db.query(Source).filter(Source.nom == s["nom"]).first()
        if not existing:
            db.add(Source(**s))

    db.commit()
    print("✅ Données de dimension initialisées")
