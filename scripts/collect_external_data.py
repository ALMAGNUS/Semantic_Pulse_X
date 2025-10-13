#!/usr/bin/env python3
"""
Collecte de données Phase 2 - Semantic Pulse X
Approche simple et progressive
"""

import pandas as pd
import requests
import logging
from pathlib import Path
from datetime import datetime
import time
import json

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def collect_news_data():
    """Collecte de données d'actualités simples"""
    logger.info("📰 Collecte de données d'actualités")
    
    # Sources d'actualités gratuites
    news_sources = [
        "https://httpbin.org/json",  # API de test
        "https://jsonplaceholder.typicode.com/posts"  # Données de test
    ]
    
    collected_data = []
    
    for source in news_sources:
        try:
            logger.info(f"🔍 Collecte depuis: {source}")
            response = requests.get(source, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ {len(data) if isinstance(data, list) else 1} éléments collectés")
                
                # Formatage des données
                if isinstance(data, list):
                    for item in data[:5]:  # Limite à 5 éléments
                        collected_data.append({
                            'source': 'news_api',
                            'title': item.get('title', 'Titre par défaut'),
                            'content': item.get('body', 'Contenu par défaut'),
                            'date': datetime.now().isoformat(),
                            'url': source
                        })
                else:
                    collected_data.append({
                        'source': 'news_api',
                        'title': data.get('title', 'Titre par défaut'),
                        'content': str(data),
                        'date': datetime.now().isoformat(),
                        'url': source
                    })
                
                time.sleep(1)  # Délai entre les requêtes
                
            else:
                logger.warning(f"⚠️ Erreur {response.status_code} pour {source}")
                
        except Exception as e:
            logger.error(f"❌ Erreur collecte {source}: {e}")
    
    logger.info(f"📊 Total collecté: {len(collected_data)} articles")
    return collected_data

def collect_social_data():
    """Collecte de données sociales simulées"""
    logger.info("📱 Collecte de données sociales")
    
    # Données simulées pour démonstration
    social_data = [
        {
            'source': 'youtube_simulated',
            'video_title': 'Actualités du jour - Émotions médiatiques',
            'comment': 'Très intéressant cette analyse des émotions !',
            'date': datetime.now().isoformat(),
            'platform': 'youtube'
        },
        {
            'source': 'instagram_simulated', 
            'post_text': 'Nouvelle tendance émotionnelle détectée 📊',
            'comment': 'Super analyse !',
            'date': datetime.now().isoformat(),
            'platform': 'instagram'
        },
        {
            'source': 'twitter_simulated',
            'tweet': 'Les émotions dans les médias évoluent rapidement',
            'date': datetime.now().isoformat(),
            'platform': 'twitter'
        }
    ]
    
    logger.info(f"📊 Total collecté: {len(social_data)} posts sociaux")
    return social_data

def collect_web_scraping_data():
    """Collecte de données par web scraping simple"""
    logger.info("🕷️ Collecte par web scraping")
    
    # Scraping simple d'une page de test
    try:
        from bs4 import BeautifulSoup
        
        # Page de test simple
        test_url = "https://httpbin.org/html"
        response = requests.get(test_url, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraction des données
            scraped_data = []
            paragraphs = soup.find_all('p')
            
            for i, p in enumerate(paragraphs[:3]):  # Limite à 3 paragraphes
                scraped_data.append({
                    'source': 'web_scraping',
                    'content': p.get_text().strip(),
                    'date': datetime.now().isoformat(),
                    'url': test_url,
                    'paragraph_id': i
                })
            
            logger.info(f"📊 Total scrapé: {len(scraped_data)} paragraphes")
            return scraped_data
            
        else:
            logger.warning(f"⚠️ Erreur scraping: {response.status_code}")
            return []
            
    except ImportError:
        logger.warning("⚠️ BeautifulSoup non installé, utilisation de données simulées")
        return [{
            'source': 'web_scraping',
            'content': 'Contenu simulé pour démonstration',
            'date': datetime.now().isoformat(),
            'url': 'simulated'
        }]
    except Exception as e:
        logger.error(f"❌ Erreur scraping: {e}")
        return []

def save_collected_data(all_data):
    """Sauvegarde des données collectées"""
    logger.info("💾 Sauvegarde des données collectées")
    
    # Création du dossier
    output_dir = Path("data/raw/external_apis")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Sauvegarde en JSON
    json_file = output_dir / f"external_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"✅ Données sauvegardées: {json_file}")
    
    # Sauvegarde en CSV
    csv_file = output_dir / f"external_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df = pd.DataFrame(all_data)
    df.to_csv(csv_file, index=False, encoding='utf-8')
    
    logger.info(f"✅ Données CSV: {csv_file}")
    
    return json_file, csv_file

def main():
    """Fonction principale de collecte Phase 2"""
    logger.info("🚀 DÉMARRAGE COLLECTE PHASE 2 - APIs EXTERNES")
    logger.info("=" * 60)
    
    all_data = []
    
    # 1. Collecte d'actualités
    news_data = collect_news_data()
    all_data.extend(news_data)
    
    # 2. Collecte de données sociales
    social_data = collect_social_data()
    all_data.extend(social_data)
    
    # 3. Collecte par web scraping
    scraping_data = collect_web_scraping_data()
    all_data.extend(scraping_data)
    
    # 4. Sauvegarde
    if all_data:
        json_file, csv_file = save_collected_data(all_data)
        
        # Résumé
        logger.info("\n" + "=" * 60)
        logger.info("📊 RÉSUMÉ COLLECTE PHASE 2")
        logger.info("=" * 60)
        logger.info(f"📈 Total données collectées: {len(all_data)}")
        
        # Par source
        sources = {}
        for item in all_data:
            source = item.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
        
        logger.info("📋 Répartition par source:")
        for source, count in sources.items():
            logger.info(f"   {source}: {count} éléments")
        
        logger.info(f"💾 Fichiers créés:")
        logger.info(f"   JSON: {json_file}")
        logger.info(f"   CSV: {csv_file}")
        
        logger.info("✅ PHASE 2 COLLECTE TERMINÉE!")
        return True
    else:
        logger.error("❌ Aucune donnée collectée")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)




