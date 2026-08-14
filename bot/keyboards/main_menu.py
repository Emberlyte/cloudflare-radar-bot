from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="📱 Устройства", callback_data="radar:devices")
    builder.button(text="🌍 Локации", callback_data="radar:locations")
    builder.button(text="🌐 Топ провайдеров", callback_data="radar:ases")
    builder.button(text="⚡ Качество интернета", callback_data="radar:quality")
    builder.button(text="🛡 Атаки и DDoS", callback_data="radar:attacks")
    builder.button(text="🔤 DNS по протоколу", callback_data="radar:dns")
    builder.button(text="📧 Email-угрозы", callback_data="radar:email")
    builder.button(text="🏆 Топ интернет-сервисов", callback_data="radar:services")
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