from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Решать билеты", callback_data="tickets")],
    [InlineKeyboardButton(text="Решать вопросы по темам", callback_data="topics")],
    [InlineKeyboardButton(text="Просмотреть статистику", callback_data="stats")],
])


async def make_tickets_keyboard():
    tickets_keyboard = InlineKeyboardBuilder()
    for number in range(1, 41):
        tickets_keyboard.add(InlineKeyboardButton(text=str(number), callback_data=f"ticket{str(number)}"))
    return tickets_keyboard.adjust(5).as_markup()
