from typing import List
from loguru import logger as log
from asuna_bot.api.nya.model import NyaaTorrent
from asuna_bot.db.mongo import mongo
from asuna_bot.db.odm.chat import Chat

class RssClient:
    """Клиент чата"""
    def __init__(self, chat_id: int) -> None:
        self._chat_id = chat_id
        self._chat: Chat = mongo.get_chat(chat_id)
        self._torrents: List[NyaaTorrent] = []
    
    def nyaa_update(self, torrents: List[NyaaTorrent]) -> None:
        chat_name = self._chat.name
        chat_config = self._chat.config.submitter
        log.info(f"{chat_name} {chat_config}")
        self._torrents = torrents
        
    
    def anilibria_update(self) -> None:
        ...

    