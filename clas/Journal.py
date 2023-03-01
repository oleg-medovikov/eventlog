from datetime import datetime
from pydantic import BaseModel

from base import database, t_users, t_journal


class Journal(BaseModel):
    j_id:   int
    u_id:   int
    date:   datetime
    task:   str

    @staticmethod
    async def add(U_ID: int, TASK: str):
        "добавлям строчку в журнал"
        query = t_journal.insert().values(
            u_id=U_ID,
            date=datetime.now(),
            task=TASK
                )
        await database.execute(query)
