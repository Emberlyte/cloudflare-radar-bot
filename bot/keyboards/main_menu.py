from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu(i18n) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=i18n.get("menu-devices"), callback_data="radar:devices")
    builder.button(text=i18n.get("menu-locations"), callback_data="radar:locations")
    builder.button(text=i18n.get("menu-ases"), callback_data="radar:ases")
    builder.button(text=i18n.get("menu-quality"), callback_data="radar:quality")
    builder.button(text=i18n.get("menu-attacks"), callback_data="radar:attacks")
    builder.button(text=i18n.get("menu-dns"), callback_data="radar:dns")
    builder.button(text=i18n.get("menu-email"), callback_data="radar:email")
    builder.button(text=i18n.get("menu-services"), callback_data="radar:services")
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


def get_attacks_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🌐 Layer 3 (сетевой уровень)", callback_data="attacks:layer3")
    builder.button(text="📡 Layer 7 (HTTP)", callback_data="attacks:layer7")
    builder.button(text="⬅️ Назад", callback_data="radar:menu")
    builder.adjust(1)
    return builder.as_markup()