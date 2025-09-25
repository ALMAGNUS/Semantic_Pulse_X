"""
Gestionnaire des sources de données - Semantic Pulse X
Orchestration de toutes les sources de données
"""

import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import json

from app.backend.data_sources.kaggle_tweets import kaggle_tweets_source
from app.backend.data_sources.youtube_api import youtube_api_source
from app.backend.data_sources.instagram_api import instagram_api_source
from app.backend.data_sources.web_scraping import web_scraping_source
from app.backend.core.anonymization import anonymizer


class DataSourceManager:
    """Gestionnaire central des sources de données"""
    
    def __init__(self):
        self.sources = {
            "kaggle_tweets": kaggle_tweets_source,
            "youtube": youtube_api_source,
            "instagram": instagram_api_source,
            "web_scraping": web_scraping_source
        }
        
        self.data_dir = Path("data/raw")
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def setup_kaggle_tweets(self, dataset_name: str = "sentiment140") -> Dict[str, str]:
        """Configure le dataset Kaggle et le découpe en 3 sources"""
        print("🔄 Configuration du dataset Kaggle Tweets...")
        
        # Télécharger le dataset
        dataset_path = kaggle_tweets_source.download_kaggle_dataset(dataset_name)
        
        # Découper en 3 sources
        split_paths = kaggle_tweets_source.split_into_three_sources(dataset_path)
        
        # Traiter pour Semantic Pulse
        processed_tweets = kaggle_tweets_source.process_tweets_for_semantic_pulse(dataset_path)
        
        # Sauvegarder les données traitées
        processed_path = self.data_dir / "kaggle_tweets_processed.json"
        with open(processed_path, 'w', encoding='utf-8') as f:
            json.dump(processed_tweets, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Dataset Kaggle configuré et découpé")
        return split_paths
    
    def collect_youtube_data(self, queries: List[str], max_videos: int = 50) -> Dict[str, Any]:
        """Collecte des données YouTube"""
        print("📺 Collecte des données YouTube...")
        
        all_data = {
            "videos": [],
            "comments": [],
            "sentiments": []
        }
        
        for query in queries:
            print(f"🔍 Recherche YouTube: {query}")
            
            # Rechercher des vidéos
            videos = youtube_api_source.search_videos(query, max_videos // len(queries))
            all_data["videos"].extend(videos)
            
            # Analyser les commentaires des vidéos
            for video in videos[:5]:  # Limiter à 5 vidéos par requête
                video_id = video["video_id"]
                
                # Récupérer les commentaires
                comments = youtube_api_source.get_video_comments(video_id, 50)
                all_data["comments"].extend(comments)
                
                # Analyser le sentiment
                sentiment = youtube_api_source.analyze_video_sentiment(video_id)
                all_data["sentiments"].append(sentiment)
        
        # Sauvegarder
        youtube_path = self.data_dir / "youtube_data.json"
        with open(youtube_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Données YouTube collectées: {len(all_data['videos'])} vidéos, {len(all_data['comments'])} commentaires")
        return all_data
    
    def collect_instagram_data(self, accounts: List[str], max_posts: int = 100) -> Dict[str, Any]:
        """Collecte des données Instagram"""
        print("📸 Collecte des données Instagram...")
        
        all_data = {
            "posts": [],
            "comments": [],
            "engagements": []
        }
        
        for account in accounts:
            print(f"📱 Collecte Instagram: @{account}")
            
            # Récupérer les posts
            posts = instagram_api_source.get_user_posts(account, max_posts // len(accounts))
            all_data["posts"].extend(posts)
            
            # Analyser l'engagement des posts
            for post in posts[:3]:  # Limiter à 3 posts par compte
                post_id = post["post_id"]
                
                # Récupérer les commentaires
                comments = instagram_api_source.get_post_comments(post_id, 30)
                all_data["comments"].extend(comments)
                
                # Analyser l'engagement
                engagement = instagram_api_source.analyze_post_engagement(post_id)
                all_data["engagements"].append(engagement)
        
        # Récupérer le contenu tendance
        trending = instagram_api_source.get_trending_content(50)
        all_data["trending"] = trending
        
        # Sauvegarder
        instagram_path = self.data_dir / "instagram_data.json"
        with open(instagram_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Données Instagram collectées: {len(all_data['posts'])} posts, {len(all_data['comments'])} commentaires")
        return all_data
    
    def collect_web_scraping_data(self, queries: List[str], sites: List[str]) -> Dict[str, Any]:
        """Collecte des données par scraping web"""
        print("🕷️ Collecte des données par scraping web...")
        
        all_data = {
            "articles": [],
            "comments": [],
            "forum_posts": [],
            "social_mentions": []
        }
        
        # Scraper les articles de presse
        for site in sites:
            for query in queries:
                print(f"📰 Scraping {site}: {query}")
                
                articles = web_scraping_source.scrape_news_articles(site, query, 3)
                all_data["articles"].extend(articles)
                
                # Scraper les commentaires des articles
                for article in articles[:2]:  # Limiter à 2 articles par site/requête
                    if article.get("url"):
                        comments = web_scraping_source.scrape_comments(site, article["url"])
                        all_data["comments"].extend(comments)
        
        # Scraper les forums
        forum_urls = [
            "https://www.jeuxvideo.com/forums/",
            "https://www.hardware.fr/forums/",
            "https://www.lesnumeriques.com/forums/"
        ]
        
        for forum_url in forum_urls:
            posts = web_scraping_source.scrape_forum_posts(forum_url, 2)
            all_data["forum_posts"].extend(posts)
        
        # Scraper les mentions sociales
        for query in queries:
            mentions = web_scraping_source.scrape_social_media_mentions(query)
            all_data["social_mentions"].extend(mentions)
        
        # Sauvegarder
        scraping_path = self.data_dir / "web_scraping_data.json"
        with open(scraping_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Données web scraping collectées: {len(all_data['articles'])} articles, {len(all_data['comments'])} commentaires")
        return all_data
    
    def collect_all_sources(self) -> Dict[str, Any]:
        """Collecte des données de toutes les sources"""
        print("🚀 Collecte complète des données de toutes les sources...")
        
        all_data = {}
        
        try:
            # 1. Configuration Kaggle Tweets
            print("\n📊 1. Configuration Kaggle Tweets...")
            kaggle_data = self.setup_kaggle_tweets("sentiment140")
            all_data["kaggle"] = kaggle_data
            
            # 2. Collecte YouTube
            print("\n📺 2. Collecte YouTube...")
            youtube_queries = ["actualité", "politique", "sport", "culture", "technologie"]
            youtube_data = self.collect_youtube_data(youtube_queries, 50)
            all_data["youtube"] = youtube_data
            
            # 3. Collecte Instagram
            print("\n📸 3. Collecte Instagram...")
            instagram_accounts = ["tf1", "france2", "bfmtv", "canalplus"]
            instagram_data = self.collect_instagram_data(instagram_accounts, 100)
            all_data["instagram"] = instagram_data
            
            # 4. Web Scraping
            print("\n🕷️ 4. Web Scraping...")
            scraping_queries = ["actualité", "politique", "sport", "culture"]
            scraping_sites = ["allocine", "purepeople", "voici"]
            scraping_data = self.collect_web_scraping_data(scraping_queries, scraping_sites)
            all_data["web_scraping"] = scraping_data
            
            # 5. Générer le rapport final
            print("\n📊 5. Génération du rapport final...")
            report = self._generate_collection_report(all_data)
            all_data["report"] = report
            
            # Sauvegarder le rapport complet
            report_path = self.data_dir / "complete_collection_report.json"
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"\n✅ Collecte complète terminée!")
            print(f"📁 Données sauvegardées dans: {self.data_dir}")
            
            return all_data
            
        except Exception as e:
            print(f"❌ Erreur lors de la collecte: {e}")
            return {"error": str(e)}
    
    def _generate_collection_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Génère un rapport de collecte"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_sources": len(data),
            "sources_status": {},
            "data_summary": {},
            "recommendations": []
        }
        
        # Analyser chaque source
        for source_name, source_data in data.items():
            if source_name == "report":
                continue
                
            if isinstance(source_data, dict):
                report["sources_status"][source_name] = "success"
                
                # Compter les éléments
                total_items = 0
                for key, value in source_data.items():
                    if isinstance(value, list):
                        total_items += len(value)
                
                report["data_summary"][source_name] = {
                    "total_items": total_items,
                    "keys": list(source_data.keys())
                }
            else:
                report["sources_status"][source_name] = "error"
        
        # Recommandations
        if report["data_summary"].get("kaggle", {}).get("total_items", 0) > 0:
            report["recommendations"].append("Dataset Kaggle configuré avec succès")
        
        if report["data_summary"].get("youtube", {}).get("total_items", 0) > 0:
            report["recommendations"].append("Données YouTube collectées")
        
        if report["data_summary"].get("instagram", {}).get("total_items", 0) > 0:
            report["recommendations"].append("Données Instagram collectées")
        
        if report["data_summary"].get("web_scraping", {}).get("total_items", 0) > 0:
            report["recommendations"].append("Données web scraping collectées")
        
        return report
    
    def get_source_status(self) -> Dict[str, Any]:
        """Retourne le statut de toutes les sources"""
        status = {}
        
        for source_name, source in self.sources.items():
            try:
                # Vérifier si la source est accessible
                if hasattr(source, 'get_status'):
                    status[source_name] = source.get_status()
                else:
                    status[source_name] = {
                        "status": "available",
                        "last_check": datetime.now().isoformat()
                    }
            except Exception as e:
                status[source_name] = {
                    "status": "error",
                    "error": str(e),
                    "last_check": datetime.now().isoformat()
                }
        
        return status


# Instance globale
data_source_manager = DataSourceManager()
