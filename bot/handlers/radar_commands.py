import asyncio
import logging

from aiogram import Router, types, F
from service.cloudflare_radar import CloudFlareRadarClient, CloudflareRateLimitError
from bot.keyboards.main_menu import get_back_button, get_main_menu, get_period_keyboard, get_attacks_menu
from bot.utils.safe_edit import safe_edit_text
from aiogram_i18n import I18nContext

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == "radar:devices")
async def ask_period_devices(callback: types.CallbackQuery, i18n: I18nContext):
    await safe_edit_text(callback.message, i18n.get("period-ask-devices"), get_period_keyboard(i18n, "devices"))
    await callback.answer()


@router.callback_query(F.data.startswith("period:devices:"))
async def show_devices(callback: types.CallbackQuery, radar_client: CloudFlareRadarClient, i18n: I18nContext):
    period = callback.data.split(":")[2]
    await callback.bot.send_chat_action(callback.message.chat.id, "typing")
    try:
        data = await radar_client.summary_device_type(date_range=period)
        text = format_device_summary(data, period, i18n)
        await safe_edit_text(callback.message, text, get_back_button(i18n))
    except CloudflareRateLimitError:
        logger.warning("Rate limited by Radar API for devices, period=%s", period)
        await safe_edit_text(callback.message, i18n.get("error-rate-limited"), get_back_button(i18n))
    except asyncio.TimeoutError:
        logger.warning("Timeout fetching device summary, period=%s", period)
        await safe_edit_text(callback.message, i18n.get("error-timeout"), get_back_button(i18n))
    except Exception:
        logger.exception("Failed to fetch device summary for period=%s", period)
        await safe_edit_text(callback.message, i18n.get("error-generic"), get_back_button(i18n))
    await callback.answer()


def format_device_summary(data: dict, period: str, i18n: I18nContext) -> str:
    summary = data["summary_0"]
    desktop = float(summary["desktop"])
    mobile = float(summary["mobile"])
    other = float(summary["other"])

    period_label = i18n.get(f"period-{period}")

    return i18n.get(
        "devices-title", period=period_label
    ) + "\n\n" + i18n.get("devices-desktop", value=f"{desktop:.1f}") + "\n" \
        + i18n.get("devices-mobile", value=f"{mobile:.1f}") + "\n" \
        + i18n.get("devices-other", value=f"{other:.1f}")

@router.callback_query(F.data == "radar:locations")
async def ask_period_locations(callback: types.CallbackQuery, i18n: I18nContext):
    await safe_edit_text(callback.message, i18n.get("period-ask-locations"), get_period_keyboard(i18n, "locations"))
    await callback.answer()


@router.callback_query(F.data.startswith("period:locations:"))
async def show_locations(callback: types.CallbackQuery, radar_client: CloudFlareRadarClient, i18n: I18nContext):
    period = callback.data.split(":")[2]
    await callback.bot.send_chat_action(callback.message.chat.id, "typing")
    try:
        data = await radar_client.top_location(date_range=period, limit=5)
        text = format_top_locations(data, period, i18n)
        await safe_edit_text(callback.message, text, get_back_button(i18n))
    except CloudflareRateLimitError:
        logger.warning("Rate limited by Radar API for locations, period=%s", period)
        await safe_edit_text(callback.message, i18n.get("error-rate-limited"), get_back_button(i18n))
    except asyncio.TimeoutError:
        logger.warning("Timeout fetching top locations, period=%s", period)
        await safe_edit_text(callback.message, i18n.get("error-timeout"), get_back_button(i18n))
    except Exception:
        logger.exception("Failed to fetch top locations for period=%s", period)
        await safe_edit_text(callback.message, i18n.get("error-generic"), get_back_button(i18n))
    await callback.answer()


def format_top_locations(data: dict, period: str, i18n: I18nContext) -> str:
    locations = data["top_0"]
    period_label = i18n.get(f"period-{period}")
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

    lines = [i18n.get("locations-title", period=period_label) + "\n"]
    for i, loc in enumerate(locations):
        medal = medals[i] if i < len(medals) else f"{i + 1}."
        name = loc["clientCountryName"]
        value = float(loc["value"])
        lines.append(f"{medal} {name}: {value:.1f}%")

    return "\n".join(lines)


@router.callback_query(F.data == "radar:ases")
async def ask_period_ases(callback: types.CallbackQuery, i18n: I18nContext):
    await safe_edit_text(callback.message, i18n.get("period-ask-ases"), get_period_keyboard(i18n, "ases"))
    await callback.answer()


@router.callback_query(F.data.startswith("period:ases:"))
async def show_ases(callback: types.CallbackQuery, radar_client: CloudFlareRadarClient, i18n: I18nContext):
    period = callback.data.split(":")[2]
    await callback.bot.send_chat_action(callback.message.chat.id, "typing")
    try:
        data = await radar_client.top_ases(date_range=period, limit=5)
        text = format_top_ases(data, period, i18n)
        await safe_edit_text(callback.message, text, get_back_button(i18n))
    except CloudflareRateLimitError:
        logger.warning("Rate limited by Radar API for ases, period=%s", period)
        await safe_edit_text(callback.message, i18n.get("error-rate-limited"), get_back_button(i18n))
    except asyncio.TimeoutError:
        logger.warning("Timeout fetching top ases, period=%s", period)
        await safe_edit_text(callback.message, i18n.get("error-timeout"), get_back_button(i18n))
    except Exception:
        logger.exception("Failed to fetch top ases for period=%s", period)
        await safe_edit_text(callback.message, i18n.get("error-generic"), get_back_button(i18n))
    await callback.answer()


def format_top_ases(data: dict, period: str, i18n: I18nContext) -> str:
    ases = data["top_0"]
    period_label = i18n.get(f"period-{period}")
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

    lines = [i18n.get("ases-title", period=period_label) + "\n"]
    for i, asn in enumerate(ases):
        medal = medals[i] if i < len(medals) else f"{i + 1}."
        name = asn["clientASName"]
        value = float(asn["value"])
        lines.append(f"{medal} {name}: {value:.1f}%")

    return "\n".join(lines)


@router.callback_query(F.data == "radar:quality")
async def show_quality(callback: types.CallbackQuery, radar_client: CloudFlareRadarClient, i18n: I18nContext):
    await callback.bot.send_chat_action(callback.message.chat.id, "typing")
    try:
        data = await radar_client.quality_speed()
        text = format_quality_speed(data, i18n)
        await safe_edit_text(callback.message, text, get_back_button(i18n))
    except CloudflareRateLimitError:
        logger.warning("Rate limited by Radar API for quality speed")
        await safe_edit_text(callback.message, i18n.get("error-rate-limited"), get_back_button(i18n))
    except asyncio.TimeoutError:
        logger.warning("Timeout fetching quality speed")
        await safe_edit_text(callback.message, i18n.get("error-timeout"), get_back_button(i18n))
    except Exception:
        logger.exception("Failed to fetch quality speed")
        await safe_edit_text(callback.message, i18n.get("error-generic"), get_back_button(i18n))
    await callback.answer()


def format_quality_speed(data: dict, i18n: I18nContext) -> str:
    summary = data["summary_0"]

    download = float(summary["bandwidthDownload"])
    upload = float(summary["bandwidthUpload"])
    latency_idle = float(summary["latencyIdle"])
    latency_loaded = float(summary["latencyLoaded"])
    jitter_idle = float(summary["jitterIdle"])
    jitter_loaded = float(summary["jitterLoaded"])
    packet_loss = float(summary["packetLoss"])

    return (
        i18n.get("quality-title") + "\n\n"
        + i18n.get("quality-download", value=f"{download:.1f}") + "\n"
        + i18n.get("quality-upload", value=f"{upload:.1f}") + "\n\n"
        + i18n.get("quality-latency-idle", value=f"{latency_idle:.0f}") + "\n"
        + i18n.get("quality-latency-loaded", value=f"{latency_loaded:.0f}") + "\n\n"
        + i18n.get("quality-jitter-idle", value=f"{jitter_idle:.1f}") + "\n"
        + i18n.get("quality-jitter-loaded", value=f"{jitter_loaded:.1f}") + "\n\n"
        + i18n.get("quality-packet-loss", value=f"{packet_loss:.2f}")
    )


@router.callback_query(F.data == "radar:attacks")
async def ask_attack_layer(callback: types.CallbackQuery, i18n: I18nContext):
    await safe_edit_text(callback.message, i18n.get("attacks-menu-title"), get_attacks_menu(i18n))
    await callback.answer()


@router.callback_query(F.data == "attacks:layer3")
async def show_attacks_layer3(callback: types.CallbackQuery, radar_client: CloudFlareRadarClient, i18n: I18nContext):
    await callback.bot.send_chat_action(callback.message.chat.id, "typing")
    try:
        data = await radar_client.attacks_layer3_summary()
        text = format_attacks_layer3(data, i18n)
        await safe_edit_text(callback.message, text, get_back_button(i18n))
    except CloudflareRateLimitError:
        logger.warning("Rate limited by Radar API for attacks layer3")
        await safe_edit_text(callback.message, i18n.get("error-rate-limited"), get_back_button(i18n))
    except asyncio.TimeoutError:
        logger.warning("Timeout fetching attacks layer3")
        await safe_edit_text(callback.message, i18n.get("error-timeout"), get_back_button(i18n))
    except Exception:
        logger.exception("Failed to fetch attacks layer3 summary")
        await safe_edit_text(callback.message, i18n.get("error-generic"), get_back_button(i18n))
    await callback.answer()


@router.callback_query(F.data == "attacks:layer7")
async def show_attacks_layer7(callback: types.CallbackQuery, radar_client: CloudFlareRadarClient, i18n: I18nContext):
    await callback.bot.send_chat_action(callback.message.chat.id, "typing")
    try:
        data = await radar_client.attacks_layer7_summary()
        text = format_attacks_layer7(data, i18n)
        await safe_edit_text(callback.message, text, get_back_button(i18n))
    except CloudflareRateLimitError:
        logger.warning("Rate limited by Radar API for attacks layer7")
        await safe_edit_text(callback.message, i18n.get("error-rate-limited"), get_back_button(i18n))
    except asyncio.TimeoutError:
        logger.warning("Timeout fetching attacks layer7")
        await safe_edit_text(callback.message, i18n.get("error-timeout"), get_back_button(i18n))
    except Exception:
        logger.exception("Failed to fetch attacks layer7 summary")
        await safe_edit_text(callback.message, i18n.get("error-generic"), get_back_button(i18n))
    await callback.answer()


def format_attacks_layer3(data: dict, i18n: I18nContext) -> str:
    summary = data["summary_0"]
    lines = [i18n.get("attacks-layer3-title") + "\n"]
    for protocol, value in sorted(summary.items(), key=lambda x: -float(x[1])):
        lines.append(f"{protocol}: {float(value):.1f}%")
    return "\n".join(lines)


def format_attacks_layer7(data: dict, i18n: I18nContext) -> str:
    summary = data["summary_0"]
    lines = [i18n.get("attacks-layer7-title") + "\n"]
    for method, value in sorted(summary.items(), key=lambda x: -float(x[1])):
        if float(value) > 0.1:
            lines.append(f"{method}: {float(value):.1f}%")
    return "\n".join(lines)


@router.callback_query(F.data == "radar:dns")
async def show_dns(callback: types.CallbackQuery, radar_client: CloudFlareRadarClient, i18n: I18nContext):
    await callback.bot.send_chat_action(callback.message.chat.id, "typing")
    try:
        data = await radar_client.dns_by_protocol_summary()
        text = format_dns_protocol(data, i18n)
        await safe_edit_text(callback.message, text, get_back_button(i18n))
    except CloudflareRateLimitError:
        logger.warning("Rate limited by Radar API for DNS")
        await safe_edit_text(callback.message, i18n.get("error-rate-limited"), get_back_button(i18n))
    except asyncio.TimeoutError:
        logger.warning("Timeout fetching DNS protocol summary")
        await safe_edit_text(callback.message, i18n.get("error-timeout"), get_back_button(i18n))
    except Exception:
        logger.exception("Failed to fetch DNS protocol summary")
        await safe_edit_text(callback.message, i18n.get("error-generic"), get_back_button(i18n))
    await callback.answer()


def format_dns_protocol(data: dict, i18n: I18nContext) -> str:
    summary = data["summary_0"]
    lines = [i18n.get("dns-title") + "\n"]
    for protocol, value in sorted(summary.items(), key=lambda x: -float(x[1])):
        lines.append(f"{protocol}: {float(value):.1f}%")
    return "\n".join(lines)


@router.callback_query(F.data == "radar:email")
async def show_email_threats(callback: types.CallbackQuery, radar_client: CloudFlareRadarClient, i18n: I18nContext):
    await callback.bot.send_chat_action(callback.message.chat.id, "typing")
    try:
        data = await radar_client.email_threat_category_summary()
        text = format_email_threats(data, i18n)
        await safe_edit_text(callback.message, text, get_back_button(i18n))
    except CloudflareRateLimitError:
        logger.warning("Rate limited by Radar API for email threats")
        await safe_edit_text(callback.message, i18n.get("error-rate-limited"), get_back_button(i18n))
    except asyncio.TimeoutError:
        logger.warning("Timeout fetching email threat summary")
        await safe_edit_text(callback.message, i18n.get("error-timeout"), get_back_button(i18n))
    except Exception:
        logger.exception("Failed to fetch email threat summary")
        await safe_edit_text(callback.message, i18n.get("error-generic"), get_back_button(i18n))
    await callback.answer()


def format_email_threats(data: dict, i18n: I18nContext) -> str:
    summary = data["summary_0"]
    period_label = i18n.get("period-30d")

    sorted_threats = sorted(summary.items(), key=lambda x: -float(x[1]))
    top_threats = sorted_threats[:8]

    lines = [i18n.get("email-title", period=period_label) + "\n"]
    for category, value in top_threats:
        lines.append(f"{category}: {float(value):.1f}%")

    lines.append("\n" + i18n.get("email-note"))

    return "\n".join(lines)


@router.callback_query(F.data == "radar:services")
async def show_top_services(callback: types.CallbackQuery, radar_client: CloudFlareRadarClient, i18n: I18nContext):
    await callback.bot.send_chat_action(callback.message.chat.id, "typing")
    try:
        data = await radar_client.top_internet_services(limit=10)
        text = format_top_services(data, i18n)
        await safe_edit_text(callback.message, text, get_back_button(i18n))
    except CloudflareRateLimitError:
        logger.warning("Rate limited by Radar API for top internet services")
        await safe_edit_text(callback.message, i18n.get("error-rate-limited"), get_back_button(i18n))
    except asyncio.TimeoutError:
        logger.warning("Timeout fetching top internet services")
        await safe_edit_text(callback.message, i18n.get("error-timeout"), get_back_button(i18n))
    except Exception:
        logger.exception("Failed to fetch top internet services")
        await safe_edit_text(callback.message, i18n.get("error-generic"), get_back_button(i18n))
    await callback.answer()


def format_top_services(data: dict, i18n: I18nContext) -> str:
    services = data["top_0"]
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    lines = [i18n.get("services-title") + "\n"]
    for item in services:
        rank = item["rank"]
        service = item["service"]
        medal = medals[rank - 1] if rank <= len(medals) else f"{rank}."
        lines.append(f"{medal} {service}")

    return "\n".join(lines)


@router.callback_query(F.data == "radar:menu")
async def back_to_menu(callback: types.CallbackQuery, i18n: I18nContext):
    await safe_edit_text(callback.message, i18n.get("menu-choose"), get_main_menu(i18n))
    await callback.answer()