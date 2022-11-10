from dataclasses import dataclass
from environs import Env

@dataclass
class DBConf:
    connection_string: str

@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    admin_chat: int

@dataclass
class Miscellaneous:
    al_url: str = "https://api.anilibria.tv/v2/"
    nyaa_url: str = "https://nyaa.si/"

@dataclass
class Config:
    bot: TgBot
    db: DBConf
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    scheme=env.str('MONGO_SCHEME')
    host=env.str('MONGO_HOST')
    password=env.str('MONGO_PASSWORD')
    username=env.str('MONGO_USERNAME')
    db_name=env.str('MONGO_DB_NAME')

    return Config(
        bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            admin_chat=env.int("ADMIN_CHAT")
        ),
        db=DBConf(
            connection_string=f"{scheme}://{username}:{password}@{host}/{db_name}"
        ),
        misc=Miscellaneous()
    )

CONFIG = load_config(".env")