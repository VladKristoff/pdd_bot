from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, FSInputFile
from database.models import Question
from keyboards.menu import make_question_keyboard


class TestStates(StatesGroup):
    waiting_for_answer = State()
    showing_explanation = State()


async def show_question(callback: CallbackQuery, question: Question, len_questions: int, current_question_index: int):
    keyboard = await make_question_keyboard(question)

    await callback.message.delete()
    if question.image_path != "./images/no_image.jpg":
        try:
            photo = FSInputFile(question.image_path)
            await callback.message.answer_photo(
                photo=photo,
                caption=(
                        f"Вопрос {current_question_index + 1} из {len_questions}\n"
                        f"{question.question_text}\n\n"
                        + "\n".join(f"{i}. {ans['answer_text']}" for i, ans in enumerate(question.answers, 1))
                ),
                reply_markup=keyboard
            )
        except Exception as e:
            print(f"Не удалось отправить картинку {e}")
            await send_text_question(callback, question, keyboard, current_question_index, len_questions)
    else:
        await send_text_question(callback, question, keyboard, current_question_index, len_questions)


async def send_text_question(callback: CallbackQuery, question: Question, keyboard, current_question_index: int, len_questions: int):
    await callback.message.answer(
        text=f"Вопрос {current_question_index + 1} из {len_questions}\n"
             f"{question.question_text}\n\n"
             + "\n".join(f"{i}. {ans['answer_text']}" for i, ans in enumerate(question.answers, 1)),
        reply_markup=keyboard
    )


def get_correct_answer_id(question: Question):
    for i, answer in enumerate(question.answers):
        if answer['is_correct']:
            return i + 1

    raise ValueError(f"Не найден правильный ответ для вопроса: {question.id}")
