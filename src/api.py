from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from src.config import settings


app = FastAPI()


app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings["ALLOWED_HOSTS"].split(",")
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=settings["ALLOWED_ORIGINS"].split(","),
    allow_methods=settings["ALLOWED_METHODS"].split(","),
    allow_headers=settings["ALLOWED_HEADERS"].split(",")
)
