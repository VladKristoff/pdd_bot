import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from bot.handlers.start import start_router
from bot.handlers.menu import menu_router
from bot.handlers.tests.topics import topic_router
from bot.handlers.tests.tickets import ticket_router
from bot.handlers.statistics_menu import stats_router
from bot.utils.command_menu import commands
from aiogram.fsm.storage.memory import MemoryStorage
from database.database import db

logging.basicConfig(level=logging.INFO)

load_dotenv(dotenv_path="misc/.env")
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def main():
    await bot.set_my_commands(commands)

    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(ticket_router)
    dp.include_router(topic_router)
    dp.include_router(stats_router)

    await db.connect()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")

