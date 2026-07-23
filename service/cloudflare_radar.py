import aiohttp

from core.config import settings


class CloudflareRateLimitError(Exception):
    """429 error from Cloudflare Radar API"""


class CloudFlareRadarClient:
    BASE_URL = "https://api.cloudflare.com/client/v4/radar"
    TIMEOUT_REQUEST = aiohttp.ClientTimeout(total=10)

    def __init__(self, session: aiohttp.ClientSession):
        self._session = session
        self._headers = {
            "Authorization": f"Bearer {settings.CF_TOKEN}"
        }

    async def summary_device_type(self, date_range: str = "30d", limit: int = 100) -> dict:
        url = f"{self.BASE_URL}/http/summary/device_type"
        params = {"dateRange": date_range, "limit": limit}

        async with self._session.get(
            url, headers=self._headers, params=params, timeout=self.TIMEOUT_REQUEST
        ) as response:
            if response.status == 429:
                raise CloudflareRateLimitError("Rate limited by Cloudflare Radar API")

            data = await response.json()

            if not data.get("success", False):
                raise Exception(f"Radar API error: {data.get('errors')}")

            return data["result"]

    async def top_location(self, date_range: str = "30d", limit: int = 100) -> dict:
        url = f"{self.BASE_URL}/http/top/locations"
        params = {"dateRange": date_range, "limit": limit}

        async with self._session.get(
            url, headers=self._headers, params=params, timeout=self.TIMEOUT_REQUEST
        ) as response:
            if response.status == 429:
                raise CloudflareRateLimitError("Rate limited by Cloudflare Radar API")

            data = await response.json()

            if not data.get("success", False):
                raise Exception(f"Radar API error: {data.get('errors')}")

            return data["result"]