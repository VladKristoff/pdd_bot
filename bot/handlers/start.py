from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.menu import main_keyboard
from requests.statistics_requests import statistics_repository

start_router = Router()

@start_router.message(CommandStart())
async def start_bot(message: Message):
    user = message.from_user

    # Создаём текст сообщения
    streak = await statistics_repository.get_streak(user)

    if streak is not None:
        if streak > 0:
            text = f"<b>Ваша серия: {streak} 🔥</b>"
        else:
            text = f"Решайте билеты каждый день, чтобы накопить серию, текущая серия: {streak}"
    else:
        text = "Не удалось получить серию"

    # Выводим приветственное сообщение
    await message.answer(text = f"""
Рады видеть вас, <b>{user.first_name}</b>! 

Этот бот поможет вам выучить теорию ПДД

{text}

👇 <b>Выберите действие:</b> 👇
""",
                         parse_mode="HTML",
                         reply_markup=main_keyboard)
