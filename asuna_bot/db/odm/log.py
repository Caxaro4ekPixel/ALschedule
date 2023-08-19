from beanie import Document, Link
from .chat import Chat
from .user import User
from datetime import datetime


class Log(Document):
    date   : datetime
    action : str
    status : str
    msg    : str
    user   : Link[User]
    chat   : Link[Chat]

    class Settings:
        name = "logs"