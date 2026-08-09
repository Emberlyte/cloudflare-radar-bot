import logging

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery, Message

logger = logging.getLogger(__name__)


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, redis_client, limit: int = 10, window_seconds: int = 30):
        self.redis = redis_client
        self.limit = limit
        self.window_seconds = window_seconds

    async def __call__(self, handler, event: TelegramObject, data: dict):
        user_id = self._get_user_id(event)
        if user_id is None:
            return await handler(event, data)

        key = f"throttle:{user_id}"
        current = await self.redis.incr(key)

        if current == 1:
            await self.redis.expire(key, self.window_seconds)

        if current > self.limit:
            logger.warning("User %s hit rate limit (%s requests)", user_id, current)
            await self._notify_limited(event)
            return

        return await handler(event, data)

    @staticmethod
    def _get_user_id(event: TelegramObject) -> int | None:
        if isinstance(event, (Message, CallbackQuery)):
            return event.from_user.id
        return None

    @staticmethod
    async def _notify_limited(event: TelegramObject) -> None:
        text = "⏳ Слишком много запросов. Подожди немного и попробуй снова."
        if isinstance(event, CallbackQuery):
            await event.answer(text, show_alert=True)
        elif isinstance(event, Message):
            await event.answer(text)
