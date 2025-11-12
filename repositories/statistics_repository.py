from database.database import db
from database.models import Question
import json
from typing import List


class StatisticsRepository:
    async def update_user_stats(self, results, user):
        await db.connect("postgres", "1234", "pdd_database", "localhost", "5432")

        total_from_ticket = results['total']
        correct_from_ticket = results['correct']

        is_user = await db.fetcher("SELECT * FROM users WHERE id = $1", str(user.id))
        if is_user:
            total = total_from_ticket + is_user['total_questions']
            correct = correct_from_ticket + is_user['correct_answers']

            await db.execute("""
                           UPDATE users 
                           SET total_questions = $1, 
                               correct_answers = $2,
                               username = $3,
                               fullname = $4
                           WHERE id = $5
                       """, total, correct, user.username, user.full_name, str(user.id))

        else:
            await db.execute("""
                            INSERT INTO users 
                            (id, username, fullname, total_questions, correct_answers)
                            VALUES ($1, $2, $3, $4, $5)
                        """, str(user.id), user.username, user.full_name, total_from_ticket, correct_from_ticket)

        print("Статистика успешно сохранена в БД")

    async def get_user_stats(self, user):
        await db.connect("postgres", "1234", "pdd_database", "localhost", "5432")

        is_user = await db.fetcher("SELECT * FROM users WHERE id = $1", str(user.id))
        if is_user:
            return is_user
        else:
            total = 0
            correct = 0
            safe_username = user.username or ""
            safe_fullname = user.full_name or ""
            await db.execute("""INSERT INTO users 
                            (id, username, fullname, total_questions, correct_answers)
                            VALUES ($1, $2, $3, $4, $5)
                            """, str(user.id), safe_username, safe_fullname, total,
                             correct)

            return await db.fetcher("SELECT * FROM users WHERE id = $1", str(user.id))

    async def reset_user_stats(self, user):
        await db.connect("postgres", "1234", "pdd_database", "localhost", "5432")

        try:
            await db.execute("""
                            UPDATE users 
                            SET total_questions = 0, 
                                correct_answers = 0,
                                username = $1,
                                fullname = $2
                            WHERE id = $3
                            """,user.username, user.full_name, str(user.id))

            return "Статистика успешно сброшена"
        except Exception as e:
            print(f"Ошибка в сбросе статистики: {e}")
            return None


statistics_repository = StatisticsRepository()
