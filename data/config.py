import os

from dotenv import load_dotenv

load_dotenv()

ip = os.getenv("ip")

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
BOT_DEEPLINK = "t.me/***?start="


log_chat_id = os.getenv("LOG_CHAT_ID")
admins = [
    int(os.getenv("ADMIN_ID")),
]

# mongodb
MONGO_HOST = str(os.getenv("DB_HOST"))
MONGO_PORT = int(os.getenv("DB_PORT"))
MONGO_DB_NAME = str(os.getenv("DB_NAME"))