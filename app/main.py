import asyncio
import os
from fastapi import FastAPI # type: ignore
from app.routes import news
from app.telegram_client import start_client , stop_client
from apscheduler.schedulers.asyncio import AsyncIOScheduler # type: ignore
from app.services.news_service import refresh_news

app = FastAPI(titlr = "Telegram News API")
FETCH_INTERVAL_MIN = int(os.getenv("FETCH_INTERVAL_MIN", "30"))
# Register routes
app.include_router(news.router)

scheduler = AsyncIOScheduler()

async def scheduled_fetch():
    # Fetch messages from all channels with delay between them
    await refresh_news()
        
@app.on_event("startup")
async def startup_event():
    await start_client()
    asyncio.create_task(refresh_news())
    scheduler.add_job(scheduled_fetch, "interval", minutes=FETCH_INTERVAL_MIN)
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    await stop_client()
    scheduler.shutdown()