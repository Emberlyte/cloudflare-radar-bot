from aiogram import Dispatcher

from bot.handlers import start, radar_commands

def register_handlers(dp: Dispatcher):
    dp.include_router(start.router)
    dp.include_router(radar_commands.router)