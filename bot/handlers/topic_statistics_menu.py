from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import F, Router

from bot.handlers.menu import show_user_stats


topic_stats_router = Router()

@topic_stats_router.callback_query(F.data == "back_to_stats_menu")
async def back_to_stats_menu(callback: CallbackQuery, state: FSMContext):
    await show_user_stats(callback, state)
