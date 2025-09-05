import asyncio
from fastapi import APIRouter , Query # type: ignore
from typing import List
from app.services.news_service import fetch_channel_news, get_news_by_source_type, get_news_from_db, refresh_news
from app.config import CHANNELS

router = APIRouter(prefix="/news", tags=["News"])

@router.get("/")
async def get_news(limit: int = 20):
    """
    Get latest saved news from the DB (sorted by date desc).
    Optional topic filter.
    """
    return await get_news_from_db(limit)

@router.get("/refresh")
async def refresh():
    """
    Manually pull from all channels (runs sequentially with backoff delay).
    """
    return await refresh_news()
    
@router.get("/source")
async def news_by_source_endpoint(source_type: str = Query(...), limit: int = 20):
    return await get_news_by_source_type(source_type, limit)