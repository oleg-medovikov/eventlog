from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from base import database, t_users


class User(BaseModel):
    u_id:        int
    name:        str
    name_tg:     str
    admin:       bool
    org_name:    str
    org_code:    str
    date_update: Optional[datetime]

    @staticmethod
    async def get(TG_ID: int) -> 'User':
        "Берем пользователя по телеграм id"
        query = t_users.select(t_users.c.u_id == int(TG_ID))
        res = await database.fetch_one(query)
        if res is not None:
            return User(**res)
        else:
            raise ValueError('неизвестный пользователь')

    @staticmethod
    async def get_all() -> list:
        "Получение списка пользователей"
        query = t_users.select()
        list_ = []
        for row in await database.fetch_all(query):
            list_.append(User(**row).dict())
        return list_

    @staticmethod
    async def update(list_: list) -> str:
        "Обновление данных о пользователе"
        if len(list_) == 0:
            return 'Нечего обновлять'

        string = ''
        for user in list_:
            try:
                query = t_users.select(t_users.c.u_id == int(user['u_id']))
            except ValueError:
                continue
            res = await database.fetch_one(query)

            # если строки нет, то добавляем
            if res is None:
                string += f"добавил пользователя {user['name']}"
                user['date_update'] = datetime.now()
                query = t_users.insert().values(**user)
                await database.execute(query)
                continue

            # если строчка есть ищем несовпадение значений, чтобы заменить
            for key, value in dict(res).items():
                if user[key] != value and key != 'date_update':
                    string += f"обновил пользователя {user['name']}"
                    user['date_update'] = datetime.now()
                    query = t_users.update()\
                        .where(t_users.c.u_id == user['u_id'])\
                        .values(**user)
                    await database.execute(query)
                    break
        if string == '':
            string = 'Нечего обновлять'
        return string
