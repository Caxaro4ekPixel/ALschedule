from urllib.parse import quote, urlencode
from lxml import etree
from dateutil.parser import *

def parse_submitter(full_str: str) -> str:
    b = full_str.find("]")
    return full_str[:b+1]


def parse_quality(full_str: str) -> str or None:
    if "480" in full_str: return "480p"
    if "720" in full_str: return "720p"
    if "1080" in full_str: return "1080p"
    else: return None


def parse_serie(full_str: str) -> int:
    ep = "00"
    if full_str.lower().startswith("[subsplease]"):
        ep = full_str.split(" (")[0].split(" ")[-1]

    if full_str.lower().startswith("[erai-raws]"):
        ep = full_str.split(" [")[0].split(" ")[-1]

    if ep.startswith("0"):
        return int(ep[1:].strip())
    return int(ep)


def rss_to_json(resp, limit):
            root = etree.fromstring(resp)
            torrents = []
            for item in root.xpath("channel/item")[:limit]:
                try:
                    is_remake = item.findtext("nyaa:remake", namespaces=item.nsmap) == "Yes"
                    is_trusted = item.findtext("nyaa:trusted", namespaces=item.nsmap) == "Yes"
                    item_type = "remake" if is_remake else "trusted" if is_trusted else "default"
                    title = item.findtext("title")

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
                        'date': parse(item.findtext("pubDate")),
                        'seeders': item.findtext("nyaa:seeders", namespaces=item.nsmap),
                        'leechers': item.findtext("nyaa:leechers", namespaces=item.nsmap),
                        'downloads': item.findtext("nyaa:downloads", namespaces=item.nsmap),
                        'type': item_type, 
                        'quality': parse_quality(title),
                        'submitter': parse_submitter(title),
                        'serie': parse_serie(title)
                    }

                    torrents.append(torrent)
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