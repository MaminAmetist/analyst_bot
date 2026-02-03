from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from db.database import async_engine, Base
from keyboards.lexicon import MAIN_MENU
from keyboards.keyboards import create_keys

from load_json import load_json_from_drive  # твой скрипт, но async
import os

start_router = Router()
keyboard_start = create_keys(1, **MAIN_MENU)

@start_router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Начинаю загрузку данных в базу...")
    await message.answer(f'Приветствую тебя, {message.from_user.full_name}.\n'
                         f'Для начала диалога нажми кнопку {MAIN_MENU["menu_start"]}.\n'
                         f'Если тебе нужна помощь вызови команду /help.\n',
                         reply_markup=keyboard_start)
    try:
        # Создаём таблицы (если ещё не созданы)
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        DATABASE_URL = os.getenv("DATABASE_URL")
        await load_json_from_drive(DATABASE_URL)

        await message.answer("Данные успешно загружены в базу!")
    except Exception as e:
        await message.answer(f"Ошибка при загрузке данных: {e}")
