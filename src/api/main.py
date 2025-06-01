from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.api.routers import router, repository  
from src.config import settings
from src.domain.entities import Package

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan manager. Runs before the server boots and allows for initialization tasks (preload).
    """
    # Startup: precharge memory packages
    packages_to_preload = [
        Package(customer_address=addr)
        for addr in settings.preload_addresses
    ]

    await repository.preload_packages(packages_to_preload)
    yield

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)

@app.get("/health", status_code=200)
async def healthcheck():
    """
    Healthcheck endpoint. Used to quickly verify
    that the server is up and running.
    """
    return {"status": "ok"}