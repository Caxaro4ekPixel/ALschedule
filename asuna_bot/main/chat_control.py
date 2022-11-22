from aiogram import Bot
from typing import List
from loguru import logger as log
from asuna_bot.api.nya.model import NyaaTorrent
from asuna_bot.db.mongo import mongo
from asuna_bot.db.odm.chat import MongoChat
from aiogram import html

from asuna_bot.db.odm.torrent import MongoTorrent

SITE_URL = "https://www.anilibria.tv/release/"
BACK_URL = "https://backoffice.anilibria.top/resources/release-resources/"

class Chat:
    def __init__(self, chat_id: int) -> None:
        self._chat_id = chat_id
        self._chat: MongoChat = mongo.get_chat(chat_id)
        self._torrents: List[NyaaTorrent] = []
    

    def nyaa_update(self, torrents: List[NyaaTorrent]) -> None:
        self._torrents = torrents
        for t in torrents:
            mongo.add_torrent_to_episode(self._chat_id, MongoTorrent(
                id=t.id,
                submitter=t.submitter,
                serie=t.serie,
                quality=t.quality,
                url=t.url,
                file_url=t.file_url,
                magnet=t.magnet,
                size=t.size,
                title=t.title,
                type=t.type,
                category=t.category,
                seeders=t.seeders,
                leechers=t.leechers,
                downloads=t.downloads,
                date=t.date
            ))
    

    def dispatch_torrents(self) -> NyaaTorrent:
        fhd, hd, sd = None

        for torrent in self._torrents:
            match torrent.quality:
                case "1080p":
                    fhd = torrent
                case "720p":
                    hd = torrent
                case "480p":
                    sd = torrent

        return fhd, hd, sd


    async def form_message_text(self) -> str:
        release = self._chat.release
        episode = release.episodes[-1]
        fhd, hd, sd = self.dispatch_torrents()

        text = [
            f"{release.ru_title} / {release.en_title}",
            f"Эпизод {episode.number} / {release.total_ep}",
            "",
        ]

        if fhd: 
            text += [f"{html.link('[1080p] ' + fhd.size, fhd.file_url)} — {html.link('🧲', fhd.magnet)}",]    

        if self._chat.config.medium_quality:
            if hd: 
                text += [f"{html.link('[720p] ' + hd.size, hd.file_url)} — {html.link('🧲', hd.magnet)}",]

        if sd:
            text += [f"{html.link('[480p] ' + sd.size, sd.file_url)} — {html.link('🧲', sd.magnet)}",]  

        text += [
            f"{html.link('❤️Сайт❤️', SITE_URL+release.code+'.html')} / {html.link('🖤Админка🖤', BACK_URL+release._id)}",
            "",
            f"Дедлайн: {episode.deadline_at}",
        ]
        
        return "\n".join(text)
