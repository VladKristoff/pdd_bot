from aiogram import types

commands = [
    types.BotCommand(command="start", description="🏠Главное меню"),
    types.BotCommand(command="tickets", description="📋Решать билеты"),
    types.BotCommand(command="topics", description="📚Решать вопросы по темам"),
    types.BotCommand(command="stats", description="📈Просмотреть статистику")
]