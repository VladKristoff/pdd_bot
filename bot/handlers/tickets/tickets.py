from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F, Router
from database.question_repository import start_ticket
from bot.utils.test_manager import read_ticket
from aiogram.fsm.context import FSMContext
from .ticket_fsm import TestStates, show_question

ticket_router = Router()
question_keyboard = InlineKeyboardBuilder()


@ticket_router.callback_query(F.data == "ticket1")
async def start_ticket1(callback: CallbackQuery, state: FSMContext):
    ticket_data = await start_ticket("Билет 1")
    questions = read_ticket(ticket_data)

    await state.update_data(
        current_ticket=1,
        questions=questions,
        current_questions_inxex=0,
        user_answers=[]
    )

    await state.set_state(TestStates.waiting_answer)
    await show_question(callback, questions[0])



