import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from handlers.query_handlers import router
from handlers.start_handlers import start_router

load_dotenv()

logger = logging.getLogger(__name__)


async def main() -> None:
    TOKEN_BOT = os.getenv("TOKEN_BOT")
    if not TOKEN_BOT:
        raise RuntimeError("TOKEN_BOT is not set")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    bot = Bot(
        token=TOKEN_BOT,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
