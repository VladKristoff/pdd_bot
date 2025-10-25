from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.menu import menu_keyboard


router = Router()


@router.message(CommandStart())
async def start_bot(message: Message):
    await message.answer(text="Привет, это бот поможет тебе выучить теорию ПДД",
                         reply_markup=menu_keyboard)
