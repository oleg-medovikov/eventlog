from .dispetcher import dp, bot
from aiogram import types
import os
import pandas as pd

from clas import User


from func import delete_message

NAMES = {
    'users.xlsx': [
        'u_id', 'name', 'name_tg', 'admin',
        'org_name', 'org_code', 'date_update'
        ],
    }


@dp.message_handler(content_types='document')
async def update_base(message: types.Message):
    """Работа с файлами которые посылает пользователь"""
    await delete_message(message)

    USER = await User.get(message['from']['id'])
    if USER is None or not USER.admin:
        return await message.answer('Зачем вы шлёте мне файлы?')

    FILE = message['document']

    if not FILE['file_name'] in NAMES.keys():
        return await message.answer('У файла неправильное имя')

    DESTINATION = 'temp/' + FILE.file_unique_id + 'xlsx'

    await bot.download_file_by_id(
        file_id=FILE.file_id,
        destination=DESTINATION
        )

    COLUMNS = NAMES.get(FILE['file_name'])
    try:
        df = pd.read_excel(DESTINATION, usecols=COLUMNS)
    except Exception as e:
        os.remove(DESTINATION)
        return await message.answer(str(e))

    for col in df.columns:
        try:
            df[col] = df[col].str.replace('\u2028', '\n')
            df[col] = df[col].str.replace("'", '"')
        except AttributeError:
            continue

    list_ = df.to_dict('records')

    MESS = {
        'users':    User.update(list_),
        }.get(FILE['file_name'][:-5])

    try:
        MESS = await MESS
    except TypeError as e:
        MESS = 'Пока не могу этот файл обработать\n' + str(e)

    await message.answer(MESS)
    os.remove(DESTINATION)
