"""
Module d'embeddings - Semantic Pulse X
Vectorisation sémantique optimisée
"""

from functools import lru_cache
from typing import Any

import numpy as np
import torch
from sentence_transformers import SentenceTransformer

from app.backend.core.config import settings


class EmbeddingEngine:
    """Moteur d'embeddings optimisé"""

    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.embedding_model
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._load_model()

    def _load_model(self):
        """Charge le modèle d'embeddings"""
        try:
            self.model = SentenceTransformer(self.model_name, device=self.device)
            print(f"✅ Modèle d'embeddings chargé: {self.model_name}")
        except Exception as e:
            print(f"❌ Erreur chargement modèle: {e}")
            # Fallback vers un modèle plus simple
            self.model = SentenceTransformer('all-MiniLM-L6-v2', device=self.device)

    @lru_cache(maxsize=1000)
    def encode_text(self, text: str) -> np.ndarray:
        """Encode un texte en vecteur"""
        if not text or not text.strip():
            return np.zeros(384)  # Dimension par défaut

        try:
            # Nettoyer le texte
            cleaned_text = self._clean_text(text)
            if not cleaned_text:
                return np.zeros(384)

            # Encoder
            embedding = self.model.encode(cleaned_text, convert_to_numpy=True)
            return embedding
        except Exception as e:
            print(f"❌ Erreur encodage: {e}")
            return np.zeros(384)

    def encode_batch(self, texts: list[str]) -> np.ndarray:
        """Encode un batch de textes"""
        if not texts:
            return np.array([])

        # Nettoyer les textes
        cleaned_texts = [self._clean_text(text) for text in texts]
        cleaned_texts = [text for text in cleaned_texts if text]

        if not cleaned_texts:
            return np.array([])

        try:
            embeddings = self.model.encode(cleaned_texts, convert_to_numpy=True)
            return embeddings
        except Exception as e:
            print(f"❌ Erreur encodage batch: {e}")
            return np.array([])

    def _clean_text(self, text: str) -> str:
        """Nettoie un texte pour l'encodage"""
        if not text:
            return ""

        # Supprimer les caractères spéciaux excessifs
        import re
        text = re.sub(r'[^\w\s.,!?]', ' ', text)
        text = re.sub(r'\s+', ' ', text)

        # Limiter la longueur
        max_length = settings.max_text_length
        if len(text) > max_length:
            text = text[:max_length]

        return text.strip()

    def compute_similarity(self, text1: str, text2: str) -> float:
        """Calcule la similarité cosinus entre deux textes"""
        emb1 = self.encode_text(text1)
        emb2 = self.encode_text(text2)

        # Similarité cosinus
        dot_product = np.dot(emb1, emb2)
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        similarity = dot_product / (norm1 * norm2)
        return float(similarity)

    def find_most_similar(self, query: str, candidates: list[str], top_k: int = 5) -> list[dict[str, Any]]:
        """Trouve les textes les plus similaires"""
        if not candidates:
            return []

        self.encode_text(query)
        candidate_embs = self.encode_batch(candidates)

        if len(candidate_embs) == 0:
            return []

        # Calculer les similarités
        similarities = []
        for i, _cand_emb in enumerate(candidate_embs):
            sim = self.compute_similarity(query, candidates[i])
            similarities.append({
                'text': candidates[i],
                'similarity': sim,
                'index': i
            })

        # Trier par similarité
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:top_k]

    def get_embedding_dimension(self) -> int:
        """Retourne la dimension des embeddings"""
        if self.model:
            return self.model.get_sentence_embedding_dimension()
        return 384  # Dimension par défaut


# Instance globale
embedding_engine = EmbeddingEngine()
