from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Решать билеты", callback_data="tickets")],
    [InlineKeyboardButton(text="Решать вопросы по темам", callback_data="topics")],
    [InlineKeyboardButton(text="Просмотреть статистику", callback_data="stats")],
])


async def make_tickets_list():
    tickets_keyboard = InlineKeyboardBuilder()
    for number in range(1, 41):
        tickets_keyboard.add(InlineKeyboardButton(text=str(number), callback_data=f"ticket_{number}"))
    return tickets_keyboard.adjust(5).as_markup()


async def make_question_keyboard(question):
    question_keyboard = InlineKeyboardBuilder()
    for i in range(1, len(question.answers) + 1):
        question_keyboard.add(InlineKeyboardButton(text=f"{i}", callback_data=f"answer{i}"))
    return question_keyboard.adjust(len(question.answers)).as_markup()


question_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад", callback_data="back"),
     InlineKeyboardButton(text="Следующий", callback_data="next")]
])
