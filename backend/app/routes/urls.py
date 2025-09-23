from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from app.db.supabase import create_supabase_client
from app.models.url_request import URLRequest
from app.utils.shortener import generate_short_id

router = APIRouter()
supabase = create_supabase_client()
print("OK: SUPABASE CONNECTOR")

@router.post("/shorten")
def shorten_url(request: Request, url_request: URLRequest):
    try:
        # Verifica se a URL já foi encurtada
        response = (
            supabase.table("urls")
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
            check = (
                supabase.table("urls")
                .select("*")
                .eq("short_id", short_id)
                .limit(1)
                .execute()
            )
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

@router.get("/{short_id}")
def redirect_url(short_id: str):
    try:
        response = (
            supabase.table("urls")
            .select("*")
            .eq("short_id", short_id)
            .limit(1)
            .execute()
        )
        
        if response.data and len(response.data) > 0:
            url = response.data[0]["original_url"]
            return RedirectResponse(url)

        raise HTTPException(status_code=404, detail="URL não encontrada")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar Supabase: {e}")
