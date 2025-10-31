from keyboards.menu import main_keyboard
from aiogram.types import CallbackQuery
from aiogram import F, Router
from keyboards.menu import make_tickets_keyboard
import asyncio

menu_router = Router()


@menu_router.callback_query(F.data == "tickets")
async def show_tickets(callback: CallbackQuery):
    await callback.answer(text="Вы выбрали решать билеты")
    await callback.message.answer(text="Выберите билет, который хотите решить",
                                  reply_markup=await make_tickets_keyboard())
