import asyncio
from asuna_bot.api.nya.rss_client import RssClient
from asuna_bot.api.nya.rss_feed import RssFeed
from asuna_bot.db.mongo import mongo

async def main():
    rss = RssFeed(180)
    chat1 = RssClient(123456789)
    chat2 = RssClient(455323443)

    rss.register(chat1)
    rss.register(chat2)


    await rss.run_polling()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())