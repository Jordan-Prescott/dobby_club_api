from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    
    import os
    from supabase import create_client, Client

    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")

    supabase: Client = create_client(url, key)

    data = supabase.table("characters").select("*").execute()
    
    return data