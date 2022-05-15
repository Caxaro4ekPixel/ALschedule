import logging
import aiohttp


class AnilibriaApi:
    def __init__(self, loop):
        self.session = aiohttp.ClientSession(loop=loop)
        self._loop = loop
        self._base_url = 'https://api.anilibria.tv/v2/'


    async def _request(self, endpoint):
        if self.session.closed:
            self.session = aiohttp.ClientSession(loop=self._loop)

        async with self.session.get(self._base_url + endpoint) as response:
            match response.status:
                case 200:
                    return await response.json()
                case 404:
                    return None
                case _:
                    logging.warning("Something went wrong! Status code is {response.status}")
                    return None

    async def get_schedule(self):
        return await self._request('getSchedule')

    async def get_title_by_id(self, title_id):
        return await self._request(f'getTitle?id={title_id}')