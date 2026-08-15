import asyncio
import logging

from aiogram import Bot, Dispatcher
import aiohttp
import redis.asyncio as redis
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from core.config import get_settings
from core.logging import setup_logging
from service.cloudflare_radar import CloudFlareRadarClient
from bot.handlers import register_handlers
from bot.middlewares.throttling import ThrottlingMiddleware


logger = logging.getLogger(__name__)

WEBAPP_HOST = "0.0.0.0"


async def setup_bot() -> tuple[Bot, Dispatcher]:
    settings = get_settings()

    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    await bot.set_my_commands([
        BotCommand(command="start", description="Открыть главное меню"),
        BotCommand(command="help", description="Как пользоваться ботом"),
        BotCommand(command="about", description="О боте"),
    ])

    session = aiohttp.ClientSession()
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    radar_client = CloudFlareRadarClient(session, redis_client)

    dp["radar_client"] = radar_client

    throttling = ThrottlingMiddleware(redis_client, limit=10, window_seconds=60)
    dp.message.middleware(throttling)
    dp.callback_query.middleware(throttling)

    register_handlers(dp)

    return bot, dp


async def run_polling():
    logger.info("Starting bot in polling mode (local dev)...")
    bot, dp = await setup_bot()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


def run_webhook():
    logger.info("Starting bot in webhook mode (production)...")
    settings = get_settings()

    async def _setup():
        bot, dp = await setup_bot()
        webhook_url = f"{settings.WEBHOOK_BASE_URL}{settings.WEBHOOK_PATH}"

        async def on_startup():
            await bot.set_webhook(
                webhook_url,
                secret_token=settings.WEBHOOK_SECRET,
            )
            logger.info("Webhook set to %s", webhook_url)

        async def on_shutdown():
            await bot.delete_webhook()

        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)

        app = web.Application()
        SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
            secret_token=settings.WEBHOOK_SECRET,
        ).register(app, path=settings.WEBHOOK_PATH)
        setup_application(app, dp, bot=bot)
        return app

    web.run_app(_setup(), host=WEBAPP_HOST, port=settings.WEBAPP_PORT)


if __name__ == "__main__":
    setup_logging()
    settings = get_settings()

    if settings.BOT_MODE == "webhook":
        run_webhook()
    else:
        asyncio.run(run_polling())