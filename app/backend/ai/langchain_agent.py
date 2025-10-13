"""
Agent LangChain - Semantic Pulse X
Moteur IA central GRATUIT pour analyse et génération
"""

from typing import List, Dict, Any, Optional
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import json

from app.backend.core.config import settings
from app.backend.ai.ollama_client import ollama_client


class SemanticPulseAgent:
    """Agent LangChain GRATUIT pour Semantic Pulse X"""
    
    def __init__(self):
        self.llm = None
        self.memory = ConversationBufferMemory()
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialise le modèle LangChain GRATUIT"""
        try:
            # Utiliser Ollama (GRATUIT) en priorité
            if ollama_client.is_available():
                self.llm = ollama_client.get_llm()
                print("✅ Agent LangChain initialisé avec Ollama (GRATUIT)")
            else:
                # Fallback vers un modèle local HuggingFace (GRATUIT)
                self._initialize_fallback()
        except Exception as e:
            print(f"❌ Erreur initialisation LangChain: {e}")
            # Fallback vers un modèle local
            self._initialize_fallback()
    
    def _initialize_fallback(self):
        """Initialise un modèle de fallback GRATUIT"""
        try:
            from langchain_community.llms import HuggingFacePipeline
            from transformers import pipeline
            
            # Modèle local simple GRATUIT
            local_pipeline = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-medium",  # GRATUIT
                max_length=512,
                temperature=0.7
            )
            
            self.llm = HuggingFacePipeline(pipeline=local_pipeline)
            print("✅ Modèle local chargé en fallback (GRATUIT)")
        except Exception as e:
            print(f"❌ Erreur fallback: {e}")
            # Dernier recours : modèle très simple
            self._initialize_simple_fallback()
    
    def _initialize_simple_fallback(self):
        """Dernier recours : modèle très simple"""
        class SimpleLLM:
            def __call__(self, text):
                return f"Analyse: {text[:100]}... (Modèle simple activé)"
        
        self.llm = SimpleLLM()
        print("✅ Modèle simple activé (dernier recours)")
    
    def analyze_emotion_trends(self, emotion_data: List[Dict[str, Any]]) -> str:
        """Analyse les tendances émotionnelles"""
        # Utiliser Ollama en priorité
        if ollama_client.is_available():
            return ollama_client.analyze_emotion_trends(emotion_data)
        
        # Fallback vers analyse simple
        if not emotion_data:
            return "Aucune donnée émotionnelle à analyser"
        
        # Analyse basique des tendances
        emotions = [item.get('emotion', 'unknown') for item in emotion_data]
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Trouver l'émotion dominante
        dominant_emotion = max(emotion_counts, key=emotion_counts.get)
        
        return f"Analyse des tendances émotionnelles:\n- Émotion dominante: {dominant_emotion}\n- Répartition: {emotion_counts}"
    
    def generate_insights(self, data: Dict[str, Any]) -> str:
        """Génère des insights à partir des données"""
        try:
            if self.llm and hasattr(self.llm, '__call__'):
                prompt = f"Analysez ces données et générez des insights: {json.dumps(data, ensure_ascii=False)}"
                response = self.llm(prompt)
                return response
            else:
                return f"Insights générés: {len(data)} éléments analysés"
        except Exception as e:
            return f"Erreur génération insights: {e}"
    
    def predict_emotional_shift(self, historical_data: List[Dict[str, Any]]) -> str:
        """Prédit les changements émotionnels"""
        if not historical_data:
            return "Pas de données historiques pour la prédiction"
        
        # Analyse simple des tendances
        recent_emotions = historical_data[-10:] if len(historical_data) >= 10 else historical_data
        emotions = [item.get('emotion', 'neutral') for item in recent_emotions]
        
        # Calculer la tendance
        positive_emotions = ['joie', 'surprise', 'anticipation']
        negative_emotions = ['tristesse', 'colère', 'peur', 'dégoût']
        
        positive_count = sum(1 for e in emotions if e in positive_emotions)
        negative_count = sum(1 for e in emotions if e in negative_emotions)
        
        if positive_count > negative_count:
            trend = "Tendance positive détectée"
        elif negative_count > positive_count:
            trend = "Tendance négative détectée"
        else:
            trend = "Tendance neutre"
        
        return f"Prédiction émotionnelle: {trend} (Positif: {positive_count}, Négatif: {negative_count})"
    
    def get_conversation_summary(self) -> str:
        """Récupère un résumé de la conversation"""
        try:
            if self.memory and hasattr(self.memory, 'chat_memory'):
                messages = self.memory.chat_memory.messages
                if messages:
                    return f"Conversation en cours: {len(messages)} messages"
            return "Aucune conversation en cours"
        except Exception as e:
            return f"Erreur résumé conversation: {e}"


# Instance globale
semantic_agent = SemanticPulseAgent()