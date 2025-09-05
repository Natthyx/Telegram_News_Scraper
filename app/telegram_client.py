from telethon import TelegramClient # type: ignore
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone_no = os.getenv("PHONE_NUMBER")

session_path = os.getenv("SESSION_PATH", "session/anon.session")
client = TelegramClient(session_path, api_id, api_hash)

async def start_client():
    await client.start()
    print("Telegram client started")
    return client
async def stop_client():
    await client.disconnect()
    print("Telegram client stopped")
    

