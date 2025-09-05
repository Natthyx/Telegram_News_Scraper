import asyncio
from datetime import timezone, datetime
import logging
import uuid
from typing import List, Dict
import os
from dotenv import load_dotenv # type: ignore

from app.config import CHANNELS
from app.services.chroma_service import ChromaDBService
from app.telegram_client import client
from app.utils.language import detect_language

logger = logging.getLogger(__name__)
load_dotenv()
chroma_service = ChromaDBService()

async def fetch_channel_news(channel_username:str , limit: int = 2) -> List[Dict]:
    """
    Fetch latest messages from a Telegram channel and store as articles in ChromaDB.
    """
    last_id = await chroma_service.get_last_message_id(channel_username)
    
    messages: List[Dict] = []
    
    async for message in client.iter_messages(channel_username, limit=limit, offset_id=last_id or 0):
        if not getattr(message, "text", None) or not message.text.strip():
            continue
        
        lines = message.text.split("\n", 1)
        title = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ""
        text = f"{title} {body}".strip()
        
        if not text:
            continue  # Skip if combined text is empty
        
        article = {
            "_id": str(uuid.uuid4()),
            "title": title,
            "content": body,
            "source_url": f"https://t.me/{channel_username}/{message.id}",
            "source_site": channel_username,
            "source_type":"Telegram",
            "published_date": message.date.isoformat(),
            "crawl_timestamp": datetime.now(timezone.utc).isoformat(),
            "lang": detect_language(message.text),
            "tg_message_id": message.id
            
        }
        
        try:
            await chroma_service.add_article(article)
            messages.append(article)
            logger.info(f"Fetched and stored article: {title} (ID: {article['_id']})")
        except Exception as e:
            logger.error(f"Failed to add article {article['_id']}: {e}")
            
            
            
    if messages:
        await chroma_service.set_last_message_id(channel_username , messages[-1]["tg_message_id"])
    
    return messages

# app/services/news_service.py

async def get_news_from_db(limit: int = 20):
    """
    Retrieve articles with aligned schema asynchronously.
    """
    results = await asyncio.to_thread(
        chroma_service.news_collection.get,
        include=["metadatas", "documents"],
        limit=limit
    )

    if not results or not results.get("ids"):
        return []

    articles = []
    for i, meta in enumerate(results.get("metadatas", [])):
        articles.append({
            "_id": results["ids"][i],
            "title": meta.get("title"),
            "content": results.get("documents", [])[i],
            "source_url": meta.get("source_url"),
            "source_site": meta.get("source_site"),
            "source_type": meta.get("source_type"),
            "published_date": meta.get("published_date"),
            "crawl_timestamp": meta.get("crawl_timestamp"),
            "lang": meta.get("lang"),
        })

    # Sort by published_date descending
    articles.sort(key=lambda x: x.get("published_date") or "", reverse=True)
    
    return articles

    
async def refresh_news():
    # Manually fetch news from all channels
    for channel in CHANNELS:
        try:
            await fetch_channel_news(channel, limit=15)
            logger.info(f"Fetched news from {channel}")
        except Exception as e:
            logger.error(f"Error fetching from {channel}: {e}")
            
        # wait 2-3 minutes before next channel
        wait_time = int(os.getenv("WAITING_TIME",120))
        print(f"Waiting {wait_time} seconds before next channel")
        logger.info(f"Waiting {wait_time} seconds before next channel")
        await asyncio.sleep(wait_time)

async def get_news_by_source_type(source_type: str, limit: int = 20):
    """
    Retrieve articles filtered by source_type and sorted by published_date descending.
    """
    results = await asyncio.to_thread(
        chroma_service.news_collection.get,
        include=["metadatas", "documents"],
        limit=1000  # fetch more in case we filter out some
    )

    if not results or not results.get("ids"):
        return []

    articles = []
    for i, meta in enumerate(results.get("metadatas", [])):
        if meta.get("source_type") != source_type:
            continue  # skip non-matching source_type
        articles.append({
            "_id": results["ids"][i],
            "title": meta.get("title"),
            "content": results.get("documents", [])[i],
            "source_url": meta.get("source_url"),
            "source_site": meta.get("source_site"),
            "source_type": meta.get("source_type"),
            "published_date": meta.get("published_date"),
            "crawl_timestamp": meta.get("crawl_timestamp"),
            "lang": meta.get("lang"),
        })

    # Sort by published_date descending
    articles.sort(key=lambda x: x.get("published_date") or "", reverse=True)

    return articles[:limit]
