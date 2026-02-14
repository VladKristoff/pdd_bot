from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from bot.utils.test_system import show_question, get_correct_answer_id, TestStates, get_user_answer
from requests.question_requests import question_requests
from requests.statistics_requests import statistics_requests
from bot.utils.test_manager import TestManager
from keyboards.menu import question_menu_keyboard
from aiogram.fsm.context import FSMContext
from bot.utils.streak_manager import streak_manager

topic_router = Router()


@topic_router.callback_query(F.data.startswith("topic_"))
async def start_topic(callback: CallbackQuery, state: FSMContext):
    try:
        topic_number = int(callback.data.replace("topic_", ""))
    except ValueError:
        await callback.answer("Неверный номер темы", show_alert=True)
        return

    test_manager = TestManager(question_requests)
    try:
        question = await test_manager.start_topic(topic_number)
    except Exception as e:
        print(f"Ошибка загрузки темы {topic_number}: {e}")
        await callback.answer("Не удалось загрузить вопросы")
        return

    if not question or not test_manager.questions:
        await callback.answer("Тема пуста")
        return

    await state.update_data(test_manager=test_manager)
    await state.set_state(TestStates.waiting_for_answer)
    await show_question(callback.message, question, len(test_manager.questions), test_manager.current_question_index)


@topic_router.message(TestStates.waiting_for_answer, F.text.in_(["1", "2", "3", "4", "5"]))
async def user_answer(message: Message, state: FSMContext):
    full_msg = await get_user_answer(message, state)

    await message.answer(full_msg, reply_markup=question_menu_keyboard)


@topic_router.message(TestStates.showing_explanation, F.text == "Следующий")
async def next_question(message: Message, state: FSMContext):
    try:
        await message.edit_reply_markup(reply_markup=None)
    except TelegramBadRequest:
        pass

    data = await state.get_data()
    test_manager: TestManager = data.get("test_manager")

    if not test_manager:
        await message.answer("Тест завершён")
        await state.clear()
        return

    next_q = test_manager.next_question()

    if next_q:
        await state.update_data(test_manager=test_manager)
        await state.set_state(TestStates.waiting_for_answer)
        await show_question(message, next_q, len(test_manager.questions), test_manager.current_question_index)
    else:
        # Тест окончен
        results = test_manager.get_results()
        user = message.from_user
        await statistics_requests.update_user_stats(results, user)
        await streak_manager.update_streak(user)

        await message.answer(
            f"<b>📊 Тест завершён!</b>\n"
            f"✅ Правильных: {results['correct']} из {results['total']}\n"
            f"📈 Результат: {results['percentage']:.1f}%",
            parse_mode="HTML"
        )
        await state.clear()