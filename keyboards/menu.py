from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Решать билеты", callback_data="tickets"),
     InlineKeyboardButton(text="Решать вопросы по темам", callback_data="topics")],
    [InlineKeyboardButton(text="Учить теорию", callback_data="theory"),
     InlineKeyboardButton(text="Просмотреть статистику", callback_data="stats")],
])

