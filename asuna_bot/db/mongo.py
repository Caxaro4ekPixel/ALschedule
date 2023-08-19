import datetime
from typing import List
from .odm import *
from beanie import Set, AddToSet

class Mongo:
    async def get_all_user_ids(self) -> List:
        return await User.find_all().to_list()

    async def get_chat(self, chat_id: int):
        return await Chat.find_one(Chat.id == chat_id)
    
    async def get_all_ongoing_chats():
        ongoings = await Release.find_all(Release.is_ongoing == True)
        return [ongoing.chat_id for ongoing in ongoings]



    async def get_release(self, release_id: int):
        return await Release.find_one(Release.id == release_id)

    
    async def get_bot_conf(self):
        return await BotConfig.find({}).first_or_none()


    async def get_nyaa_rss_last_id(self) -> int:
        return await self.get_bot_conf().nyaa_rss_last_id


    async def add_chat(self, chat_id: int, name: str):
        new_chat = Chat(id=chat_id, name=name, release=None)
        await new_chat.create()


    async def add_release(self, release_id: int, chat_id: int, ru_title: str, 
                          en_title: str, code: str, season: str):
        
        new_release = Release(id=release_id, chat_id=chat_id, code=code, 
                              en_title=en_title, ru_title=ru_title, season=season)
        await new_release.create()
        await Chat.find_one(Chat.id == chat_id).update(Set({Chat.release: new_release}))


    async def add_episode(self, release_id: int, series_num: int, status: str,
                         released_at: datetime, deadline_at: datetime):
        
        release = await Release.find_one(Release.id == release_id)
        new_episode = Episode(series_num=series_num, status=status, 
                              released_at=released_at, deadline_at=deadline_at,
                              release=release)
        await new_episode.create()

    
    async def add_torrent_to_episode(self, release_id: int, ep_num, torrent):
        release = await self.get_release(release_id)
        await Episode.find_one(release=release).update(AddToSet({Episode.torrents : torrent}))

    
    async def add_user(self, id: int, full_name: str, user_name: str, role: list[str]):
        new_user = User(id=id, full_name=full_name, user_name=user_name, role=role)
        await new_user.create()


    async def update_chat_conf(self, chat_id: int, **settings):
        for key, val in settings.items():
            await Chat.find_one(Chat.id == chat_id).update({"$set": {f"chats.config.{key}" : val}})


    async def update_bot_conf(self, **settings):
        for key, val in settings.items():
            await BotConfig.find({}).update({"$set": {f"bot_config.{key}" : val}})


mongo = Mongo()
