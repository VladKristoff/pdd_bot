import asyncpg
import asyncio
from database.models import Question
from repositories.question_repository import QuestionRepository
from typing import List, Dict, Optional


class TestManager:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository
        self.current_question_index: int = 0
        self.questions: List[Question] = []
        self.user_answers: Dict[int, str] = {}

    async def start_ticket(self, ticket_number: str):
        self.questions = await self.question_repository.get_ticket_questions(ticket_number)
        print(self.questions)
        self.user_answers.clear()
        return self.get_current_question()

    def get_current_question(self) -> Optional[Question]:
        if self.questions and 0 <= self.current_question_index < len(self.questions):
            print(self.questions[self.current_question_index])
            return self.questions[self.current_question_index]
        return None

    def next_question(self) -> Optional[Question]:
        if self.current_question_index - len(self.questions) - 1:
            self.current_question_index += 1
            return self.get_current_question()
        return None

    def previous_question(self) -> Optional[Question]:
        if self.current_question_index > 0:
            self.current_question_index -= 1
            return self.get_current_question()
        return None

    def save_answer(self, answer: str):
        self.user_answers[self.current_question_index] = answer

    def get_results(self) -> Dict:
        correct = 0
        total = len(self.questions)

        for i, question in enumerate(self.questions):
            if self.user_answers.get(i) == question.correct_answer:
                correct += 1

        return {
            "correct": correct,
            "total": total,
            "percentage": (correct / total) * 100 if total > 0 else 0
        }

