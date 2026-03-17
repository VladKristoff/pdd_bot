from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

from keyboards.menu import make_tickets_list, make_topics_list, statistic_menu_keyboard
from misc.utils.consts import TOPICS
from requests.statistics_requests import statistics_requests

menu_router = Router()

@menu_router.callback_query(F.data == "tickets")
async def show_tickets(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        """Выберите билет, который хотите решить:
<b>? - случайный билет.</b>""",
        reply_markup=await make_tickets_list(),
        parse_mode="HTML"
    )


@menu_router.message(F.text == "/tickets")
async def show_tickets_command(message: Message, state: FSMContext):
    await state.clear()

    await message.answer("Загрузка меню билетов...", reply_markup=ReplyKeyboardRemove())

    await message.answer(
        """Выберите билет, который хотите решить:
<b>? - случайный билет.</b>""",
        reply_markup=await make_tickets_list(),
        parse_mode="HTML"
    )


@menu_router.callback_query(F.data == "topics")
async def show_topics_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "Выберите тему:",
        reply_markup=await make_topics_list()
    )


@menu_router.message(F.text == "/topics")
async def show_topics(message: Message, state: FSMContext):
    await state.clear()

    await message.answer("Загрузка тем...", reply_markup=ReplyKeyboardRemove())

    await message.answer(
        "Выберите тему:",
        reply_markup=await make_topics_list()
    )


@menu_router.callback_query(F.data == "stats")
async def show_user_stats(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    # Получаем общую статистику
    user_stats = await statistics_requests.get_user_stats(callback.from_user)
    total = user_stats["total_questions"]
    correct = user_stats["correct_answers"]
    percent = (correct / total * 100) if total else 0

    # Получаем статистику по темам
    topic_stats = await statistics_requests.get_user_all_topics_stats(str(callback.from_user.id))

    # Создаем словарь для быстрого доступа к статистике по topic_id
    stats_dict = {stat['topic_id']: stat for stat in topic_stats}

    # Формируем основную часть сообщения
    text = (
        f"<b>📊 Общая статистика:</b>\n\n"
        f"✅ Всего решено вопросов: {total}\n"
        f"🎯 Правильных ответов: {correct}\n"
        f"📈 Процент правильных: {percent:.1f}%\n\n"
        f"<b>📚 Статистика по темам:</b>\n"
    )

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=statistic_menu_keyboard
    )


@menu_router.message(F.text == "/stats")
async def show_user_stats_cmd(message: Message, state: FSMContext):
    await state.clear()

    await message.answer("Загрузка статистики...", reply_markup=ReplyKeyboardRemove())

    user_stats = await statistics_requests.get_user_stats(message.from_user)
    total = user_stats["total_questions"]
    correct = user_stats["correct_answers"]
    percent = (correct / total * 100) if total else 0

    await message.answer(
        f"<b>📊 Статистика:\n\n</b>"
        f"✅ Всего решено вопросов: {total}\n"
        f"🎯 Правильных ответов: {correct}\n\n"
        f"📈 Процент правильный ответов: {percent:.1f}%",
        parse_mode="HTML",
        reply_markup=statistic_menu_keyboard
    )
