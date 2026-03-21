from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.menu import main_keyboard
from bot.utils.streak_manager import streak_manager
from aiogram.fsm.context import FSMContext


start_router = Router()


@start_router.message(CommandStart())
async def start_bot(message: Message, state: FSMContext, user=None):
    await state.clear()

    if user is None:
        user = message.from_user

    await streak_manager.check_streak(user)
    streak = await streak_manager.get_streak(user)

    if streak is not None:
        if streak > 0:
            text = f"<b>Ваша серия: {streak} 🔥</b>"
        else:
            text = f"""Решайте билеты каждый день, чтобы накопить серию

<b>Ваша серия: {streak}</b>"""
    else:
        text = "Решите билет, чтобы начать серию"

    try:
        await message.edit_text(
            f"""
        Этот бот поможет вам выучить теорию ПДД

{text}

👇 <b>Выберите действие:</b> 👇
        """,
            parse_mode="HTML",
            reply_markup=main_keyboard
        )
    except:
        await message.answer(f"Рады видеть вас, <b>{user.first_name}</b>!",
                             reply_markup=ReplyKeyboardRemove(),
                             parse_mode="HTML")
        await message.answer(
            f"""
Этот бот поможет вам выучить теорию ПДД

{text}

👇 <b>Выберите действие:</b> 👇
        """,
            parse_mode="HTML",
            reply_markup=main_keyboard
        )
