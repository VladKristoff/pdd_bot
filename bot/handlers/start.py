from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.menu import main_keyboard

start_router = Router()


@start_router.message(CommandStart())
async def start_bot(message: Message):
    user = message.from_user
    await message.answer(text=
                         f"""Рады видеть вас, <b>{user.first_name}!</b>
Этот бот поможет тебе выучить теорию ПДД""",
                         parse_mode="HTML",
                         reply_markup=main_keyboard)
