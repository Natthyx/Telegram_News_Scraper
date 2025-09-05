import os
import chromadb # type: ignore
# from chromadb.config import Settings  # type: ignore # noqa: F401 (kept for future tuning)
import os
from dotenv import load_dotenv # type: ignore
load_dotenv()
CHROMA_PATH = os.getenv("CHROMA_PATH")

# Create Chroma persistent client
client = chromadb.CloudClient(
            api_key=os.getenv("CHROMA_DB_API_KEY"),
            tenant=os.getenv("CHROMA_DB_TENANT"),
            database=os.getenv("CHROMA_DB")
        )

# Collections
news_collection = client.get_or_create_collection(
    name="news_articles",
)

last_message_collection = client.get_or_create_collection(
    name="last_message_tracker",
)
