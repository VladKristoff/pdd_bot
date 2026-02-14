from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

from keyboards.menu import make_tickets_list, make_topics_list, statistic_menu_keyboard, accept_exam_keyboard
from requests.statistics_requests import statistics_requests

menu_router = Router()

text = """Режим "Экзамен" полностью имитирует официальный тест в ГИБДД. 
Вам будет предложено 20 случайных вопросов. На выполнение дается 20 минут. 
Чтобы успешно сдать, нужно ответить на все вопросы, допустив не более 2 ошибок. Если ошибок 3 или больше, либо две ошибки будут сделаны в одном тематическом блоке, экзамен считается несданным. 
Во время прохождения подсказки и возможность исправить ответ недоступны — всё как на реальном экзамене. 
Результат и разбор ошибок вы увидите после завершения теста.
    
<b>Начать экзамен?</b>"""

@menu_router.message(F.text == "/exam")
async def show_exam_description(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text, reply_markup=accept_exam_keyboard,
                         parse_mode="HTML")

@menu_router.callback_query(F.data == "exam")
async def show_exam_description(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(text, reply_markup=accept_exam_keyboard,
                                  parse_mode="HTML")

@menu_router.callback_query(F.data == "tickets")
async def show_tickets(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "Выберите билет, который хотите решить",
        reply_markup=await make_tickets_list()
    )


@menu_router.message(F.text == "/tickets")
async def show_tickets_command(message: Message, state: FSMContext):
    await state.clear()

    await message.answer("Загрузка меню билетов...", reply_markup=ReplyKeyboardRemove())

    await message.answer(
        "Выберите билет, который хотите решить",
        reply_markup=await make_tickets_list()
    )


@menu_router.callback_query(F.data == "topics")
async def show_topics_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "Выберите тему, вопросы по которой хотите пройти",
        reply_markup=await make_topics_list()
    )


@menu_router.message(F.text == "/topics")
async def show_topics(message: Message, state: FSMContext):
    await state.clear()

    await message.answer("Загрузка тем...", reply_markup=ReplyKeyboardRemove())

    await message.answer(
        "Выберите тему, вопросы по которой хотите пройти",
        reply_markup=await make_topics_list()
    )


@menu_router.callback_query(F.data == "stats")
async def show_user_stats(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    user_stats = await statistics_requests.get_user_stats(callback.from_user)
    total = user_stats["total_questions"]
    correct = user_stats["correct_answers"]
    percent = (correct / total * 100) if total else 0

    await callback.message.edit_text(
        f"<b>📊 Статистика:\n\n</b>"
        f"✅ Всего решено вопросов: {total}\n"
        f"🎯 Правильных ответов: {correct}\n\n"
        f"📈 Процент правильный ответов: {percent:.1f}%",
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
