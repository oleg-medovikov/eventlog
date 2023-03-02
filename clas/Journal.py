from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import select, and_, desc

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

    @staticmethod
    async def get_all() -> list:
        "Получение списка пользователей"
        join = t_journal.join(
                t_users,
                t_journal.c.u_id == t_journal.c.u_id
                )
        query = select([
            t_journal.c.j_id,
            t_users.c.name,
            t_users.c.org_name,
            t_journal.c.date,
            t_journal.c.task
            ]).order_by(t_journal.c.j_id).select_from(join)

        list_ = []
        for row in await database.fetch_all(query):
            list_.append({**row})
        return list_

    @staticmethod
    async def get_last_time(U_ID: int, TASK: str) -> int:
        "сколько осталось времени по таймауту"
        query = t_journal.select().where(and_(
            t_journal.c.u_id == U_ID,
            t_journal.c.task == TASK
            )).order_by(desc('date'))

        res = await database.fetch_one(query)
        if res is None:
            return 0
        else:
            return 300 - (datetime.now() - res['date']).seconds
