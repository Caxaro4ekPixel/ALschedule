import asyncio
from aiohttp import ClientSession, ClientConnectorError
from typing import List
# from fuzzywuzzy import fuzz
from loguru import logger as log

# from asuna_bot.db.mongo import mongo
# from asuna_bot.db.odm.chat import Chat

from .model import NyaaTorrent
from .rss_parser import rss_to_json
from .errors import HTTPException


class RssFeed:
    def __init__(self, interval) -> None:
        self._chats = set()
        self._session = ClientSession()
        self._interval = interval
        self._last_id = 0 
        
        self.running = True
        
        self._base_url = 'https://nyaa.si/?'
        self._params = {
            "page": "rss",
            "q": "",
            "c": "0_0",
            "f": "0"
        }


    def register(self, chat) -> None:
        self._chats.add(chat)

    def unregister(self, chat) -> None:
        self._chats.discard(chat)

    def push_update(self, torrents) -> None:
        for chat in self._chats:
            chat.nyaa_update(torrents)
            # for torrent in torrents:
            #     ratio = fuzz.partial_ratio(chat.release.en_title, torrent.title)
            #     if ratio > 75:
            #         chat.nyaa_update(torrent)


    async def _request(self, url: str, params: dict = None, limit=None):
        log.debug(f"Send GET request to {url} with data: {params}")
        try:
            response = await self._session.get(url, params=params, timeout=30)
            raw = await response.text()
        except ClientConnectorError as ex:
            log.error(ex)
            return None

        try:
            json = rss_to_json(raw, limit=limit)
        except Exception as ex:
            json = raw
            log.debug(ex)
        
        log.debug(f"Got response from request {json}")
        self.__catch_error(json)
        return json


    def __catch_error(self, data: dict):
        if not isinstance(data, dict):
            return
        if error := data.get("error"):
            raise HTTPException(error["code"], error["message"])
        if data.get("err"):
            raise HTTPException(0, data["mes"])


    async def run_polling(self):
        """Поллинг rss ленты"""
        while self.running:
            parsed_rss = await self._request(self._base_url, params=self._params, limit=10)
            
            if parsed_rss == None:
                await asyncio.sleep(self._interval)
                continue
            
            # TODO берем id из бд
            if int(parsed_rss[0].get("id")) <= self._last_id:
                log.info("Нет новых торрентов")
                 
            else:
                torrents = [NyaaTorrent(**torrent) for torrent in parsed_rss]
                self.push_update(torrents) # Делаем пуш чатам
                self._last_id = int(parsed_rss[0].get("id")) # TODO добавлять id В базу
            
            await asyncio.sleep(self._interval)


