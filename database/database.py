import asyncpg
from typing import Optional


class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self, user, password, database, host, port):
        self.pool = await asyncpg.create_pool(
            user=user,
            password=password,
            database=database,
            host=host,
            port=port,
            min_size=5,
            max_size=10
        )

    async def close(self):
        await self.pool.close()

    async def fetch(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetcher(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)


db = Database()
