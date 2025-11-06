from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F, Router
from database.question_repository import start_ticket
from bot.utils.test_manager import read_ticket
from aiogram.fsm.context import FSMContext
from .ticket_fsm import TestStates, show_question

ticket_router = Router()
question_keyboard = InlineKeyboardBuilder()


@ticket_router.callback_query(F.data.startswith("ticket_"))
async def start_ticket1(callback: CallbackQuery, state: FSMContext):
    ticket_number = int(callback.data.replace("ticket_", ""))

    try:
        ticket_name = f"Билет {ticket_number}"

    except ValueError:
        await callback.answer("Некорректный номер билета")
        return

    ticket_data = await start_ticket(ticket_name)
    questions = read_ticket(ticket_data)

    await state.update_data(
        current_ticket=ticket_number,
        questions=questions,
        current_questions_inxex=0,
        user_answers=[]
    )

    await state.set_state(TestStates.waiting_answer)
    await show_question(callback, questions[0])
