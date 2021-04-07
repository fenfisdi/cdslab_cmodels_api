from dotenv import dotenv_values
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

settings = dotenv_values(".env")

app.add_middleware(
    TrustedHostMiddleware,
    allow_hosts=settings["ALLOWED_HOSTS"].split(",")
    )

app.add_middleware(
    CORSMiddleware,
    allow_credentials=settings["ALLOW_CREDENTIALS"],
    allow_origins=settings["ALLOWED_ORIGINS"].split(","),
    allow_methods=settings["ALLOWED_METHODS"].split(","),
    allow_headers=settings["ALLOWED_HEADERS"].split(",")
    )