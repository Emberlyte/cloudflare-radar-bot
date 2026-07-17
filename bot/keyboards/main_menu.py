from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="📱 Устройства", callback_data="radar:devices")

    builder.adjust(1)

    return builder.as_markup()

def get_back_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад", callback_data="radar:menu")
    return builder.as_markup()

def get_period_keyboard(section: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="7 дней", callback_data=f"period:{section}:7d")
    builder.button(text="30 дней", callback_data=f"period:{section}:30d")
    builder.button(text="90 дней", callback_data=f"period:{section}:90d")
    builder.button(text="⬅️ Назад", callback_data="radar:menu")
    builder.adjust(3, 1)
    return builder.as_markup()