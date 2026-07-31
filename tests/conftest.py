import pytest
import aiohttp
import fakeredis

from service.cloudflare_radar import CloudFlareRadarClient

@pytest.fixture
async def redis_client():
    client = fakeredis.aioredis.FakeRedis(decode_responses=True)
    yield client
    await client.aclose()


@pytest.fixture
async def http_session():
    async with aiohttp.ClientSession() as session:
        yield session

@pytest.fixture
async def radar_client(http_session, redis_client):
    return CloudFlareRadarClient(http_session, redis_client)

