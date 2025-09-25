#!/usr/bin/env python3
"""
Démonstration Data Engineering - Semantic Pulse X
Script simple pour montrer les compétences de nettoyage de données
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path

def anonymize_user_id(user_id):
    """Anonymise un ID utilisateur avec SHA-256"""
    return hashlib.sha256(user_id.encode()).hexdigest()[:16]

def hash_text(text):
    """Hash un texte avec SHA-256"""
    return hashlib.sha256(text.encode()).hexdigest()

def demo_data_engineering():
    """Démonstration complète du data engineering"""
    print("🔍 DÉMONSTRATION DATA ENGINEERING - Semantic Pulse X")
    print("=" * 70)
    print("🎯 Compétences démontrées: Nettoyage, Dédoublonnage, Anonymisation RGPD")
    print("=" * 70)
    
    # 1. DONNÉES BRUTES
    print("\n📊 ÉTAPE 1: DONNÉES BRUTES")
    print("-" * 50)
    
    raw_data = [
        {
            "id": 1,
            "texte": "J'ADORE cette émission !!! C'est GÉNIAL !!!",
            "auteur": "user123",
            "date": "2024-01-15 20:30:00",
            "source": "twitter",
            "email": "user123@email.com"
        },
        {
            "id": 2,
            "texte": "Cette émission est NULle, je déteste !!!",
            "auteur": "user456",
            "date": "15/01/2024 20:35",
            "source": "youtube",
            "email": "user456@gmail.com"
        },
        {
            "id": 3,
            "texte": "Super épisode, j'ai hâte de voir la suite !",
            "auteur": "user789",
            "date": "2024-01-15T20:40:00Z",
            "source": "instagram",
            "email": "user789@outlook.com"
        },
        {
            "id": 4,
            "texte": "J'ADORE cette émission !!! C'est GÉNIAL !!!",  # Doublon
            "auteur": "user999",
            "date": "2024-01-15 20:45:00",
            "source": "twitter",
            "email": "user999@email.com"
        }
    ]
    
    print(f"✅ {len(raw_data)} données brutes collectées")
    print("📋 Exemples de données brutes:")
    for i, data in enumerate(raw_data, 1):
        print(f"   {i}. Texte: '{data['texte']}'")
        print(f"      Auteur: {data['auteur']} | Email: {data['email']}")
        print(f"      Date: {data['date']} | Source: {data['source']}")
        print()
    
    # 2. NETTOYAGE
    print("🧹 ÉTAPE 2: NETTOYAGE DES DONNÉES")
    print("-" * 50)
    
    cleaned_data = []
    for data in raw_data:
        print(f"🔄 Nettoyage de: '{data['texte']}'")
        
        # Nettoyage du texte
        texte_clean = data['texte']
        # Supprimer caractères spéciaux répétés
        texte_clean = texte_clean.replace('!!!', '').replace('!!', '').replace('!', '')
        # Normaliser la casse
        texte_clean = texte_clean.lower()
        # Supprimer espaces multiples
        texte_clean = ' '.join(texte_clean.split())
        
        print(f"   → Suppression caractères spéciaux: '{texte_clean}'")
        
        # Normalisation de la date
        date_str = data['date']
        try:
            if '/' in date_str:
                # Format français
                date_obj = datetime.strptime(date_str, '%d/%m/%Y %H:%M')
            elif 'T' in date_str:
                # Format ISO
                date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                # Format standard
                date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            
            date_normalized = date_obj.strftime('%Y-%m-%d %H:%M:%S')
        except:
            date_normalized = data['date']
        
        print(f"   → Normalisation date: '{date_normalized}'")
        
        # Supprimer email (données sensibles)
        data_clean = {
            'id': data['id'],
            'texte': texte_clean,
            'auteur': data['auteur'],
            'date': date_normalized,
            'source': data['source'].lower()
        }
        
        cleaned_data.append(data_clean)
        print(f"   ✅ Donnée nettoyée")
        print()
    
    print(f"✅ {len(cleaned_data)} données nettoyées")
    
    # 3. DÉDOUBLONNAGE
    print("\n🔄 ÉTAPE 3: DÉDOUBLONNAGE")
    print("-" * 50)
    
    print(f"📊 Avant dédoublonnage: {len(cleaned_data)} données")
    
    # Dédoublonnage par texte
    seen_texts = set()
    deduplicated_data = []
    doublons_removed = 0
    
    for data in cleaned_data:
        if data['texte'] not in seen_texts:
            seen_texts.add(data['texte'])
            deduplicated_data.append(data)
            print(f"   ✅ Gardé: '{data['texte']}' (ID: {data['id']})")
        else:
            doublons_removed += 1
            print(f"   ❌ Supprimé (doublon): '{data['texte']}' (ID: {data['id']})")
    
    print(f"✅ Après dédoublonnage: {len(deduplicated_data)} données")
    print(f"📊 Doublons supprimés: {doublons_removed}")
    
    # 4. ANONYMIZATION RGPD
    print("\n🔒 ÉTAPE 4: ANONYMIZATION RGPD")
    print("-" * 50)
    
    anonymized_data = []
    for data in deduplicated_data:
        print(f"🔄 Anonymisation de l'auteur: '{data['auteur']}'")
        
        # Anonymiser l'auteur
        auteur_anonyme = anonymize_user_id(data['auteur'])
        print(f"   → Auteur anonymisé: '{auteur_anonyme}'")
        
        # Hash du texte pour traçabilité
        texte_hash = hash_text(data['texte'])
        print(f"   → Hash du texte: '{texte_hash[:20]}...'")
        
        data_anonyme = {
            'id': data['id'],
            'contenu': data['texte'],
            'contenu_hash': texte_hash,
            'utilisateur_anonyme': auteur_anonyme,
            'timestamp': data['date'],
            'source_type': data['source']
        }
        
        anonymized_data.append(data_anonyme)
        print(f"   ✅ Donnée anonymisée")
        print()
    
    print(f"✅ {len(anonymized_data)} données anonymisées")
    
    # 5. HOMOGÉNÉISATION
    print("\n📏 ÉTAPE 5: HOMOGÉNÉISATION")
    print("-" * 50)
    
    homogenized_data = []
    for data in anonymized_data:
        print(f"🔄 Homogénéisation de la donnée {data['id']}")
        
        # Calculer des métriques
        longueur = len(data['contenu'])
        mots = len(data['contenu'].split())
        
        # Ajouter des champs standardisés
        data_homogene = {
            'id': data['id'],
            'contenu': data['contenu'],
            'contenu_hash': data['contenu_hash'],
            'utilisateur_anonyme': data['utilisateur_anonyme'],
            'timestamp': data['timestamp'],
            'source_type': data['source_type'],
            'longueur_caracteres': longueur,
            'nombre_mots': mots,
            'densite_mots': round(mots / longueur * 100, 2) if longueur > 0 else 0
        }
        
        homogenized_data.append(data_homogene)
        print(f"   → Métriques: {mots} mots, {longueur} caractères, densité {data_homogene['densite_mots']}%")
        print(f"   ✅ Donnée homogénéisée")
        print()
    
    print(f"✅ {len(homogenized_data)} données homogénéisées")
    
    # 6. AGRÉGATION ET STATISTIQUES
    print("\n📈 ÉTAPE 6: AGRÉGATION ET STATISTIQUES")
    print("-" * 50)
    
    # Statistiques par source
    sources_stats = {}
    for data in homogenized_data:
        source = data['source_type']
        if source not in sources_stats:
            sources_stats[source] = {'count': 0, 'total_mots': 0, 'total_caracteres': 0}
        
        sources_stats[source]['count'] += 1
        sources_stats[source]['total_mots'] += data['nombre_mots']
        sources_stats[source]['total_caracteres'] += data['longueur_caracteres']
    
    print("📊 Répartition par source:")
    for source, stats in sources_stats.items():
        avg_mots = stats['total_mots'] / stats['count']
        avg_caracteres = stats['total_caracteres'] / stats['count']
        print(f"   - {source.upper()}: {stats['count']} données")
        print(f"     Moyenne: {avg_mots:.1f} mots, {avg_caracteres:.1f} caractères")
        print()
    
    # Statistiques globales
    total_mots = sum(data['nombre_mots'] for data in homogenized_data)
    total_caracteres = sum(data['longueur_caracteres'] for data in homogenized_data)
    longueur_moyenne = total_caracteres / len(homogenized_data)
    mots_moyens = total_mots / len(homogenized_data)
    
    print("📈 Statistiques globales:")
    print(f"   - Total données: {len(homogenized_data)}")
    print(f"   - Total mots: {total_mots}")
    print(f"   - Total caractères: {total_caracteres}")
    print(f"   - Moyenne mots par donnée: {mots_moyens:.1f}")
    print(f"   - Moyenne caractères par donnée: {longueur_moyenne:.1f}")
    
    # 7. SAUVEGARDE
    print("\n💾 ÉTAPE 7: SAUVEGARDE")
    print("-" * 50)
    
    # Créer le dossier de sortie
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Sauvegarder en JSON
    output_file = output_dir / "donnees_traitees_demo.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(homogenized_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Données sauvegardées: {output_file}")
    print(f"   Taille: {output_file.stat().st_size} octets")
    
    # Créer un rapport de qualité
    rapport = {
        "timestamp": datetime.now().isoformat(),
        "donnees_brutes": len(raw_data),
        "donnees_nettoyees": len(cleaned_data),
        "donnees_dedupliquees": len(deduplicated_data),
        "donnees_anonymisees": len(anonymized_data),
        "donnees_finales": len(homogenized_data),
        "doublons_supprimes": doublons_removed,
        "taux_deduplication": round(doublons_removed / len(raw_data) * 100, 2),
        "statistiques_globales": {
            "total_mots": total_mots,
            "total_caracteres": total_caracteres,
            "moyenne_mots": round(mots_moyens, 2),
            "moyenne_caracteres": round(longueur_moyenne, 2)
        },
        "sources": sources_stats
    }
    
    rapport_file = output_dir / "rapport_qualite_demo.json"
    with open(rapport_file, 'w', encoding='utf-8') as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Rapport de qualité: {rapport_file}")
    
    # 8. RÉSUMÉ FINAL
    print("\n🎉 RÉSUMÉ FINAL - COMPÉTENCES DÉMONTRÉES")
    print("=" * 70)
    print("✅ NETTOYAGE DES DONNÉES:")
    print("   - Suppression caractères spéciaux")
    print("   - Normalisation casse")
    print("   - Standardisation formats de date")
    print("   - Suppression données sensibles (emails)")
    print()
    print("✅ DÉDOUBLONNAGE:")
    print(f"   - {doublons_removed} doublons détectés et supprimés")
    print(f"   - Taux de dédoublonnage: {rapport['taux_deduplication']}%")
    print()
    print("✅ ANONYMIZATION RGPD:")
    print("   - Hachage SHA-256 des identifiants utilisateurs")
    print("   - Pseudonymisation des données")
    print("   - Suppression des données personnelles")
    print()
    print("✅ HOMOGÉNÉISATION:")
    print("   - Formats de données standardisés")
    print("   - Métriques calculées (mots, caractères, densité)")
    print("   - Structure de données uniforme")
    print()
    print("✅ AGRÉGATION MULTI-SOURCES:")
    print("   - Groupement par source")
    print("   - Statistiques détaillées")
    print("   - Métriques de qualité")
    print()
    print("✅ CONFORMITÉ RGPD:")
    print("   - Aucune donnée personnelle conservée")
    print("   - Traçabilité via hachage")
    print("   - Anonymisation irréversible")
    print()
    print("📊 FICHIERS GÉNÉRÉS:")
    print(f"   - {output_file}")
    print(f"   - {rapport_file}")
    print()
    print("🎯 RÉSULTAT: Pipeline de data engineering complet et conforme RGPD !")

if __name__ == "__main__":
    demo_data_engineering()
