from beanie import Document, Link
from typing import Optional
from .user import User
from .release import Release
from .episode import Episode
from datetime import datetime

class File(Document):
    user         : Link[User]
    release      : Link[Release]
    episode      : Optional[Link[Episode]]
    tg_id        : str
    type         : str
    size         : str
    name         : str
    message_text : str
    date         : datetime
    
    class Settings:
        name = "files"