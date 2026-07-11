from aiogram import Router, types
from aiogram.filters import Command

from service.cloudflare_radar import CloudFlareRadarClient

router = Router()

@router.message(Command("top_devices"))
async def top_devices_handler(message: types.Message, radar_client: CloudFlareRadarClient):
    data = await radar_client.summary_device_type()
    text = format_device_summary(data)
    await message.answer(str(text))

def format_device_summary(data: dict) -> str:
    summary = data["summary_0"]

    desktop = float(summary["desktop"])
    mobile = float(summary["mobile"])
    other = float(summary["other"])

    return (
        "📊 <b>Распределение трафика по устройствам</b>\n\n"
        f"🖥 Десктоп: {desktop:.1f}%\n"
        f"📱 Мобильные: {mobile:.1f}%\n"
        f"❓ Другое: {other:.1f}%"
    )