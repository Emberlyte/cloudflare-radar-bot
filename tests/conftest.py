import pytest
import aiohttp
import fakeredis

from service.cloudflare_radar import CloudFlareRadarClient
from unittest.mock import MagicMock, AsyncMock


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


@pytest.fixture
def mock_callback():
    callback = MagicMock()
    callback.message = AsyncMock()
    callback.message.chat.id = 12345
    callback.answer = AsyncMock()
    callback.bot = AsyncMock()
    return callback


@pytest.fixture
def mock_radar_client():
    return AsyncMock()


@pytest.fixture
def mock_i18n():
    i18n = MagicMock()
    i18n.get.side_effect = lambda key, **kwargs: key
    return i18n
