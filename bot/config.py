import os

from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
BOT_DEEPLINK = "t.me/***?start="

# mongodb
MONGO_HOST = str(os.getenv("MONGO_HOST"))

ADMIN_CHAT = int(os.getenv("ADMIN_CHAT"))
admins = [
    int(os.getenv("ADMINS"))
]