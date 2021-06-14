from os import environ

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from src.config import fastApiConfig
from src.db.mongo import MongoEngine
from src.routes import ins_routes, model_routes, root_routes, simulation_routes

db = MongoEngine().get_connection()
app = FastAPI(**fastApiConfig)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=environ.get("ALLOWED_HOSTS", "*").split(",")
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=bool(environ.get('ALLOWED_CREDENTIALS', '1')),
    allow_origins=environ.get("ALLOWED_ORIGINS", "*").split(","),
    allow_methods=environ.get("ALLOWED_METHODS", "*").split(","),
    allow_headers=environ.get("ALLOWED_HEADERS", "*").split(",")
)

app.include_router(model_routes)
app.include_router(simulation_routes)
app.include_router(ins_routes)
app.include_router(root_routes)
