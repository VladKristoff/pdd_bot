from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, FSInputFile, Message

from bot.utils.test_manager import TestManager
from database.models import Question
from keyboards.menu import make_question_keyboard
from aiogram.fsm.context import FSMContext


class TestStates(StatesGroup):
    waiting_for_answer = State()
    showing_explanation = State()


async def show_question(message: Message, question: Question, len_questions: int, current_question_index: int):
    keyboard = await make_question_keyboard(question)

    if question.image_path != "./images/no_image.jpg":
        try:
            photo = FSInputFile(question.image_path)
            await message.answer_photo(
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
            await send_text_question(message, question, keyboard, current_question_index, len_questions)
    else:
        await send_text_question(message, question, keyboard, current_question_index, len_questions)


async def send_text_question(message: Message, question: Question, keyboard, current_question_index: int, len_questions: int):
    await message.answer(
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

async def get_user_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    test_manager: TestManager = data.get("test_manager")

    if not test_manager:
        await message.answer("Тест устарел. Начните заново")
        await state.clear()
        return

    current_question = test_manager.get_current_question()
    if not current_question:
        await message.answer("Вопрос не доступен")
        await state.clear()
        return

    try:
        answer_id = int(message.text)
    except ValueError:
        await message.answer("Неверный ответ")
        return

    test_manager.save_answer(answer_id)

    correct_answer_number = get_correct_answer_id(current_question) # 1-based
    is_correct = (answer_id == correct_answer_number)
    correct_answer_text = current_question.answers[correct_answer_number - 1]['answer_text']

    result_msg = "✅ Правильно!" if is_correct else "❌ Неправильно!"
    full_msg = (
        f"{result_msg}\n"
        f"Правильный ответ: {correct_answer_text}\n\n"
        f"Объяснение:\n{current_question.answer_explanation}"
    )

    await state.set_state(TestStates.showing_explanation)
    await state.update_data(test_manager=test_manager)

    return full_msg
