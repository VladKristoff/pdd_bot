from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder, ReplyKeyboardMarkup

main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📋Билеты", callback_data="tickets"),
     InlineKeyboardButton(text="📚Темы", callback_data="topics")],
    [InlineKeyboardButton(text="🏃‍♂️Марафон (800 вопросов)", callback_data="ticket_marathon")],
    [InlineKeyboardButton(text="📈Просмотреть статистику", callback_data="stats")]
])


async def make_tickets_list():
    tickets_keyboard = InlineKeyboardBuilder()
    tickets_keyboard.add(InlineKeyboardButton(text="?", callback_data="ticket_random"))
    for number in range(1, 41):
        tickets_keyboard.add(InlineKeyboardButton(text=str(number), callback_data=f"ticket_{number}"))

    tickets_keyboard.add(InlineKeyboardButton(text="⬅️Назад", callback_data="back_to_main_menu"))

    return tickets_keyboard.adjust(5).as_markup()


async def make_topics_list():
    topics_keyboard = InlineKeyboardBuilder()

    topics_keyboard.add(InlineKeyboardButton(text="?", callback_data="topic_random"))
    for number in range(1, 27):
        topics_keyboard.add(InlineKeyboardButton(text=f"{number}", callback_data=f"topic_{number}"))

    topics_keyboard.add(InlineKeyboardButton(text="⬅️Назад", callback_data="back_to_main_menu"))

    return topics_keyboard.adjust(5).as_markup()


async def make_question_keyboard(question):
    buttons = []
    row = []

    for i in range(1, len(question.answers) + 1):
        row.append(KeyboardButton(text=str(i)))
        if len(row) == 2:  # по 2 в ряд
            buttons.append(row)
            row = []

    if row:  # если осталась одна кнопка
        buttons.append(row)

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


question_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Следующий")]],
    resize_keyboard=True
)

statistic_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⬅️Назад", callback_data="back_to_main_menu")],
    [InlineKeyboardButton(text="🗑️Сбросить статистику", callback_data="reset_stats")],
    [InlineKeyboardButton(text="📊Стастистика по темам", callback_data="get_topic_stats")]
])

topic_statistic_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⬅️Назад", callback_data="back_to_stats_menu")]
])