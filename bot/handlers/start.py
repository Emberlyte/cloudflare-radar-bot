from aiogram import Router, types
from aiogram.filters import Command

from bot.keyboards.main_menu import get_main_menu

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "Привет! Выбери, что показать!!",
        reply_markup=get_main_menu())


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