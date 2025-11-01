import asyncpg
import asyncio
from database.db import connect_db


async def start_ticket(ticket_number: str):
    conn = await connect_db()

    ticket_data = await conn.fetch("SELECT * FROM questions WHERE ticket_number = $1", ticket_number)
    await conn.close()

    return ticket_data
