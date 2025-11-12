from aiogram.types import CallbackQuery, Message
from aiogram import F, Router
from keyboards.menu import make_tickets_list, make_topics_list, statistic_menu_keyboard
from repositories.statistics_repository import statistics_repository

menu_router = Router()


@menu_router.callback_query(F.data == "tickets")
async def show_tickets(callback: CallbackQuery):
    await callback.message.edit_text(text="Выберите билет, который хотите решить",
                                     reply_markup=await make_tickets_list())


@menu_router.message(F.text == "/tickets")
async def show_tickets_command(message: Message):
    await message.answer(
        text="Выберите билет, который хотите решить",
        reply_markup=await make_tickets_list()
    )


@menu_router.callback_query(F.data == "topics")
async def show_tickets(callback: CallbackQuery):
    await callback.message.edit_text(text="Выберите тему, вопросы по которой хотите пройти",
                                     reply_markup=await make_topics_list())


@menu_router.message(F.text == "/topics")
async def show_topics(message: Message):
    await message.answer(text="Выберите тему, вопросы по которой хотите пройти",
                         reply_markup=await make_topics_list())


@menu_router.callback_query(F.data == "stats")
async def show_user_stats(callback: CallbackQuery):
    user = callback.from_user

    user_stats = await statistics_repository.get_user_stats(user)

    total_questions = user_stats['total_questions']
    correct_answers = user_stats['correct_answers']
    success_rate = (correct_answers / total_questions * 100) if total_questions > 0 else 0

    await callback.message.answer(
        f"<b>📊 Статистика:\n\n</b>"
        f"✅ Всего решено вопросов: {total_questions}\n"
        f"🎯 Правильных ответов: {correct_answers}\n\n"
        f"📈 Процент правильный ответов: {success_rate:.1f}%",
        parse_mode="HTML",
        reply_markup=statistic_menu_keyboard
    )


@menu_router.message(F.text == "/stats")
async def show_user_stats(message: Message):
    user = message.from_user

    user_stats = await statistics_repository.get_user_stats(user)

    total_questions = user_stats['total_questions']
    correct_answers = user_stats['correct_answers']
    success_rate = (correct_answers / total_questions * 100) if total_questions > 0 else 0

    await message.answer(
        f"<b>📊 Статистика:\n\n</b>"
        f"✅ Всего решено вопросов: {total_questions}\n"
        f"🎯 Правильных ответов: {correct_answers}\n\n"
        f"📈 Процент правильный ответов: {success_rate:.1f}%",
        parse_mode="HTML",
        reply_markup=statistic_menu_keyboard
    )
