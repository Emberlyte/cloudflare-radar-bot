import aiohttp
import json
import redis.asyncio as redis

from core.config import settings


class CloudflareRateLimitError(Exception):
    """429 error from Cloudflare Radar API"""


class CloudFlareRadarClient:
    BASE_URL = "https://api.cloudflare.com/client/v4/radar"
    TIMEOUT_REQUEST = aiohttp.ClientTimeout(total=10)
    TTL_CACHED_TIMEOUT = 300

    def __init__(self, session: aiohttp.ClientSession, redis_client: redis.Redis):
        self._session = session
        self._headers = {
            "Authorization": f"Bearer {settings.CF_TOKEN}"
        }
        self._redis = redis_client

    async def _get(self, url: str, params: dict) -> dict:
        cache_key = f"radar:{url}:{sorted(params.items())}"

        cached = await self._redis.get(cache_key)
        if cached is not None:
            return json.loads(cached)

        async with self._session.get(
                url, headers=self._headers, params=params, timeout=self.TIMEOUT_REQUEST
        ) as response:
            if response.status == 429:
                raise CloudflareRateLimitError("Rate limited by Cloudflare Radar API")

            data = await response.json()

            if not data.get("success", False):
                raise Exception(f"Radar API error: {data.get('errors')}")

            result = data["result"]
            await self._redis.set(cache_key, json.dumps(result), ex=self.TTL_CACHED_TIMEOUT)
            return result

    async def summary_device_type(self, date_range: str = "30d", limit: int = 100) -> dict:
        url = f"{self.BASE_URL}/http/summary/device_type"
        params = {"dateRange": date_range, "limit": limit}
        return await self._get(url, params)

    async def top_location(self, date_range: str = "30d", limit: int = 100) -> dict:
        url = f"{self.BASE_URL}/http/top/locations"
        params = {"dateRange": date_range, "limit": limit}
        return await self._get(url, params)

    async def top_ases(self, date_range: str = "30d", limit: int = 5) -> dict:
        url = f"{self.BASE_URL}/http/top/ases"
        params = {"dateRange": date_range, "limit": limit}
        return await self._get(url, params)

    async def quality_speed(self, date_range: str = "30d") -> dict:
        url = f"{self.BASE_URL}/quality/speed/summary"
        params = {"dateRange": date_range}
        return await self._get(url, params)