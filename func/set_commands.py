from aiogram.types import BotCommand


async def set_commands(dp):
    commands = []
    DICT = {
        'start': 'Приветсвие',
            }
    for key, value in DICT.items():
        commands.append(BotCommand(
            command=key,
            description=value
            ))

    await dp.bot.set_my_commands(commands)
