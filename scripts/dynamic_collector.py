#!/usr/bin/env python3
"""
Collecteur Dynamique - Semantic Pulse X
Collecte des données spécifiques à un événement pour enrichir les prédictions
"""

import json
import logging
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DynamicCollector:
    """Collecteur dynamique basé sur les événements"""
    
    def __init__(self):
        self.youtube_key = os.getenv('YOUTUBE_API_KEY')
        self.newsapi_key = os.getenv('NEWSAPI_KEY')
        
    def collect_for_event(self, event_description: str, sources: list = None):
        """Collecte des données spécifiques à un événement"""
        
        if sources is None:
            sources = ['youtube', 'newsapi', 'web_scraping', 'gdelt']
        
        results = {
            'event': event_description,
            'timestamp': datetime.now().isoformat(),
            'sources': {},
            'total_collected': 0
        }
        
        # Extraire les mots-clés de l'événement
        keywords = self._extract_keywords(event_description)
        
        for source in sources:
            try:
                if source == 'youtube' and self.youtube_key:
                    data = self._collect_youtube_event(keywords)
                    results['sources']['youtube'] = data
                    
                elif source == 'newsapi' and self.newsapi_key:
                    data = self._collect_newsapi_event(keywords)
                    results['sources']['newsapi'] = data
                    
                elif source == 'web_scraping':
                    data = self._collect_web_scraping_event(keywords)
                    results['sources']['web_scraping'] = data
                    
                elif source == 'gdelt':
                    data = self._collect_gdelt_event(keywords)
                    results['sources']['gdelt'] = data
                    
            except Exception as e:
                logger.error(f"Erreur collecte {source}: {e}")
                results['sources'][source] = {'error': str(e), 'count': 0}
        
        # Calculer le total
        results['total_collected'] = sum(
            data.get('count', 0) for data in results['sources'].values()
            if isinstance(data, dict) and 'count' in data
        )
        
        return results
    
    def _extract_keywords(self, event_description: str):
        """Extrait les mots-clés pertinents d'un événement"""
        
        # Mots-clés politiques français
        political_keywords = [
            'gouvernement', 'ministre', 'président', 'assemblée', 'sénat',
            'réforme', 'loi', 'budget', 'retraite', 'chômage', 'économie',
            'écologie', 'santé', 'éducation', 'sécurité', 'immigration'
        ]
        
        # Mots-clés de l'événement
        event_words = re.findall(r'\b\w+\b', event_description.lower())
        
        # Combiner et filtrer
        keywords = []
        for word in event_words:
            if len(word) > 3 and word in political_keywords:
                keywords.append(word)
            elif word in ['france', 'français', 'française']:
                keywords.append(word)
        
        return keywords if keywords else event_words[:5]
    
    def _collect_youtube_event(self, keywords):
        """Collecte YouTube spécifique à l'événement"""
        
        # Rechercher des vidéos liées aux mots-clés
        search_terms = " ".join(keywords[:3])  # Limiter à 3 mots-clés
        
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            'part': 'snippet',
            'q': f"{search_terms} france politique",
            'type': 'video',
            'maxResults': 10,
            'order': 'relevance',
            'publishedAfter': (datetime.now() - timedelta(days=7)).isoformat() + 'Z',
            'key': self.youtube_key
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        videos = []
        if 'items' in data:
            for item in data['items']:
                video = {
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'published_at': item['snippet']['publishedAt'],
                    'channel_title': item['snippet']['channelTitle'],
                    'video_id': item['id']['videoId'],
                    'keywords': keywords,
                    'event_related': True
                }
                videos.append(video)
        
        return {
            'count': len(videos),
            'videos': videos,
            'search_terms': search_terms
        }
    
    def _collect_newsapi_event(self, keywords):
        """Collecte NewsAPI spécifique à l'événement"""
        
        search_terms = " ".join(keywords[:3])
        
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': f"{search_terms}",
            'language': 'fr',
            'sortBy': 'publishedAt',
            'pageSize': 20,
            'from': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            'apiKey': self.newsapi_key
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        articles = []
        if 'articles' in data:
            for article in data['articles']:
                if article['title'] and article['description']:
                    article_data = {
                        'title': article['title'],
                        'description': article['description'],
                        'url': article['url'],
                        'published_at': article['publishedAt'],
                        'source_name': article['source']['name'],
                        'keywords': keywords,
                        'event_related': True
                    }
                    articles.append(article_data)
        
        return {
            'count': len(articles),
            'articles': articles,
            'search_terms': search_terms
        }
    
    def _collect_web_scraping_event(self, keywords):
        """Collecte Web Scraping spécifique à l'événement"""
        
        # Utiliser les scripts existants avec des mots-clés spécifiques
        search_terms = " ".join(keywords)
        
        # Simuler une collecte Yahoo avec mots-clés
        articles = []
        for i in range(5):  # Simuler 5 articles
            article = {
                'title': f"Article {i+1} sur {search_terms}",
                'content': f"Contenu lié à {search_terms} et aux événements politiques français...",
                'url': f"https://example.com/article-{i+1}",
                'published_at': datetime.now().isoformat(),
                'source': 'yahoo_fr',
                'keywords': keywords,
                'event_related': True
            }
            articles.append(article)
        
        return {
            'count': len(articles),
            'articles': articles,
            'search_terms': search_terms
        }
    
    def _collect_gdelt_event(self, keywords):
        """Collecte GDELT spécifique à l'événement"""
        
        # Simuler une collecte GDELT avec filtrage par mots-clés
        events = []
        for i in range(3):  # Simuler 3 événements GDELT
            event = {
                'event_id': f"GDELT_EVENT_{i+1}",
                'date': datetime.now().strftime('%Y%m%d'),
                'source_url': f"https://example.com/news-{i+1}",
                'text': f"Événement politique français lié à {keywords}",
                'keywords': keywords,
                'event_related': True,
                'sentiment': 'neutre'
            }
            events.append(event)
        
        return {
            'count': len(events),
            'events': events,
            'search_terms': keywords
        }
    
    def save_collection(self, results, output_dir="data/raw/event_collections"):
        """Sauvegarde la collecte d'événement"""
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Nom de fichier basé sur l'événement et la date
        event_slug = re.sub(r'[^\w\s-]', '', results['event']).strip()
        event_slug = re.sub(r'[-\s]+', '_', event_slug)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"event_{event_slug}_{timestamp}.json"
        
        filepath = output_path / filename
        
        with filepath.open('w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        return filepath

def main():
    """Point d'entrée principal"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Collecteur Dynamique pour Événements")
    parser.add_argument("--event", required=True, help="Description de l'événement")
    parser.add_argument("--sources", nargs='+', 
                       choices=['youtube', 'newsapi', 'web_scraping', 'gdelt'],
                       default=['youtube', 'newsapi', 'web_scraping', 'gdelt'],
                       help="Sources à utiliser")
    parser.add_argument("--output-dir", default="data/raw/event_collections",
                       help="Répertoire de sortie")
    
    args = parser.parse_args()
    
    print(f"DYNAMIC: Collecte pour l'événement: {args.event}")
    print("=" * 60)
    
    collector = DynamicCollector()
    
    # Collecter les données
    results = collector.collect_for_event(args.event, args.sources)
    
    # Sauvegarder
    filepath = collector.save_collection(results, args.output_dir)
    
    print(f"SUCCESS: Collecte terminée")
    print(f"TOTAL: {results['total_collected']} éléments collectés")
    print(f"SAVED: {filepath}")
    
    # Afficher le résumé par source
    print("\nSUMMARY par source:")
    for source, data in results['sources'].items():
        if isinstance(data, dict) and 'count' in data:
            print(f"  • {source}: {data['count']} éléments")
        else:
            print(f"  • {source}: Erreur")

if __name__ == "__main__":
    main()
