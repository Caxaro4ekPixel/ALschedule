import asyncio
from datetime import datetime

from asuna_bot.api.nya.rss_feed import RssFeed
from asuna_bot.db.mongo import mongo
from asuna_bot.db.odm.episode import Episode
from asuna_bot.db.odm.torrent import MongoTorrent
from asuna_bot.db.odm.release import Release
from asuna_bot.main.chat_control import ChatControl


async def main():
    rss = RssFeed(180)
    await rss.run_polling()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())