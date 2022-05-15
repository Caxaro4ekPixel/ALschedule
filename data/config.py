import os

from dotenv import load_dotenv

load_dotenv()

ip = os.getenv("ip")

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
BOT_DEEPLINK = "t.me/***?start="

# mongodb
MONGO_HOST = str(os.getenv("DB_HOST"))
MONGO_DB_NAME = str(os.getenv("DB_NAME"))