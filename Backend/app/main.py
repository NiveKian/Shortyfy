from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import urls

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://dominio-NIVE.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(urls.router)