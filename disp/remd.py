from .dispetcher import dp
from aiogram import types

from clas import User
from func import write_styling_excel_file


@dp.message_handler(commands=['remd'])
async def event_log_remd(message: types.Message):
    USER = await User.get(message['from']['id'])

    write_styling_excel_file(file, df, 'svod')
    await message.answer_document(open(file, 'rb'))
    await message.answer(MESS, parse_mode='html')
