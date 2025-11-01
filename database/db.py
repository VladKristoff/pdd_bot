import asyncpg


async def connect_db():
    try:
        conn = await asyncpg.connect(user="postgres",
                                     password="1234",
                                     database="pdd_database",
                                     host="localhost",
                                     port=5432)
        return conn
    except Exception as e:
        print(f"Ошибка подключения к базы данных: {e}")
