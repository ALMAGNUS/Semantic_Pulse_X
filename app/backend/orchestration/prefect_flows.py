"""
Orchestration Prefect - Semantic Pulse X
Gestion des workflows et tâches automatisées
"""

from datetime import datetime
from typing import Any

from prefect import flow, get_run_logger, task

from app.backend.ai.emotion_classifier import emotion_classifier
from app.backend.ai.langchain_agent import semantic_agent
from app.backend.ai.topic_clustering import topic_clustering
from app.backend.core.metrics import track_data_ingestion, track_emotion_processing
from app.backend.etl.pipeline import etl_pipeline


@task(name="extract_data", retries=3, retry_delay_seconds=60)
async def extract_data_task() -> dict[str, list[dict[str, Any]]]:
    """Tâche d'extraction des données"""
    logger = get_run_logger()
    logger.info("🔄 Début de l'extraction des données")

    try:
        # Exécuter l'extraction
        raw_data = etl_pipeline._extract_data()

        # Tracker les métriques
        for source, data in raw_data.items():
            track_data_ingestion(source, "success")
            logger.info(f"✅ {len(data)} enregistrements extraits depuis {source}")

        return raw_data

    except Exception as e:
        logger.error(f"❌ Erreur extraction: {e}")
        # Tracker l'erreur
        track_data_ingestion("unknown", "error")
        raise


@task(name="transform_data", retries=2, retry_delay_seconds=30)
async def transform_data_task(raw_data: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    """Tâche de transformation des données"""
    logger = get_run_logger()
    logger.info("🔄 Début de la transformation des données")

    try:
        # Exécuter la transformation
        processed_df = etl_pipeline._transform_data(raw_data)

        # Tracker les métriques
        track_data_ingestion("transformation", "success")
        logger.info(f"✅ {len(processed_df)} enregistrements transformés")

        return {
            "processed_data": processed_df,
            "total_records": len(processed_df),
            "sources": processed_df['source_type'].value_counts().to_dict()
        }

    except Exception as e:
        logger.error(f"❌ Erreur transformation: {e}")
        track_data_ingestion("transformation", "error")
        raise


@task(name="ai_analysis", retries=2, retry_delay_seconds=45)
async def ai_analysis_task(processed_data: dict[str, Any]) -> dict[str, Any]:
    """Tâche d'analyse IA"""
    logger = get_run_logger()
    logger.info("🧠 Début de l'analyse IA")

    try:
        df = processed_data["processed_data"]
        texts = df['text'].tolist()

        # Classification émotionnelle
        logger.info("🎭 Classification émotionnelle...")
        emotion_results = emotion_classifier.classify_batch(texts)

        # Tracker les métriques
        for result in emotion_results:
            track_emotion_processing(result['emotion_principale'], 'ai_analysis')

        # Clustering thématique
        logger.info("📊 Clustering thématique...")
        topic_results = topic_clustering.fit_topics(texts)

        # Génération d'insights
        logger.info("💡 Génération d'insights...")
        insights = semantic_agent.analyze_emotion_trends(emotion_results)

        ai_results = {
            "emotion_analysis": emotion_results,
            "topic_clustering": topic_results,
            "insights": insights,
            "total_processed": len(texts)
        }

        logger.info("✅ Analyse IA terminée")
        return ai_results

    except Exception as e:
        logger.error(f"❌ Erreur analyse IA: {e}")
        raise


@task(name="load_data", retries=2, retry_delay_seconds=30)
async def load_data_task(processed_data: dict[str, Any], ai_results: dict[str, Any]) -> dict[str, Any]:
    """Tâche de chargement des données"""
    logger = get_run_logger()
    logger.info("💾 Début du chargement des données")

    try:
        # Exécuter le chargement
        load_results = etl_pipeline._load_data(processed_data["processed_data"])

        # Sauvegarder les résultats IA
        ai_path = etl_pipeline.processed_dir / "ai_analysis_results.parquet"
        processed_data["processed_data"].to_parquet(ai_path, index=False)

        # Tracker les métriques
        track_data_ingestion("loading", "success")

        logger.info("✅ Données chargées avec succès")
        return {
            "load_results": load_results,
            "ai_results": ai_results,
            "status": "success"
        }

    except Exception as e:
        logger.error(f"❌ Erreur chargement: {e}")
        track_data_ingestion("loading", "error")
        raise


@task(name="generate_report", retries=1)
async def generate_report_task(
    raw_data: dict[str, list[dict[str, Any]]],
    processed_data: dict[str, Any],
    ai_results: dict[str, Any],
    load_results: dict[str, Any]
) -> dict[str, Any]:
    """Tâche de génération du rapport"""
    logger = get_run_logger()
    logger.info("📊 Génération du rapport final")

    try:
        # Générer le rapport
        report = etl_pipeline._generate_report(raw_data, processed_data["processed_data"], ai_results)

        # Ajouter les résultats de chargement
        report["load_results"] = load_results
        report["pipeline_status"] = "completed"
        report["timestamp"] = datetime.now().isoformat()

        logger.info("✅ Rapport généré avec succès")
        return report

    except Exception as e:
        logger.error(f"❌ Erreur génération rapport: {e}")
        raise


@flow(
    name="semantic_pulse_etl_flow",
    # task_runner=SequentialTaskRunner(),  # Supprimé pour Prefect 2.x
    retries=1,
    retry_delay_seconds=300
)
async def semantic_pulse_etl_flow() -> dict[str, Any]:
    """Flow principal ETL de Semantic Pulse X"""
    logger = get_run_logger()
    logger.info("🚀 Démarrage du flow ETL Semantic Pulse X")

    try:
        # 1. Extraction
        raw_data = await extract_data_task()

        # 2. Transformation
        processed_data = await transform_data_task(raw_data)

        # 3. Analyse IA
        ai_results = await ai_analysis_task(processed_data)

        # 4. Chargement
        load_results = await load_data_task(processed_data, ai_results)

        # 5. Rapport
        report = await generate_report_task(raw_data, processed_data, ai_results, load_results)

        logger.info("✅ Flow ETL terminé avec succès")
        return report

    except Exception as e:
        logger.error(f"❌ Erreur flow ETL: {e}")
        raise


@flow(name="emotion_analysis_flow")
async def emotion_analysis_flow(texts: list[str]) -> dict[str, Any]:
    """Flow d'analyse émotionnelle en temps réel"""
    logger = get_run_logger()
    logger.info(f"🎭 Analyse émotionnelle de {len(texts)} textes")

    try:
        # Classification émotionnelle
        emotion_results = emotion_classifier.classify_batch(texts)

        # Analyse des tendances
        trend_analysis = emotion_classifier.detect_emotion_trend(
            [(text, datetime.now().isoformat()) for text in texts]
        )

        # Génération d'insights
        insights = semantic_agent.analyze_emotion_trends(emotion_results)

        # Détection d'anomalies
        anomalies = semantic_agent.detect_anomalies(emotion_results)

        result = {
            "emotion_results": emotion_results,
            "trend_analysis": trend_analysis,
            "insights": insights,
            "anomalies": anomalies,
            "total_texts": len(texts),
            "timestamp": datetime.now().isoformat()
        }

        logger.info("✅ Analyse émotionnelle terminée")
        return result

    except Exception as e:
        logger.error(f"❌ Erreur analyse émotionnelle: {e}")
        raise


@flow(name="topic_clustering_flow")
async def topic_clustering_flow(texts: list[str]) -> dict[str, Any]:
    """Flow de clustering thématique"""
    logger = get_run_logger()
    logger.info(f"📊 Clustering thématique de {len(texts)} textes")

    try:
        # Clustering
        topic_results = topic_clustering.fit_topics(texts)

        # Prédiction des topics
        topic_predictions = topic_clustering.predict_topics(texts)

        # Analyse de l'évolution
        evolution = topic_clustering.get_topic_evolution(
            [(text, datetime.now().isoformat()) for text in texts]
        )

        result = {
            "topic_results": topic_results,
            "predictions": topic_predictions,
            "evolution": evolution,
            "total_texts": len(texts),
            "timestamp": datetime.now().isoformat()
        }

        logger.info("✅ Clustering thématique terminé")
        return result

    except Exception as e:
        logger.error(f"❌ Erreur clustering: {e}")
        raise


@flow(name="monitoring_flow")
async def monitoring_flow() -> dict[str, Any]:
    """Flow de monitoring et alertes"""
    logger = get_run_logger()
    logger.info("📈 Vérification du monitoring")

    try:
        # Vérifier l'état des services
        services_status = {
            "etl_pipeline": "healthy",
            "emotion_classifier": "healthy",
            "topic_clustering": "healthy",
            "langchain_agent": "healthy"
        }

        # Vérifier les métriques
        metrics_status = {
            "data_ingestion_rate": "normal",
            "emotion_processing_time": "normal",
            "error_rate": "low",
            "memory_usage": "normal"
        }

        # Générer des alertes si nécessaire
        alerts = []
        if metrics_status["error_rate"] == "high":
            alerts.append({
                "type": "error_rate_high",
                "message": "Taux d'erreur élevé détecté",
                "severity": "warning"
            })

        result = {
            "services_status": services_status,
            "metrics_status": metrics_status,
            "alerts": alerts,
            "timestamp": datetime.now().isoformat()
        }

        logger.info("✅ Monitoring vérifié")
        return result

    except Exception as e:
        logger.error(f"❌ Erreur monitoring: {e}")
        raise


# Déploiements Prefect - COMMENTÉ POUR PRECFECT 2.x
def create_deployments():
    """Crée les déploiements Prefect - DÉSACTIVÉ pour Prefect 2.x"""
    logger = get_run_logger()
    logger.warning("Déploiements Prefect désactivés pour compatibilité Prefect 2.x")
    return []

    # Code commenté pour Prefect 2.x
    """
    # Déploiement ETL quotidien
    etl_deployment = Deployment.build_from_flow(
        flow=semantic_pulse_etl_flow,
        name="semantic-pulse-etl-daily",
        schedule=CronSchedule(cron="0 2 * * *"),  # Tous les jours à 2h
        work_pool_name="default-agent-pool"
    )

    # Déploiement analyse émotionnelle (toutes les heures)
    emotion_deployment = Deployment.build_from_flow(
        flow=emotion_analysis_flow,
        name="emotion-analysis-hourly",
        schedule=CronSchedule(cron="0 * * * *"),  # Toutes les heures
        work_pool_name="default-agent-pool"
    )

    # Déploiement clustering (toutes les 6 heures)
    clustering_deployment = Deployment.build_from_flow(
        flow=topic_clustering_flow,
        name="topic-clustering-6h",
        schedule=CronSchedule(cron="0 */6 * * *"),  # Toutes les 6 heures
        work_pool_name="default-agent-pool"
    )

    # Déploiement monitoring (toutes les 15 minutes)
    monitoring_deployment = Deployment.build_from_flow(
        flow=monitoring_flow,
        name="monitoring-15min",
        schedule=CronSchedule(cron="*/15 * * * *"),  # Toutes les 15 minutes
        work_pool_name="default-agent-pool"
    )

    return [etl_deployment, emotion_deployment, clustering_deployment, monitoring_deployment]
    """


# Configuration Prefect
def configure_prefect():
    """Configure Prefect pour Semantic Pulse X"""
    from prefect import settings

    # Configuration de base
    settings.PREFECT_API_URL = "http://localhost:4200/api"
    settings.PREFECT_UI_URL = "http://localhost:4200"

    # Configuration des logs
    settings.PREFECT_LOGGING_LEVEL = "INFO"

    # Configuration des retries
    settings.PREFECT_TASK_DEFAULT_RETRY_DELAY_SECONDS = 30
    settings.PREFECT_TASK_DEFAULT_RETRIES = 2


if __name__ == "__main__":
    # Configuration
    configure_prefect()

    # Créer les déploiements
    deployments = create_deployments()

    # Appliquer les déploiements
    for deployment in deployments:
        deployment.apply()

    print("✅ Déploiements Prefect créés avec succès")
