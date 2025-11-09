import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from bot.handlers.start import start_router
from bot.handlers.menu import menu_router
from bot.handlers.tickets.tickets import ticket_router
from bot.utils.command_menu import commands

load_dotenv(dotenv_path="misc/.env")
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    await bot.set_my_commands(commands)

    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(ticket_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
