from pydantic import BaseModel
from typing import List, Dict


class Question(BaseModel):
    id: str
    question_text: str = None
    answers: List[Dict] = None
    correct_answer: str
    image_path: str = None
    answer_explanation: str
    question_number_in_ticket: int
