from typing import List
from mongoengine import connect
from .odm.release import Release
from .odm.chat import Chat
from .odm.episode import Episode
from .odm.user import User
from asuna_bot.config import CONFIG


class Mongo():
    def __init__(self) -> None:
        connect(host=CONFIG.db.connection_string)

    def get_chat(self, chat_id: int) -> Chat:
        return Chat.objects.get(_id=chat_id)
        

    def add_chat(self, _id: int, name: str) -> Chat:
        return Chat(_id=_id, name=name).save()


    def add_release_to_chat(self, _id: int, chat: Chat, 
                            ru_title: str, en_title: str, code: str) -> Release:
        return Release(_id=_id, chat_id=chat._id, 
                    ru_title=ru_title, en_title=en_title, code=code).save()


    def add_new_episode(self, release: Release, chat: Chat) -> Episode:
        pass


    def add_user(self, _id: int, full_name: str, user_name: str) -> User:
        return User(_id=_id, full_name=full_name, user_name=user_name).save()


    def get_all_user_ids(self) -> List:
        return [user._id for user in User.objects]


    def update_config(self, chat_id: int, **settings):
        chat = Chat.objects.get(_id=chat_id)
        update_dict = {}
        for key, val in settings.items():
            update_dict.update({f"set__config__{key}": val})

        chat.update(**update_dict)


mongo = Mongo()