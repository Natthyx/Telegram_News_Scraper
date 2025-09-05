# app/services/chroma_service.py
from typing import Dict, Optional
from datetime import datetime
import asyncio
from app.db import news_collection, last_message_collection
from app.utils.language import detect_language
import logging

logger = logging.getLogger(__name__)

class ChromaDBService:
    def __init__(self):
        self.news_collection = news_collection
        self.last_message_collection = last_message_collection

    # -------------------------------
    # Last Message ID Handling
    # -------------------------------
    async def get_last_message_id(self, channel: str) -> Optional[int]:
        res = await asyncio.to_thread(
            self.last_message_collection.get,
            ids=[channel],
            include=["metadatas"]
        )
        if res and res.get("ids"):
            md = (res.get("metadatas") or [{}])[0]
            return md.get("last_id")
        return None

    async def set_last_message_id(self, channel: str, message_id: int):
        try:
            await asyncio.to_thread(
                self.last_message_collection.upsert,
                ids=[channel],
                documents=["last_id_placeholder"],  # REQUIRED
                metadatas=[{"channel": channel, "last_id": int(message_id)}]
            )
            logger.info(f"Updated last message ID for {channel}: {message_id}")
        except Exception as e:
            logger.error(f"Failed to update last message ID for {channel}: {e}")


    # -------------------------------
    # Article Handling
    # -------------------------------
    async def add_article(self, article: Dict):
        """
        Upsert a single article into ChromaDB. 
        Ensures documents is non-empty.
        """
        text = f"{article.get('title', '')} {article.get('content', '')}".strip()
        if not text:
            logger.warning(f"Skipped empty article: {article.get('_id')}")
            return

        metadata = {
            "title": article.get("title"),
            "source_url": article.get("source_url"),
            "source_site": article.get("source_site"),
            "source_type": article.get("source_type"),
            "published_date": article.get("published_date"),
            "crawl_timestamp": article.get("crawl_timestamp", datetime.utcnow().isoformat()),
            "lang": article.get("lang", detect_language(text))
        }

        try:
            # Wrap blocking add call in asyncio.to_thread
            await asyncio.to_thread(
                self.news_collection.add,
                ids=[article["_id"]],
                documents=[text],
                metadatas=[metadata]
            )
            logger.info(f"Stored in ChromaDB: {article.get('title')} (ID: {article.get('_id')})")
        except Exception as e:
            logger.error(f"Failed to add article {article.get('title')}: {e}")
