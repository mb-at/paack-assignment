import os
import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from src.logger import setup_logging
from src.api.routers import router, repository
from src.config import settings
from src.domain.entities import Package

log_path = os.getenv("LOG_FILE", "logs/app.log")

# Make sure the folder exists
os.makedirs(os.path.dirname(log_path), exist_ok=True)

#We configure logging: console + file
setup_logging(log_file=log_path)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan manager. Runs before the server boots and allows for initialization tasks (preload).
    """
    # Startup: precharge memory packages
    logger.info("Starting up: preloading packages into memory")
    packages_to_preload = [
        Package(customer_address=addr)
        for addr in settings.preload_addresses
    ]

    await repository.preload_packages(packages_to_preload)
    logger.info(
        "Finished preloading %d packages", len(settings.preload_addresses)
    )

    yield

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Captures validation errors (HTTP 422) produced by Pydantic,
    logs them with logger.error(), and returns the JSON response in the same format.
    """

    # Log validation error with details of failed fields
    logger.error(
        "Validation error for request %s %s: %s",
        request.method,
        request.url.path,
        exc.errors(),
    )

    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

app.include_router(router)

@app.get("/health", status_code=200)
async def healthcheck():
    """
    Healthcheck endpoint. Used to quickly verify
    that the server is up and running.
    """
    logger.info("Healthcheck requested")
    return {"status": "ok"}