from typing import List
from mongoengine import connect

from asuna_bot.config import CONFIG
from asuna_bot.db.odm.bot_conf import BotConfig
from asuna_bot.db.odm.chat import MongoChat
from asuna_bot.db.odm.episode import Episode
from asuna_bot.db.odm.release import Release
from asuna_bot.db.odm.user import User


class Mongo:
    def __init__(self) -> None:
        connect(host=CONFIG.db.connection_string)
    
    def get_chat_by_title_id(title_id):
        return MongoChat.objects(release=title_id).first()


    def get_all_active_chats(self) -> List:
        return [release.chat_id for release in Release.objects(is_ongoing=True)]


    def get_all_user_ids(self) -> List:
        return [user._id for user in User.objects]


    def get_chat(self, chat_id: int) -> MongoChat:
        return MongoChat.objects.get(_id=chat_id)
        

    def add_chat(self, _id: int, name: str) -> MongoChat:
        return MongoChat(
            _id=_id, 
            name=name, 
            release=None
        ).save()


    def add_release_to_chat(self, _id: int, chat_id: int, 
                            ru_title: str, en_title: str, code: str) -> Release:
        chat = self.get_chat(chat_id)
        chat.release = Release(
            _id=_id, 
            chat_id=chat_id, 
            ru_title=ru_title, 
            en_title=en_title, 
            code=code
        )
        chat.save(cascade=True)


    def add_episode_to_release(self, chat_id: int, new_ep: Episode):
        chat = self.get_chat(chat_id)
        Release.objects(_id=chat.release._id).update_one(push__episodes=new_ep)

    
    def add_torrent_to_episode(self, chat_id: int, torrent):
        chat = self.get_chat(chat_id)
        release = Release.objects(_id=chat.release._id).first()
        release.episodes[-1].torrents.append(torrent)
        release.save()

    
    def add_user(self, _id: int, full_name: str, user_name: str):
        User(
            _id=_id, 
            full_name=full_name, 
            user_name=user_name
        ).save()


    def update_config(self, chat_id: int, **settings):
        chat = MongoChat.objects.get(_id=chat_id)
        update_dict = {}
        for key, val in settings.items():
            update_dict.update({f"set__config__{key}": val})

        chat.update(**update_dict)


    def update_rss_interval(self, interval):
        BotConfig(rss_interval=interval).save()


    def update_rss_last_id(self, last_id):
        BotConfig(rss_last_id=last_id).save()


mongo = Mongo()
