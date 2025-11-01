import asyncpg
import asyncio
from database.db import connect_db
from database.models import Question
import json


def read_ticket(ticket_data):
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
