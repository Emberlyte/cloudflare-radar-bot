from aiogram import Router, types, F
from service.cloudflare_radar import CloudFlareRadarClient

from bot.keyboards.main_menu import get_back_button
from bot.keyboards.main_menu import get_main_menu
router = Router()

@router.callback_query(F.data == "radar:devices")
async def show_devices(callback: types.CallbackQuery, radar_client: CloudFlareRadarClient):
    data = await radar_client.summary_device_type()
    text = format_device_summary(data)

    await callback.message.edit_text(text, reply_markup=get_back_button())
    await callback.answer()


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

@router.callback_query(F.data == "radar:menu")
async def back_to_menu(callback: types.CallbackQuery):
    await callback.message.edit_text("Выбери, что показать:", reply_markup=get_main_menu())
    await callback.answer()