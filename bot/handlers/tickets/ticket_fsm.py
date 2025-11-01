from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from database.models import Question
from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.menu import make_question_keyboard


class TestStates(StatesGroup):
    waiting_answer = State()
    showing_explanation = State()


async def show_question(callback: CallbackQuery, question: Question):
    keyboard = await make_question_keyboard(question)

    await callback.message.delete()
    with open(f"{question.image_path}", "rb") as photo:
        await callback.message.answer_photo(photo=f"{photo}",
                                            caption=f"Вопрос №{question.question_number_in_ticket}\n{question.question_text}",
                                            reply_markup=keyboard)
