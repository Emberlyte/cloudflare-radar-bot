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

    async def summary_device_type(self, date_range: str = "30d", limit: int = 100) -> dict:
        url = f"{self.BASE_URL}/http/summary/device_type"
        params = {"dateRange": date_range, "limit": limit}

        async with self._session.get(url, headers=self._headers, params=params) as response:
            data = await response.json()

            if not data.get("success", False):
                raise Exception(f"Radar API error: {data.get('errors')}")

            return data["result"]

    async def top_location(self, date_range: str = "30d", limit: int = 100) -> dict:
        url = f"{self.BASE_URL}/http/top/locations"
        params = {"dateRange": date_range, "limit": limit}

        async with self._session.get(url, headers=self._headers, params=params) as response:
            data = await response.json()

            if not data.get("success", False):
                raise Exception(f"Radar API error: {data.get('errors')}")

            return data["result"]
