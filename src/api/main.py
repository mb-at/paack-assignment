from fastapi import FastAPI
from src.api.routers import router
from src.config import settings

app = FastAPI(
    title=settings.app_name,
    version="1.0.0"
)

app.include_router(router)


@app.get("/health", status_code=200)
async def healthcheck():
    """
    Healthcheck endpoint. Used to quickly verify
    that the server is up and running.
    """
    return {"status": "ok"}