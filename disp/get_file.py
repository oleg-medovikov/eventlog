from .dispetcher import dp
from aiogram import types
import pandas as pd
import os

from func import delete_message, write_styling_excel
from clas import User

DICT_XLSX = [
    'get_users',
    ]


@dp.message_handler(commands='files')
async def get_files_help(message: types.Message):
    await delete_message(message)

    try:
        USER = await User.get(message['from']['id'])
    except ValueError:
        return None
    if not USER.admin:
        return None

    MESS = """*Доступные команды для редактирования базы*
    /get_users
    """.replace('_', '\\_')

    return await message.answer(MESS, parse_mode='Markdown')


@dp.message_handler(commands=DICT_XLSX)
async def send_objects_file(message: types.Message):
    # удалим команду для чистоты
    await delete_message(message)
    try:
        USER = await User.get(message['from']['id'])
    except ValueError:
        return None
    if not USER.admin:
        return None

    COMMAND = message.text.replace('/', '')

    JSON = {
        'get_users':    User.get_all(),
        }.get(COMMAND)

    try:
        JSON = await JSON
    except TypeError:
        return await message.answer('Пока проблемы с этой командой')

    df = pd.DataFrame(data=JSON)
    try:
        df['date_update'] = df['date_update'].dt.strftime('%H:%M  %d.%m.%Y')
    except:
        pass
    FILENAME = f'temp/{COMMAND[4:]}.xlsx'
    SHETNAME = 'def'

    write_styling_excel(FILENAME, df, SHETNAME)

    await message.answer_document(open(FILENAME, 'rb'))
    os.remove(FILENAME)
