from fastapi import APIRouter
from app.services.news import get_news

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/digest")
async def digest():
    news = await get_news()
    return {"digest": news}