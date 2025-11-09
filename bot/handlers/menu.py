from aiogram.types import CallbackQuery, Message
from aiogram import F, Router
from keyboards.menu import make_tickets_list
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


@menu_router.callback_query(F.data == "stats")
async def show_user_stats(callback: CallbackQuery):
    user = callback.from_user

    user_stats = await statistics_repository.get_user_stats(user)

    total_questions = user_stats['total_questions']
    correct_answers = user_stats['correct_answers']
    success_rate = (correct_answers / total_questions * 100) if total_questions > 0 else 0

    await callback.message.answer(
        f"📊 Статистика:\n"
        f"✅ Вопросов: {total_questions}\n"
        f"🎯 Правильно: {correct_answers}\n"
        f"📈 Успех: {success_rate:.1f}%"
    )


@menu_router.message(F.text == "/stats")
async def show_user_stats(message: Message):
    user = message.from_user

    user_stats = await statistics_repository.get_user_stats(user)

    total_questions = user_stats['total_questions']
    correct_answers = user_stats['correct_answers']
    success_rate = (correct_answers / total_questions * 100) if total_questions > 0 else 0

    await message.answer(
        f"📊 Статистика:\n\n"
        f"✅ Всего решено вопросов: {total_questions}\n"
        f"🎯 Правильных ответов: {correct_answers}\n\n"
        f"📈 Процент правильный ответов: {success_rate:.1f}%"
    )
