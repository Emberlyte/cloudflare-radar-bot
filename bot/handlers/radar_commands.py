import asyncio
import logging

from aiogram import Router, types, F
from service.cloudflare_radar import CloudFlareRadarClient, CloudflareRateLimitError
from bot.keyboards.main_menu import get_back_button, get_main_menu, get_period_keyboard, get_attacks_menu
from bot.utils.safe_edit import safe_edit_text

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == "radar:devices")
async def ask_period_devices(callback: types.CallbackQuery):
    await safe_edit_text(callback.message, "📱 За какой период показать устройства?", get_period_keyboard("devices"))
    await callback.answer()


@router.callback_query(F.data.startswith("period:devices:"))
async def show_devices(callback: types.CallbackQuery, radar_client: CloudFlareRadarClient):
    period = callback.data.split(":")[2]
    await callback.bot.send_chat_action(callback.message.chat.id, "typing")
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
    await safe_edit_text(callback.message, "🌍 За какой период показать топ локаций?", get_period_keyboard("locations"))
    await callback.answer()


@router.callback_query(F.data.startswith("period:locations:"))
async def show_locations(callback: types.CallbackQuery, radar_client: CloudFlareRadarClient):
    period = callback.data.split(":")[2]
    await callback.bot.send_chat_action(callback.message.chat.id, "typing")
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


@router.callback_query(F.data == "radar:ases")
async def ask_period_ases(callback: types.CallbackQuery):
    await safe_edit_text(callback.message, "🌐 За какой период показать топ провайдеров?", get_period_keyboard("ases"))
    await callback.answer()

@router.callback_query(F.data.startswith("period:ases:"))
async def show_ases(callback: types.CallbackQuery, radar_client: CloudFlareRadarClient):
    period = callback.data.split(":")[2]
    await callback.bot.send_chat_action(callback.message.chat.id, "typing")
    try:
        data = await radar_client.top_ases(date_range=period, limit=5)
        text = format_top_ases(data, period)
        await safe_edit_text(callback.message, text, get_back_button())
    except CloudflareRateLimitError:
        logger.warning("Rate limited by Radar API for ases, period=%s", period)
        await safe_edit_text(callback.message, "⏳ Слишком много запросов к Cloudflare. Попробуй через минуту.", get_back_button())
    except asyncio.TimeoutError:
        logger.warning("Timeout fetching top ases, period=%s", period)
        await safe_edit_text(callback.message, "⏱ Cloudflare долго отвечает. Попробуй ещё раз.", get_back_button())
    except Exception:
        logger.exception("Failed to fetch top ases for period=%s", period)
        await safe_edit_text(callback.message, "⚠️ Не удалось получить данные. Попробуй позже.", get_back_button())
    await callback.answer()


def format_top_ases(data, period):
    ases = data["top_0"]
    period_label = {"7d": "7 дней", "30d": "30 дней", "90d": "90 дней"}.get(period, period)
    lines = [f"🌐 <b>Топ провайдеров за {period_label}</b>\n"]
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
    for i, asn in enumerate(ases):
        medal = medals[i] if i < len(medals) else f"{i + 1}."
        name = asn["clientASName"]
        value = float(asn["value"])
        lines.append(f"{medal} {name}: {value:.1f}%")
    return "\n".join(lines)


@router.callback_query(F.data == "radar:quality")
async def show_quality(callback: types.CallbackQuery, radar_client: CloudFlareRadarClient):
    await callback.bot.send_chat_action(callback.message.chat.id, "typing")
    try:
        data = await radar_client.quality_speed()
        text = format_quality_speed(data)
        await safe_edit_text(callback.message, text, get_back_button())
    except CloudflareRateLimitError:
        logger.warning("Rate limited by Radar API for quality speed")
        await safe_edit_text(callback.message, "⏳ Слишком много запросов к Cloudflare. Попробуй через минуту.", get_back_button())
    except asyncio.TimeoutError:
        logger.warning("Timeout fetching quality speed")
        await safe_edit_text(callback.message, "⏱ Cloudflare долго отвечает. Попробуй ещё раз.", get_back_button())
    except Exception:
        logger.exception("Failed to fetch quality speed")
        await safe_edit_text(callback.message, "⚠️ Не удалось получить данные. Попробуй позже.", get_back_button())
    await callback.answer()

def format_quality_speed(data: dict) -> str:
    summary = data["summary_0"]

    download = float(summary["bandwidthDownload"])
    upload = float(summary["bandwidthUpload"])
    latency_idle = float(summary["latencyIdle"])
    latency_loaded = float(summary["latencyLoaded"])
    jitter_idle = float(summary["jitterIdle"])
    jitter_loaded = float(summary["jitterLoaded"])
    packet_loss = float(summary["packetLoss"])

    return (
        "⚡ <b>Качество интернета (глобально)</b>\n\n"
        f"⬇️ Скачивание: {download:.1f} Mbps\n"
        f"⬆️ Отдача: {upload:.1f} Mbps\n\n"
        f"⏱ Задержка (простой): {latency_idle:.0f} ms\n"
        f"⏱ Задержка (под нагрузкой): {latency_loaded:.0f} ms\n\n"
        f"📶 Джиттер (простой): {jitter_idle:.1f} ms\n"
        f"📶 Джиттер (под нагрузкой): {jitter_loaded:.1f} ms\n\n"
        f"📉 Потеря пакетов: {packet_loss:.2f}%"
    )


@router.callback_query(F.data == "radar:attacks")
async def ask_attack_layer(callback: types.CallbackQuery):
    await safe_edit_text(callback.message,  "🛡 Какой уровень атак показать?", get_attacks_menu())
    await callback.answer()


@router.callback_query(F.data == "attacks:layer3")
async def show_attacks_layer3(callback: types.CallbackQuery, radar_client: CloudFlareRadarClient):
    await callback.bot.send_chat_action(callback.message.chat.id, "typing")
    try:
        data = await radar_client.attacks_layer3_summary()
        text = format_attacks_layer3(data)
        await safe_edit_text(callback.message, text, get_back_button())
    except CloudflareRateLimitError:
        logger.warning("Rate limited by Radar API for attacks layer3")
        await safe_edit_text(callback.message, "⏳ Слишком много запросов к Cloudflare. Попробуй через минуту.", get_back_button())
    except asyncio.TimeoutError:
        logger.warning("Timeout fetching attacks layer3")
        await safe_edit_text(callback.message, "⏱ Cloudflare долго отвечает. Попробуй ещё раз.", get_back_button())
    except Exception:
        logger.exception("Failed to fetch attacks layer3 summary")
        await safe_edit_text(callback.message, "⚠️ Не удалось получить данные. Попробуй позже.", get_back_button())
    await callback.answer()


@router.callback_query(F.data == "attacks:layer7")
async def show_attacks_layer7(callback: types.CallbackQuery, radar_client: CloudFlareRadarClient):
    await callback.bot.send_chat_action(callback.message.chat.id, "typing")
    try:
        data = await radar_client.attacks_layer7_summary()
        text = format_attacks_layer7(data)
        await safe_edit_text(callback.message, text, get_back_button())
    except CloudflareRateLimitError:
        logger.warning("Rate limited by Radar API for attacks layer7")
        await safe_edit_text(callback.message, "⏳ Слишком много запросов к Cloudflare. Попробуй через минуту.", get_back_button())
    except asyncio.TimeoutError:
        logger.warning("Timeout fetching attacks layer7")
        await safe_edit_text(callback.message, "⏱ Cloudflare долго отвечает. Попробуй ещё раз.", get_back_button())
    except Exception:
        logger.exception("Failed to fetch attacks layer3 summary")
        await safe_edit_text(callback.message, "⚠️ Не удалось получить данные. Попробуй позже.", get_back_button())
    await callback.answer()


def format_attacks_layer3(data: dict) -> str:
    summary = data["summary_0"]

    udp = float(summary.get("UDP", 0))
    tcp = float(summary.get("TCP", 0))
    gre = float(summary.get("GRE", 0))
    icmp = float(summary.get("ICMP", 0))

    return (
        "🌐 <b>Layer 3 атаки — распределение по протоколам</b>\n\n"
        f"⚡ <b>UDP:</b> {udp:.1f}%\n"
        f"🔌 <b>TCP:</b> {tcp:.1f}%\n"
        f"🛡️ <b>GRE:</b> {gre:.1f}%\n"
        f"📡 <b>ICMP:</b> {icmp:.1f}%\n"
    )

def format_attacks_layer7(data: dict) -> str:
    summary = data["summary_0"]

    get_req = float(summary.get("GET", 0))
    post = float(summary.get("POST", 0))
    head = float(summary.get("HEAD", 0))
    options = float(summary.get("OPTIONS", 0))
    patch = float(summary.get("PATCH", 0))
    put = float(summary.get("PUT", 0))
    delete = float(summary.get("DELETE", 0))

    other = (
            float(summary.get("UNKNOWN", 0))
            + float(summary.get("ACL", 0))
            + float(summary.get("other", 0))
    )

    return (
        "🔥 <b>Layer 7 атаки — распределение по методам</b>\n\n"
        f"📥 <b>GET:</b> {get_req:.1f}%\n"
        f"📤 <b>POST:</b> {post:.1f}%\n"
        f"👤 <b>HEAD:</b> {head:.1f}%\n"
        f"⚙️ <b>OPTIONS:</b> {options:.1f}%\n"
        f"🩹 <b>PATCH:</b> {patch:.1f}%\n"
        f"📦 <b>PUT:</b> {put:.1f}%\n"
        f"🗑️ <b>DELETE:</b> {delete:.1f}%\n"
        f"❓ <b>Другие:</b> {other:.1f}%\n"
    )


@router.callback_query(F.data == "radar:dns")
async def show_dns(callback: types.CallbackQuery, radar_client: CloudFlareRadarClient):
    await callback.bot.send_chat_action(callback.message.chat.id, "typing")
    try:
        data = await radar_client.dns_by_protocol_summary()
        text = format_dns_protocol(data)
        await safe_edit_text(callback.message, text, get_back_button())
    except CloudflareRateLimitError:
        logger.warning("Rate limited by Radar API for DNS protocol")
        await safe_edit_text(callback.message, "⏳ Слишком много запросов к Cloudflare. Попробуй через минуту.", get_back_button())
    except asyncio.TimeoutError:
        logger.warning("Timeout fetching DNS protocol summary")
        await safe_edit_text(callback.message, "⏱ Cloudflare долго отвечает. Попробуй ещё раз.", get_back_button())
    except Exception:
        logger.exception("Failed to fetch DNS protocol summary")
        await safe_edit_text(callback.message, "⚠️ Не удалось получить данные. Попробуй позже.", get_back_button())
    await callback.answer()


def format_dns_protocol(data: dict) -> str:
    summary = data["summary_0"]
    lines = ["🔤 <b>DNS-запросы по протоколу</b>\n"]
    for protocol, value in sorted(summary.items(), key=lambda x: -float(x[1])):
        lines.append(f"{protocol}: {float(value):.1f}%")
    return "\n".join(lines)


@router.callback_query(F.data == "radar:menu")
async def back_to_menu(callback: types.CallbackQuery):
    await safe_edit_text(callback.message, "Выбери, что показать:", get_main_menu())
    await callback.answer()