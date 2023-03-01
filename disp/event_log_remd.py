from .dispetcher import dp
from aiogram import types
import os

from clas import User, Journal
from func import delete_message, write_styling_excel,\
    get_remd
from conf import USER_UNKNOW


@dp.message_handler(commands=['remd'])
async def event_log_remd(message: types.Message):
    await delete_message(message)
    try:
        USER = await User.get(message['from']['id'])
    except ValueError:
        return await message.answer(USER_UNKNOW, parse_mode='html')

    df = get_remd(USER)
    await Journal.add(USER.u_id, 'REMD')
    file = 'temp/filename.xlsx'

    write_styling_excel(file, df, 'svod')
    await message.answer_document(open(file, 'rb'))
    os.remove(file)
