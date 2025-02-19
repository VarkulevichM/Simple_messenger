import logging
import time

from fastapi import Request

from app.core.metrics import REQUEST_COUNT
from app.core.metrics import REQUEST_LATENCY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")


async def log_request(request: Request, call_next):
    """
        Логирует информацию о каждом HTTP запросе и ответе, включая:
        - метод запроса
        - URL запроса
        - IP клиента
        - статус код ответа
        - размер ответа
        - время обработки запроса
    """

    logger.info(f"Request: {request.method} {request.url}")
    logger.info(f"Client: {request.client.host}")

    start_time = time.time()

    response = await call_next(request)
    end_time = time.time() - start_time

    logger.info(f"Response status: {response.status_code}")
    logger.info(f"Response size: {response.headers.get("content-length")} bytes")
    logger.info(f"Process time: {end_time:.2f} seconds")

    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path,
                         status_code=response.status_code).inc()
    REQUEST_LATENCY.labels(method=request.method,
                           endpoint=request.url.path).observe(end_time)

    return response
