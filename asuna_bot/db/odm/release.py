from typing import List, Optional
from beanie import Document



class Release(Document):
    id         : int
    chat_id    : int
    status     : str = None
    code       : str
    en_title   : str
    ru_title   : str
    total_ep   : Optional[int]
    season     : str
    is_ongoing : bool = False
    is_top     : bool = False
    is_commer  : bool = False

    class Settings:
        name = "releases"