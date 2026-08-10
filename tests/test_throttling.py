import pytest

from unittest.mock import MagicMock, AsyncMock
from bot.middlewares.throttling import ThrottlingMiddleware



def make_mock_event(user_id: int = 12345, is_callback: bool = False):
    """Собирает мок Message или CallbackQuery с нужным from_user.id."""
    event = MagicMock()
    event.from_user.id = user_id
    event.answer = AsyncMock()

    if is_callback:
        from aiogram.types import CallbackQuery
        event.__class__ = CallbackQuery
    else:
        from aiogram.types import Message
        event.__class__ = Message

    return event


async def test_allows_requests_under_limit(redis_client):
    middleware = ThrottlingMiddleware(redis_client, limit=3, window_seconds=60)
    handler = AsyncMock(return_value="ok")
    event = make_mock_event()

    result = await middleware(handler, event, {})

    assert result == "ok"
    handler.assert_called_once_with(event, {})


async def test_blocks_requests_over_limit(redis_client):
    middleware = ThrottlingMiddleware(redis_client, limit=2, window_seconds=60)
    handler = AsyncMock(return_value="ok")
    event = make_mock_event()

    await middleware(handler, event, {})
    await middleware(handler, event, {})
    result = await middleware(handler, event, {})

    assert handler.call_count == 2
    assert result is None
    event.answer.assert_called_once()


async def test_counter_resets_per_user(redis_client):
    middleware = ThrottlingMiddleware(redis_client, limit=1, window_seconds=60)
    handler = AsyncMock(return_value="ok")

    user_a = make_mock_event(user_id=111)
    user_b = make_mock_event(user_id=222)

    result_a = await middleware(handler, user_a, {})
    result_b = await middleware(handler, user_b, {})

    assert result_a == "ok"
    assert result_b == "ok"
    assert handler.call_count == 2


async def test_callback_query_uses_show_alert(redis_client):
    middleware = ThrottlingMiddleware(redis_client, limit=1, window_seconds=60)
    handler = AsyncMock(return_value="ok")
    event = make_mock_event(is_callback=True)

    await middleware(handler, event, {})
    await middleware(handler, event, {})

    event.answer.assert_called_once_with(
        "⏳ Слишком много запросов. Подожди немного и попробуй снова.",
        show_alert=True,
    )


async def test_event_without_user_passes_through(redis_client):
    middleware = ThrottlingMiddleware(redis_client, limit=1, window_seconds=60)
    handler = AsyncMock(return_value="ok")

    event = MagicMock()
    event.__class__ = object

    result = await middleware(handler, event, {})

    assert result == "ok"
    handler.assert_called_once()