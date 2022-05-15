import os

from dotenv import load_dotenv

load_dotenv()

ip = os.getenv("ip")

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
BOT_DEEPLINK = "t.me/***?start="
