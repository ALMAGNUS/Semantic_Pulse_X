#!/usr/bin/env python3
"""
Script de démonstration traitement - Semantic Pulse X
Démonstration détaillée du traitement des données avec prints explicites
"""

import sys
import os
from pathlib import Path
import pandas as pd
import json

# Ajouter le répertoire racine au PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.backend.core.anonymization import anonymizer

def demo_traitement_detaille():
    """Démonstration détaillée du traitement des données"""
    print("🔍 DÉMONSTRATION TRAITEMENT DÉTAILLÉ - Semantic Pulse X")
    print("=" * 70)
    
    # Créer des données de test
    print("\n📊 Étape 1: Création des données de test")
    print("-" * 50)
    
    test_data = [
        {
            "id": 1,
            "texte": "J'adore cette émission, c'est génial !",
            "auteur": "user123",
            "date": "2024-01-15 20:30:00",
            "source": "twitter"
        },
        {
            "id": 2,
            "texte": "Cette émission est nulle, je déteste !",
            "auteur": "user456",
            "date": "2024-01-15 20:35:00",
            "source": "youtube"
        },
        {
            "id": 3,
            "texte": "Super épisode, j'ai hâte de voir la suite",
            "auteur": "user789",
            "date": "2024-01-15 20:40:00",
            "source": "instagram"
        }
    ]
    
    print(f"✅ {len(test_data)} données de test créées")
    for i, data in enumerate(test_data, 1):
        print(f"   {i}. {data['texte'][:50]}... (auteur: {data['auteur']})")
    
    # Nettoyage
    print("\n🧹 Étape 2: Nettoyage des données")
    print("-" * 50)
    
    cleaned_data = []
    for data in test_data:
        print(f"🔄 Nettoyage de: '{data['texte']}'")
        
        # Supprimer les caractères spéciaux
        texte_clean = data['texte'].replace('!', '').replace('?', '').strip()
        print(f"   → Suppression caractères spéciaux: '{texte_clean}'")
        
        # Normaliser la casse
        texte_normalise = texte_clean.lower()
        print(f"   → Normalisation casse: '{texte_normalise}'")
        
        data_clean = data.copy()
        data_clean['texte'] = texte_normalise
        cleaned_data.append(data_clean)
        print(f"   ✅ Donnée nettoyée")
    
    print(f"✅ {len(cleaned_data)} données nettoyées")
    
    # Dédoublonnage
    print("\n🔄 Étape 3: Dédoublonnage")
    print("-" * 50)
    
    # Simuler un doublon
    cleaned_data.append(cleaned_data[0].copy())
    print(f"📊 Avant dédoublonnage: {len(cleaned_data)} données")
    
    # Dédoublonnage par texte
    seen_texts = set()
    deduplicated_data = []
    for data in cleaned_data:
        if data['texte'] not in seen_texts:
            seen_texts.add(data['texte'])
            deduplicated_data.append(data)
            print(f"   ✅ Gardé: '{data['texte']}'")
        else:
            print(f"   ❌ Supprimé (doublon): '{data['texte']}'")
    
    print(f"✅ Après dédoublonnage: {len(deduplicated_data)} données")
    
    # Anonymisation RGPD
    print("\n🔒 Étape 4: Anonymisation RGPD")
    print("-" * 50)
    
    anonymized_data = []
    for data in deduplicated_data:
        print(f"🔄 Anonymisation de: auteur='{data['auteur']}'")
        
        # Anonymiser l'auteur
        auteur_anonyme = anonymizer.anonymize_user_id(data['auteur'])
        print(f"   → Auteur anonymisé: '{auteur_anonyme}'")
        
        # Pseudonymiser le texte (hashage)
        texte_hash = anonymizer.hash_text(data['texte'])
        print(f"   → Texte hashé: '{texte_hash[:20]}...'")
        
        data_anonyme = data.copy()
        data_anonyme['auteur'] = auteur_anonyme
        data_anonyme['texte_hash'] = texte_hash
        anonymized_data.append(data_anonyme)
        print(f"   ✅ Donnée anonymisée")
    
    print(f"✅ {len(anonymized_data)} données anonymisées")
    
    # Homogénéisation
    print("\n📏 Étape 5: Homogénéisation des formats")
    print("-" * 50)
    
    homogenized_data = []
    for data in anonymized_data:
        print(f"🔄 Homogénéisation de la donnée {data['id']}")
        
        # Standardiser le format de date
        from datetime import datetime
        date_obj = datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
        date_iso = date_obj.isoformat()
        print(f"   → Date ISO: '{date_iso}'")
        
        # Ajouter des champs standardisés
        data_homogene = {
            'id': data['id'],
            'contenu': data['texte'],
            'contenu_hash': data['texte_hash'],
            'utilisateur_anonyme': data['auteur'],
            'timestamp': date_iso,
            'source_type': data['source'],
            'longueur': len(data['texte']),
            'mots': len(data['texte'].split())
        }
        
        homogenized_data.append(data_homogene)
        print(f"   ✅ Donnée homogénéisée: {data_homogene['mots']} mots")
    
    print(f"✅ {len(homogenized_data)} données homogénéisées")
    
    # Agrégation multi-sources
    print("\n🔗 Étape 6: Agrégation multi-sources")
    print("-" * 50)
    
    # Grouper par source
    sources = {}
    for data in homogenized_data:
        source = data['source_type']
        if source not in sources:
            sources[source] = []
        sources[source].append(data)
    
    print("📊 Répartition par source:")
    for source, data_list in sources.items():
        print(f"   - {source}: {len(data_list)} données")
    
    # Statistiques globales
    total_mots = sum(data['mots'] for data in homogenized_data)
    longueur_moyenne = sum(data['longueur'] for data in homogenized_data) / len(homogenized_data)
    
    print(f"\n📈 Statistiques globales:")
    print(f"   - Total données: {len(homogenized_data)}")
    print(f"   - Total mots: {total_mots}")
    print(f"   - Longueur moyenne: {longueur_moyenne:.1f} caractères")
    
    # Sauvegarde
    print("\n💾 Étape 7: Sauvegarde des données traitées")
    print("-" * 50)
    
    output_file = project_root / "data" / "processed" / "donnees_traitees.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(homogenized_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Données sauvegardées: {output_file}")
    print(f"   Taille: {output_file.stat().st_size} octets")
    
    print("\n🎉 DÉMONSTRATION TERMINÉE !")
    print("=" * 70)
    print("✅ Toutes les étapes de traitement ont été démontrées:")
    print("   1. Création des données de test")
    print("   2. Nettoyage (caractères spéciaux, casse)")
    print("   3. Dédoublonnage (suppression des doublons)")
    print("   4. Anonymisation RGPD (hachage, pseudonymisation)")
    print("   5. Homogénéisation (formats standardisés)")
    print("   6. Agrégation multi-sources (groupement)")
    print("   7. Sauvegarde (fichier JSON)")

if __name__ == "__main__":
    demo_traitement_detaille()
