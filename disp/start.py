from .dispetcher import dp
from aiogram import types

from clas import User
from conf import USER_UNKNOW
from func import delete_message


@dp.message_handler(commands=['start', 'старт'])
async def send_welcome(message: types.Message):
    "Здороваемся и определяем, зарегистрирован ли пользователь"
    await delete_message(message)
    try:
        USER = await User.get(message['from']['id'])
    except ValueError:
        return await message.answer(USER_UNKNOW, parse_mode='html')

    MESS = f"Здравствуйте, {USER.name}"
    return await message.answer(MESS, parse_mode='html')
