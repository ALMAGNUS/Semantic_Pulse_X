#!/usr/bin/env python3
"""
Module de Surveillance de Dérive des Modèles - Semantic Pulse X
Implémentation PSI et KS Test pour détection de dérive
"""

import json
import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Tuple
from scipy import stats
import sqlite3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelDriftMonitor:
    """Surveillance de la dérive des modèles avec PSI et KS Test"""
    
    def __init__(self, db_path: str = "semantic_pulse.db"):
        self.db_path = db_path
        self.drift_thresholds = {
            "psi": 0.2,
            "ks": 0.05,
            "accuracy": 0.85
        }
        self.alerts = []
        
    def calculate_psi(self, reference_data: np.ndarray, current_data: np.ndarray, bins: int = 10) -> float:
        """Calcule le Population Stability Index (PSI)"""
        try:
            min_val = min(np.min(reference_data), np.min(current_data))
            max_val = max(np.max(reference_data), np.max(current_data))
            bin_edges = np.linspace(min_val, max_val, bins + 1)
            
            ref_counts, _ = np.histogram(reference_data, bins=bin_edges)
            curr_counts, _ = np.histogram(current_data, bins=bin_edges)
            
            ref_props = ref_counts / len(reference_data)
            curr_props = curr_counts / len(current_data)
            
            ref_props = np.where(ref_props == 0, 0.0001, ref_props)
            curr_props = np.where(curr_props == 0, 0.0001, curr_props)
            
            psi = np.sum((curr_props - ref_props) * np.log(curr_props / ref_props))
            return float(psi)
            
        except Exception as e:
            logger.error(f"Erreur calcul PSI: {e}")
            return 0.0
    
    def ks_test(self, reference_data: np.ndarray, current_data: np.ndarray) -> Tuple[float, float]:
        """Test de Kolmogorov-Smirnov"""
        try:
            ks_statistic, p_value = stats.ks_2samp(reference_data, current_data)
            return float(ks_statistic), float(p_value)
        except Exception as e:
            logger.error(f"Erreur KS Test: {e}")
            return 0.0, 1.0
    
    def detect_data_drift(self, reference_data: np.ndarray, current_data: np.ndarray) -> Dict[str, Any]:
        """Détecte la dérive des données"""
        psi_score = self.calculate_psi(reference_data, current_data)
        ks_statistic, ks_p_value = self.ks_test(reference_data, current_data)
        
        psi_drift = psi_score > self.drift_thresholds["psi"]
        ks_drift = ks_statistic > self.drift_thresholds["ks"]
        drift_detected = psi_drift or ks_drift
        
        result = {
            "drift_detected": drift_detected,
            "psi_score": psi_score,
            "ks_statistic": ks_statistic,
            "ks_p_value": ks_p_value,
            "timestamp": datetime.now().isoformat()
        }
        
        if drift_detected:
            alert_msg = f"Dérive détectée - PSI: {psi_score:.3f}, KS: {ks_statistic:.3f}"
            self.alerts.append({
                "type": "data_drift",
                "message": alert_msg,
                "severity": "warning",
                "timestamp": datetime.now().isoformat()
            })
        
        return result
    
    def get_reference_data(self, days_back: int = 30) -> np.ndarray:
        """Récupère les données de référence"""
        try:
            conn = sqlite3.connect(self.db_path)
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            query = """
            SELECT r.score FROM contenus c
            JOIN reactions r ON c.id = r.contenu_id
            WHERE c.created_at < ?
            LIMIT 1000
            """
            
            df = pd.read_sql_query(query, conn, params=[cutoff_date.isoformat()])
            conn.close()
            
            if df.empty:
                return np.array([])
            
            return df['score'].values
            
        except Exception as e:
            logger.error(f"Erreur récupération données: {e}")
            return np.array([])
    
    def get_current_data(self, days_back: int = 7) -> np.ndarray:
        """Récupère les données actuelles"""
        try:
            conn = sqlite3.connect(self.db_path)
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            query = """
            SELECT r.score FROM contenus c
            JOIN reactions r ON c.id = r.contenu_id
            WHERE c.created_at >= ?
            LIMIT 500
            """
            
            df = pd.read_sql_query(query, conn, params=[cutoff_date.isoformat()])
            conn.close()
            
            if df.empty:
                return np.array([])
            
            return df['score'].values
            
        except Exception as e:
            logger.error(f"Erreur récupération données: {e}")
            return np.array([])
    
    def run_monitoring(self) -> Dict[str, Any]:
        """Exécute la surveillance complète"""
        logger.info("Démarrage surveillance de dérive...")
        
        ref_data = self.get_reference_data()
        curr_data = self.get_current_data()
        
        if len(ref_data) == 0 or len(curr_data) == 0:
            return {"error": "Données insuffisantes"}
        
        drift_results = self.detect_data_drift(ref_data, curr_data)
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "drift_detected": drift_results["drift_detected"],
            "psi_score": drift_results["psi_score"],
            "ks_statistic": drift_results["ks_statistic"],
            "alerts": self.alerts
        }
        
        logger.info(f"Surveillance terminée - Dérive: {'DÉTECTÉE' if drift_results['drift_detected'] else 'Non détectée'}")
        return results


def main():
    """Test du module"""
    monitor = ModelDriftMonitor()
    results = monitor.run_monitoring()
    
    output_file = "data/processed/drift_results.json"
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"Résultats sauvegardés: {output_file}")


if __name__ == "__main__":
    main()
