from database.database import db
from typing import List, Dict, Optional


class StatisticsRequests:
    # === Существующие методы (без изменений) ===

    async def update_user_stats(self, results, user):
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

        print("Общая статистика сохранена в БД")

    async def get_user_stats(self, user):
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
        try:
            await db.execute("""
                            UPDATE users 
                            SET total_questions = 0, 
                                correct_answers = 0,
                                username = $1,
                                fullname = $2
                            WHERE id = $3
                            """, user.username, user.full_name, str(user.id))

            # Также сбрасываем статистику по темам
            await self.reset_user_topic_stats(str(user.id))

            return "Статистика успешно сброшена"
        except Exception as e:
            print(f"Ошибка в сбросе статистики: {e}")
            return None

    # === Новые методы для статистики по темам ===

    async def update_topic_stat(self, user_id: str, topic_id: int, is_correct: bool):
        """
        Обновляет статистику по теме после каждого ответа
        Использует INSERT ... ON CONFLICT для атомарности
        """
        try:
            await db.execute("""
                INSERT INTO user_topic_stats (user_id, topic_id, total_answers, correct_answers)
                VALUES ($1, $2, 1, $3)
                ON CONFLICT (user_id, topic_id) 
                DO UPDATE SET 
                    total_answers = user_topic_stats.total_answers + 1,
                    correct_answers = user_topic_stats.correct_answers + $3
            """, user_id, topic_id, 1 if is_correct else 0)

            print(f"Статистика по теме {topic_id} обновлена: {'✅' if is_correct else '❌'}")
        except Exception as e:
            print(f"Ошибка при обновлении статистики по теме {topic_id}: {e}")

    async def get_user_all_topics_stats(self, user_id: str) -> List[Dict]:
        """
        Получает статистику пользователя по всем темам с названиями тем
        """
        records = await db.fetch("""
            SELECT uts.*, t.name as topic_name
            FROM user_topic_stats uts
            JOIN topics t ON uts.topic_id = t.id
            WHERE uts.user_id = $1
            ORDER BY uts.topic_id
        """, user_id)

        return [dict(record) for record in records]

    async def get_user_topic_stat(self, user_id: str, topic_id: int) -> Optional[Dict]:
        """
        Получает статистику пользователя по конкретной теме
        """
        record = await db.fetchrow("""
            SELECT uts.*, t.name as topic_name
            FROM user_topic_stats uts
            JOIN topics t ON uts.topic_id = t.id
            WHERE uts.user_id = $1 AND uts.topic_id = $2
        """, user_id, topic_id)

        return dict(record) if record else None

    async def reset_user_topic_stats(self, user_id: str):
        """
        Сбрасывает всю статистику пользователя по темам
        """
        await db.execute(
            "DELETE FROM user_topic_stats WHERE user_id = $1",
            user_id
        )
        print(f"Статистика по темам для пользователя {user_id} сброшена")

    async def get_topics_summary(self, user_id: str) -> Dict:
        """
        Получает сводку по темам: сколько всего отвечено, сколько правильных
        """
        record = await db.fetchrow("""
            SELECT 
                COUNT(*) as topics_attempted,
                COALESCE(SUM(total_answers), 0) as total_answers,
                COALESCE(SUM(correct_answers), 0) as total_correct
            FROM user_topic_stats
            WHERE user_id = $1
        """, user_id)

        return dict(record) if record else {
            'topics_attempted': 0,
            'total_answers': 0,
            'total_correct': 0
        }

    async def get_topic_stats_dict(self, user_id: str) -> Dict[int, Dict]:
        """
        Получает статистику по темам в виде словаря {topic_id: stats}
        Удобно для быстрого доступа при формировании сообщения
        """
        stats = await self.get_user_all_topics_stats(user_id)
        return {stat['topic_id']: stat for stat in stats}


# Создаем экземпляр класса
statistics_requests = StatisticsRequests()