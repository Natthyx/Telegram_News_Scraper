from telethon import TelegramClient # type: ignore
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone_no = os.getenv("PHONE_NUMBER")
session_dir = "session"
os.makedirs(session_dir, exist_ok=True)
session_path = os.path.join(session_dir, "anon.session")

client = TelegramClient(session_path, api_id, api_hash)

async def start_client():
    await client.start(phone_no)
    print("Telegram client started")
    return client
async def stop_client():
    await client.disconnect()
    print("Telegram client stopped")
    

