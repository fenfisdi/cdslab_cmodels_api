from os import environ

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import PlainTextResponse

from src.config import fastApiConfig
from src.db.mongo import MongoEngine
from src.routes import ins_routes, model_routes, root_routes, simulation_routes
from src.services import ErrorAPI

db = MongoEngine().get_connection()
app = FastAPI(**fastApiConfig)


@app.exception_handler(Exception)
def http_error_report(_, exc: Exception):
    ErrorAPI.report_error(str(exc), code=500)
    return PlainTextResponse("Internal Server Error", status_code=500)


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
