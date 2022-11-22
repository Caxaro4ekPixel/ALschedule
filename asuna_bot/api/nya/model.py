from typing import Optional
from pydantic import BaseModel, HttpUrl, FileUrl, AnyUrl
from datetime import datetime


class NyaaTorrent(BaseModel):
    # основные атрибуты торрента
    id: int
    submitter: Optional[str | None]
    serie: Optional[int | None]
    quality: Optional[str | None]
    url: HttpUrl
    file_url: HttpUrl
    magnet: AnyUrl
    size: str 

    # доп атрибуты, мб понадобятся где-нибудь
    title: str
    type: str
    category: str
    seeders: int
    leechers: int
    downloads: int
    date: datetime