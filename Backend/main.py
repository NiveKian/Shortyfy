from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os, random, string

# Carrega variáveis do arquivo .env
load_dotenv() 
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# Conecta com SSL
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode":"require"}
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI() # Cria e executa a API

class URL(Base):
    __tablename__ = "urls"
    short_id = Column(String, primary_key=True, index=True)
    original_url = Column(String)

Base.metadata.create_all(bind=engine)

class URLRequest(BaseModel):
    url: str

# Gera strings para servir de URL curtas
def generate_short_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.post("/shortyfy")
def shorten_url(request: Request, url_request: URLRequest):
    db = SessionLocal()
    
    # Verifica se já existe essa URL
    existing = db.query(URL).filter(URL.original_url == url_request.url).first()
    if existing:
        return {"short_url": f"{str(request.base_url)}{existing.short_id}"}
    
    # Gera short_id único
    while True:
        short_id = generate_short_id()
        if not db.query(URL).filter(URL.short_id == short_id).first():
            break
    
    url = URL(short_id=short_id, original_url=url_request.url)
    db.add(url)
    db.commit()
    db.refresh(url)
    return {"short_url": f"{str(request.base_url)}{short_id}"}

@app.get("/{short_id}")
def redirect_url(short_id: str):
    db = SessionLocal()
    url = db.query(URL).filter(URL.short_id == short_id).first()
    if url:
        return {"redirect": url.original_url}
    raise HTTPException(status_code=404, detail="URL não encontrada")
