from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram_i18n import I18nContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.main_menu import get_main_menu

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message, i18n: I18nContext):
    await message.answer(
        i18n.get("start-greeting"),
        reply_markup=get_main_menu(i18n),
    )


@router.message(Command("help"))
async def cmd_command(message: types.Message):
    await message.answer(
        "📖 <b>Как пользоваться ботом</b>\n\n"
        "/start — открыть главное меню\n"
        "/help — эта справка\n\n"
        "<b>Разделы:</b>\n"
        "📱 <b>Устройства</b> — с каких устройств заходят в интернет (десктоп/мобильные)\n"
        "🌍 <b>Топ локаций</b> — страны с наибольшим объёмом HTTP-трафика\n"
        "🌐 <b>Топ провайдеров</b> — крупнейшие интернет-провайдеры (ASes)\n"
        "⚡ <b>Качество интернета</b> — глобальная скорость, задержка, потери пакетов\n\n"
        "Для разделов с историей можно выбрать период: 7, 30 или 90 дней.\n\n"
        "Данные предоставлены Cloudflare Radar API и обновляются каждые несколько часов."
    )


@router.message(Command("about"))
async def about_handler(message: types.Message):
    await message.answer(
        "ℹ️ <b>О боте</b>\n\n"
        "Этот бот показывает статистику интернет-трафика через Cloudflare Radar API — "
        "публичный сервис Cloudflare с агрегированными данными о трафике, атаках, DNS и качестве интернета по всему миру.\n\n"
        "🔧 Технологии: Python, aiogram 3, Redis, Docker\n"
        "📊 Источник данных: Cloudflare Radar (radar.cloudflare.com)\n"
        "📄 Лицензия: MIT\n"
        "Исходный код: github.com/emberlyte/cloudflare-radar-bot"
    )


@router.message(Command("language"))
async def cmd_language(message: types.Message, i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    builder.button(text="🇷🇺 Русский", callback_data="lang:ru")
    builder.button(text="🇬🇧 English", callback_data="lang:en")
    builder.adjust(1)
    await message.answer(i18n.get("language-choose"), reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("lang:"))
async def set_language(callback: types.CallbackQuery, i18n: I18nContext):
    locale = callback.data.split(":")[1]
    await i18n.set_locale(locale)
    await callback.message.edit_text(i18n.get("language-changed"))
    await callback.answer()