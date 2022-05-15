from urllib import response
import aiohttp


class AnilibriaApi:
    def __init__(self, loop):
        self.session = aiohttp.ClientSession(loop=loop)
        self.loop = loop
        self._base_url = 'https://api.anilibria.tv/v2/'


    async def _request(self, endpoint) -> dict or str:
        if self.session.closed:
            self.session = aiohttp.ClientSession(loop=self.loop)

        async with self.session.get(self._base_url + endpoint) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f'Except status 200, got {response.status}')


    async def get_schedule(self):
        return await self._request('getSchedule')


    async def get_title(self, title_id):
        return await self._request(f'getTitle?id={title_id}')