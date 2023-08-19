import asyncio
from asuna_bot.db.mongo import mongo
import json
from asuna_bot.db.odm import *
from asuna_bot.db.odm.chat import ChatConfig
from asuna_bot.db.odm.release import Episode, Torrent






def create_chat_list():
    new_chats = []
    chat_file = open("C:\\Users\\Admin\\Desktop\\asuna db\\chats.json", encoding='utf8')
    chats = json.load(chat_file)

    for chat in chats:
        chat_id = chat.get("id")
        status = "idle"
        name = chat.get("name")
        release = chat.get("id_relese")

        new_config = ChatConfig()
        new_chat = Chat(id=chat_id, status=status, name=name, config=new_config, release=release)
        new_chats.append(new_chat)
    
    return new_chats


def create_user_list():
    new_users = []
    user_file = open("C:\\Users\\Admin\\Desktop\\asuna db\\team_tg.json", encoding='utf8')
    users = json.load(user_file)
    _id=0

    for user in users:
        full_name = user.get("al_name").strip()
        user_name = user.get("tg_username").strip()

        new_user = User(id=_id, full_name=full_name, user_name=user_name, role=["team"])
        new_users.append(new_user)
        _id += 1

    return new_users


def create_release_list():
    new_releases = []
    release_file = open("C:\\Users\\Admin\\Desktop\\asuna db\\relesAL.json", encoding='utf8')
    releases = json.load(release_file)

    for release in releases:
        _id = release.get("id")
        code = release.get("code")
        en_title = release.get("name_en")
        ru_title = release.get("name_ru")
        total_ep = release.get("series")
        new_release = Release(id=_id, chat_id=0, status="idle", code=code, en_title=en_title, ru_title=ru_title, total_ep=total_ep)
        new_releases.append(new_release)

    return new_releases