from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dotenv import load_dotenv

from keyboards.keyboards import create_keys
from keyboards.lexicon import MAIN_MENU

load_dotenv()

start_router = Router()
keyboard_start = create_keys(1, **MAIN_MENU)


@start_router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(f'Приветствую тебя, {message.from_user.full_name}.\n'
                         f'Для начала работы нажми кнопку {MAIN_MENU["menu_start"]}.\n'
                         f'Если тебе нужна помощь вызови команду /help.\n',
                         reply_markup=keyboard_start)


@start_router.message(Command("help"))
async def help_bot(message: Message):
    await message.answer(f'Не паникуй, {message.from_user.full_name}, помощь уже в пути.')
