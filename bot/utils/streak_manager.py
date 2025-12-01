from database.database import db
from datetime import date
from datetime import timedelta



class StreakManager:
    # Возвращает стрик
    async def get_streak(self, user):
        try:
            record =  await db.fetcher("SELECT streak FROM users WHERE id = $1", str(user.id))
            return record['streak']
        except Exception as e:
            print(f"Ошибка в получении стрика: {e}")
            return None

    # Обновляет стрик, если пользователь пропустил день (Вызывается при вызове главного меню)
    async def check_streak(self, user):
        today = date.today()
        yesterday = today - timedelta(days=1)

        try:
            record = await db.fetcher("SELECT streak, last_solved_date FROM users WHERE id = $1", str(user.id))
            print(record)
            current_streak = record['streak']
            last_date = record['last_solved_date']
        except Exception as e:
            print(f"Не удалось получить стрик и дату: {e}")
            return

        if current_streak == 0:
            return

        if last_date is not None:
            if last_date != today and last_date != yesterday:
                streak = 0
            else:
                return
        else:
            streak = 0

        try:
            await db.execute("""UPDATE users SET streak = $1 WHERE id = $2""", streak, str(user.id))
        except Exception as e:
            print(f"Не удалось установить streak = 0: {e}")

    # Обновляет стрик и дату последнего решения (Вызывается в конце билета или темы)
    async def update_streak(self, user):
        today = date.today()
        yesterday = today - timedelta(days=1)

        try:
            record = await db.fetcher("SELECT streak, last_solved_date FROM users WHERE id = $1", str(user.id))
        except Exception as e:
            print(f"Не удалось получить стрик и дату: {e}, user_streak_and_date = None")
            return

        if record is not None:
            last_date = record['last_solved_date']
            db_streak = record['streak']

            if last_date == today:
                streak = db_streak
            elif last_date == yesterday:
                streak = db_streak + 1
            else:
                streak = 1
        else:
            streak = 1

        try:
            await db.execute("""UPDATE users 
            SET streak = $1, last_solved_date = $2
            WHERE id = $3
            """, streak, today, str(user.id))

        except Exception as e:
            print(f"Не удалось обновить стрик: {e}")

streak_manager = StreakManager()