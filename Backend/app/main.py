import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import urls
from dotenv import load_dotenv

load_dotenv()
FRONT_DOMAIN = os.getenv("SHORTYFY_FRONT_DOMAIN")

origins = ["http://localhost:5173"]
if FRONT_DOMAIN is not None:
    origins.append(FRONT_DOMAIN)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(urls.router)