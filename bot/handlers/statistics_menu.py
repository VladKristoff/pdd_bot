from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from aiogram import F, Router
from requests.statistics_requests import statistics_requests
from keyboards.menu import statistic_menu_keyboard


stats_router = Router()

@stats_router.callback_query(F.data == "reset_stats")
async def reset_stats(callback: CallbackQuery):
    user = callback.from_user
    try:
        await statistics_requests.reset_user_stats(user)
        await callback.answer("Статистика успешно сброшена")
        user_stats = await statistics_requests.get_user_stats(user)

        total_questions = user_stats['total_questions']
        correct_answers = user_stats['correct_answers']
        success_rate = (correct_answers / total_questions * 100) if total_questions > 0 else 0

        try:
            await callback.message.edit_text(
                f"<b>📊 Статистика:\n\n</b>"
                f"✅ Всего решено вопросов: {total_questions}\n"
                f"🎯 Правильных ответов: {correct_answers}\n\n"
                f"📈 Процент правильный ответов: {success_rate:.1f}%",
                parse_mode="HTML",
                reply_markup=statistic_menu_keyboard
            )
        except TelegramBadRequest:
            pass
    except Exception as e:
        await callback.answer(f"Ошибка в сбросе статистики: {e}")
