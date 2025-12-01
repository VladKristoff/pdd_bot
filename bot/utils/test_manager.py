from database.models import Question
from requests.question_requests import QuestionRequests
from typing import List, Dict, Optional


class TestManager:
    def __init__(self, question_repository: QuestionRequests):
        self.question_repository = question_repository
        self.current_question_index: int = 0
        self.questions: List[Question] = []
        self.user_answers: Dict[int, int] = {}

    async def start_ticket(self, ticket_number: str):
        self.current_question_index = 0
        self.questions = await self.question_repository.get_ticket_questions(ticket_number)
        self.user_answers.clear()
        return self.get_current_question()

    async def start_topic(self, topic_number: int):
        self.current_question_index = 0
        self.questions = await self.question_repository.get_topic_questions(topic_number)
        if not self.questions:
            raise ValueError(f"Тема {topic_number} не содержит вопросов или не существует")
        self.user_answers.clear()
        return self.get_current_question()

    async def start_marathon(self):
        self.current_question_index = 0
        self.questions = await self.question_repository.get_all_questions()
        self.user_answers.clear()
        return self.get_current_question()

    def get_current_question(self) -> Optional[Question]:
        if self.questions and 0 <= self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None

    def next_question(self):
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            return self.get_current_question()
        return None

    def previous_question(self) -> Optional[Question]:
        if self.current_question_index > 0:
            self.current_question_index -= 1
            return self.get_current_question()
        return None

    def save_answer(self, answer_id: int):
        self.user_answers[self.current_question_index] = answer_id

    def get_results(self) -> Dict:
        correct = 0
        total = len(self.questions)
        for i, question in enumerate(self.questions):
            user_answer = self.user_answers.get(i)
            if f"Правильный ответ: {user_answer}" == question.correct_answer:
                correct += 1

        return {
            "correct": correct,
            "total": total,
            "percentage": (correct / total) * 100 if total > 0 else 0
        }
