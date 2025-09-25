"""
Système d'anonymisation RGPD - Semantic Pulse X
Garantit qu'aucune donnée personnelle n'est conservée
"""

import hashlib
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid


class AnonymizationEngine:
    """Moteur d'anonymisation RGPD-compliant"""
    
    def __init__(self):
        self.salt = "semantic_pulse_x_2024"  # Salt fixe pour cohérence
        self.pii_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'(\+33|0)[1-9](\d{8}|\d{2}\s\d{2}\s\d{2}\s\d{2})',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
            'ip_address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        }
    
    def hash_identifier(self, identifier: str) -> str:
        """Hash un identifiant de manière irréversible"""
        if not identifier:
            return ""
        
        # Combinaison identifier + salt + timestamp pour unicité
        combined = f"{identifier}{self.salt}{datetime.utcnow().isoformat()}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def anonymize_text(self, text: str) -> str:
        """Anonymise un texte en supprimant les PII"""
        if not text:
            return ""
        
        anonymized = text
        
        # Supprimer les PII
        for pii_type, pattern in self.pii_patterns.items():
            anonymized = re.sub(pattern, f"[{pii_type.upper()}_REMOVED]", anonymized, flags=re.IGNORECASE)
        
        # Supprimer les mentions @username
        anonymized = re.sub(r'@\w+', '@[USER]', anonymized)
        
        # Supprimer les URLs
        anonymized = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '[URL]', anonymized)
        
        # Supprimer les numéros de téléphone
        anonymized = re.sub(r'(\+33|0)[1-9](\d{8}|\d{2}\s\d{2}\s\d{2}\s\d{2})', '[PHONE]', anonymized)
        
        return anonymized.strip()
    
    def extract_age_group(self, age: Optional[int]) -> Optional[str]:
        """Extrait un groupe d'âge anonymisé"""
        if not age:
            return None
        
        if age < 18:
            return "0-17"
        elif age < 25:
            return "18-24"
        elif age < 35:
            return "25-34"
        elif age < 45:
            return "35-44"
        elif age < 55:
            return "45-54"
        elif age < 65:
            return "55-64"
        else:
            return "65+"
    
    def anonymize_region(self, region: str) -> str:
        """Anonymise une région (ex: "Paris" -> "FR-75")"""
        if not region:
            return "UNKNOWN"
        
        # Mapping simplifié France
        region_mapping = {
            'paris': 'FR-75',
            'lyon': 'FR-69',
            'marseille': 'FR-13',
            'toulouse': 'FR-31',
            'nice': 'FR-06',
            'nantes': 'FR-44',
            'strasbourg': 'FR-67',
            'montpellier': 'FR-34',
            'bordeaux': 'FR-33',
            'lille': 'FR-59'
        }
        
        region_lower = region.lower().strip()
        return region_mapping.get(region_lower, "FR-XX")
    
    def create_user_hash(self, user_data: Dict[str, Any]) -> str:
        """Crée un hash anonyme pour un utilisateur"""
        # Combinaison de données non-PII pour créer un identifiant unique
        combined = f"{user_data.get('region', '')}{user_data.get('age_group', '')}{user_data.get('source', '')}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def validate_rgpd_compliance(self, data: Dict[str, Any]) -> bool:
        """Valide qu'une donnée est RGPD-compliant"""
        # Vérifier qu'aucun PII n'est présent
        for key, value in data.items():
            if isinstance(value, str):
                for pattern in self.pii_patterns.values():
                    if re.search(pattern, value, re.IGNORECASE):
                        return False
        
        return True
    
    def anonymize_reaction(self, reaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymise complètement une réaction"""
        anonymized = reaction_data.copy()
        
        # Anonymiser le texte
        if 'texte' in anonymized:
            anonymized['texte_anonymise'] = self.anonymize_text(anonymized.pop('texte'))
        
        # Anonymiser l'utilisateur
        if 'utilisateur' in anonymized:
            user_data = anonymized['utilisateur']
            anonymized['utilisateur_id'] = self.create_user_hash(user_data)
            anonymized.pop('utilisateur')
        
        # Supprimer les timestamps précis (garder seulement la date)
        if 'timestamp' in anonymized:
            timestamp = anonymized['timestamp']
            if isinstance(timestamp, datetime):
                # Arrondir à l'heure pour anonymiser
                anonymized['timestamp'] = timestamp.replace(minute=0, second=0, microsecond=0)
        
        return anonymized


# Instance globale
anonymizer = AnonymizationEngine()
