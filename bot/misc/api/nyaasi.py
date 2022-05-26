import logging
from typing import List
import aiohttp
from pydantic import BaseModel
from lxml import etree
from urllib.parse import urlencode, quote


class NyaaTorrent(BaseModel):
    id: str
    name: str
    type: str
    size: str
    url: str
    download_url: str
    magnet: str
    category: str
    seeders: int
    leechers: int
    downloads: int
    date: str
    

class NyaaRss:
    def __init__(self, loop) -> None:
        self.session = aiohttp.ClientSession(loop=loop)
        self._loop = loop
        self._base_url = 'https://nyaa.si/'

    async def _request(self, params):
        if self.session.closed:
            self.session = aiohttp.ClientSession(loop=self._loop)

        async with self.session.get(self._base_url, params=params) as response:
            match response.status:
                case 200:
                    return await response.read()
                case _:
                    logging.warning(f"Something went wrong! Status code is {response.status}")
                    return None
    
    async def search_torrent(self, query, category="1_2", filter="2", limit=5) -> List[NyaaTorrent]:
        """
        query: 
            Что хотим найти
        category:
            1_0 - All Anime
            1_1 - Anime AMV 
            1_2 - Anime English-translated
            1_3 - Anime Non-English-translated
            1_4 - Anime Raw
        другие категории нам не интересны

        filter:
            0 - No filter
            1 - No remakes (хз что значит)
            2 - Trusted only

        """
        params = {
            "page": "rss",
            "q": query, 
            "c": category, 
            "f": filter
        }
        resp = await self._request(params)
        torrents = parse_nyaa_rss(resp, limit=limit)
        return torrents


    async def watch_user(self, user) -> List[NyaaTorrent]:
        pass



def parse_nyaa_rss(resp, limit):
        """
        Extracts torrent information from a given rss response.
        """
        root = etree.fromstring(resp)
        torrents = []
        
        for item in root.xpath("channel/item")[:limit]:
            try:
                is_remake = item.findtext("nyaa:remake", namespaces=item.nsmap) == "Yes"
                is_trusted = item.findtext("nyaa:trusted", namespaces=item.nsmap) == "Yes"
                item_type = "remake" if is_remake else "trusted" if is_trusted else "default"

                torrent = {
                    'id': item.findtext("guid").split("/")[-1],
                    'category': item.findtext("nyaa:categoryId", namespaces=item.nsmap),
                    'url': item.findtext("guid"),
                    'name': item.findtext("title"),
                    'download_url': item.findtext("link"),
                    #пока нет своего редиректа, поюзаем чужой xD
                    'magnet': f'https://nyaasi.herokuapp.com/nyaamagnet/urn:btih:{item.findtext("nyaa:infoHash", namespaces=item.nsmap)}',
                    # 'magnet': magnet_builder(item.findtext("nyaa:infoHash", namespaces=item.nsmap), item.findtext("title")),
                    'size': item.findtext("nyaa:size", namespaces=item.nsmap),
                    'date': item.findtext("pubDate"),
                    'seeders': item.findtext("nyaa:seeders", namespaces=item.nsmap),
                    'leechers': item.findtext("nyaa:leechers", namespaces=item.nsmap),
                    'downloads': item.findtext("nyaa:downloads", namespaces=item.nsmap),
                    'type': item_type
                }
                torrents.append(NyaaTorrent(**torrent))
            except IndexError:
                pass

        return torrents

def magnet_builder(info_hash, title):
    """
    Generates a magnet link using the info_hash and title of a given file.
    """
    known_trackers = [
        "http://nyaa.tracker.wf:7777/announce",
        "udp://open.stealth.si:80/announce",
        "udp://tracker.opentrackr.org:1337/announce",
        "udp://exodus.desync.com:6969/announce",
        "udp://tracker.torrent.eu.org:451/announce"
    ]

    magnet_link = f"magnet:?xt=urn:btih:{info_hash}&" + urlencode({"dn": title}, quote_via=quote)
    for tracker in known_trackers:
        magnet_link += f"&{urlencode({'tr': tracker})}"

    return magnet_link