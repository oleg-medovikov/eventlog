from starlette.config import Config

config = Config('../.config/bot/.conf')

DATABASE_POSTGRESS = config('DB_PSS_EVENTLOG', cast=str)
TELEGRAM_API = config('TELEGRAM_API_EVENTLOG', cast=str)
