#!/usr/bin/env python3
"""
Script de configuration Ollama - Semantic Pulse X
Installe et configure Ollama avec les modèles recommandés
"""

import requests
import json
import time
import subprocess
import sys
from pathlib import Path


class OllamaSetup:
    """Configuration d'Ollama pour Semantic Pulse X"""
    
    def __init__(self, base_url: str = None):
        if base_url is None:
            import os
            ollama_host = os.getenv("OLLAMA_HOST", "localhost:11434")
            base_url = f"http://{ollama_host}"
        self.base_url = base_url
        self.recommended_models = [
            "mistral:7b",      # Modèle principal - excellent pour le français
            "llama2:7b",       # Modèle alternatif - polyvalent
            "codellama:7b",    # Pour la génération de code
            "phi3:3.8b"        # Modèle léger et rapide
        ]
    
    def check_ollama_status(self) -> bool:
        """Vérifie si Ollama est en cours d'exécution"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def wait_for_ollama(self, timeout: int = 300) -> bool:
        """Attend qu'Ollama soit disponible"""
        print("⏳ Attente du démarrage d'Ollama...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.check_ollama_status():
                print("✅ Ollama est disponible!")
                return True
            time.sleep(5)
            print(".", end="", flush=True)
        
        print(f"\n❌ Timeout: Ollama n'est pas disponible après {timeout}s")
        return False
    
    def pull_model(self, model_name: str) -> bool:
        """Télécharge un modèle Ollama"""
        print(f"📥 Téléchargement du modèle {model_name}...")
        
        try:
            url = f"{self.base_url}/api/pull"
            payload = {"name": model_name}
            
            response = requests.post(url, json=payload, stream=True, timeout=300)
            response.raise_for_status()
            
            # Afficher la progression
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        if 'status' in data:
                            print(f"\r{data['status']}", end="", flush=True)
                    except json.JSONDecodeError:
                        continue
            
            print(f"\n✅ Modèle {model_name} téléchargé avec succès!")
            return True
            
        except Exception as e:
            print(f"\n❌ Erreur téléchargement {model_name}: {e}")
            return False
    
    def test_model(self, model_name: str) -> bool:
        """Teste un modèle"""
        print(f"🧪 Test du modèle {model_name}...")
        
        try:
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": model_name,
                "prompt": "Bonjour, comment allez-vous?",
                "stream": False
            }
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if 'response' in data and data['response'].strip():
                print(f"✅ Modèle {model_name} fonctionne correctement!")
                return True
            else:
                print(f"❌ Modèle {model_name} ne répond pas correctement")
                return False
                
        except Exception as e:
            print(f"❌ Erreur test {model_name}: {e}")
            return False
    
    def setup_models(self) -> Dict[str, bool]:
        """Configure tous les modèles recommandés"""
        print("🚀 Configuration des modèles Ollama...")
        
        results = {}
        
        for model in self.recommended_models:
            print(f"\n📦 Configuration de {model}")
            
            # Télécharger le modèle
            if self.pull_model(model):
                # Tester le modèle
                if self.test_model(model):
                    results[model] = True
                    print(f"✅ {model} configuré avec succès!")
                else:
                    results[model] = False
                    print(f"⚠️ {model} téléchargé mais ne fonctionne pas")
            else:
                results[model] = False
                print(f"❌ {model} échec du téléchargement")
        
        return results
    
    def create_model_alias(self, model_name: str, alias: str) -> bool:
        """Crée un alias pour un modèle"""
        try:
            # Créer un alias pour le modèle principal
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": model_name,
                "prompt": "test",
                "stream": False
            }
            
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
            
        except:
            return False
    
    def get_available_models(self) -> List[str]:
        """Retourne la liste des modèles disponibles"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
        except:
            pass
        return []
    
    def generate_test_report(self) -> str:
        """Génère un rapport de test"""
        print("\n📊 Génération du rapport de test...")
        
        available_models = self.get_available_models()
        
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "ollama_status": "running" if self.check_ollama_status() else "stopped",
            "available_models": available_models,
            "recommended_models": self.recommended_models,
            "setup_status": {
                "mistral_7b": "mistral:7b" in available_models,
                "llama2_7b": "llama2:7b" in available_models,
                "codellama_7b": "codellama:7b" in available_models,
                "phi3_3.8b": "phi3:3.8b" in available_models
            }
        }
        
        # Sauvegarder le rapport
        report_path = Path("ollama_setup_report.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Rapport sauvegardé: {report_path}")
        return str(report_path)
    
    def run_setup(self) -> bool:
        """Exécute la configuration complète"""
        print("🎯 Configuration Ollama pour Semantic Pulse X")
        print("=" * 50)
        
        # Vérifier si Ollama est disponible
        if not self.check_ollama_status():
            print("❌ Ollama n'est pas disponible!")
            print("💡 Démarrez Ollama avec: docker-compose -f docker-compose.ollama.yml up -d")
            return False
        
        # Attendre qu'Ollama soit prêt
        if not self.wait_for_ollama():
            return False
        
        # Configurer les modèles
        results = self.setup_models()
        
        # Générer le rapport
        report_path = self.generate_test_report()
        
        # Afficher le résumé
        print("\n📈 Résumé de la configuration:")
        print(f"   - Modèles configurés: {sum(results.values())}/{len(results)}")
        print(f"   - Rapport: {report_path}")
        
        success_count = sum(results.values())
        if success_count > 0:
            print(f"✅ Configuration réussie! {success_count} modèles disponibles.")
            return True
        else:
            print("❌ Aucun modèle configuré avec succès.")
            return False


def main():
    """Fonction principale"""
    setup = OllamaSetup()
    
    if len(sys.argv) > 1 and sys.argv[1] == "docker":
        print("🐳 Mode Docker détecté")
        # Attendre plus longtemps en mode Docker
        setup.wait_for_ollama(600)
    
    success = setup.run_setup()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
