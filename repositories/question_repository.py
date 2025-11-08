from database.database import db
from database.models import Question
import json
from typing import List


class QuestionRepository:

    async def get_ticket_questions(self, ticket_number: str) -> List[Question]:
        await db.connect("postgres", "1234", "pdd_database", "localhost", "5432")
        ticket_data = await db.fetch("SELECT * FROM questions WHERE ticket_number = $1", ticket_number)

        questions = []
        for i, question in enumerate(ticket_data, 1):
            question_data = Question(id=question['id'],
                                     question_text=question['question_text'],
                                     answers=json.loads(question['answers']),
                                     correct_answer=question['correct_answer'],
                                     image_path=question['image_path'],
                                     answer_explanation=question['answer_explanation'],
                                     question_number_in_ticket=question['question_number_in_ticket'])

            questions.append(question_data)

        return questions

    async def get_question_by_id(self, question_id: str) -> Question:
        await db.connect("postgres", "1234", "pdd_database", "localhost", "5432")
        record = await db.fetchrow("SELECT * FROM questions WHERE id = $1", question_id)
        if record:
            return Question(
                id=record['id'],
                question_text=record['question_text'],
                answers=json.loads(record['answers']),
                correct_answer=record['correct_answer'],
                image_path=record['image_path'],
                answer_explanation=record['answer_explanation'],
                question_number_in_ticket=record['question_number_in_ticket']
            )


question_repository = QuestionRepository()
