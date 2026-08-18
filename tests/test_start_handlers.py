from unittest.mock import AsyncMock

from bot.handlers.start import start_handler, about_handler, cmd_command


async def test_cmd_about_sends_info():
    message = AsyncMock()

    await about_handler(message)

    message.answer.assert_called_once()
    text_arg = message.answer.call_args[0][0]
    assert "О боте" in text_arg
    assert "MIT" in text_arg


async def test_cmd_start_sends_main_menu():
    message = AsyncMock()

    await start_handler(message)

    message.answer.assert_called_once()
    call_kwargs = message.answer.call_args
    assert "reply_markup" in call_kwargs.kwargs


async def test_cmd_help_sends_instructions():
    message = AsyncMock()

    await cmd_command(message)

    message.answer.assert_called_once()
    text_arg = message.answer.call_args[0][0]
    assert "Как пользоваться" in text_arg