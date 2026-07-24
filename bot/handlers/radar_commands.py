import asyncio
import logging

from aiogram import Router, types, F
from service.cloudflare_radar import CloudFlareRadarClient, CloudflareRateLimitError
from bot.keyboards.main_menu import get_back_button, get_main_menu, get_period_keyboard
from bot.utils.safe_edit import safe_edit_text

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == "radar:devices")
async def ask_period_devices(callback: types.CallbackQuery):
    await safe_edit_text(callback.message, "Выбери период:", get_period_keyboard("devices"))
    await callback.answer()


@router.callback_query(F.data.startswith("period:devices:"))
async def show_devices(callback: types.CallbackQuery, radar_client: CloudFlareRadarClient):
    period = callback.data.split(":")[2]
    try:
        data = await radar_client.summary_device_type(date_range=period)
        text = format_device_summary(data, period)
        await safe_edit_text(callback.message, text, get_back_button())
    except CloudflareRateLimitError:
        logger.warning("Rate limited by Radar API for devices, period=%s", period)
        await safe_edit_text(
            callback.message,
            "⏳ Слишком много запросов к Cloudflare. Попробуй через минуту.",
            get_back_button(),
        )
    except asyncio.TimeoutError:
        logger.warning("Timeout fetching device summary, period=%s", period)
        await safe_edit_text(
            callback.message,
            "⏱ Cloudflare долго отвечает. Попробуй ещё раз.",
            get_back_button(),
        )
    except Exception:
        logger.exception("Failed to fetch device summary for period=%s", period)
        await safe_edit_text(
            callback.message,
            "⚠️ Не удалось получить данные. Попробуй позже.",
            get_back_button(),
        )
    await callback.answer()


def format_device_summary(data: dict, period: str) -> str:
    summary = data["summary_0"]
    desktop = float(summary["desktop"])
    mobile = float(summary["mobile"])
    other = float(summary["other"])
    period_label = {"7d": "7 дней", "30d": "30 дней", "90d": "90 дней"}.get(period, period)
    return (
        f"📊 <b>Устройства за {period_label}</b>\n\n"
        f"🖥 Десктоп: {desktop:.1f}%\n"
        f"📱 Мобильные: {mobile:.1f}%\n"
        f"❓ Другое: {other:.1f}%"
    )


@router.callback_query(F.data == "radar:locations")
async def ask_period_locations(callback: types.CallbackQuery):
    await safe_edit_text(callback.message, "Выбери период:", get_period_keyboard("locations"))
    await callback.answer()


@router.callback_query(F.data.startswith("period:locations:"))
async def show_locations(callback: types.CallbackQuery, radar_client: CloudFlareRadarClient):
    period = callback.data.split(":")[2]
    try:
        data = await radar_client.top_location(date_range=period, limit=5)
        text = format_top_locations(data, period)
        await safe_edit_text(callback.message, text, get_back_button())
    except CloudflareRateLimitError:
        logger.warning("Rate limited by Radar API for locations, period=%s", period)
        await safe_edit_text(
            callback.message,
            "⏳ Слишком много запросов к Cloudflare. Попробуй через минуту.",
            get_back_button(),
        )
    except asyncio.TimeoutError:
        logger.warning("Timeout fetching top locations, period=%s", period)
        await safe_edit_text(
            callback.message,
            "⏱ Cloudflare долго отвечает. Попробуй ещё раз.",
            get_back_button(),
        )
    except Exception:
        logger.exception("Failed to fetch top locations for period=%s", period)
        await safe_edit_text(
            callback.message,
            "⚠️ Не удалось получить данные. Попробуй позже.",
            get_back_button(),
        )
    await callback.answer()


def format_top_locations(data: dict, period: str) -> str:
    locations = data["top_0"]
    period_label = {"7d": "7 дней", "30d": "30 дней", "90d": "90 дней"}.get(period, period)
    lines = [f"🌍 <b>Топ локаций за {period_label}</b>\n"]
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
    for i, loc in enumerate(locations):
        medal = medals[i] if i < len(medals) else f"{i + 1}."
        name = loc["clientCountryName"]
        value = float(loc["value"])
        lines.append(f"{medal} {name}: {value:.1f}%")
    return "\n".join(lines)


@router.callback_query(F.data == "radar:menu")
async def back_to_menu(callback: types.CallbackQuery):
    await safe_edit_text(callback.message, "Выбери, что показать:", get_main_menu())
    await callback.answer()