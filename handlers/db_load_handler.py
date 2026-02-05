import asyncio
import os

from aiogram import Router, F
from aiogram.types import Message
from dotenv import load_dotenv

from db.database import async_session_maker
from keyboards.keyboards import create_keys
from keyboards.lexicon import MAIN_MENU
from services.json_loader import DriveJSONLoader

load_dotenv()

load_router = Router()
keyboard_start = create_keys(1, **MAIN_MENU)


@load_router.message(F.text == MAIN_MENU["menu_start"])
async def load_handler(message: Message) -> None:
    await message.answer("Загрузка началась, это займёт несколько минут.")
    asyncio.create_task(_background_load(message))


async def _background_load(message: Message) -> None:
    try:
        async with async_session_maker() as session:
            loader = DriveJSONLoader(os.getenv("DRIVE_LINK"))
            count = await loader.load(session)

        await message.answer(f"Загружено видео: {count}")

    except Exception as e:
        await message.answer(f"Ошибка загрузки: {type(e).__name__}")
