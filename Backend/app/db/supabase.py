import os
from supabase import Client, create_client
from supabase.client import ClientOptions
from dotenv import load_dotenv

# Carrega o .env que está fora da pasta /app
load_dotenv()
DATABASE_URL = os.getenv("dburl")
DATABASE_KEY = os.getenv("dbkey")

if DATABASE_URL is None or DATABASE_KEY is None:
    raise ValueError("DBURL/DBKEY not found")

api_url: str = DATABASE_URL
key: str = DATABASE_KEY

def create_supabase_client():
    supabase: Client = create_client(
        api_url,
        key,
        options=ClientOptions(
            postgrest_client_timeout=10,
            storage_client_timeout=10,
            schema="public",
        )
    )
    return supabase
