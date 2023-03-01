from .dispetcher import dp
from aiogram import types

from clas import User
from func import delete_message, write_styling_excel
from conf import USER_UNKNOW


@dp.message_handler(commands=['remd'])
async def event_log_remd(message: types.Message):
    await delete_message(message)
    try:
        USER = await User.get(message['from']['id'])
    except ValueError:
        return await message.answer(USER_UNKNOW, parse_mode='html')




    write_styling_excel_file(file, df, 'svod')
    await message.answer_document(open(file, 'rb'))
    await message.answer(MESS, parse_mode='html')
