#!/usr/bin/env python3
"""
Convertisseur YouTube vers format standard - Semantic Pulse X
Convertit les fichiers YouTube Hugo Decrypte vers le format attendu par aggregate_sources.py
"""

import json
import logging
from datetime import datetime
from pathlib import Path

# Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_youtube_to_standard(input_file: str, output_file: str):
    """Convertit un fichier YouTube vers le format standard"""
    
    try:
        # Lire le fichier YouTube avec encodage UTF-8
        with open(input_file, 'r', encoding='utf-8') as f:
            youtube_data = json.load(f)
        
        # Convertir vers le format standard
        standard_data = []
        
        if isinstance(youtube_data, list):
            for video in youtube_data:
                standard_item = {
                    "url": f"https://youtube.com/watch?v={video.get('video_id', '')}",
                    "source": "youtube_hugo",
                    "pays": "france",
                    "domaine": "politique",
                    "titre": video.get('title', ''),
                    "resume": video.get('description', '')[:200] + "..." if video.get('description') else "",
                    "texte": f"{video.get('title', '')} {video.get('description', '')}",
                    "publication_date": video.get('published_at', datetime.now().isoformat()),
                    "auteur": video.get('channel_title', 'Hugo Decrypte'),
                    "langue": "fr",
                    "collected_at": datetime.now().isoformat(),
                    "metadata": {
                        "video_id": video.get('video_id', ''),
                        "view_count": video.get('view_count', 0),
                        "like_count": video.get('like_count', 0),
                        "channel_title": video.get('channel_title', '')
                    }
                }
                standard_data.append(standard_item)
        
        # Sauvegarder au format standard
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(standard_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"SUCCESS: {len(standard_data)} vidéos converties vers {output_file}")
        return len(standard_data)
        
    except Exception as e:
        logger.error(f"ERROR: Erreur conversion YouTube: {e}")
        return 0

def convert_newsapi_to_standard(input_file: str, output_file: str):
    """Convertit un fichier NewsAPI vers le format standard"""
    
    try:
        # Lire le fichier NewsAPI avec encodage UTF-8
        with open(input_file, 'r', encoding='utf-8') as f:
            newsapi_data = json.load(f)
        
        # Convertir vers le format standard
        standard_data = []
        
        if isinstance(newsapi_data, list):
            for article in newsapi_data:
                standard_item = {
                    "url": article.get('url', ''),
                    "source": "newsapi_fr",
                    "pays": "france",
                    "domaine": "politique",
                    "titre": article.get('title', ''),
                    "resume": article.get('description', '')[:200] + "..." if article.get('description') else "",
                    "texte": f"{article.get('title', '')} {article.get('description', '')}",
                    "publication_date": article.get('published_at', datetime.now().isoformat()),
                    "auteur": article.get('source_name', 'NewsAPI'),
                    "langue": "fr",
                    "collected_at": datetime.now().isoformat(),
                    "metadata": {
                        "source_name": article.get('source_name', ''),
                        "published_at": article.get('published_at', '')
                    }
                }
                standard_data.append(standard_item)
        
        # Sauvegarder au format standard
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(standard_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"SUCCESS: {len(standard_data)} articles convertis vers {output_file}")
        return len(standard_data)
        
    except Exception as e:
        logger.error(f"ERROR: Erreur conversion NewsAPI: {e}")
        return 0

def convert_gdelt_to_standard(input_file: str, output_file: str):
    """Convertit un fichier GDELT vers le format standard"""
    
    try:
        # Lire le fichier GDELT avec encodage UTF-8
        with open(input_file, 'r', encoding='utf-8') as f:
            gdelt_data = json.load(f)
        
        # Convertir vers le format standard
        standard_data = []
        
        if isinstance(gdelt_data, list):
            for event in gdelt_data:
                standard_item = {
                    "url": event.get('source_url', ''),
                    "source": "gdelt_gkg",
                    "pays": "france",
                    "domaine": "international",
                    "titre": event.get('text', '')[:100] + "..." if event.get('text') else "Événement GDELT",
                    "resume": event.get('text', '')[:200] + "..." if event.get('text') else "",
                    "texte": event.get('text', ''),
                    "publication_date": f"{event.get('date', '20251016')[:4]}-{event.get('date', '20251016')[4:6]}-{event.get('date', '20251016')[6:8]}T00:00:00Z",
                    "auteur": "GDELT",
                    "langue": "fr",
                    "collected_at": datetime.now().isoformat(),
                    "metadata": {
                        "event_id": event.get('event_id', ''),
                        "date": event.get('date', ''),
                        "sentiment": event.get('sentiment', 'neutre')
                    }
                }
                standard_data.append(standard_item)
        
        # Sauvegarder au format standard
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(standard_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"SUCCESS: {len(standard_data)} événements convertis vers {output_file}")
        return len(standard_data)
        
    except Exception as e:
        logger.error(f"ERROR: Erreur conversion GDELT: {e}")
        return 0

def main():
    """Point d'entrée principal"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Convertisseur vers format standard")
    parser.add_argument("--input", required=True, help="Fichier d'entrée")
    parser.add_argument("--output", required=True, help="Fichier de sortie")
    parser.add_argument("--type", required=True, choices=['youtube', 'newsapi', 'gdelt'], 
                       help="Type de fichier à convertir")
    
    args = parser.parse_args()
    
    print(f"CONVERT: Conversion {args.type} vers format standard")
    print(f"INPUT: {args.input}")
    print(f"OUTPUT: {args.output}")
    print("=" * 50)
    
    if args.type == 'youtube':
        count = convert_youtube_to_standard(args.input, args.output)
    elif args.type == 'newsapi':
        count = convert_newsapi_to_standard(args.input, args.output)
    elif args.type == 'gdelt':
        count = convert_gdelt_to_standard(args.input, args.output)
    
    print(f"RESULT: {count} éléments convertis")

if __name__ == "__main__":
    main()
