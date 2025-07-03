from fastapi import APIRouter
from app.services.newsapi_client import NewsAPIClient

router = APIRouter()
newsapi_client = NewsAPIClient()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/digest")
async def digest():
    news = await newsapi_client.get_top_headlines()
    return {"digest": news}