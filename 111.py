from aiogram import Bot
import asyncio
import os
from dotenv import load_dotenv

from db.create_db import get_async_db
from handlers.query_handlers import router

load_dotenv()
async def drop_webhook():
    bot = Bot(token=os.getenv("TOKEN_BOT"))
    await bot.delete_webhook(drop_pending_updates=True)

asyncio.run(drop_webhook())
