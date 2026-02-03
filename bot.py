import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from create_db import get_db
from handlers.query_handler import router

load_dotenv()

logger = logging.getLogger(__name__)


async def main() -> None:
    TOKEN_BOT = os.getenv('TOKEN_BOT')
    bot: Bot = Bot(token=TOKEN_BOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp: Dispatcher = Dispatcher()

    logging.basicConfig(level=logging.INFO)

    get_db()

    dp.include_router(router)

    # Логгирование
    logging.basicConfig(
        level=logging.INFO, filemode='w', filename='runner_tests.log', encoding='UTF-8',
        format='%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )


if __name__ == '__main__':
    asyncio.run(main())
