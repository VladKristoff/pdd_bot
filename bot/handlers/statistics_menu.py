from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from aiogram import F, Router

from misc.utils.consts import TOPICS
from requests.statistics_requests import statistics_requests
from keyboards.menu import statistic_menu_keyboard, topic_statistic_menu_keyboard


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

@stats_router.callback_query(F.data == "get_topic_stats")
async def show_topic_stats(callback: CallbackQuery):
    user = str(callback.from_user.id)

    text = "<b>Статистика по каждой теме:</b>\n"

    try:
        topic_stats = await statistics_requests.get_user_all_topics_stats(user)

        # Создаем словарь для быстрого доступа к статистике по topic_id
        stats_dict = {stat['topic_id']: stat for stat in topic_stats}

        # Добавляем статистику по каждой теме
        for topic_id, topic_name in enumerate(TOPICS, 1):
            stat = stats_dict.get(topic_id)

            if stat and stat['total_answers'] > 0:
                # Если есть данные по теме
                topic_total = stat['total_answers']
                topic_correct = stat['correct_answers']
                topic_percent = (topic_correct / topic_total * 100)

                # Добавляем эмодзи в зависимости от процента
                if topic_percent >= 80:
                    emoji = "🟢"
                elif topic_percent >= 60:
                    emoji = "🟡"
                else:
                    emoji = "🔴"

                text += f"\n{emoji} {topic_name}: {topic_correct}/{topic_total} ({topic_percent:.1f}%)\n"
            else:
                # Если тему еще не решали
                text += f"\n⚪ {topic_name}: <b>не решали</b>\n"

        # Добавляем информацию о прогрессе
        solved_topics = len([s for s in topic_stats if s['total_answers'] > 0])
        text += f"\n<b>📊 Прогресс:</b> {solved_topics}/{len(TOPICS)} тем изучено"
    except TelegramBadRequest:
        pass

    try:
        await callback.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=topic_statistic_menu_keyboard
        )
    except Exception as e:
        print(f"Ошибка в отправке статистики по темам: {e}")