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
    if question.image_path != "./images/no_image.jpg":
        with open(f"{question.image_path}", "rb") as photo:
            await callback.message.answer_photo(photo=f"{photo}",
                                                caption=(
                                                        f"Вопрос №{question.question_number_in_ticket}\n"
                                                        f"{question.question_text}\n\n"
                                                        + "\n".join(f"{i}. {ans['answer_text']}" for i, ans in
                                                                    enumerate(question.answers, 1))),
                                                reply_markup=keyboard)
    else:
        await callback.message.answer(text=f"Вопрос №{question.question_number_in_ticket}\n"
                                            f"{question.question_text}\n\n"
                                            + "\n".join(f"{i}. {ans['answer_text']}" for i, ans in enumerate(question.answers, 1)),
                                            reply_markup=keyboard)
