# tests/test_bot_modules.py
import sys
import os

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import date, timedelta
from database.models import Question
from bot.utils.test_manager import TestManager
from bot.utils.streak_manager import streak_manager
from requests.statistics_requests import statistics_requests
from requests.question_requests import question_requests
from keyboards.menu import make_question_keyboard, make_tickets_list, make_topics_list
from misc.utils.consts import TOPICS


# ==================== ТЕСТ 1: Модель вопроса ====================
class TestQuestionModel:
    def test_question_creation(self):
        """Тест создания модели вопроса"""
        question = Question(
            id="1",
            question_text="Какой знак запрещает движение?",
            answers=[
                {"answer_text": "Знак 3.1", "is_correct": True},
                {"answer_text": "Знак 1.1", "is_correct": False},
            ],
            correct_answer="1",
            image_path="./images/test.jpg",
            answer_explanation="Знак 3.1 'Въезд запрещен'",
            question_number_in_ticket=1,
            topic_id=1
        )

        assert question.id == "1"
        assert question.question_text == "Какой знак запрещает движение?"
        assert len(question.answers) == 2
        assert question.answers[0]["is_correct"] is True
        assert question.topic_id == 1


# ==================== ТЕСТ 2: Константы тем ====================
class TestTopicsConst:
    def test_topics_count(self):
        """Тест количества тем"""
        assert len(TOPICS) == 26

    def test_first_topic(self):
        """Тест первой темы"""
        assert TOPICS[0] == "1. Общие обязанности водителей"

    def test_last_topic(self):
        """Тест последней темы"""
        assert TOPICS[25] == "26. Остановка и стоянка"


# ==================== ТЕСТ 3: TestManager - начало билета ====================
class TestTestManager:
    @pytest.mark.asyncio
    async def test_start_ticket(self):
        """Тест начала работы с билетом"""
        mock_repo = AsyncMock()
        sample_question = Question(
            id="1", question_text="Test", answers=[], correct_answer="1",
            answer_explanation="", question_number_in_ticket=1, topic_id=1
        )
        mock_repo.get_ticket_questions.return_value = [sample_question]

        manager = TestManager(mock_repo)
        question = await manager.start_ticket("Билет 1")

        assert question == sample_question
        assert len(manager.questions) == 1
        assert manager.current_question_index == 0
        mock_repo.get_ticket_questions.assert_called_once_with("Билет 1")

    @pytest.mark.asyncio
    async def test_start_topic(self):
        """Тест начала работы с темой"""
        mock_repo = AsyncMock()
        sample_question = Question(
            id="1", question_text="Test", answers=[], correct_answer="1",
            answer_explanation="", question_number_in_ticket=1, topic_id=1
        )
        mock_repo.get_topic_questions.return_value = [sample_question]

        manager = TestManager(mock_repo)
        question = await manager.start_topic(1)

        assert question == sample_question
        mock_repo.get_topic_questions.assert_called_once_with(1)


# ==================== ТЕСТ 4: TestManager - навигация ====================
class TestTestManagerNavigation:
    def test_next_question(self):
        """Тест перехода к следующему вопросу"""
        manager = TestManager(AsyncMock())
        manager.questions = ["q1", "q2"]
        manager.current_question_index = 0

        next_q = manager.next_question()

        assert manager.current_question_index == 1
        assert next_q == "q2"

    def test_previous_question(self):
        """Тест перехода к предыдущему вопросу"""
        manager = TestManager(AsyncMock())
        manager.questions = ["q1", "q2"]
        manager.current_question_index = 1

        prev_q = manager.previous_question()

        assert manager.current_question_index == 0
        assert prev_q == "q1"

    def test_get_current_question(self):
        """Тест получения текущего вопроса"""
        manager = TestManager(AsyncMock())
        manager.questions = ["current"]
        manager.current_question_index = 0

        assert manager.get_current_question() == "current"


# ==================== ТЕСТ 5: TestManager - результаты ====================
class TestTestManagerResults:
    def test_empty_results(self):
        """Тест результатов пустого теста"""
        manager = TestManager(AsyncMock())
        manager.questions = []

        results = manager.get_results()

        assert results["correct"] == 0
        assert results["total"] == 0
        assert results["percentage"] == 0

    def test_results_with_questions(self):
        """Тест результатов с вопросами"""
        manager = TestManager(AsyncMock())
        question = Question(
            id="1", question_text="Test", answers=[
                {"answer_text": "A1", "is_correct": True},
                {"answer_text": "A2", "is_correct": False}
            ],
            correct_answer="Правильный ответ: 1",
            answer_explanation="",
            question_number_in_ticket=1, topic_id=1
        )
        manager.questions = [question]
        manager.user_answers = {0: 1}

        results = manager.get_results()

        assert results["correct"] == 1
        assert results["total"] == 1
        assert results["percentage"] == 100.0


# ==================== ТЕСТ 6: Статистика пользователя ====================
class TestStatisticsUser:
    @pytest.mark.asyncio
    async def test_update_new_user(self):
        """Тест обновления статистики нового пользователя"""
        mock_user = MagicMock()
        mock_user.id = 12345
        mock_user.username = "test"
        mock_user.full_name = "Test User"
        results = {"total": 10, "correct": 8}

        # Создаем асинхронный мок для db
        mock_db = AsyncMock()
        mock_db.fetcher.return_value = None

        with patch('requests.statistics_requests.db', mock_db):
            await statistics_requests.update_user_stats(results, mock_user)

            mock_db.execute.assert_called_once()
            call_args = mock_db.execute.call_args[0][0]
            assert "INSERT INTO users" in call_args

    @pytest.mark.asyncio
    async def test_get_user_stats(self):
        """Тест получения статистики пользователя"""
        mock_user = MagicMock()
        mock_user.id = 12345
        expected = {"total_questions": 50, "correct_answers": 40}

        mock_db = AsyncMock()
        mock_db.fetcher.return_value = expected

        with patch('requests.statistics_requests.db', mock_db):
            stats = await statistics_requests.get_user_stats(mock_user)

            assert stats == expected


# ==================== ТЕСТ 7: Статистика по темам ====================
class TestStatisticsTopics:
    @pytest.mark.asyncio
    async def test_update_topic_stat(self):
        """Тест обновления статистики по теме"""
        mock_db = AsyncMock()

        with patch('requests.statistics_requests.db', mock_db):
            await statistics_requests.update_topic_stat("12345", 1, True)

            mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_all_topics_stats(self):
        """Тест получения статистики по всем темам"""
        expected = [{"topic_id": 1, "topic_name": "Тема 1", "total_answers": 10, "correct_answers": 8}]

        mock_db = AsyncMock()
        mock_db.fetch.return_value = expected

        with patch('requests.statistics_requests.db', mock_db):
            stats = await statistics_requests.get_user_all_topics_stats("12345")

            assert len(stats) == 1
            assert stats[0]["topic_id"] == 1

    @pytest.mark.asyncio
    async def test_reset_user_topic_stats(self):
        """Тест сброса статистики по темам"""
        mock_db = AsyncMock()

        with patch('requests.statistics_requests.db', mock_db):
            await statistics_requests.reset_user_topic_stats("12345")

            mock_db.execute.assert_called_once_with(
                "DELETE FROM user_topic_stats WHERE user_id = $1",
                "12345"
            )


# ==================== ТЕСТ 8: StreakManager ====================
class TestStreakManager:
    @pytest.mark.asyncio
    async def test_get_streak(self):
        """Тест получения стрика"""
        mock_user = MagicMock()
        mock_user.id = 12345

        mock_db = AsyncMock()
        mock_db.fetcher.return_value = {"streak": 7}

        with patch('bot.utils.streak_manager.db', mock_db):
            streak = await streak_manager.get_streak(mock_user)

            assert streak == 7

    @pytest.mark.asyncio
    async def test_check_streak_keep(self):
        """Тест сохранения стрика при ежедневном решении"""
        mock_user = MagicMock()
        mock_user.id = 12345
        today = date.today()

        mock_db = AsyncMock()
        mock_db.fetcher.return_value = {
            "streak": 5,
            "last_solved_date": today
        }

        with patch('bot.utils.streak_manager.db', mock_db):
            await streak_manager.check_streak(mock_user)

            # Если решал сегодня, стрик не должен сбрасываться
            mock_db.execute.assert_not_called()

    @pytest.mark.asyncio
    async def test_check_streak_reset(self):
        """Тест сброса стрика при пропуске дня"""
        mock_user = MagicMock()
        mock_user.id = 12345
        two_days_ago = date.today() - timedelta(days=2)

        mock_db = AsyncMock()
        mock_db.fetcher.return_value = {
            "streak": 5,
            "last_solved_date": two_days_ago
        }

        with patch('bot.utils.streak_manager.db', mock_db):
            await streak_manager.check_streak(mock_user)

            mock_db.execute.assert_called_once()
            call_args = mock_db.execute.call_args[0]
            assert call_args[1] == 0

    @pytest.mark.asyncio
    async def test_update_streak(self):
        """Тест обновления стрика"""
        mock_user = MagicMock()
        mock_user.id = 12345

        mock_db = AsyncMock()
        mock_db.fetcher.return_value = {
            "streak": 3,
            "last_solved_date": date.today() - timedelta(days=1)
        }

        with patch('bot.utils.streak_manager.db', mock_db):
            await streak_manager.update_streak(mock_user)

            mock_db.execute.assert_called_once()
            call_args = mock_db.execute.call_args[0]
            assert call_args[1] == 4


# ==================== ТЕСТ 9: QuestionRequests ====================
class TestQuestionRequests:
    @pytest.mark.asyncio
    async def test_get_ticket_questions(self):
        """Тест получения вопросов по билету"""
        mock_db = AsyncMock()
        mock_db.fetch.return_value = [{
            'id': '1',
            'question_text': 'Test',
            'answers': '[{"answer_text": "A", "is_correct": true}]',
            'correct_answer': '1',
            'image_path': './images/no_image.jpg',
            'answer_explanation': 'Exp',
            'question_number_in_ticket': 1,
            'topic_id': 1
        }]

        with patch('requests.question_requests.db', mock_db):
            questions = await question_requests.get_ticket_questions("Билет 1")

            assert len(questions) == 1
            assert questions[0].question_text == "Test"
            mock_db.fetch.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_topic_questions_empty(self):
        """Тест получения вопросов по пустой теме"""
        mock_db = AsyncMock()
        mock_db.fetch.return_value = []

        with patch('requests.question_requests.db', mock_db):
            questions = await question_requests.get_topic_questions(999)

            assert questions == []
            mock_db.fetch.assert_called_once_with(
                "SELECT * FROM questions WHERE topic_id = $1",
                999
            )


# ==================== ТЕСТ 10: Клавиатуры ====================
class TestKeyboards:
    @pytest.mark.asyncio
    async def test_make_question_keyboard(self):
        """Тест создания клавиатуры для вопросов"""
        question = Question(
            id="1", question_text="Test",
            answers=[
                {"answer_text": "A1", "is_correct": True},
                {"answer_text": "A2", "is_correct": False},
                {"answer_text": "A3", "is_correct": False},
            ],
            correct_answer="1", answer_explanation="",
            question_number_in_ticket=1, topic_id=1
        )

        keyboard = await make_question_keyboard(question)

        assert keyboard is not None
        assert hasattr(keyboard, 'keyboard')
        assert len(keyboard.keyboard) == 2

    @pytest.mark.asyncio
    async def test_make_tickets_list(self):
        """Тест создания клавиатуры билетов"""
        keyboard = await make_tickets_list()

        assert keyboard is not None
        assert hasattr(keyboard, 'inline_keyboard')

        buttons_text = []
        for row in keyboard.inline_keyboard:
            for btn in row:
                buttons_text.append(btn.text)
        assert "⬅️Назад" in buttons_text
        assert "?" in buttons_text

    @pytest.mark.asyncio
    async def test_make_topics_list(self):
        """Тест создания клавиатуры тем"""
        keyboard = await make_topics_list()

        assert keyboard is not None
        assert hasattr(keyboard, 'inline_keyboard')

        buttons_text = []
        for row in keyboard.inline_keyboard:
            for btn in row:
                buttons_text.append(btn.text)
        assert "?" in buttons_text
        assert "⬅️Назад" in buttons_text

# Для запуска тестов:
# pytest tests/test_bot_modules.py -v