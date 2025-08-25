from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from app.db.supabase import create_supabase_client
import random, string

app = FastAPI() # Cria e executa a API
print("OK: API CREATED")

supabase = create_supabase_client() # Cria conexão com DB Supabase
print("OK: SUPABASE CONECTOR")

class URLRequest(BaseModel):
    url: str

# Gera strings para servir de URL curtas
def generate_short_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.post("/shortyfy")
def shorten_url(request: Request, url_request: URLRequest):
    try:
        # Verifica se já existe essa URL
        response = (
            supabase.table("urls")  # type: ignore
            .select("*")
            .eq("original_url", url_request.url)
            .limit(1)
            .execute()
        )
        if response.data and len(response.data) > 0:
            existing = response.data[0]
            return {"short_url": f"{str(request.base_url)}{existing['short_id']}"}

        # Gera short_id único
        while True:
            short_id = generate_short_id()
            check = supabase.table("urls").select("*").eq("short_id", short_id).limit(1).execute()
            if not check.data or len(check.data) == 0:
                break

        # Insere no Supabase
        supabase.table("urls").insert({
            "short_id": short_id,
            "original_url": url_request.url
        }).execute()

        return {"short_url": f"{str(request.base_url)}{short_id}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar Supabase: {e}")


@app.get("/{short_id}")
def redirect_url(short_id: str):
    try:
        response = supabase.table("urls").select("*").eq("short_id", short_id).limit(1).execute()
        if response.data and len(response.data) > 0:
            url = response.data[0]
            return {"redirect": url["original_url"]}
        raise HTTPException(status_code=404, detail="URL não encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar Supabase: {e}")