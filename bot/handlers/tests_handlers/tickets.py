from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from bot.utils.test_system import TestStates, show_question, get_correct_answer_id, get_user_answer
from requests.statistics_requests import statistics_requests
from requests.question_requests import question_requests
from keyboards.menu import question_menu_keyboard, main_keyboard
from aiogram.fsm.context import FSMContext
from bot.utils.streak_manager import streak_manager
import random

from ..start import start_bot
from ...utils.test_manager import TestManager

ticket_router = Router()


@ticket_router.callback_query(F.data.startswith("ticket_"))
async def start_ticket(callback: CallbackQuery, state: FSMContext):
    try:
        ticket_number = callback.data.replace("ticket_", "")
    except ValueError:
        await callback.answer("Неверный номер билета", show_alert=True)
        return

    test_manager = TestManager(question_requests)

    if ticket_number != "marathon": # Проверка, начал ли пользователь марафон
        if ticket_number == "random": # Проверка, выбрал ли пользователь случайный билет
            ticket_number = random.randint(1, 41) # Если выбрал случайный билет, то ticket_number ->
        try:                                            # меняется с random на случайное число от 1 до 40
            ticket_number_in_bd = f"Билет {ticket_number}"
        except ValueError:
            await callback.answer("Ошибка в начале билета")
            return

        try:
            await callback.answer(f"Билет №{ticket_number}")
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
        await show_question(callback.message, question, len(test_manager.questions), test_manager.current_question_index)

    else:
        try:
            question = await test_manager.start_marathon()
            if not question or not test_manager.questions:
                await callback.answer("Марафон не доступен", show_alert=True)
                return

            await state.update_data(test_manager=test_manager)
            await state.set_state(TestStates.waiting_for_answer)
            await show_question(callback.message, question, len(test_manager.questions), test_manager.current_question_index)
        except ValueError:
            await callback.answer("Ошибка в начале марафона")


@ticket_router.message(TestStates.waiting_for_answer, F.text.in_(["1","2","3","4"]))
async def user_answer(message: Message, state: FSMContext):
    full_msg = await get_user_answer(message, state)

    await message.answer(full_msg, reply_markup=question_menu_keyboard)


@ticket_router.message(TestStates.showing_explanation, F.text == "Следующий")
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
        await streak_manager.update_streak(user)

        await message.answer(
            f"<b>📊 Тест завершён!</b>\n"
            f"✅ Правильных: {results['correct']} из {results['total']}\n"
            f"📈 Результат: {results['percentage']:.1f}%",
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()

@ticket_router.callback_query(F.data == "back_to_main_menu")
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await start_bot(callback.message, state, callback.from_user)