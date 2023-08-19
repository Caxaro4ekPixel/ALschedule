from aiogram import Bot
from typing import List
from loguru import logger as log
from asuna_bot.api.nya.model import NyaaTorrent
from asuna_bot.db.mongo import mongo
from aiogram import html
from thefuzz import fuzz

from asuna_bot.db.odm import Chat, Release
from asuna_bot.db.odm.episode import Episode, Torrent

SITE_URL = "https://www.anilibria.tv/release/"
BACK_URL = "https://backoffice.anilibria.top/resources/release-resources/"

class ChatControl:
    async def __init__(self, chat_id: int) -> None:
        self._chat_id = chat_id
        self._chat: Chat = await mongo.get_chat(chat_id)
        self._release_id = self._chat.release.id
        self._release: Release = await mongo.get_release(self._release_id)

        self._torrents: List[NyaaTorrent] = []
    

    async def add_new_ep(self, torrent):
        if self._release.episodes[-1] == torrent.serie:
            return print("Эпизод уже существует")
        
        await mongo.add_episode(self._release_id, Episode(
                number=torrent.serie,
                released_at=torrent.date,
                status="Just released"
            ))
        print("Добавили новый эпизод")
        
        #TODO: поддтягивать эпизоды с лайфчарта


    def nyaa_update(self, torrents: List[NyaaTorrent]) -> None:
        for torrent in torrents:
            self._torrents.clear()
            s1 = f"[{self._chat.config.submitter}] {self._chat.release.en_title}"

            if self._chat.config.submitter in torrent.submitter:
                ratio = fuzz.partial_ratio(s1, torrent.title)
                log.debug(f"comparing: {s1} AND {torrent.title}; ratio={ratio}")
                if ratio > 75:
                    
                    self.add_new_ep(torrent)

                    self._torrents.append(torrent)
                    mongo.add_torrent_to_episode(self._release_id, torrent.serie, Torrent(**torrent))   
    

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


    def craft_message_text(self) -> str:
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

        if self._chat.config.show_hd:
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
