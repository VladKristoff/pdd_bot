from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from .test_system import TestStates, show_question, get_correct_answer_id
from requests.statistics_requests import statistics_repository
from requests.question_requests import question_repository
from keyboards.menu import question_menu_keyboard
from aiogram.fsm.context import FSMContext

from ...utils.test_manager import TestManager

ticket_router = Router()
question_keyboard = InlineKeyboardBuilder()


@ticket_router.callback_query(F.data.startswith("ticket_"))
async def start_ticket(callback: CallbackQuery, state: FSMContext):
    try:
        ticket_number = callback.data.replace("ticket_", "")
    except ValueError:
        await callback.answer("Неверный номер билета", show_alert=True)
        return

    test_manager = TestManager(question_repository)

    if ticket_number != "marathon":
        try:
            ticket_number_in_bd = f"Билет {ticket_number}"
        except ValueError:
            await callback.answer("Ошибка в начале билета")
            return

        try:
            question = await test_manager.start_ticket(ticket_number_in_bd)
        except Exception as e:
            print(f"Ошибка в загрузке билета {ticket_number_in_bd}: {e}")
            await callback.answer("Не удалось загрузить вопросы", show_alert=True)
            return

        if not question or not test_manager.questions:
            await callback.answer("Билет пустой", show_alert=True)
            return

        await state.update_data(test_manager=test_manager)
        await state.set_state(TestStates.waiting_for_answer)
        await show_question(callback, question, len(test_manager.questions), test_manager.current_question_index)

    else:
        try:
            question = await test_manager.start_marathon()
            if not question or not test_manager.questions:
                await callback.answer("Марафон не доступен", show_alert=True)
                return

            await state.update_data(test_manager=test_manager)
            await state.set_state(TestStates.waiting_for_answer)
            await show_question(callback, question, len(test_manager.questions), test_manager.current_question_index)
        except ValueError:
            await callback.answer("Ошибка в начале марафона")


@ticket_router.callback_query(TestStates.waiting_for_answer, F.data.startswith("answer"))
async def user_answer(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    test_manager: TestManager = data.get("test_manager")

    if not test_manager:
        await callback.answer("Тест устарел. Начните заново", show_alert=True)
        await state.clear()
        return

    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass

    current_question = test_manager.get_current_question()
    if not current_question:
        await callback.answer("Вопрос не доступен", show_alert=True)
        await state.clear()
        return

    try:
        answer_id = int(callback.data.replace("answer", ""))
    except ValueError:
        await callback.answer("Неверный ответ", show_alert=True)
        return

    test_manager.save_answer(answer_id)

    correct_answer_number = get_correct_answer_id(current_question) # 1-based
    is_correct = (answer_id == correct_answer_number)
    correct_answer_text = current_question.answers[correct_answer_number - 1]['answer_text']
    result_msg = "✅ Правильно!" if is_correct else "❌ Неправильно!"
    full_msg = (
        f"{result_msg}\n"
        f"Правильный ответ: {correct_answer_text}\n\n"
        f"Объяснение:\n{current_question.answer_explanation}"
    )

    await callback.message.answer(full_msg, reply_markup=question_menu_keyboard)
    await state.set_state(TestStates.showing_explanation)
    await state.update_data(test_manager=test_manager)


@ticket_router.callback_query(TestStates.showing_explanation, F.data == "next")
async def next_question(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except TelegramBadRequest:
        pass

    data = await state.get_data()
    test_manager: TestManager = data.get("test_manager")

    if not test_manager:
        await callback.answer("Тест завершён", show_alert=True)
        await state.clear()
        return

    next_q = test_manager.next_question()

    if next_q:
        await state.update_data(test_manager=test_manager)
        await state.set_state(TestStates.waiting_for_answer)
        await show_question(callback, next_q, len(test_manager.questions), test_manager.current_question_index)
    else:
        # Тест окончен
        results = test_manager.get_results()
        user = callback.from_user
        await statistics_repository.update_user_stats(results, user)

        await callback.message.answer(
            f"<b>📊 Тест завершён!</b>\n"
            f"✅ Правильных: {results['correct']} из {results['total']}\n"
            f"📈 Результат: {results['percentage']:.1f}%",
            parse_mode="HTML"
        )
        await state.clear()