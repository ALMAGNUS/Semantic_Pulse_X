"""
Agent LangChain - Semantic Pulse X
Moteur IA central pour analyse et génération
"""

from typing import List, Dict, Any, Optional
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import json

from app.backend.core.config import settings
from app.backend.ai.ollama_client import ollama_client


class SemanticPulseAgent:
    """Agent LangChain pour Semantic Pulse X"""
    
    def __init__(self):
        self.llm = None
        self.memory = ConversationBufferMemory()
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialise le modèle LangChain"""
        try:
            # Utiliser un modèle local ou API
            self.llm = ChatOpenAI(
                model_name="gpt-3.5-turbo",
                temperature=0.7,
                max_tokens=1000
            )
            print("✅ Agent LangChain initialisé")
        except Exception as e:
            print(f"❌ Erreur initialisation LangChain: {e}")
            # Fallback vers un modèle local
            self._initialize_fallback()
    
    def _initialize_fallback(self):
        """Initialise un modèle de fallback"""
        try:
            from langchain.llms import HuggingFacePipeline
            from transformers import pipeline
            
            # Modèle local simple
            local_pipeline = pipeline(
                "text-generation",
                model="gpt2",
                max_length=200,
                do_sample=True
            )
            
            self.llm = HuggingFacePipeline(pipeline=local_pipeline)
            print("✅ Modèle local chargé en fallback")
        except Exception as e:
            print(f"❌ Erreur fallback: {e}")
            self.llm = None
    
    def analyze_emotion_trends(self, emotion_data: List[Dict[str, Any]]) -> str:
        """Analyse les tendances émotionnelles"""
        # Utiliser Ollama en priorité
        if ollama_client.is_available():
            return ollama_client.analyze_emotion_trends(emotion_data)
        
        if not self.llm:
            return "Agent non disponible"
        
        # Préparer les données
        emotion_summary = self._prepare_emotion_summary(emotion_data)
        
        prompt = f"""
        Analysez les tendances émotionnelles suivantes et fournissez un résumé concis :
        
        Données émotionnelles :
        {emotion_summary}
        
        Fournissez :
        1. Les émotions dominantes
        2. Les tendances temporelles
        3. Les insights clés
        4. Les recommandations
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            print(f"❌ Erreur analyse tendances: {e}")
            return "Erreur d'analyse"
    
    def generate_insights(self, data: Dict[str, Any]) -> str:
        """Génère des insights à partir des données"""
        # Utiliser Ollama en priorité
        if ollama_client.is_available():
            return ollama_client.generate_insights(data)
        
        if not self.llm:
            return "Agent non disponible"
        
        prompt = f"""
        Générez des insights pertinents à partir de ces données d'analyse émotionnelle :
        
        {json.dumps(data, indent=2, ensure_ascii=False)}
        
        Focus sur :
        - Les patterns émotionnels
        - Les sujets émergents
        - Les recommandations stratégiques
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            print(f"❌ Erreur génération insights: {e}")
            return "Erreur de génération"
    
    def answer_question(self, question: str, context: Dict[str, Any]) -> str:
        """Répond à une question avec contexte"""
        # Utiliser Ollama en priorité
        if ollama_client.is_available():
            return ollama_client.answer_question(question, context)
        
        if not self.llm:
            return "Agent non disponible"
        
        context_str = json.dumps(context, indent=2, ensure_ascii=False)
        
        prompt = f"""
        Contexte des données émotionnelles :
        {context_str}
        
        Question : {question}
        
        Répondez de manière précise et actionnable.
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            print(f"❌ Erreur réponse question: {e}")
            return "Erreur de réponse"
    
    def detect_anomalies(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Détecte les anomalies émotionnelles"""
        # Utiliser Ollama en priorité
        if ollama_client.is_available():
            return ollama_client.detect_anomalies(data)
        
        if not self.llm:
            return []
        
        # Analyser les patterns
        anomalies = []
        
        # Détection de pics émotionnels
        emotion_counts = {}
        for item in data:
            emotion = item.get('emotion_principale', 'neutre')
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Identifier les émotions anormalement élevées
        total = sum(emotion_counts.values())
        for emotion, count in emotion_counts.items():
            percentage = (count / total) * 100
            if percentage > 50:  # Seuil d'anomalie
                anomalies.append({
                    'type': 'emotion_spike',
                    'emotion': emotion,
                    'percentage': percentage,
                    'severity': 'high' if percentage > 70 else 'medium'
                })
        
        return anomalies
    
    def generate_alert(self, anomaly: Dict[str, Any]) -> str:
        """Génère une alerte pour une anomalie"""
        # Utiliser Ollama en priorité
        if ollama_client.is_available():
            return ollama_client.generate_alert(anomaly)
        
        if not self.llm:
            return "Alerte générée automatiquement"
        
        prompt = f"""
        Générez une alerte professionnelle pour cette anomalie émotionnelle :
        
        {json.dumps(anomaly, indent=2, ensure_ascii=False)}
        
        L'alerte doit être :
        - Concise et claire
        - Actionnable
        - Professionnelle
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            print(f"❌ Erreur génération alerte: {e}")
            return "Alerte générée automatiquement"
    
    def _prepare_emotion_summary(self, emotion_data: List[Dict[str, Any]]) -> str:
        """Prépare un résumé des données émotionnelles"""
        if not emotion_data:
            return "Aucune donnée disponible"
        
        # Compter les émotions
        emotion_counts = {}
        total_polarity = 0
        
        for item in emotion_data:
            emotion = item.get('emotion_principale', 'neutre')
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            total_polarity += item.get('polarite', 0)
        
        # Créer le résumé
        summary = f"Total réactions: {len(emotion_data)}\n"
        summary += f"Polarité moyenne: {total_polarity / len(emotion_data):.2f}\n\n"
        summary += "Distribution des émotions:\n"
        
        for emotion, count in sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(emotion_data)) * 100
            summary += f"- {emotion}: {count} ({percentage:.1f}%)\n"
        
        return summary
    
    def get_conversation_history(self) -> str:
        """Retourne l'historique de conversation"""
        return self.memory.buffer


# Instance globale
semantic_agent = SemanticPulseAgent()
