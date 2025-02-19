from prometheus_client import Counter
from prometheus_client import Histogram
from prometheus_client import make_asgi_app

# Счётчик запросов
REQUEST_COUNT = Counter(
    "request_count", "Total number of requests", ["method", "endpoint", "status_code"]
)
# Гистограмма для замера времени обработки запросов
REQUEST_LATENCY = Histogram(
    "request_latency_seconds", "Request latency in seconds", ["method", "endpoint"]
)
# Создание приложения для экспорта метрик
metrics_app = make_asgi_app()