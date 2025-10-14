#!/usr/bin/env python3
"""
Scraper Franceinfo (simple, indépendant, low-code)

Usage exemples:
  - python scripts/scrape_franceinfo.py --url https://www.francetvinfo.fr/... --pays FR --domaine politique
  - python scripts/scrape_franceinfo.py --urls urls.txt --pays FR --domaine politique
  - python scripts/scrape_franceinfo.py --discover 3 --pays FR --domaine politique   # auto-découverte depuis la page d'accueil

Sortie:
  - JSON normalisé dans data/raw/scraped/franceinfo_YYYYmmdd_HHMMSS.json

Champs normalisés:
  - url, source, pays, domaine, titre, resume, texte, publication_date, auteur, langue, collected_at
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup


def normalize_text(text: str) -> str:
    if not text:
        return ""
    return " ".join(text.split()).strip()


def fix_mojibake(text: str) -> str:
    if not text:
        return text
    if "Ã" in text or "Â" in text:
        try:
            return text.encode("latin-1", errors="ignore").decode("utf-8", errors="ignore")
        except Exception:
            return text
    return text


def fetch_html(url: str, timeout: int = 15) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.content.decode(resp.apparent_encoding or resp.encoding or "utf-8", errors="replace")


def parse_franceinfo_article(html: str, url: str) -> dict[str, Any]:
    soup = BeautifulSoup(html, "lxml")

    # Titre
    title = None
    for sel in [
        "h1.c-page-article-title",
        "h1",
        "title",
    ]:
        node = soup.select_one(sel)
        if node and node.get_text(strip=True):
            title = node.get_text(strip=True)
            break

    # Résumé (chapeau)
    resume = None
    for sel in [
        "p.c-chapo",
        "div.c-article-intro p",
        "meta[name='description']",
    ]:
        node = soup.select_one(sel)
        if node:
            if node.name == "meta":
                resume = node.get("content")
            else:
                resume = node.get_text(strip=True)
            if resume:
                break

    # Corps article
    paragraphs: list[str] = []
    for sel in [
        "div.c-article-text p",
        "article p",
        "div p",
    ]:
        nodes = soup.select(sel)
        if nodes:
            for p in nodes:
                txt = p.get_text(" ", strip=True)
                if txt and len(txt) > 30:
                    paragraphs.append(txt)
            if paragraphs:
                break

    texte_raw = " ".join(paragraphs)
    texte = normalize_text(fix_mojibake(texte_raw))

    # Auteur
    auteur = None
    for sel in [
        "span.c-signature__author",
        "span.c-author",
        "meta[name='author']",
    ]:
        node = soup.select_one(sel)
        if node:
            auteur_val = node.get("content") if node.name == "meta" else node.get_text(strip=True)
            auteur = fix_mojibake(auteur_val)
            if auteur:
                break

    # Date publication
    publication_date = None
    for sel in [
        "time[datetime]",
        "meta[property='article:published_time']",
        "meta[name='date']",
    ]:
        node = soup.select_one(sel)
        if node:
            publication_date = node.get("datetime") or node.get("content")
            if publication_date:
                break

    return {
        "url": url,
        "source": "franceinfo",
        "titre": fix_mojibake(title or ""),
        "resume": fix_mojibake(resume or ""),
        "texte": texte or "",
        "publication_date": publication_date or "",
        "auteur": auteur or "",
        "langue": "fr",
    }


def load_urls_from_file(path: Path) -> list[str]:
    urls: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            urls.append(line)
    return urls


def main() -> int:
    parser = argparse.ArgumentParser(description="Scraper Franceinfo")
    parser.add_argument("--url", type=str, help="URL d'article à scraper")
    parser.add_argument("--urls", type=str, help="Fichier contenant une liste d'URLs")
    parser.add_argument("--pays", type=str, default="FR", help="Code pays (ISO-3166-1 alpha-2)")
    parser.add_argument("--domaine", type=str, default="inconnu", help="Domaine (politique, economie, sport, culture, international, tech)")
    parser.add_argument("--output-dir", type=str, default="data/raw/scraped", help="Dossier de sortie")
    parser.add_argument("--discover", type=int, default=0, help="Nombre d'articles à auto-découvrir depuis la page d'accueil Franceinfo")

    args = parser.parse_args()

    urls: list[str] = []
    if args.url:
        urls.append(args.url)
    if args.urls:
        urls.extend(load_urls_from_file(Path(args.urls)))

    if not urls and args.discover > 0:
        try:
            home_html = fetch_html("https://www.francetvinfo.fr/")
            soup = BeautifulSoup(home_html, "lxml")
            found: list[str] = []
            for a in soup.select("a"):
                href = a.get("href")
                if not href:
                    continue
                if href.startswith("/"):
                    href = "https://www.francetvinfo.fr" + href
                if href.startswith("https://www.francetvinfo.fr/") and href not in found:
                    if any(seg.isdigit() for seg in href.split("-")) or href.endswith(".html"):
                        found.append(href)
                if len(found) >= args.discover:
                    break
            urls = found
            if not urls:
                print("⚠️ Auto-découverte n'a trouvé aucun article Franceinfo.")
        except Exception as e:
            print(f"⚠️ Auto-découverte échouée: {e}")

    if not urls:
        print("⚠️ Fournissez --url, --urls ou utilisez --discover N pour auto-découvrir des articles")
        return 2

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    collected: list[dict[str, Any]] = []
    for u in urls:
        try:
            html = fetch_html(u)
            item = parse_franceinfo_article(html, u)
            item["pays"] = args.pays or "FR"
            item["domaine"] = args.domaine or "inconnu"
            item["collected_at"] = datetime.utcnow().isoformat()
            collected.append(item)
        except Exception as e:
            print(f"❌ Erreur sur {u}: {e}")

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"franceinfo_{ts}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(collected, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(collected)} articles sauvegardés → {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())


