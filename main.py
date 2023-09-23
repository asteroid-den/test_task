import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import handlers
from config import Config
from middlewares import DAOMiddleware
from services.database import DatabaseManager


async def main():
    config = Config()
    database_manager = DatabaseManager(
        user=config.db_user,
        password=config.db_password,
        db_name=config.db_name,
        host=config.db_host,
    )

    database_manager.create_database()
    await database_manager.create_tables()

    storage = MemoryStorage()
    bot = Bot(token=config.bot_token, parse_mode="HTML")

    dispatcher = Dispatcher(storage=storage)
    dispatcher.message.middleware(DAOMiddleware(database_manager=database_manager))

    dispatcher.include_router(handlers.menu.router)
    dispatcher.include_router(handlers.add_address.router)
    dispatcher.include_router(handlers.extra.router)

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    await dispatcher.start_polling(bot)


asyncio.run(main())
