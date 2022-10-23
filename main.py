from aiogram.utils import executor
from create_bot import dp, bot
from data_base import sqlite_db


async def start(*args):
    print('DOLJNIK bot start')
    sqlite_db.sql_start()


from handlers import client, admin, other
client.register_handlers_client(dp)
admin.register_handlers_admin(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start)