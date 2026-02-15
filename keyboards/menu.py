from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder, ReplyKeyboardMarkup

main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🎓Экзамен", callback_data="exam")],
    [InlineKeyboardButton(text="📋Билеты", callback_data="tickets"),
     InlineKeyboardButton(text="📚Темы", callback_data="topics")],
    [InlineKeyboardButton(text="🏃‍♂️Марафон (800 вопросов)", callback_data="ticket_marathon")],
    [InlineKeyboardButton(text="📈Просмотреть статистику", callback_data="stats")]
])


async def make_tickets_list():
    tickets_keyboard = InlineKeyboardBuilder()
    for number in range(1, 41):
        tickets_keyboard.add(InlineKeyboardButton(text=str(number), callback_data=f"ticket_{number}"))
    return tickets_keyboard.adjust(5).as_markup()


async def make_topics_list():
    topics_keyboard = InlineKeyboardBuilder()

    topics = [
        "Общие обязанности водителей",
        "Пешеходные переходы и места остановок маршрутных транспортных средств",
        "Проезд перекрестков",
        "Неисправности и условия допуска транспортных средств к эксплуатации",
        "Буксировка механических транспортных средств",
        "Движение в жилых зонах",
        "Движение через железнодорожные пути",
        "Начало движения, маневрирование",
        "Расположение транспортных средств на проезжей части",
        "Дорожные знаки",
        "Сигналы светофора и регулировщика",
        "Перевозка людей и грузов",
        "Дорожная разметка",
        "Ответственность водителя",
        "Учебная езда и дополнительные требования к движению велосипедистов",
        "Пользование внешними световыми приборами и звуковыми сигналами",
        "Общие положения",
        "Применение специальных сигналов",
        "Движение по автомагистралям",
        "Обгон, опережение, встречный разъезд",
        "Приоритет маршрутных транспортных средств",
        "Скорость движения",
        "Оказание доврачебной медицинской помощи",
        "Применение аварийной сигнализации и знака аварийной остановки",
        "Безопасность движения и техника управления автомобилем",
        "Остановка и стоянка"
    ]
    for i, topic in enumerate(topics):
        topics_keyboard.add(InlineKeyboardButton(text=f"{topic}", callback_data=f"topic_{i+1}"))

    return topics_keyboard.adjust(1).as_markup()


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
    [InlineKeyboardButton(text="Сбросить статистику", callback_data="reset_stats")]
])