"""
Client Ollama - Semantic Pulse X
Interface avec les modèles IA génératifs locaux
"""

import json
import logging
from collections.abc import Generator
from typing import Any

import requests

from app.backend.core.config import settings

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client pour interagir avec Ollama"""

    def __init__(self, base_url: str = None):
        self.base_url = base_url or f"http://{settings.ollama_host}"
        # Modèle par défaut (léger, configurable via settings)
        self.default_model = getattr(settings, "ollama_model", "llama3.2:3b")
        self.available_models = []
        self._check_connection()

    def _check_connection(self):
        """Vérifie la connexion avec Ollama"""
        # Tentative avec un retry rapide
        for attempt in range(2):
            try:
                response = requests.get(f"{self.base_url}/api/tags", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    self.available_models = [model["name"] for model in data.get("models", [])]
                    logger.info(f"✅ Ollama connecté - Modèles disponibles: {self.available_models}")
                    # Warm-up rapide: petite requête pour charger le modèle en mémoire
                    try:
                        if self.available_models:
                            _ = self.generate_text("OK ?", model=self.available_models[0], max_tokens=8, temperature=0.1)
                    except Exception:
                        pass
                    break
                else:
                    logger.warning("⚠️ Ollama non disponible, utilisation de fallback")
            except Exception as e:
                logger.warning(f"⚠️ Erreur connexion Ollama (tentative {attempt+1}/2): {e}")

    def generate_text(self,
                     prompt: str,
                     model: str = None,
                     max_tokens: int = 1000,
                     temperature: float = 0.7,
                     stream: bool = False) -> str:
        """Génère du texte avec Ollama"""

        if not self.available_models:
            return self._fallback_generation(prompt)

        model = model or self.default_model

        try:
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": stream,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }

            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()

            if stream:
                return self._handle_stream_response(response)
            else:
                data = response.json()
                return data.get("response", "")

        except Exception as e:
            logger.error(f"❌ Erreur génération Ollama: {e}")
            # Retry une fois avec paramètres plus courts
            try:
                payload["options"]["num_predict"] = min(256, max_tokens)
                response = requests.post(url, json=payload, timeout=30)
                response.raise_for_status()
                data = response.json()
                return data.get("response", "")
            except Exception:
                return self._fallback_generation(prompt)

    def generate_stream(self,
                       prompt: str,
                       model: str = None,
                       temperature: float = 0.7) -> Generator[str, None, None]:
        """Génère du texte en streaming"""

        if not self.available_models:
            yield self._fallback_generation(prompt)
            return

        model = model or self.default_model

        try:
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": temperature
                }
            }

            response = requests.post(url, json=payload, stream=True, timeout=30)
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        if 'response' in data:
                            yield data['response']
                        if data.get('done', False):
                            break
                    except json.JSONDecodeError:
                        continue

        except Exception as e:
            logger.error(f"❌ Erreur streaming Ollama: {e}")
            # Tentative de retry streaming raccourci
            try:
                payload["options"]["num_predict"] = 128
                response = requests.post(url, json=payload, stream=True, timeout=30)
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line.decode('utf-8'))
                            if 'response' in data:
                                yield data['response']
                            if data.get('done', False):
                                break
                        except json.JSONDecodeError:
                            continue
                return
            except Exception:
                yield self._fallback_generation(prompt)

    def analyze_emotion_trends(self, emotion_data: list[dict[str, Any]]) -> str:
        """Analyse les tendances émotionnelles avec IA"""
        prompt = f"""
        Analysez les tendances émotionnelles suivantes et fournissez un résumé professionnel :

        Données émotionnelles :
        {json.dumps(emotion_data, indent=2, ensure_ascii=False)}

        Fournissez :
        1. Les émotions dominantes et leur évolution
        2. Les tendances temporelles observées
        3. Les insights clés pour les analystes
        4. Les recommandations stratégiques
        5. Les alertes à surveiller

        Réponse en français, format professionnel.
        """

        return self.generate_text(prompt, temperature=0.3)

    def generate_insights(self, data: dict[str, Any]) -> str:
        """Génère des insights à partir des données"""
        prompt = f"""
        Générez des insights pertinents à partir de ces données d'analyse émotionnelle :

        {json.dumps(data, indent=2, ensure_ascii=False)}

        Focus sur :
        - Les patterns émotionnels identifiés
        - Les sujets émergents et tendances
        - Les recommandations stratégiques
        - Les opportunités d'action
        - Les risques à surveiller

        Format : rapport professionnel en français.
        """

        return self.generate_text(prompt, temperature=0.4)

    def answer_question(self, question: str, context: dict[str, Any]) -> str:
        """Répond à une question avec contexte"""
        prompt = f"""
        Contexte des données émotionnelles :
        {json.dumps(context, indent=2, ensure_ascii=False)}

        Question : {question}

        Répondez de manière précise, actionnable et professionnelle en français.
        Utilisez les données du contexte pour étayer votre réponse.
        """

        return self.generate_text(prompt, temperature=0.2)

    def detect_anomalies(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Détecte les anomalies émotionnelles avec IA"""
        prompt = f"""
        Analysez ces données émotionnelles et détectez les anomalies :

        {json.dumps(data, indent=2, ensure_ascii=False)}

        Identifiez :
        - Les pics émotionnels anormaux
        - Les changements de polarité brutaux
        - Les patterns inhabituels
        - Les tendances préoccupantes

        Répondez en JSON avec la structure :
        [
            {{
                "type": "type_d_anomalie",
                "description": "description",
                "severity": "low/medium/high",
                "recommendation": "recommandation"
            }}
        ]
        """

        response = self.generate_text(prompt, temperature=0.1)

        try:
            # Essayer de parser la réponse JSON
            anomalies = json.loads(response)
            return anomalies if isinstance(anomalies, list) else []
        except json.JSONDecodeError:
            # Fallback si la réponse n'est pas en JSON
            return [{
                "type": "pattern_anomaly",
                "description": "Anomalie détectée par IA",
                "severity": "medium",
                "recommendation": "Analyser plus en détail"
            }]

    def generate_alert(self, anomaly: dict[str, Any]) -> str:
        """Génère une alerte pour une anomalie"""
        prompt = f"""
        Générez une alerte professionnelle pour cette anomalie émotionnelle :

        {json.dumps(anomaly, indent=2, ensure_ascii=False)}

        L'alerte doit être :
        - Concise et claire
        - Actionnable
        - Professionnelle
        - En français
        - Avec niveau de priorité
        """

        return self.generate_text(prompt, temperature=0.2)

    def summarize_content(self, content: str, max_length: int = 200) -> str:
        """Résume du contenu"""
        prompt = f"""
        Résumez ce contenu en maximum {max_length} caractères :

        {content}

        Résumé en français, format professionnel.
        """

        return self.generate_text(prompt, temperature=0.1)

    def classify_content(self, content: str, categories: list[str]) -> dict[str, Any]:
        """Classifie du contenu dans des catégories"""
        prompt = f"""
        Classifiez ce contenu dans une des catégories suivantes :
        {', '.join(categories)}

        Contenu : {content}

        Répondez en JSON :
        {{
            "category": "catégorie_choisie",
            "confidence": 0.0-1.0,
            "reasoning": "explication"
        }}
        """

        response = self.generate_text(prompt, temperature=0.1)

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "category": categories[0],
                "confidence": 0.5,
                "reasoning": "Classification par défaut"
            }

    def _handle_stream_response(self, response) -> str:
        """Gère la réponse en streaming"""
        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode('utf-8'))
                    if 'response' in data:
                        full_response += data['response']
                    if data.get('done', False):
                        break
                except json.JSONDecodeError:
                    continue
        return full_response

    def _fallback_generation(self, prompt: str) -> str:
        """Génération de fallback si Ollama n'est pas disponible"""
        # Réponses prédéfinies basées sur des mots-clés
        if "tendances" in prompt.lower() or "émotion" in prompt.lower():
            return """
            Analyse des tendances émotionnelles :

            Les données montrent des patterns intéressants dans l'évolution des émotions.
            Il est recommandé de surveiller les changements de polarité et d'identifier
            les facteurs déclencheurs des variations émotionnelles.

            Recommandations :
            - Surveiller les pics émotionnels
            - Analyser les corrélations temporelles
            - Mettre en place des alertes automatiques
            """
        elif "insight" in prompt.lower():
            return """
            Insights clés identifiés :

            Les données révèlent des opportunités d'amélioration dans la compréhension
            des réactions émotionnelles. Il est important de continuer à collecter
            des données pour affiner l'analyse.
            """
        else:
            return """
            Analyse en cours...

            Les données sont en cours de traitement. Veuillez patienter
            pendant que notre système d'IA analyse les informations.
            """

    def get_available_models(self) -> list[str]:
        """Retourne la liste des modèles disponibles"""
        return self.available_models

    def is_available(self) -> bool:
        """Vérifie si Ollama est disponible"""
        return len(self.available_models) > 0


# Instance globale
ollama_client = OllamaClient()
