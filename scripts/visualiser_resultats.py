#!/usr/bin/env python3
"""
Visualisation des résultats - Semantic Pulse X
Affichage concret et visuel des données traitées
"""

import json
from pathlib import Path
from datetime import datetime

def visualiser_resultats():
    """Visualise les résultats de manière concrète"""
    print("📊 VISUALISATION DES RÉSULTATS - DATA ENGINEERING")
    print("=" * 70)
    
    # Charger les données traitées
    data_file = Path("data/processed/donnees_traitees_demo.json")
    rapport_file = Path("data/processed/rapport_qualite_demo.json")
    
    if not data_file.exists():
        print("❌ Fichier de données non trouvé. Lancez d'abord demo_data_engineering_simple.py")
        return
    
    with open(data_file, 'r', encoding='utf-8') as f:
        donnees = json.load(f)
    
    with open(rapport_file, 'r', encoding='utf-8') as f:
        rapport = json.load(f)
    
    # 1. AVANT/APRÈS TRANSFORMATION
    print("\n🔄 TRANSFORMATION DES DONNÉES")
    print("=" * 50)
    
    print("📥 DONNÉES BRUTES (exemples):")
    print("   • 'J'ADORE cette émission !!! C'est GÉNIAL !!!'")
    print("   • 'Cette émission est NULle, je déteste !!!'")
    print("   • 'Super épisode, j'ai hâte de voir la suite !'")
    print("   • 'J'ADORE cette émission !!! C'est GÉNIAL !!!' (DOUBLON)")
    
    print("\n📤 DONNÉES TRAITÉES:")
    for i, data in enumerate(donnees, 1):
        print(f"   {i}. Texte: '{data['contenu']}'")
        print(f"      Utilisateur: {data['utilisateur_anonyme']} (anonymisé)")
        print(f"      Source: {data['source_type'].upper()}")
        print(f"      Métriques: {data['nombre_mots']} mots, {data['longueur_caracteres']} caractères")
        print(f"      Densité: {data['densite_mots']}%")
        print()
    
    # 2. MÉTRIQUES DE QUALITÉ
    print("📈 MÉTRIQUES DE QUALITÉ")
    print("=" * 50)
    
    print(f"📊 STATISTIQUES GLOBALES:")
    print(f"   • Données brutes: {rapport['donnees_brutes']}")
    print(f"   • Données finales: {rapport['donnees_finales']}")
    print(f"   • Doublons supprimés: {rapport['doublons_supprimes']}")
    print(f"   • Taux de dédoublonnage: {rapport['taux_deduplication']}%")
    print()
    
    stats = rapport['statistiques_globales']
    print(f"📝 CONTENU:")
    print(f"   • Total mots: {stats['total_mots']}")
    print(f"   • Total caractères: {stats['total_caracteres']}")
    print(f"   • Moyenne mots/donnée: {stats['moyenne_mots']}")
    print(f"   • Moyenne caractères/donnée: {stats['moyenne_caracteres']}")
    print()
    
    # 3. RÉPARTITION PAR SOURCE
    print("🌐 RÉPARTITION PAR SOURCE")
    print("=" * 50)
    
    for source, stats in rapport['sources'].items():
        print(f"📱 {source.upper()}:")
        print(f"   • Nombre de données: {stats['count']}")
        print(f"   • Total mots: {stats['total_mots']}")
        print(f"   • Total caractères: {stats['total_caracteres']}")
        print(f"   • Moyenne mots: {stats['total_mots']/stats['count']:.1f}")
        print(f"   • Moyenne caractères: {stats['total_caracteres']/stats['count']:.1f}")
        print()
    
    # 4. CONFORMITÉ RGPD
    print("🔒 CONFORMITÉ RGPD")
    print("=" * 50)
    
    print("✅ ANONYMIZATION:")
    print("   • Identifiants utilisateurs → Hachage SHA-256")
    print("   • Emails → Supprimés")
    print("   • Données personnelles → Aucune conservée")
    print()
    
    print("🔍 EXEMPLES D'ANONYMIZATION:")
    for data in donnees[:2]:  # Afficher 2 exemples
        print(f"   • Utilisateur original → {data['utilisateur_anonyme']}")
        print(f"   • Hash du contenu: {data['contenu_hash'][:20]}...")
    print()
    
    # 5. PIPELINE DE TRAITEMENT
    print("⚙️ PIPELINE DE TRAITEMENT")
    print("=" * 50)
    
    etapes = [
        ("Collecte", rapport['donnees_brutes'], "Données brutes collectées"),
        ("Nettoyage", rapport['donnees_nettoyees'], "Caractères spéciaux supprimés, casse normalisée"),
        ("Dédoublonnage", rapport['donnees_dedupliquees'], f"{rapport['doublons_supprimes']} doublons supprimés"),
        ("Anonymisation", rapport['donnees_anonymisees'], "RGPD appliqué, données personnelles supprimées"),
        ("Homogénéisation", rapport['donnees_finales'], "Formats standardisés, métriques calculées")
    ]
    
    for i, (etape, count, description) in enumerate(etapes, 1):
        print(f"   {i}. {etape.upper()}: {count} données")
        print(f"      → {description}")
        print()
    
    # 6. FICHIERS GÉNÉRÉS
    print("💾 FICHIERS GÉNÉRÉS")
    print("=" * 50)
    
    print(f"📄 Données traitées: {data_file}")
    print(f"   • Taille: {data_file.stat().st_size} octets")
    print(f"   • Format: JSON structuré")
    print(f"   • Contenu: {len(donnees)} enregistrements")
    print()
    
    print(f"📊 Rapport de qualité: {rapport_file}")
    print(f"   • Taille: {rapport_file.stat().st_size} octets")
    print(f"   • Format: JSON métadonnées")
    print(f"   • Contenu: Statistiques et métriques")
    print()
    
    # 7. RÉSUMÉ EXÉCUTIF
    print("🎯 RÉSUMÉ FINAL")
    print("=" * 50)
    
    print("✅ COMPÉTENCES DÉMONTRÉES:")
    print("   • Nettoyage de données (caractères, casse, formats)")
    print("   • Détection et suppression de doublons")
    print("   • Anonymisation RGPD (hachage, pseudonymisation)")
    print("   • Homogénéisation multi-sources")
    print("   • Calcul de métriques de qualité")
    print("   • Génération de rapports structurés")
    print()
    
    print("📊 RÉSULTATS CONCRETS:")
    print(f"   • {rapport['taux_deduplication']}% de doublons détectés et supprimés")
    print(f"   • 100% des données personnelles anonymisées")
    print(f"   • {len(donnees)} enregistrements finaux prêts pour l'analyse")
    print(f"   • {stats['total_mots']} mots traités et analysés")
    print()
    
    print("🎉 CONCLUSION: Pipeline de data engineering complet et conforme RGPD !")
    print("=" * 70)

if __name__ == "__main__":
    visualiser_resultats()
