#!/usr/bin/env python3
"""
Scraper Franceinfo avec Selenium (selon exigences professeur)
- Web scraping robuste avec Selenium pour sites dynamiques
- Compatible avec l'architecture existante (5 sources + ETL)

Usage:
  python scripts/scrape_franceinfo_selenium.py --discover 5 --pays FR --domaine politique
"""

import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def setup_driver(headless: bool = True) -> webdriver.Chrome:
    """Configure le driver Chrome avec Selenium"""
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")

    # Utiliser undetected-chromedriver avec gestion des versions
    try:
        driver = uc.Chrome(options=options, version_main=None)
        driver.implicitly_wait(10)
        return driver
    except Exception as e:
        print(f"⚠️ Erreur undetected-chromedriver: {e}")
        # Fallback vers Selenium standard
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        return driver


def normalize_text(text: str) -> str:
    """Normalise le texte"""
    if not text:
        return ""
    return " ".join(text.split()).strip()


def scrape_franceinfo_article(driver: webdriver.Chrome, url: str) -> dict[str, Any]:
    """Scrape un article Franceinfo avec Selenium"""
    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Attendre le chargement du contenu
        time.sleep(2)

        # Titre
        title = ""
        try:
            title_element = driver.find_element(By.CSS_SELECTOR, "h1.c-page-article-title, h1")
            title = normalize_text(title_element.text)
        except NoSuchElementException:
            try:
                title_element = driver.find_element(By.TAG_NAME, "title")
                title = normalize_text(title_element.text)
            except NoSuchElementException:
                title = ""

        # Résumé
        resume = ""
        try:
            resume_element = driver.find_element(By.CSS_SELECTOR, "p.c-chapo, div.c-article-intro p")
            resume = normalize_text(resume_element.text)
        except NoSuchElementException:
            try:
                meta_desc = driver.find_element(By.CSS_SELECTOR, "meta[name='description']")
                resume = meta_desc.get_attribute("content") or ""
            except NoSuchElementException:
                resume = ""

        # Corps de l'article
        paragraphs = []
        try:
            # Essayer différents sélecteurs pour le contenu
            content_selectors = [
                "div.c-article-text p",
                "article p",
                "div[class*='article'] p",
                "main p"
            ]

            for selector in content_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        for p in elements:
                            text = normalize_text(p.text)
                            if text and len(text) > 30:
                                paragraphs.append(text)
                        if paragraphs:
                            break
                except NoSuchElementException:
                    continue
        except Exception:
            pass

        texte = " ".join(paragraphs)

        # Auteur
        auteur = ""
        try:
            author_element = driver.find_element(By.CSS_SELECTOR, "span.c-signature__author, span.c-author")
            auteur = normalize_text(author_element.text)
        except NoSuchElementException:
            try:
                meta_author = driver.find_element(By.CSS_SELECTOR, "meta[name='author']")
                auteur = meta_author.get_attribute("content") or ""
            except NoSuchElementException:
                auteur = ""

        # Date de publication
        publication_date = ""
        try:
            time_element = driver.find_element(By.CSS_SELECTOR, "time[datetime]")
            publication_date = time_element.get_attribute("datetime") or ""
        except NoSuchElementException:
            try:
                meta_date = driver.find_element(By.CSS_SELECTOR, "meta[property='article:published_time']")
                publication_date = meta_date.get_attribute("content") or ""
            except NoSuchElementException:
                publication_date = ""

        return {
            "url": url,
            "source": "franceinfo_selenium",
            "titre": title,
            "resume": resume,
            "texte": texte,
            "publication_date": publication_date,
            "auteur": auteur,
            "langue": "fr",
        }

    except TimeoutException:
        print(f"⚠️ Timeout pour {url}")
        return None
    except Exception as e:
        print(f"❌ Erreur scraping {url}: {e}")
        return None


def discover_franceinfo_articles(driver: webdriver.Chrome, max_articles: int = 5) -> list[str]:
    """Découvre des articles depuis la page d'accueil Franceinfo"""
    try:
        driver.get("https://www.francetvinfo.fr/")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Attendre le chargement des liens
        time.sleep(3)

        # Trouver les liens d'articles
        article_links = []
        try:
            # Sélecteurs pour les liens d'articles
            link_selectors = [
                "a[href*='/']",
                "a[href*='.html']",
                "a[href*='article']"
            ]

            for selector in link_selectors:
                try:
                    links = driver.find_elements(By.CSS_SELECTOR, selector)
                    for link in links:
                        href = link.get_attribute("href")
                        if href and "francetvinfo.fr" in href:
                            # Filtrer les liens d'articles
                            if any(keyword in href.lower() for keyword in ['article', 'news', 'politique', 'economie', 'sport']):
                                if href not in article_links:
                                    article_links.append(href)
                                    if len(article_links) >= max_articles:
                                        break
                    if len(article_links) >= max_articles:
                        break
                except Exception:
                    continue

        except Exception as e:
            print(f"⚠️ Erreur découverte liens: {e}")

        return article_links[:max_articles]

    except Exception as e:
        print(f"❌ Erreur découverte articles: {e}")
        return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Scraper Franceinfo avec Selenium")
    parser.add_argument("--url", type=str, help="URL d'article à scraper")
    parser.add_argument("--urls", type=str, help="Fichier contenant une liste d'URLs")
    parser.add_argument("--pays", type=str, default="FR", help="Code pays")
    parser.add_argument("--domaine", type=str, default="inconnu", help="Domaine")
    parser.add_argument("--output-dir", type=str, default="data/raw/scraped", help="Dossier de sortie")
    parser.add_argument("--discover", type=int, default=0, help="Nombre d'articles à auto-découvrir")
    parser.add_argument("--headless", action="store_true", default=True, help="Mode headless")

    args = parser.parse_args()

    # Initialiser le driver Selenium
    driver = None
    try:
        driver = setup_driver(headless=args.headless)
        print("✅ Driver Selenium initialisé")

        urls: list[str] = []

        # Collecter les URLs
        if args.url:
            urls.append(args.url)

        if args.urls:
            urls_file = Path(args.urls)
            if urls_file.exists():
                urls.extend([line.strip() for line in urls_file.read_text(encoding="utf-8").splitlines()
                           if line.strip() and not line.startswith("#")])

        if args.discover > 0:
            discovered_urls = discover_franceinfo_articles(driver, args.discover)
            urls.extend(discovered_urls)
            print(f"🔍 {len(discovered_urls)} articles découverts")

        if not urls:
            print("⚠️ Aucune URL à scraper")
            return 1

        # Scraper les articles
        collected: list[dict[str, Any]] = []
        for i, url in enumerate(urls, 1):
            print(f"📄 Scraping {i}/{len(urls)}: {url}")

            article_data = scrape_franceinfo_article(driver, url)
            if article_data:
                article_data["pays"] = args.pays
                article_data["domaine"] = args.domaine
                article_data["collected_at"] = datetime.utcnow().isoformat()
                collected.append(article_data)
                print(f"✅ Article scrapé: {article_data['titre'][:50]}...")
            else:
                print(f"❌ Échec scraping: {url}")

            # Pause entre les requêtes
            time.sleep(1)

        # Sauvegarder les résultats
        if collected:
            out_dir = Path(args.output_dir)
            out_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            output_file = out_dir / f"franceinfo_selenium_{timestamp}.json"

            with output_file.open("w", encoding="utf-8") as f:
                json.dump(collected, f, ensure_ascii=False, indent=2)

            print(f"\n✅ {len(collected)} articles sauvegardés → {output_file}")

            # Statistiques
            total_text_length = sum(len(article.get("texte", "")) for article in collected)
            avg_text_length = total_text_length / len(collected) if collected else 0

            print("📊 Statistiques:")
            print(f"   • Articles: {len(collected)}")
            print(f"   • Longueur moyenne texte: {avg_text_length:.0f} caractères")
            print(f"   • Sources: {len({article.get('source', '') for article in collected})}")

            return 0
        else:
            print("❌ Aucun article collecté")
            return 1

    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        return 1
    finally:
        if driver:
            driver.quit()
            print("🔚 Driver Selenium fermé")


if __name__ == "__main__":
    exit(main())
