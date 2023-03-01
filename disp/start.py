from .dispetcher import dp
from aiogram import types


@dp.message_handler(commands=['start', 'старт'])
async def send_welcome(message: types.Message):
    USER = await User.get(message['from']['id'])

    write_styling_excel_file(file, df, 'svod')
    await message.answer_document(open(file, 'rb'))
    await message.answer(MESS, parse_mode='html')
