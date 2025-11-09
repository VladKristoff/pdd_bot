from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from .ticket_fsm import TestStates, show_question, get_correct_answer_id
from repositories.question_repository import question_repository
from repositories.statistics_repository import statistics_repository
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

    user_answer_text = callback.data.replace("answer", "")
    answer_id = int(user_answer_text)

    test_manager.save_answer(answer_id)

    correct_answer_id = get_correct_answer_id(question)
    correct_answer_text = question.answers[correct_answer_id - 1]['answer_text']

    if answer_id == correct_answer_id:
        text = "✔️Правильно!"
    else:
        text = "❌Неправильно"

    await callback.message.answer(
        text=text + f"\nПравильный ответ: {correct_answer_text}"
        + "\n\nОбъяснение:\n" + question.answer_explanation,
        reply_markup=question_menu_keyboard
    )


@ticket_router.callback_query(F.data == "next")
async def next_question(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    question = test_manager.next_question()

    if question:
        await show_question(callback, question)
    else:
        user = callback.from_user
        results = test_manager.get_results()

        await statistics_repository.update_user_stats(results, user)

        await callback.message.answer(
            f"📊 Тест завершен!\n"
            f"✅ Правильных ответов: {results['correct']} из {results['total']}"
            f"\n📈 Результат: {results['percentage']:.1f}%"
        )
