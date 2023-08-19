from typing import List, Optional
from beanie import Document, Link
from pydantic import BaseModel, HttpUrl, AnyUrl
from datetime import datetime
from .release import Release



class Torrent(BaseModel):
    # основные атрибуты торрента
    id        : int
    submitter : str
    serie     : int
    quality   : str
    url       : HttpUrl
    file_url  : HttpUrl
    magnet    : AnyUrl
    size      : str

    # доп атрибуты, мб понадобятся где-нибудь
    title     : str
    type      : str
    category  : str
    seeders   : str
    leechers  : str
    downloads : str
    date      : datetime


class Episode(Document):
    series_num   : int = None
    status       : str = None
    released_at  : datetime = None
    deadline_at  : datetime = None
    uploaded_at  : datetime = None
    time_work_on : int = None
    release      : Link[Release]
    torrents     : Optional[List[Torrent]]

    class Settings:
        name = "episodes"