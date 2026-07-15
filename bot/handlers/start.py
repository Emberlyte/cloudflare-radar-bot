from aiogram import Router, types
from aiogram.filters import Command

from bot.keyboards.main_menu import get_main_menu

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "Привет! Выбери, что показать!!",
        reply_markup=get_main_menu())