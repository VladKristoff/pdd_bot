from database.database import db
from database.models import Question
import json
from typing import List


class QuestionRequests:
    async def get_ticket_questions(self, ticket_number: str) -> List[Question]:
        ticket_data = await db.fetch("SELECT * FROM questions WHERE ticket_number = $1", ticket_number)

        questions = []
        for i, question in enumerate(ticket_data, 1):
            question_data = Question(id=question['id'],
                                     question_text=question['question_text'],
                                     answers=json.loads(question['answers']),
                                     correct_answer=question['correct_answer'],
                                     image_path=question['image_path'],
                                     answer_explanation=question['answer_explanation'],
                                     question_number_in_ticket=question['question_number_in_ticket'],
                                     topic_id=question['topic_id'])

            questions.append(question_data)

        return questions

    async def get_topic_questions(self, topic_id: int) -> List[Question]:
        ticket_data = await db.fetch("SELECT * FROM questions WHERE topic_id = $1", topic_id)

        questions = []
        for i, question in enumerate(ticket_data, 1):
            question_data = Question(id=question['id'],
                                     question_text=question['question_text'],
                                     answers=json.loads(question['answers']),
                                     correct_answer=question['correct_answer'],
                                     image_path=question['image_path'],
                                     answer_explanation=question['answer_explanation'],
                                     question_number_in_ticket=question['question_number_in_ticket'],
                                     topic_id=question['topic_id'])

            questions.append(question_data)

        return questions

    async def get_all_questions(self) -> List[Question]:
        ticket_data = await db.fetch("SELECT * FROM questions")

        questions = []
        for i, question in enumerate(ticket_data, 1):
            question_data = Question(id=question['id'],
                                     question_text=question['question_text'],
                                     answers=json.loads(question['answers']),
                                     correct_answer=question['correct_answer'],
                                     image_path=question['image_path'],
                                     answer_explanation=question['answer_explanation'],
                                     question_number_in_ticket=question['question_number_in_ticket'],
                                     topic_id=question['topic_id'])

            questions.append(question_data)

        return questions

question_requests = QuestionRequests()
