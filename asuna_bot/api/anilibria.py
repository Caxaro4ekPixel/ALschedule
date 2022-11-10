import logging as log
import httpx
from pydantic import BaseModel
from asuna_bot.config import CONFIG

class Names(BaseModel):
    ru: str
    en: str

class ALTitle(BaseModel):
    id: int
    code: str
    names: Names

class Schedule(BaseModel):
    day: int
    list: list[ALTitle]

class AnilibriaApi:
    
    def _request(self, endpoint):
        resp = httpx.get(CONFIG.misc.al_url + endpoint)
        log.info(resp.url)
        match resp.status_code:
            case 200:
                return resp.json()
            case 404:
                log.warning(f"404 - Title not found")
                return None
            case _:
                log.warning(f"Something went wrong! Status code is {resp.status_code}")
                return None

    def get_schedule(self):
        days = self._request('getSchedule')
        return [Schedule(**day) for day in days] if days else []


    def get_title_by_id(self, title_id):
        title = self._request(f'getTitle?id={title_id}')
        if not title:
            return False
        return ALTitle(**title)


    def get_titles(self, search):
        titles = self._request(f'searchTitles?search={search}')
        return [ALTitle(**title) for title in titles] if titles else []