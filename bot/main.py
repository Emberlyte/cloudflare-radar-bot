import asyncio
import logging

from aiogram import Bot, Dispatcher
import aiohttp
import redis.asyncio as redis
from aiogram.client.default import DefaultBotProperties

from core.config import settings
from core.logging import setup_logging
from service.cloudflare_radar import CloudFlareRadarClient
from bot.handlers import register_handlers

logger = logging.getLogger(__name__)


async def main():
    setup_logging()
    logger.info("Starting bot...")

    bot = Bot(token=settings.BOT_TOKEN,
              default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    session = aiohttp.ClientSession()
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    radar_client = CloudFlareRadarClient(session, redis_client)

    dp["radar_client"] = radar_client

    register_handlers(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await session.close()
        await redis_client.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())