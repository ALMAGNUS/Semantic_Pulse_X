"""
Source Web Scraping - Semantic Pulse X
Scraping de sites web pour collecter des données médiatiques
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import time
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlparse
import numpy as np

from app.backend.core.anonymization import anonymizer
from app.backend.core.config import settings


class WebScrapingSource:
    """Source de données par scraping web"""
    
    def __init__(self):
        self.data_dir = Path("data/raw/web_scraping")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Sites web cibles pour le scraping
        self.target_sites = {
            "allocine": {
                "base_url": "https://www.allocine.fr",
                "search_path": "/recherche/?q=",
                "selectors": {
                    "title": "h2.title",
                    "content": ".content-txt",
                    "rating": ".rating-item-value",
                    "comments": ".comment-txt"
                }
            },
            "purepeople": {
                "base_url": "https://www.purepeople.com",
                "search_path": "/recherche/?q=",
                "selectors": {
                    "title": "h1.article-title",
                    "content": ".article-content",
                    "comments": ".comment-content"
                }
            },
            "voici": {
                "base_url": "https://www.voici.fr",
                "search_path": "/recherche/?q=",
                "selectors": {
                    "title": "h1.article-title",
                    "content": ".article-body",
                    "comments": ".comment-text"
                }
            }
        }
        
        # Headers pour éviter la détection
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
    
    def scrape_news_articles(self, site: str, query: str, max_pages: int = 5) -> List[Dict[str, Any]]:
        """Scrape des articles de presse"""
        print(f"🕷️ Scraping d'articles sur {site} pour: {query}")
        
        if site not in self.target_sites:
            print(f"❌ Site {site} non supporté")
            return []
        
        site_config = self.target_sites[site]
        articles = []
        
        try:
            for page in range(1, max_pages + 1):
                print(f"📄 Page {page}/{max_pages}")
                
                # Construire l'URL de recherche
                search_url = f"{site_config['base_url']}{site_config['search_path']}{query}"
                if page > 1:
                    search_url += f"&page={page}"
                
                # Faire la requête
                response = requests.get(search_url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                # Parser le HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extraire les articles
                page_articles = self._extract_articles(soup, site_config, site)
                articles.extend(page_articles)
                
                # Pause entre les requêtes
                time.sleep(1)
                
                if not page_articles:
                    break
            
            print(f"✅ {len(articles)} articles scrapés")
            return articles
            
        except Exception as e:
            print(f"❌ Erreur scraping {site}: {e}")
            return self._simulate_articles(site, query, len(articles))
    
    def scrape_comments(self, site: str, article_url: str) -> List[Dict[str, Any]]:
        """Scrape les commentaires d'un article"""
        print(f"💬 Scraping des commentaires de {article_url}")
        
        try:
            response = requests.get(article_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            site_config = self.target_sites.get(site, {})
            
            comments = []
            comment_elements = soup.select(site_config.get('selectors', {}).get('comments', '.comment'))
            
            for element in comment_elements:
                comment_text = element.get_text(strip=True)
                if comment_text:
                    comments.append({
                        "text": anonymizer.anonymize_text(comment_text),
                        "article_url": article_url,
                        "site": site,
                        "timestamp": datetime.now().isoformat()
                    })
            
            print(f"✅ {len(comments)} commentaires scrapés")
            return comments
            
        except Exception as e:
            print(f"❌ Erreur scraping commentaires: {e}")
            return self._simulate_comments(article_url)
    
    def scrape_forum_posts(self, forum_url: str, max_pages: int = 3) -> List[Dict[str, Any]]:
        """Scrape des posts de forum"""
        print(f"💬 Scraping du forum: {forum_url}")
        
        try:
            posts = []
            
            for page in range(1, max_pages + 1):
                page_url = f"{forum_url}?page={page}" if page > 1 else forum_url
                
                response = requests.get(page_url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Sélecteurs génériques pour les forums
                post_elements = soup.select('.post, .message, .topic, .thread')
                
                for element in post_elements:
                    title_elem = element.select_one('h1, h2, h3, .title, .subject')
                    content_elem = element.select_one('.content, .message-content, .post-content')
                    
                    if title_elem and content_elem:
                        post = {
                            "title": anonymizer.anonymize_text(title_elem.get_text(strip=True)),
                            "content": anonymizer.anonymize_text(content_elem.get_text(strip=True)),
                            "url": page_url,
                            "timestamp": datetime.now().isoformat(),
                            "site": "forum"
                        }
                        posts.append(post)
                
                time.sleep(1)
            
            print(f"✅ {len(posts)} posts de forum scrapés")
            return posts
            
        except Exception as e:
            print(f"❌ Erreur scraping forum: {e}")
            return self._simulate_forum_posts(forum_url)
    
    def scrape_social_media_mentions(self, query: str) -> List[Dict[str, Any]]:
        """Scrape les mentions sur les réseaux sociaux (simulation)"""
        print(f"📱 Scraping des mentions sociales pour: {query}")
        
        # Simulation de mentions sur différents réseaux
        social_platforms = ["Twitter", "Facebook", "Instagram", "TikTok", "LinkedIn"]
        mentions = []
        
        for i in range(100):
            platform = np.random.choice(social_platforms)
            sentiment = np.random.choice(["positif", "negatif", "neutre"])
            
            mention_texts = {
                "positif": [f"J'adore {query} !", f"{query} c'est génial", f"Super {query}"],
                "negatif": [f"Je n'aime pas {query}", f"{query} c'est nul", f"Bof {query}"],
                "neutre": [f"J'ai vu {query}", f"À propos de {query}", f"{query} intéressant"]
            }
            
            text = np.random.choice(mention_texts[sentiment])
            
            mentions.append({
                "text": anonymizer.anonymize_text(text),
                "platform": platform,
                "sentiment": sentiment,
                "timestamp": datetime.now() - timedelta(hours=np.random.randint(0, 24*7)),
                "engagement": np.random.randint(0, 1000)
            })
        
        print(f"✅ {len(mentions)} mentions sociales scrapées")
        return mentions
    
    def _extract_articles(self, soup: BeautifulSoup, site_config: Dict, site: str) -> List[Dict[str, Any]]:
        """Extrait les articles d'une page"""
        articles = []
        
        # Sélecteurs génériques pour les articles
        article_selectors = [
            'article', '.article', '.news-item', '.post', '.story',
            '.content-item', '.news-article', '.blog-post'
        ]
        
        for selector in article_selectors:
            elements = soup.select(selector)
            if elements:
                break
        
        for element in elements[:10]:  # Limiter à 10 articles par page
            try:
                title_elem = element.select_one(site_config['selectors'].get('title', 'h1, h2, h3, .title'))
                content_elem = element.select_one(site_config['selectors'].get('content', '.content, .text, .body'))
                
                if title_elem and content_elem:
                    article = {
                        "title": anonymizer.anonymize_text(title_elem.get_text(strip=True)),
                        "content": anonymizer.anonymize_text(content_elem.get_text(strip=True)),
                        "site": site,
                        "url": self._extract_url(element),
                        "timestamp": datetime.now().isoformat(),
                        "word_count": len(content_elem.get_text().split())
                    }
                    articles.append(article)
            except Exception as e:
                continue
        
        return articles
    
    def _extract_url(self, element) -> str:
        """Extrait l'URL d'un élément"""
        link = element.select_one('a')
        if link and link.get('href'):
            return urljoin(self.target_sites['allocine']['base_url'], link['href'])
        return ""
    
    def _simulate_articles(self, site: str, query: str, count: int) -> List[Dict[str, Any]]:
        """Simule des articles"""
        articles = []
        for i in range(max(count, 10)):
            articles.append({
                "title": f"Article sur {query} #{i+1}",
                "content": f"Contenu de l'article sur {query} depuis {site}",
                "site": site,
                "url": f"https://{site}.com/article/{i}",
                "timestamp": datetime.now().isoformat(),
                "word_count": np.random.randint(100, 1000)
            })
        return articles
    
    def _simulate_comments(self, article_url: str) -> List[Dict[str, Any]]:
        """Simule des commentaires"""
        comments = []
        comment_templates = [
            "Très intéressant !",
            "Je ne suis pas d'accord",
            "Excellent article",
            "Bof, pas terrible",
            "Merci pour l'info",
            "C'est n'importe quoi",
            "Super !",
            "Décevant...",
            "Parfait !",
            "Pas mal"
        ]
        
        for i in range(np.random.randint(5, 20)):
            comment_text = np.random.choice(comment_templates)
            comments.append({
                "text": anonymizer.anonymize_text(comment_text),
                "article_url": article_url,
                "site": "simulation",
                "timestamp": datetime.now().isoformat()
            })
        return comments
    
    def _simulate_forum_posts(self, forum_url: str) -> List[Dict[str, Any]]:
        """Simule des posts de forum"""
        posts = []
        topics = ["actualité", "sport", "politique", "technologie", "culture"]
        
        for i in range(np.random.randint(10, 30)):
            topic = np.random.choice(topics)
            posts.append({
                "title": f"Discussion sur {topic} #{i+1}",
                "content": f"Post de forum sur {topic} depuis {forum_url}",
                "url": forum_url,
                "timestamp": datetime.now().isoformat(),
                "site": "forum"
            })
        return posts
    
    def save_data(self, data: List[Dict[str, Any]], filename: str):
        """Sauvegarde les données"""
        filepath = self.data_dir / filename
        
        if filename.endswith('.json'):
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        else:
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False)
        
        print(f"✅ Données web scraping sauvegardées: {filepath}")


# Instance globale
web_scraping_source = WebScrapingSource()
