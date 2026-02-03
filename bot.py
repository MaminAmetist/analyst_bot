import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from db.create_db import get_async_db
from handlers.query_handlers import router
from handlers.start_handlers import start_router

load_dotenv()

logger = logging.getLogger(__name__)


async def main() -> None:
    TOKEN_BOT = os.getenv('TOKEN_BOT')
    bot: Bot = Bot(token=TOKEN_BOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp: Dispatcher = Dispatcher()

    logging.basicConfig(level=logging.INFO)

    get_async_db()

    dp.include_router(router)
    dp.include_router(start_router)

    # Логгирование
    logging.basicConfig(
        level=logging.INFO, filemode='w', filename='runner_tests.log', encoding='UTF-8',
        format='%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
