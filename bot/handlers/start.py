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
async def cmd_command(message: types.Message, i18n: I18nContext):
    await message.answer(i18n.get("help-text"))


@router.message(Command("about"))
async def about_handler(message: types.Message, i18n: I18nContext):
    await message.answer(i18n.get("about-text"))


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