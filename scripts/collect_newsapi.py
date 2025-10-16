#!/usr/bin/env python3
"""
Collecte NewsAPI - Semantic Pulse X
Collecte les actualités françaises via NewsAPI pour l'analyse émotionnelle
"""

import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsAPICollector:
    """Collecteur NewsAPI pour les actualités françaises"""
    
    def __init__(self):
        self.api_key = os.getenv('NEWSAPI_KEY', '0c60e7050af540789303e332e2aa3741')
        self.base_url = "https://newsapi.org/v2"
        
    def collect_french_news(self, days=1, max_articles=50):
        """Collecte les actualités françaises"""
        
        if not self.api_key:
            logger.error("Clé API NewsAPI manquante")
            return []
        
        try:
            # Calculer la date de début
            from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            # Paramètres de recherche
            params = {
                'apiKey': self.api_key,
                'country': 'fr',
                'language': 'fr',
                'from': from_date,
                'sortBy': 'publishedAt',
                'pageSize': min(max_articles, 100)  # Limite NewsAPI
            }
            
            # Récupérer les actualités
            response = requests.get(f"{self.base_url}/top-headlines", params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] != 'ok':
                logger.error(f"Erreur NewsAPI: {data.get('message', 'Erreur inconnue')}")
                return []
            
            # Formater les articles
            articles = []
            for article in data['articles']:
                article_data = {
                    'title': article['title'],
                    'description': article['description'],
                    'content': article['content'],
                    'url': article['url'],
                    'published_at': article['publishedAt'],
                    'source_name': article['source']['name'],
                    'author': article['author'],
                    'url_to_image': article['urlToImage'],
                    'collected_at': datetime.now().isoformat()
                }
                articles.append(article_data)
            
            logger.info(f"✅ {len(articles)} articles français collectés")
            return articles
            
        except Exception as e:
            logger.error(f"❌ Erreur collecte NewsAPI: {e}")
            return []
    
    def collect_by_keywords(self, keywords, max_articles=30):
        """Collecte les actualités par mots-clés"""
        
        if not self.api_key:
            logger.error("Clé API NewsAPI manquante")
            return []
        
        try:
            # Paramètres de recherche
            params = {
                'apiKey': self.api_key,
                'q': keywords,
                'language': 'fr',
                'sortBy': 'publishedAt',
                'pageSize': min(max_articles, 100)
            }
            
            # Récupérer les actualités
            response = requests.get(f"{self.base_url}/everything", params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] != 'ok':
                logger.error(f"Erreur NewsAPI: {data.get('message', 'Erreur inconnue')}")
                return []
            
            # Formater les articles
            articles = []
            for article in data['articles']:
                article_data = {
                    'title': article['title'],
                    'description': article['description'],
                    'content': article['content'],
                    'url': article['url'],
                    'published_at': article['publishedAt'],
                    'source_name': article['source']['name'],
                    'author': article['author'],
                    'url_to_image': article['urlToImage'],
                    'keywords': keywords,
                    'collected_at': datetime.now().isoformat()
                }
                articles.append(article_data)
            
            logger.info(f"✅ {len(articles)} articles collectés pour '{keywords}'")
            return articles
            
        except Exception as e:
            logger.error(f"❌ Erreur collecte NewsAPI: {e}")
            return []
    
    def save_to_file(self, articles, output_dir="data/raw/external_apis"):
        """Sauvegarde les articles dans un fichier JSON"""
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"newsapi_fr_{timestamp}.json"
        filepath = output_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        
        logger.info(f"📄 Articles sauvegardés: {filepath}")
        return filepath

def main():
    """Point d'entrée principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Collecte NewsAPI")
    parser.add_argument("--keywords", help="Mots-clés pour la recherche")
    args = parser.parse_args()
    
    print("NewsAPI: Collecte France")
    print("=" * 30)
    
    collector = NewsAPICollector()
    
    # Collecter les actualités générales
    print("Collecte actualites generales...")
    general_articles = collector.collect_french_news(days=1, max_articles=30)
    
    # Collecter par mots-clés spécifiques ou généraux
    if args.keywords:
        print(f"Collecte par mots-cles: {args.keywords}")
        keyword_articles = collector.collect_by_keywords(args.keywords, max_articles=20)
    else:
        print("Collecte par mots-cles generaux...")
        keyword_articles = collector.collect_by_keywords("politique", max_articles=20)
    
    # Combiner les articles
    all_articles = general_articles + keyword_articles
    
    if all_articles:
        # Sauvegarder
        filepath = collector.save_to_file(all_articles)
        
        print(f"SUCCESS: {len(all_articles)} articles collectes")
        print(f"SAVED: {filepath}")
        
        # Afficher quelques exemples
        print("\nEXAMPLES:")
        for i, article in enumerate(all_articles[:3]):
            print(f"  {i+1}. {article['title'][:60]}...")
            print(f"     Source: {article['source_name']}")
            print(f"     Date: {article['published_at'][:10]}")
    else:
        print("ERROR: Aucun article collecte")

if __name__ == "__main__":
    main()
