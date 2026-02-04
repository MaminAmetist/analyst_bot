import os

from aiogram import Router, F
from aiogram.types import Message
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import async_engine, Base
from keyboards.keyboards import create_keys
from keyboards.lexicon import MAIN_MENU
from services.json_loader import DriveJSONLoader

load_dotenv()

load_router = Router()
keyboard_start = create_keys(1, **MAIN_MENU)


@load_router.message(F.text == MAIN_MENU['menu_start'])
async def load_handler(message: Message, session: AsyncSession):
    try:
        await message.answer("Загрузка началась, это займёт несколько минут.")
        # Создаём таблицы (если ещё не созданы)
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        DATABASE_URL = os.getenv("DATABASE_URL")
        loader = DriveJSONLoader(os.getenv("DRIVE_LINK"))
        count = await loader.load(session)

        await message.answer(f"Загружено видео: {count}")

    except Exception as e:
        await message.answer(f"Ошибка при загрузке данных: {str(e)[:40] + '...'}", parse_mode=None)
