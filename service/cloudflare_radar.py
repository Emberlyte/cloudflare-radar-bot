import aiohttp

from core.logging import setup_logging
from core.config import settings

class CloudFlareRadarClient:
    setup_logging()
    BASE_URL = "https://api.cloudflare.com/client/v4/radar"

    def __init__(self, session: aiohttp.ClientSession):
        self._session = session
        self._headers = {
            "Authorization": f"Bearer {settings.CF_TOKEN}"
        }

    async def summary_device_type(self, limit: int = 100)-> dict:
        url = f"{self.BASE_URL}/http/summary/device_type?dateRange=30d&format=json"
        params = {"limit: ": limit}
        async with self._session.get(url, headers=self._headers, params=params) as response:
            data = await response.json()
            return data["result"]
