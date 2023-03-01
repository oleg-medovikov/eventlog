from aiogram.types import BotCommand


async def set_commands(dp):
    commands = []
    DICT = {
        'start': 'Приветсвие',
        'remd':  'Получить лог отправки в РЭМД'
            }
    for key, value in DICT.items():
        commands.append(BotCommand(
            command=key,
            description=value
            ))

    await dp.bot.set_my_commands(commands)
