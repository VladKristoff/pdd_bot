from keyboards.menu import main_keyboard
from aiogram.types import CallbackQuery
from aiogram import F, Router
from keyboards.menu import make_tickets_list
import asyncio

menu_router = Router()


@menu_router.callback_query(F.data == "tickets")
async def show_tickets(callback: CallbackQuery):
    await callback.message.edit_text(text="Выберите билет, который хотите решить",
                                     reply_markup=await make_tickets_list())
