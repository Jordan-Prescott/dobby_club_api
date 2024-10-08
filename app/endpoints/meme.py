import logging

from fastapi import APIRouter, HTTPException, Query, Request
from typing import List, Optional

from ..db.supabase import SupabaseClient
from ..schemas.meme import Meme
from ..dependancies.rate_limiter import limiter

router = APIRouter(prefix="/memes", tags=["meme"])
db = SupabaseClient().get_client()
logger = logging.getLogger("app")

@router.get("/", response_model=List[Meme])
@limiter.limit("5/second")
async def get_memes(
    request: Request,
    file_name: Optional[str] = Query(None, example="everythings-cool-in-dobby-club")    
    ) -> List[Meme]:
    
    query = db.table("meme_metadata").select(
        "file_name, file_type, file_url"
    )
    
    if file_name:
        query = query.eq("file_name", file_name)
    
    try:
        response = query.execute()
    except Exception as e:
        logger.error(f"Query failed with error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Meme not found")
    
    return [
        Meme(**meme) for meme in response.data
    ]
    
    
@router.get("/random/", response_model=Meme)
@limiter.limit("5/second")
async def get_random_meme(
    request: Request
    ) -> Meme:
    
    import random
    
    query = db.table("meme_metadata").select(
        "file_name, file_type, file_url"
    )
    
    try: 
        response = query.execute()
    except Exception as e:
        logger.error(f"Query failed with error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Meme not found")
    
    return Meme(**random.choice(response.data))