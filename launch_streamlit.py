#!/usr/bin/env python3
"""
Script de lancement Streamlit avec PYTHONPATH correct
"""

import os
import subprocess
import sys
from pathlib import Path


def launch_streamlit():
    """Lance Streamlit avec la configuration correcte"""

    # Ajouter le répertoire racine au PYTHONPATH
    project_root = Path(__file__).parent.absolute()
    sys.path.insert(0, str(project_root))

    # Définir la variable d'environnement
    os.environ['PYTHONPATH'] = str(project_root) + os.pathsep + os.environ.get('PYTHONPATH', '')

    print("🚀 Lancement de Streamlit - Semantic Pulse X")
    print(f"📁 Répertoire projet: {project_root}")
    print(f"🐍 PYTHONPATH: {os.environ['PYTHONPATH']}")
    print("=" * 60)

    # Lancer Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "app/frontend/streamlit_app.py",
            "--server.port", "8501",
            "--server.headless", "true"
        ], cwd=project_root)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de Streamlit")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    launch_streamlit()
