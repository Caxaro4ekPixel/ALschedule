from typing import List
from pydantic import BaseModel, HttpUrl, FileUrl, AnyUrl
from lxml import etree
from urllib.parse import urlencode, quote
from urllib.request import urlopen
from datetime import datetime


class NyaaTorrent(BaseModel):
    # основные атрибуты торрента
    id: str
    submitter: str
    episode: int
    quality: str
    url: HttpUrl
    file_url: FileUrl
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
     

class NyaaRss:
    def __init__(self) -> None:
        self._base_url = 'https://nyaa.si/?'

    def _make_request(self, params):
        params = urlencode(params)
        with urlopen(self._base_url + params) as data:
            return data.read().decode('utf-8')


    def get_updates(self) -> List[NyaaTorrent]:
        params = {
            "page": "rss",
            "q": "[Erai-Raws] boruto", 
            "c": "1_2", 
            "f": "2"
        }
        resp = self._make_request(params)
        torrents = self.parse_nyaa_rss(resp, limit=20)
        return torrents


    def search_torrent(self, query, category="1_2", filter="2", limit=5) -> List[NyaaTorrent]:
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
        resp = self._make_request(params)
        torrents = self.parse_nyaa_rss(resp, limit=limit)
        return torrents


    def _parse_submitter(self, full_str: str) -> str:
        return full_str.split()[0]


    def _parse_quality(self, full_str: str) -> str:
        if "480" in full_str: return "480p"
        if "720" in full_str: return "720p"
        if "1080" in full_str: return "1080p"
        else: return None


    def _parse_ep_number(self, full_str: str) -> str:
        if full_str.lower().startswith("[subsplease]"):
            ep = full_str.split(" (")[0].split(" ")[-1]

        if full_str.lower().startswith("[erai-raws]"):
            ep = full_str.split(" [")[0].split(" ")[-1]

        if ep.startswith("0"):
            return int(ep[1:].strip())
        return int(ep)


    def parse_nyaa_rss(self, resp, limit):
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
                    title = item.findtext("title")
                    print(title)
                    torrent = {
                        'id': item.findtext("guid").split("/")[-1],
                        'category': item.findtext("nyaa:categoryId", namespaces=item.nsmap),
                        'url': item.findtext("guid"),
                        'title': title,
                        'file_url': item.findtext("link"),
                        #пока нет своего редиректа, поюзаем чужой xD
                        'magnet': f'https://nyaasi.herokuapp.com/nyaamagnet/urn:btih:{item.findtext("nyaa:infoHash", namespaces=item.nsmap)}',
                        # 'magnet': magnet_builder(item.findtext("nyaa:infoHash", namespaces=item.nsmap), item.findtext("title")),
                        'size': item.findtext("nyaa:size", namespaces=item.nsmap),
                        'date': item.findtext("pubDate"),
                        'seeders': item.findtext("nyaa:seeders", namespaces=item.nsmap),
                        'leechers': item.findtext("nyaa:leechers", namespaces=item.nsmap),
                        'downloads': item.findtext("nyaa:downloads", namespaces=item.nsmap),
                        'type': item_type, 
                        'quality': self._parse_quality(title),
                        'submitter': self._parse_submitter(title),
                        'episode': self._parse_ep_number(title)
                    }
                    print(torrent)
                    torrents.append(NyaaTorrent(**torrent))
                except IndexError:
                    pass

            return torrents


    @staticmethod
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