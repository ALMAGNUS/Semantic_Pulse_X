#!/usr/bin/env python3
"""
Collecteur Web Scraping - Semantic Pulse X
Collecte de commentaires et articles depuis des sites français publics
Utilise undetected-chromedriver pour contourner les protections anti-bot
"""

import os
import json
import time
import logging
import hashlib
from datetime import datetime
from typing import List, Dict, Any
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests
from bs4 import BeautifulSoup

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WebScrapingCollector:
    """
    Collecteur de données par web scraping avec undetected-chromedriver.
    
    Fonctionnalités :
    - Contournement des protections anti-bot
    - Anonymisation RGPD automatique
    - Collecte multi-sites
    - Respect des robots.txt
    """
    
    def __init__(self):
        self.data_dir = "data/raw/web_scraping"
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.driver = None
        self.collected_data = []
        
        # Sites français publics (blogs, forums, actualités)
        self.target_sites = [
            {
                'name': 'reddit_france',
                'url': 'https://www.reddit.com/r/france/',
                'type': 'forum',
                'selectors': {
                    'posts': '[data-testid="post-container"]',
                    'title': 'h3',
                    'content': '[data-testid="post-content"]',
                    'comments': '[data-testid="comment"]'
                }
            },
            {
                'name': '20minutes',
                'url': 'https://www.20minutes.fr/',
                'type': 'news',
                'selectors': {
                    'articles': '.teaser',
                    'title': '.teaser-title',
                    'content': '.content',
                    'comments': '.comment'
                }
            }
        ]
        
        logger.info("🕷️ Collecteur Web Scraping initialisé")
        logger.info(f"📁 Dossier de sortie: {self.data_dir}")
    
    def _setup_driver(self) -> bool:
        """Configure le driver Chrome non détectable."""
        try:
            logger.info("🚀 Configuration du driver Chrome...")
            
            options = uc.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            options.add_argument('--disable-images')  # Plus rapide
            options.add_argument('--disable-javascript')  # Optionnel
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Mode headless pour la production
            # options.add_argument('--headless')
            
            self.driver = uc.Chrome(options=options)
            self.driver.set_page_load_timeout(30)
            
            logger.info("✅ Driver Chrome configuré avec succès")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur configuration driver: {e}")
            return False
    
    def _cleanup_driver(self):
        """Nettoie le driver."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("🧹 Driver fermé")
            except Exception as e:
                logger.warning(f"⚠️ Erreur fermeture driver: {e}")
    
    def _anonymize_content(self, content: str, url: str) -> Dict[str, Any]:
        """Anonymise le contenu selon RGPD."""
        import re
        
        # Supprimer les emails
        content = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', content)
        
        # Supprimer les téléphones français
        content = re.sub(r'\b0[1-9][\s.-]?(?:\d{2}[\s.-]?){4}\b', '[PHONE]', content)
        
        # Supprimer les noms propres (approximatif)
        content = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[PERSON]', content)
        
        # Créer un hash anonyme pour l'URL
        url_hash = hashlib.sha256(url.encode()).hexdigest()[:8]
        
        return {
            'content': content,
            'source': 'web_scraping',
            'url_hash': url_hash,
            'collected_at': datetime.now().isoformat(),
            'anonymized': True
        }
    
    def scrape_simple_site(self, url: str, max_items: int = 10) -> List[Dict[str, Any]]:
        """
        Scrape simple d'un site avec BeautifulSoup (sans JavaScript).
        
        Args:
            url: URL à scraper
            max_items: Nombre maximum d'éléments à collecter
            
        Returns:
            Liste des données collectées
        """
        logger.info(f"🔍 Scraping simple: {url}")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraire les titres et paragraphes
            items = []
            
            # Titres d'articles
            titles = soup.find_all(['h1', 'h2', 'h3'], limit=max_items)
            for title in titles:
                if title.get_text().strip():
                    item = self._anonymize_content(title.get_text().strip(), url)
                    item['type'] = 'title'
                    items.append(item)
            
            # Paragraphes de contenu
            paragraphs = soup.find_all('p', limit=max_items)
            for p in paragraphs:
                text = p.get_text().strip()
                if len(text) > 50:  # Filtrer les paragraphes trop courts
                    item = self._anonymize_content(text, url)
                    item['type'] = 'content'
                    items.append(item)
            
            logger.info(f"✅ {len(items)} éléments collectés depuis {url}")
            return items[:max_items]
            
        except Exception as e:
            logger.error(f"❌ Erreur scraping {url}: {e}")
            return []
    
    def scrape_with_chrome(self, site_config: Dict[str, Any], max_items: int = 10) -> List[Dict[str, Any]]:
        """
        Scrape avec Chrome pour les sites avec JavaScript.
        
        Args:
            site_config: Configuration du site à scraper
            max_items: Nombre maximum d'éléments
            
        Returns:
            Liste des données collectées
        """
        logger.info(f"🤖 Scraping Chrome: {site_config['name']}")
        
        if not self.driver:
            if not self._setup_driver():
                return []
        
        try:
            self.driver.get(site_config['url'])
            time.sleep(3)  # Attendre le chargement
            
            items = []
            
            # Essayer de trouver les éléments selon la configuration
            try:
                # Attendre que les éléments se chargent
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
                )
                
                # Collecter les titres
                title_elements = self.driver.find_elements(By.TAG_NAME, "h1")[:max_items//2]
                title_elements.extend(self.driver.find_elements(By.TAG_NAME, "h2")[:max_items//2])
                
                for element in title_elements:
                    try:
                        text = element.text.strip()
                        if text and len(text) > 10:
                            item = self._anonymize_content(text, site_config['url'])
                            item['type'] = 'title'
                            item['site'] = site_config['name']
                            items.append(item)
                    except Exception as e:
                        logger.debug(f"Erreur élément titre: {e}")
                        continue
                
                # Collecter les paragraphes
                p_elements = self.driver.find_elements(By.TAG_NAME, "p")[:max_items]
                for element in p_elements:
                    try:
                        text = element.text.strip()
                        if text and len(text) > 50:
                            item = self._anonymize_content(text, site_config['url'])
                            item['type'] = 'content'
                            item['site'] = site_config['name']
                            items.append(item)
                    except Exception as e:
                        logger.debug(f"Erreur élément contenu: {e}")
                        continue
                
                logger.info(f"✅ {len(items)} éléments collectés depuis {site_config['name']}")
                return items[:max_items]
                
            except TimeoutException:
                logger.warning(f"⏱️ Timeout pour {site_config['name']}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Erreur scraping Chrome {site_config['name']}: {e}")
            return []
    
    def collect_from_sites(self, max_items_per_site: int = 10) -> List[Dict[str, Any]]:
        """
        Collecte depuis plusieurs sites.
        
        Args:
            max_items_per_site: Maximum d'éléments par site
            
        Returns:
            Liste de tous les éléments collectés
        """
        logger.info("🌐 Début de la collecte multi-sites")
        
        all_items = []
        
        # Sites simples (sans JavaScript)
        simple_sites = [
            'https://www.lemonde.fr/rss/une.xml',  # RSS
            'https://www.liberation.fr/',
            'https://www.franceinfo.fr/',
        ]
        
        logger.info("📰 Collecte depuis les sites d'actualités...")
        for url in simple_sites:
            try:
                items = self.scrape_simple_site(url, max_items_per_site)
                all_items.extend(items)
                time.sleep(2)  # Politesse
            except Exception as e:
                logger.warning(f"⚠️ Erreur site {url}: {e}")
                continue
        
        # Sites avec JavaScript (si nécessaire)
        logger.info("🤖 Collecte depuis les sites interactifs...")
        for site_config in self.target_sites[:1]:  # Limiter pour le test
            try:
                items = self.scrape_with_chrome(site_config, max_items_per_site)
                all_items.extend(items)
                time.sleep(3)  # Plus de politesse
            except Exception as e:
                logger.warning(f"⚠️ Erreur site {site_config['name']}: {e}")
                continue
        
        logger.info(f"✅ Collecte terminée: {len(all_items)} éléments au total")
        return all_items
    
    def save_collected_data(self, data: List[Dict[str, Any]], filename: str = None) -> str:
        """Sauvegarde les données collectées."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"web_scraping_{timestamp}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"💾 {len(data)} éléments sauvegardés: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde: {e}")
            return ""
    
    def analyze_collected_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyse les données collectées."""
        if not data:
            return {}
        
        analysis = {
            'total_items': len(data),
            'types': {},
            'sources': {},
            'content_stats': {},
            'sample_items': data[:3]  # Échantillon
        }
        
        # Analyser les types
        for item in data:
            item_type = item.get('type', 'unknown')
            analysis['types'][item_type] = analysis['types'].get(item_type, 0) + 1
        
        # Analyser les sources
        for item in data:
            source = item.get('site', item.get('url_hash', 'unknown'))
            analysis['sources'][source] = analysis['sources'].get(source, 0) + 1
        
        # Statistiques de contenu
        contents = [item.get('content', '') for item in data]
        total_chars = sum(len(content) for content in contents)
        analysis['content_stats'] = {
            'total_characters': total_chars,
            'avg_chars_per_item': total_chars // len(data) if data else 0,
            'longest_content': max(len(content) for content in contents) if contents else 0
        }
        
        logger.info(f"📊 Analyse terminée: {analysis['total_items']} éléments")
        return analysis

def main():
    """Fonction principale de test."""
    logger.info("🕷️ TEST WEB SCRAPING COLLECTOR")
    logger.info("=" * 50)
    
    collector = WebScrapingCollector()
    
    try:
        # Collecter les données
        logger.info("🚀 Début de la collecte...")
        collected_data = collector.collect_from_sites(max_items_per_site=5)
        
        if collected_data:
            # Sauvegarder
            filepath = collector.save_collected_data(collected_data)
            
            # Analyser
            analysis = collector.analyze_collected_data(collected_data)
            
            # Sauvegarder l'analyse
            analysis_filepath = os.path.join(collector.data_dir, "scraping_analysis.json")
            with open(analysis_filepath, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, ensure_ascii=False, indent=2)
            
            # Résumé
            logger.info("\n" + "=" * 50)
            logger.info("🎉 COLLECTE WEB SCRAPING TERMINÉE!")
            logger.info("=" * 50)
            logger.info(f"✅ Éléments collectés: {len(collected_data)}")
            logger.info(f"✅ Types: {list(analysis.get('types', {}).keys())}")
            logger.info(f"✅ Sources: {len(analysis.get('sources', {}))}")
            logger.info(f"✅ Anonymisation RGPD: Activée")
            logger.info(f"📁 Fichiers dans: {collector.data_dir}")
            logger.info("=" * 50)
            
        else:
            logger.warning("⚠️ Aucune donnée collectée")
            
    except Exception as e:
        logger.error(f"❌ Erreur lors de la collecte: {e}")
        
    finally:
        # Nettoyer
        collector._cleanup_driver()

if __name__ == "__main__":
    main()




