from fastapi import FastAPI

from app.api.v1.endpoints.messages import router
from app.core.log_file import log_request
from app.core.metrics import metrics_app
from app.db.session import create_database
from app.db.session import init_db

app = FastAPI(title="Simple messenger")

app.middleware("http")(log_request)

app.include_router(router, prefix="/api/v1")

app.mount("/metrics", metrics_app)


@app.on_event("startup")
async def startup():
      # Импортируем новый код
    await create_database()
    await init_db()