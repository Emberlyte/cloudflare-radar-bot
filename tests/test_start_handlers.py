from unittest.mock import AsyncMock, MagicMock

from bot.handlers.start import cmd_start, about_handler, cmd_command


def make_mock_i18n():
    i18n = MagicMock()
    i18n.get.side_effect = lambda key, **kwargs: key
    return i18n


async def test_cmd_start_sends_main_menu():
    message = AsyncMock()
    i18n = make_mock_i18n()

    await cmd_start(message, i18n)

    message.answer.assert_called_once()
    call_kwargs = message.answer.call_args
    assert "reply_markup" in call_kwargs.kwargs


async def test_about_handler_sends_info():
    message = AsyncMock()

    await about_handler(message)

    message.answer.assert_called_once()
    text_arg = message.answer.call_args[0][0]
    assert "MIT" in text_arg


async def test_cmd_command_sends_instructions():
    message = AsyncMock()

    await cmd_command(message)

    message.answer.assert_called_once()