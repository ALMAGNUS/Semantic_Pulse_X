#!/usr/bin/env python3
"""
Collecteur NewsAPI - Semantic Pulse X
Collecte des articles de presse français pour analyse émotionnelle
"""

import os
import requests
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NewsAPICollector:
    """
    Collecteur d'articles de presse via NewsAPI.
    
    Fonctionnalités :
    - Collecte d'articles français
    - Anonymisation RGPD
    - Stockage structuré
    - Analyse émotionnelle
    """
    
    def __init__(self):
        self.api_key = os.getenv('NEWSAPI_KEY')
        self.base_url = "https://newsapi.org/v2"
        self.data_dir = "data/raw/newsapi"
        os.makedirs(self.data_dir, exist_ok=True)
        
        if not self.api_key:
            logger.warning("⚠️ NEWSAPI_KEY non définie dans .env")
            logger.info("💡 Obtenez une clé gratuite sur: https://newsapi.org/register")
        else:
            logger.info(f"🔑 Clé NewsAPI chargée: {self.api_key[:10]}...")
    
    def test_connection(self) -> bool:
        """Teste la connexion à NewsAPI."""
        if not self.api_key:
            logger.error("❌ Clé API manquante")
            return False
        
        logger.info("🔍 Test de connexion NewsAPI...")
        
        try:
            url = f"{self.base_url}/top-headlines"
            params = {
                'country': 'fr',
                'pageSize': 1,
                'apiKey': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Connexion réussie: {data.get('totalResults', 0)} articles disponibles")
                return True
            else:
                logger.error(f"❌ Erreur API: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur de connexion: {e}")
            return False
    
    def collect_headlines(self, country: str = 'fr', page_size: int = 20) -> List[Dict[str, Any]]:
        """
        Collecte les titres d'actualité.
        
        Args:
            country: Code pays (fr, us, etc.)
            page_size: Nombre d'articles à récupérer
            
        Returns:
            Liste des articles collectés
        """
        logger.info(f"📰 Collecte des titres d'actualité ({country})")
        
        if not self.api_key:
            logger.error("❌ Clé API manquante")
            return []
        
        try:
            url = f"{self.base_url}/top-headlines"
            params = {
                'country': country,
                'pageSize': page_size,
                'apiKey': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get('articles', [])
            
            logger.info(f"✅ {len(articles)} articles collectés")
            
            # Traiter et anonymiser les articles
            processed_articles = []
            for article in articles:
                processed_article = self._process_article(article)
                if processed_article:
                    processed_articles.append(processed_article)
            
            logger.info(f"✅ {len(processed_articles)} articles traités")
            return processed_articles
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la collecte: {e}")
            return []
    
    def collect_everything(self, query: str = "actualités", language: str = 'fr', 
                         page_size: int = 20, days_back: int = 7) -> List[Dict[str, Any]]:
        """
        Collecte tous les articles correspondant à une requête.
        
        Args:
            query: Terme de recherche
            language: Langue des articles
            page_size: Nombre d'articles
            days_back: Nombre de jours en arrière
            
        Returns:
            Liste des articles collectés
        """
        logger.info(f"🔍 Recherche d'articles: '{query}' ({language})")
        
        if not self.api_key:
            logger.error("❌ Clé API manquante")
            return []
        
        try:
            # Calculer la date de début
            from_date = datetime.now() - timedelta(days=days_back)
            from_date_str = from_date.strftime('%Y-%m-%d')
            
            url = f"{self.base_url}/everything"
            params = {
                'q': query,
                'language': language,
                'from': from_date_str,
                'sortBy': 'publishedAt',
                'pageSize': page_size,
                'apiKey': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get('articles', [])
            
            logger.info(f"✅ {len(articles)} articles trouvés pour '{query}'")
            
            # Traiter et anonymiser les articles
            processed_articles = []
            for article in articles:
                processed_article = self._process_article(article)
                if processed_article:
                    processed_articles.append(processed_article)
            
            logger.info(f"✅ {len(processed_articles)} articles traités")
            return processed_articles
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la recherche: {e}")
            return []
    
    def _process_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Traite et anonymise un article.
        
        Args:
            article: Article brut de NewsAPI
            
        Returns:
            Article traité et anonymisé
        """
        try:
            # Extraire les informations principales
            processed = {
                'source': 'newsapi',
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'content': article.get('content', ''),
                'url': article.get('url', ''),
                'published_at': article.get('publishedAt', ''),
                'source_name': article.get('source', {}).get('name', ''),
                'author': article.get('author', ''),
                'collected_at': datetime.now().isoformat(),
                'anonymized': True
            }
            
            # Anonymisation RGPD
            processed = self._anonymize_article(processed)
            
            # Filtrer les articles vides
            if not processed['title'] and not processed['description']:
                return None
            
            return processed
            
        except Exception as e:
            logger.warning(f"⚠️ Erreur traitement article: {e}")
            return None
    
    def _anonymize_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Anonymise un article selon RGPD.
        
        Args:
            article: Article à anonymiser
            
        Returns:
            Article anonymisé
        """
        # Anonymiser l'auteur
        if article.get('author'):
            article['author'] = f"author_{hash(article['author']) % 10000}"
        
        # Anonymiser l'URL (garder seulement le domaine)
        if article.get('url'):
            try:
                from urllib.parse import urlparse
                parsed = urlparse(article['url'])
                article['url'] = f"{parsed.scheme}://{parsed.netloc}/***"
            except:
                article['url'] = "***"
        
        # Nettoyer le contenu (supprimer les PII potentielles)
        content = article.get('content', '')
        if content:
            # Supprimer les emails
            import re
            content = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', content)
            # Supprimer les téléphones
            content = re.sub(r'\b\d{2}[\s.-]?\d{2}[\s.-]?\d{2}[\s.-]?\d{2}[\s.-]?\d{2}\b', '[PHONE]', content)
            article['content'] = content
        
        return article
    
    def save_articles(self, articles: List[Dict[str, Any]], filename: str = None) -> str:
        """
        Sauvegarde les articles dans un fichier JSON.
        
        Args:
            articles: Liste des articles à sauvegarder
            filename: Nom du fichier (optionnel)
            
        Returns:
            Chemin du fichier sauvegardé
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"newsapi_articles_{timestamp}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
            
            logger.info(f"💾 {len(articles)} articles sauvegardés: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde: {e}")
            return ""
    
    def analyze_articles(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyse les articles collectés.
        
        Args:
            articles: Liste des articles
            
        Returns:
            Dictionnaire d'analyse
        """
        logger.info(f"📊 Analyse de {len(articles)} articles")
        
        if not articles:
            return {}
        
        analysis = {
            'total_articles': len(articles),
            'sources': {},
            'date_range': {},
            'content_stats': {},
            'themes': {}
        }
        
        # Analyser les sources
        sources = [article.get('source_name', 'Unknown') for article in articles]
        source_counts = {}
        for source in sources:
            source_counts[source] = source_counts.get(source, 0) + 1
        analysis['sources'] = source_counts
        
        # Analyser les dates
        dates = [article.get('published_at', '') for article in articles if article.get('published_at')]
        if dates:
            analysis['date_range'] = {
                'earliest': min(dates),
                'latest': max(dates),
                'span_days': len(set([d[:10] for d in dates]))
            }
        
        # Analyser le contenu
        total_chars = sum(len(article.get('title', '') + article.get('description', '')) for article in articles)
        analysis['content_stats'] = {
            'total_characters': total_chars,
            'avg_chars_per_article': total_chars // len(articles) if articles else 0,
            'articles_with_content': len([a for a in articles if a.get('content')])
        }
        
        # Analyser les thèmes (mots-clés simples)
        all_text = ' '.join([article.get('title', '') + ' ' + article.get('description', '') for article in articles])
        words = all_text.lower().split()
        word_counts = {}
        for word in words:
            if len(word) > 4:  # Filtrer les mots courts
                word_counts[word] = word_counts.get(word, 0) + 1
        
        # Top 10 mots
        top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        analysis['themes'] = dict(top_words)
        
        logger.info("✅ Analyse terminée")
        logger.info(f"   📰 Sources: {len(source_counts)}")
        logger.info(f"   📅 Période: {analysis['date_range'].get('span_days', 0)} jours")
        logger.info(f"   📊 Contenu: {analysis['content_stats']['avg_chars_per_article']} chars/article")
        
        return analysis

def main():
    """Fonction principale de test."""
    logger.info("🚀 TEST NEWSAPI COLLECTOR")
    logger.info("=" * 50)
    
    # Créer le collecteur
    collector = NewsAPICollector()
    
    # Tester la connexion
    if not collector.test_connection():
        logger.error("❌ Impossible de se connecter à NewsAPI")
        logger.info("💡 Vérifiez votre clé API dans le fichier .env")
        return False
    
    try:
        # Collecter les titres d'actualité
        logger.info("\n📰 COLLECTE DES TITRES D'ACTUALITÉ")
        headlines = collector.collect_headlines(country='fr', page_size=10)
        
        if headlines:
            # Sauvegarder
            filepath = collector.save_articles(headlines, "french_headlines.json")
            
            # Analyser
            analysis = collector.analyze_articles(headlines)
            
            # Collecter des articles sur des sujets spécifiques
            logger.info("\n🔍 COLLECTE D'ARTICLES SPÉCIFIQUES")
            topics = ["politique", "économie", "sport", "culture"]
            
            all_articles = headlines.copy()
            
            for topic in topics:
                logger.info(f"   Recherche: {topic}")
                topic_articles = collector.collect_everything(query=topic, language='fr', page_size=5)
                all_articles.extend(topic_articles)
            
            # Sauvegarder tous les articles
            if all_articles:
                all_filepath = collector.save_articles(all_articles, "all_newsapi_articles.json")
                
                # Analyse complète
                complete_analysis = collector.analyze_articles(all_articles)
                
                # Sauvegarder l'analyse
                analysis_filepath = os.path.join(collector.data_dir, "newsapi_analysis.json")
                with open(analysis_filepath, 'w', encoding='utf-8') as f:
                    json.dump(complete_analysis, f, ensure_ascii=False, indent=2)
                
                logger.info(f"💾 Analyse sauvegardée: {analysis_filepath}")
        
        # Résumé final
        logger.info("\n" + "=" * 50)
        logger.info("🎉 COLLECTE NEWSAPI TERMINÉE!")
        logger.info("=" * 50)
        logger.info(f"✅ Articles collectés: {len(all_articles) if 'all_articles' in locals() else len(headlines)}")
        logger.info(f"✅ Fichiers créés dans: {collector.data_dir}")
        logger.info("✅ Anonymisation RGPD appliquée")
        logger.info("✅ Prêt pour l'analyse émotionnelle")
        logger.info("=" * 50)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la collecte: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)




