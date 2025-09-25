"""
Planificateur de tâches - Semantic Pulse X
Gestion des tâches programmées et des workflows
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Callable
import schedule
import time
from threading import Thread
import logging

from app.backend.orchestration.prefect_flows import (
    semantic_pulse_etl_flow,
    emotion_analysis_flow,
    topic_clustering_flow,
    monitoring_flow
)
from app.backend.core.metrics import update_metrics

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskScheduler:
    """Planificateur de tâches pour Semantic Pulse X"""
    
    def __init__(self):
        self.running = False
        self.tasks = {}
        self.scheduler_thread = None
    
    def add_task(self, name: str, func: Callable, schedule_time: str, **kwargs):
        """Ajoute une tâche au planificateur"""
        self.tasks[name] = {
            "func": func,
            "schedule": schedule_time,
            "kwargs": kwargs,
            "last_run": None,
            "status": "pending"
        }
        logger.info(f"✅ Tâche '{name}' ajoutée - Planification: {schedule_time}")
    
    def remove_task(self, name: str):
        """Supprime une tâche du planificateur"""
        if name in self.tasks:
            del self.tasks[name]
            logger.info(f"🗑️ Tâche '{name}' supprimée")
    
    def get_task_status(self, name: str) -> Dict[str, Any]:
        """Retourne le statut d'une tâche"""
        if name not in self.tasks:
            return {"error": "Tâche non trouvée"}
        
        task = self.tasks[name]
        return {
            "name": name,
            "status": task["status"],
            "last_run": task["last_run"],
            "schedule": task["schedule"]
        }
    
    def get_all_tasks_status(self) -> Dict[str, Any]:
        """Retourne le statut de toutes les tâches"""
        return {
            "total_tasks": len(self.tasks),
            "running": self.running,
            "tasks": {name: self.get_task_status(name) for name in self.tasks}
        }
    
    async def run_task(self, name: str):
        """Exécute une tâche"""
        if name not in self.tasks:
            logger.error(f"❌ Tâche '{name}' non trouvée")
            return
        
        task = self.tasks[name]
        task["status"] = "running"
        task["last_run"] = datetime.now().isoformat()
        
        try:
            logger.info(f"🔄 Exécution de la tâche '{name}'")
            
            # Exécuter la tâche
            if asyncio.iscoroutinefunction(task["func"]):
                result = await task["func"](**task["kwargs"])
            else:
                result = task["func"](**task["kwargs"])
            
            task["status"] = "completed"
            logger.info(f"✅ Tâche '{name}' terminée avec succès")
            
            return result
            
        except Exception as e:
            task["status"] = "error"
            logger.error(f"❌ Erreur tâche '{name}': {e}")
            raise
    
    def start_scheduler(self):
        """Démarre le planificateur"""
        if self.running:
            logger.warning("⚠️ Le planificateur est déjà en cours d'exécution")
            return
        
        self.running = True
        self.scheduler_thread = Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        logger.info("🚀 Planificateur démarré")
    
    def stop_scheduler(self):
        """Arrête le planificateur"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
        logger.info("🛑 Planificateur arrêté")
    
    def _run_scheduler(self):
        """Boucle principale du planificateur"""
        while self.running:
            try:
                # Vérifier les tâches programmées
                for name, task in self.tasks.items():
                    if self._should_run_task(name, task):
                        # Exécuter la tâche dans un thread séparé
                        asyncio.run(self.run_task(name))
                
                # Mettre à jour les métriques
                update_metrics()
                
                # Attendre avant la prochaine vérification
                time.sleep(60)  # Vérifier toutes les minutes
                
            except Exception as e:
                logger.error(f"❌ Erreur planificateur: {e}")
                time.sleep(30)  # Attendre avant de réessayer
    
    def _should_run_task(self, name: str, task: Dict[str, Any]) -> bool:
        """Détermine si une tâche doit être exécutée"""
        schedule_time = task["schedule"]
        last_run = task["last_run"]
        
        # Tâches immédiates
        if schedule_time == "immediate":
            return True
        
        # Tâches programmées
        if schedule_time == "daily" and self._is_daily_time():
            return True
        
        if schedule_time == "hourly" and self._is_hourly_time():
            return True
        
        if schedule_time == "every_15min" and self._is_15min_time():
            return True
        
        # Tâches avec intervalle personnalisé
        if schedule_time.startswith("every_"):
            interval = int(schedule_time.split("_")[1])
            if last_run:
                last_run_time = datetime.fromisoformat(last_run)
                if datetime.now() - last_run_time >= timedelta(minutes=interval):
                    return True
            else:
                return True
        
        return False
    
    def _is_daily_time(self) -> bool:
        """Vérifie si c'est l'heure quotidienne (2h du matin)"""
        now = datetime.now()
        return now.hour == 2 and now.minute == 0
    
    def _is_hourly_time(self) -> bool:
        """Vérifie si c'est l'heure (minute 0)"""
        now = datetime.now()
        return now.minute == 0
    
    def _is_15min_time(self) -> bool:
        """Vérifie si c'est l'heure des 15 minutes"""
        now = datetime.now()
        return now.minute % 15 == 0


class SemanticPulseScheduler:
    """Planificateur spécialisé pour Semantic Pulse X"""
    
    def __init__(self):
        self.scheduler = TaskScheduler()
        self._setup_default_tasks()
    
    def _setup_default_tasks(self):
        """Configure les tâches par défaut"""
        
        # ETL quotidien (2h du matin)
        self.scheduler.add_task(
            name="etl_daily",
            func=semantic_pulse_etl_flow,
            schedule_time="daily"
        )
        
        # Analyse émotionnelle (toutes les heures)
        self.scheduler.add_task(
            name="emotion_analysis_hourly",
            func=emotion_analysis_flow,
            schedule_time="hourly",
            texts=[]  # Sera rempli dynamiquement
        )
        
        # Clustering thématique (toutes les 6 heures)
        self.scheduler.add_task(
            name="topic_clustering_6h",
            func=topic_clustering_flow,
            schedule_time="every_360"  # 6 heures = 360 minutes
        )
        
        # Monitoring (toutes les 15 minutes)
        self.scheduler.add_task(
            name="monitoring_15min",
            func=monitoring_flow,
            schedule_time="every_15min"
        )
        
        # Mise à jour des métriques (toutes les 5 minutes)
        self.scheduler.add_task(
            name="update_metrics_5min",
            func=update_metrics,
            schedule_time="every_5"
        )
    
    def start(self):
        """Démarre le planificateur"""
        self.scheduler.start_scheduler()
        logger.info("🚀 Planificateur Semantic Pulse X démarré")
    
    def stop(self):
        """Arrête le planificateur"""
        self.scheduler.stop_scheduler()
        logger.info("🛑 Planificateur Semantic Pulse X arrêté")
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut du planificateur"""
        return self.scheduler.get_all_tasks_status()
    
    def run_task_now(self, task_name: str):
        """Exécute une tâche immédiatement"""
        asyncio.run(self.scheduler.run_task(task_name))
    
    def add_custom_task(self, name: str, func: Callable, schedule_time: str, **kwargs):
        """Ajoute une tâche personnalisée"""
        self.scheduler.add_task(name, func, schedule_time, **kwargs)
    
    def remove_custom_task(self, name: str):
        """Supprime une tâche personnalisée"""
        self.scheduler.remove_task(name)


# Instance globale
semantic_scheduler = SemanticPulseScheduler()


def start_scheduler():
    """Démarre le planificateur global"""
    semantic_scheduler.start()


def stop_scheduler():
    """Arrête le planificateur global"""
    semantic_scheduler.stop()


def get_scheduler_status():
    """Retourne le statut du planificateur global"""
    return semantic_scheduler.get_status()


if __name__ == "__main__":
    # Démarrage du planificateur
    start_scheduler()
    
    try:
        # Boucle principale
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        stop_scheduler()
        print("🛑 Planificateur arrêté")
