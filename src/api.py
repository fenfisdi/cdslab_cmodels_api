from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from src.config import settings
from src.routers.main import main_router

app = FastAPI()

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.get("ALLOWED_HOSTS", "*").split(",")
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=settings.get("ALLOWED_ORIGINS", "*").split(","),
    allow_methods=settings.get("ALLOWED_METHODS", "*").split(","),
    allow_headers=settings.get("ALLOWED_HEADERS", "*").split(",")
)

app.include_router(
    main_router,
    tags=["Main"],
)
