"""
Métriques Prometheus - Semantic Pulse X
Monitoring des performances et de la qualité
"""

import time
from collections.abc import Callable
from functools import wraps

from prometheus_client import Counter, Gauge, Histogram, Summary, start_http_server

# Métriques principales
emotion_processing_total = Counter(
    'emotion_processing_total',
    'Total number of emotions processed',
    ['emotion', 'source']
)

emotion_processing_duration = Histogram(
    'emotion_processing_duration_seconds',
    'Time spent processing emotions',
    ['emotion']
)

data_ingestion_total = Counter(
    'data_ingestion_total',
    'Total data ingested',
    ['source', 'status']
)

api_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

api_request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

active_connections = Gauge(
    'active_connections',
    'Number of active connections'
)

memory_usage = Gauge(
    'process_resident_memory_bytes',
    'Process memory usage in bytes'
)

# Métriques IA
ai_model_accuracy = Gauge(
    'ai_model_accuracy',
    'AI model accuracy',
    ['model_type']
)

ai_processing_time = Summary(
    'ai_processing_time_seconds',
    'AI processing time',
    ['model_type']
)

# Métriques de qualité des données
data_quality_score = Gauge(
    'data_quality_score',
    'Data quality score (0-1)',
    ['source']
)

anonymization_rate = Gauge(
    'anonymization_rate',
    'Rate of successful anonymization',
    ['source']
)


def track_emotion_processing(emotion: str, source: str):
    """Track emotion processing"""
    emotion_processing_total.labels(emotion=emotion, source=source).inc()


def track_data_ingestion(source: str, status: str):
    """Track data ingestion"""
    data_ingestion_total.labels(source=source, status=status).inc()


def track_api_request(method: str, endpoint: str, status: str, duration: float):
    """Track API request"""
    api_requests_total.labels(method=method, endpoint=endpoint, status=status).inc()
    api_request_duration.labels(method=method, endpoint=endpoint).observe(duration)


def track_ai_processing(model_type: str, duration: float, accuracy: float = None):
    """Track AI processing"""
    ai_processing_time.labels(model_type=model_type).observe(duration)
    if accuracy is not None:
        ai_model_accuracy.labels(model_type=model_type).set(accuracy)


def track_data_quality(source: str, score: float):
    """Track data quality"""
    data_quality_score.labels(source=source).set(score)


def track_anonymization(source: str, success_rate: float):
    """Track anonymization success rate"""
    anonymization_rate.labels(source=source).set(success_rate)


def monitor_emotion_processing(func: Callable) -> Callable:
    """Decorator to monitor emotion processing"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()

        try:
            result = func(*args, **kwargs)

            # Track success
            if hasattr(result, 'emotion_principale'):
                track_emotion_processing(
                    result.emotion_principale,
                    kwargs.get('source', 'unknown')
                )

            return result

        except Exception as e:
            # Track error
            track_emotion_processing('error', kwargs.get('source', 'unknown'))
            raise e

        finally:
            duration = time.time() - start_time
            emotion_processing_duration.labels(emotion='unknown').observe(duration)

    return wrapper


def monitor_api_request(func: Callable) -> Callable:
    """Decorator to monitor API requests"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        status = '200'

        try:
            result = func(*args, **kwargs)
            return result

        except Exception as e:
            status = '500'
            raise e

        finally:
            duration = time.time() - start_time
            track_api_request('GET', func.__name__, status, duration)

    return wrapper


def start_metrics_server(port: int = 8000):
    """Start Prometheus metrics server"""
    start_http_server(port)
    print(f"✅ Serveur de métriques démarré sur le port {port}")


def update_system_metrics():
    """Update system-level metrics"""
    import os

    import psutil

    # Memory usage
    process = psutil.Process(os.getpid())
    memory_usage.set(process.memory_info().rss)

    # Active connections (simulation)
    active_connections.set(10)  # Placeholder


# Fonction utilitaire pour mettre à jour les métriques
def update_metrics():
    """Update all metrics"""
    update_system_metrics()

    # Mettre à jour d'autres métriques si nécessaire
    pass
