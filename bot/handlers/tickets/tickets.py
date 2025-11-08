from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from .ticket_fsm import TestStates, show_question, get_correct_answer_id
from repositories.question_repository import question_repository
from bot.utils.test_manager import TestManager
from keyboards.menu import question_menu_keyboard

ticket_router = Router()
question_keyboard = InlineKeyboardBuilder()

test_manager = TestManager(question_repository)


@ticket_router.callback_query(F.data.startswith("ticket_"))
async def start_ticket(callback: CallbackQuery):
    ticket_number = callback.data.replace("ticket_", "")

    try:
        ticket_number_in_bd = f"Билет {ticket_number}"

    except ValueError:
        await callback.answer("Некорректный номер билета")
        return

    question = await test_manager.start_ticket(ticket_number_in_bd)

    await show_question(callback, question)


@ticket_router.callback_query(F.data.startswith("answer"))
async def user_answer(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)

    question = test_manager.get_current_question()
    true_answer = question.correct_answer

    test_manager.save_answer(true_answer)

    answer_id = int(callback.data.replace("answer", ""))
    correct_answer_id = get_correct_answer_id(question)
    correct_answer_text = question.answers[answer_id-1]['answer_text']

    if answer_id == correct_answer_id:
        text = "✔️Правильно!"
    else:
        text = "❌Неправильно"

    await callback.message.answer(
        text=text + f"\nПравильный ответ: {correct_answer_text}"
        + "\n\nОбъяснение:\n" + question.answer_explanation,
        reply_markup=question_menu_keyboard
    )
