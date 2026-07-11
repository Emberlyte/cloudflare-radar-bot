import asyncio
import logging

from aiogram import Bot, Dispatcher
import aiohttp
from aiogram.client.default import DefaultBotProperties

from core.config import settings
from core.logging import setup_logging

from service.cloudflare_radar import CloudFlareRadarClient
from bot.handlers import register_handlers

async def main():
    setup_logging()

    bot = Bot(token=settings.BOT_TOKEN,
              default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    session = aiohttp.ClientSession()
    radar_client = CloudFlareRadarClient(session)

    dp["radar_client"] = radar_client

    register_handlers(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())