"""
Dashboard de monitoring - Semantic Pulse X
Interface de supervision des workflows et tâches
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, Any, List
import json

from app.backend.orchestration.scheduler import get_scheduler_status
from app.backend.core.metrics import (
    emotion_processing_total,
    data_ingestion_total,
    api_requests_total,
    memory_usage
)


def show_orchestration_dashboard():
    """Affiche le dashboard d'orchestration"""
    st.header("🎛️ Dashboard d'Orchestration")
    
    # Statut du planificateur
    st.subheader("📊 Statut du Planificateur")
    
    try:
        scheduler_status = get_scheduler_status()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Tâches totales",
                scheduler_status["total_tasks"],
                delta="0"
            )
        
        with col2:
            running_tasks = sum(1 for task in scheduler_status["tasks"].values() 
                              if task["status"] == "running")
            st.metric(
                "Tâches en cours",
                running_tasks,
                delta=f"+{running_tasks}" if running_tasks > 0 else "0"
            )
        
        with col3:
            completed_tasks = sum(1 for task in scheduler_status["tasks"].values() 
                                if task["status"] == "completed")
            st.metric(
                "Tâches terminées",
                completed_tasks,
                delta=f"+{completed_tasks}" if completed_tasks > 0 else "0"
            )
        
        # Détails des tâches
        st.subheader("📋 Détails des Tâches")
        
        tasks_data = []
        for name, task_info in scheduler_status["tasks"].items():
            tasks_data.append({
                "Nom": name,
                "Statut": task_info["status"],
                "Dernière exécution": task_info["last_run"] or "Jamais",
                "Planification": task_info["schedule"]
            })
        
        if tasks_data:
            df_tasks = pd.DataFrame(tasks_data)
            st.dataframe(df_tasks, use_container_width=True)
        else:
            st.info("Aucune tâche configurée")
        
        # Graphique des statuts
        if tasks_data:
            status_counts = df_tasks["Statut"].value_counts()
            
            fig_status = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="Répartition des statuts des tâches",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_status, use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ Erreur lors de la récupération du statut: {e}")
    
    # Métriques de performance
    st.subheader("📈 Métriques de Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Métriques d'ingestion
        st.write("**Ingestion de données**")
        
        # Simulation de métriques (en production, récupérer depuis Prometheus)
        ingestion_data = {
            "Source": ["file", "database", "bigdata", "scraping", "api"],
            "Enregistrements": [200, 300, 250, 150, 100],
            "Statut": ["success", "success", "success", "success", "success"]
        }
        
        df_ingestion = pd.DataFrame(ingestion_data)
        
        fig_ingestion = px.bar(
            df_ingestion,
            x="Source",
            y="Enregistrements",
            color="Statut",
            title="Enregistrements par source",
            color_discrete_map={"success": "green", "error": "red"}
        )
        st.plotly_chart(fig_ingestion, use_container_width=True)
    
    with col2:
        # Métriques de traitement
        st.write("**Traitement des émotions**")
        
        # Simulation de métriques
        emotion_data = {
            "Émotion": ["joie", "colere", "tristesse", "surprise", "peur", "neutre"],
            "Nombre": [45, 20, 15, 10, 5, 5],
            "Temps moyen (ms)": [120, 150, 130, 110, 140, 100]
        }
        
        df_emotion = pd.DataFrame(emotion_data)
        
        fig_emotion = px.bar(
            df_emotion,
            x="Émotion",
            y="Nombre",
            title="Distribution des émotions traitées",
            color="Temps moyen (ms)",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig_emotion, use_container_width=True)
    
    # Logs en temps réel
    st.subheader("📝 Logs en Temps Réel")
    
    # Simulation de logs
    logs_data = [
        {
            "Timestamp": datetime.now() - timedelta(minutes=5),
            "Niveau": "INFO",
            "Message": "Tâche ETL quotidienne démarrée",
            "Tâche": "etl_daily"
        },
        {
            "Timestamp": datetime.now() - timedelta(minutes=4),
            "Niveau": "INFO",
            "Message": "Extraction des données terminée - 1000 enregistrements",
            "Tâche": "etl_daily"
        },
        {
            "Timestamp": datetime.now() - timedelta(minutes=3),
            "Niveau": "INFO",
            "Message": "Transformation des données en cours",
            "Tâche": "etl_daily"
        },
        {
            "Timestamp": datetime.now() - timedelta(minutes=2),
            "Niveau": "WARNING",
            "Message": "Temps de traitement plus long que prévu",
            "Tâche": "emotion_analysis_hourly"
        },
        {
            "Timestamp": datetime.now() - timedelta(minutes=1),
            "Niveau": "INFO",
            "Message": "Tâche de monitoring terminée",
            "Tâche": "monitoring_15min"
        }
    ]
    
    df_logs = pd.DataFrame(logs_data)
    
    # Filtrer par niveau
    log_levels = st.multiselect(
        "Filtrer par niveau",
        ["INFO", "WARNING", "ERROR"],
        default=["INFO", "WARNING", "ERROR"]
    )
    
    filtered_logs = df_logs[df_logs["Niveau"].isin(log_levels)]
    
    if not filtered_logs.empty:
        st.dataframe(
            filtered_logs,
            use_container_width=True,
            column_config={
                "Timestamp": st.column_config.DatetimeColumn(
                    "Timestamp",
                    format="DD/MM/YYYY HH:mm:ss"
                ),
                "Niveau": st.column_config.TextColumn(
                    "Niveau",
                    help="Niveau de log"
                ),
                "Message": st.column_config.TextColumn(
                    "Message",
                    help="Message de log"
                ),
                "Tâche": st.column_config.TextColumn(
                    "Tâche",
                    help="Nom de la tâche"
                )
            }
        )
    else:
        st.info("Aucun log correspondant aux filtres")
    
    # Alertes
    st.subheader("🚨 Alertes")
    
    # Simulation d'alertes
    alerts_data = [
        {
            "Timestamp": datetime.now() - timedelta(minutes=10),
            "Type": "Performance",
            "Message": "Temps de traitement des émotions élevé",
            "Severité": "Warning",
            "Statut": "Active"
        },
        {
            "Timestamp": datetime.now() - timedelta(minutes=30),
            "Type": "Système",
            "Message": "Utilisation mémoire élevée",
            "Severité": "Critical",
            "Statut": "Resolved"
        },
        {
            "Timestamp": datetime.now() - timedelta(hours=1),
            "Type": "Données",
            "Message": "Taux d'erreur d'ingestion élevé",
            "Severité": "Warning",
            "Statut": "Active"
        }
    ]
    
    df_alerts = pd.DataFrame(alerts_data)
    
    # Filtrer par statut
    alert_status = st.selectbox(
        "Filtrer par statut",
        ["Tous", "Active", "Resolved"],
        index=0
    )
    
    if alert_status != "Tous":
        df_alerts = df_alerts[df_alerts["Statut"] == alert_status]
    
    if not df_alerts.empty:
        # Colorer par sévérité
        def color_severity(severity):
            if severity == "Critical":
                return "background-color: #ffebee; color: #c62828"
            elif severity == "Warning":
                return "background-color: #fff3e0; color: #ef6c00"
            else:
                return "background-color: #e8f5e8; color: #2e7d32"
        
        styled_alerts = df_alerts.style.applymap(
            color_severity,
            subset=["Severité"]
        )
        
        st.dataframe(
            styled_alerts,
            use_container_width=True,
            column_config={
                "Timestamp": st.column_config.DatetimeColumn(
                    "Timestamp",
                    format="DD/MM/YYYY HH:mm:ss"
                ),
                "Type": st.column_config.TextColumn("Type"),
                "Message": st.column_config.TextColumn("Message"),
                "Severité": st.column_config.TextColumn("Severité"),
                "Statut": st.column_config.TextColumn("Statut")
            }
        )
    else:
        st.info("Aucune alerte active")
    
    # Actions
    st.subheader("⚡ Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Redémarrer le planificateur", type="primary"):
            st.success("Planificateur redémarré!")
    
    with col2:
        if st.button("📊 Actualiser les métriques"):
            st.success("Métriques actualisées!")
    
    with col3:
        if st.button("🧹 Nettoyer les logs"):
            st.success("Logs nettoyés!")


def show_workflow_visualization():
    """Affiche la visualisation des workflows"""
    st.header("🔄 Visualisation des Workflows")
    
    # Workflow ETL
    st.subheader("📥 Workflow ETL")
    
    # Créer un diagramme de workflow
    workflow_steps = [
        "Extraction",
        "Transformation", 
        "Analyse IA",
        "Chargement",
        "Rapport"
    ]
    
    # Simulation des statuts
    step_statuses = ["completed", "running", "pending", "pending", "pending"]
    
    # Créer le diagramme
    fig = go.Figure()
    
    for i, (step, status) in enumerate(zip(workflow_steps, step_statuses)):
        color = "green" if status == "completed" else "orange" if status == "running" else "gray"
        
        fig.add_trace(go.Scatter(
            x=[i],
            y=[0],
            mode='markers+text',
            marker=dict(size=50, color=color),
            text=[step],
            textposition="top center",
            name=step,
            hovertemplate=f"<b>{step}</b><br>Statut: {status}<extra></extra>"
        ))
    
    # Ajouter des flèches
    for i in range(len(workflow_steps) - 1):
        fig.add_annotation(
            x=i + 0.5,
            y=0,
            ax=i,
            ay=0,
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="black"
        )
    
    fig.update_layout(
        title="Workflow ETL Semantic Pulse X",
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, showticklabels=False),
        showlegend=False,
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Légende des statuts
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("🟢 **Terminé**")
    with col2:
        st.markdown("🟠 **En cours**")
    with col3:
        st.markdown("⚪ **En attente**")
    
    # Détails des étapes
    st.subheader("📋 Détails des Étapes")
    
    steps_data = []
    for step, status in zip(workflow_steps, step_statuses):
        steps_data.append({
            "Étape": step,
            "Statut": status,
            "Début": datetime.now() - timedelta(minutes=10),
            "Fin": datetime.now() - timedelta(minutes=5) if status == "completed" else None,
            "Durée": "5 min" if status == "completed" else "En cours"
        })
    
    df_steps = pd.DataFrame(steps_data)
    st.dataframe(df_steps, use_container_width=True)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Orchestration Dashboard",
        page_icon="🎛️",
        layout="wide"
    )
    
    tab1, tab2 = st.tabs(["📊 Dashboard", "🔄 Workflows"])
    
    with tab1:
        show_orchestration_dashboard()
    
    with tab2:
        show_workflow_visualization()

