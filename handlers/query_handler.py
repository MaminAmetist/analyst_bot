from aiogram import Router
from aiogram.types import Message
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session

from db.create_db import DATABASE_URL
from models.videos import Video
from models.video_snapshots import VideoSnapshot
from scripts.nl_parser import parse_nl
from scripts.nl_connect import get_ai_response

router = Router()

engine = create_engine(DATABASE_URL, echo=False)


@router.message()
async def handle_query(message: Message):
    text = message.text.strip()

    # 1. Сначала пробуем наш чёткий парсер
    parsed = parse_nl(text)

    if parsed["intent"] == "unknown":
        # 2. Если не получилось — спрашиваем LLM
        try:
            llm_answer = get_ai_response(text)
        except Exception as e:
            await message.answer(f"Ошибка внешнего AI: {e}")
            return

        # 3. Парсим то, что вернул LLM
        parsed = parse_nl(llm_answer)

        if parsed["intent"] == "unknown":
            await message.answer("Не смогла понять запрос, даже с помощью модели.")
            return

    # 4. Теперь у нас есть корректный intent
    try:
        result = run_query(parsed["intent"], parsed["params"])
        await message.answer(str(result))
    except Exception as e:
        await message.answer(f"Ошибка при выполнении запроса: {e}")


def run_query(intent: str, params: dict):
    with Session(engine) as session:

        # 1. Сколько всего видео?
        if intent == "count_all_videos":
            return session.scalar(select(func.count()).select_from(Video))

        # 2. Видео конкретного креатора за период
        if intent == "count_videos_by_creator_period":
            creator = params["creator_id"]
            d1 = params["date_from"]
            d2 = params["date_to"]

            stmt = (
                select(func.count())
                .select_from(Video)
                .where(Video.creator_id == creator)
                .where(Video.video_created_at.between(d1, d2))
            )
            return session.scalar(stmt)

        # 3. Видео с количеством просмотров > N
        if intent == "count_videos_over_views":
            n = params["views_threshold"]
            stmt = (
                select(func.count())
                .select_from(Video)
                .where(Video.views_count > n)
            )
            return session.scalar(stmt)

        # 4. Сумма прироста просмотров (delta) за дату
        if intent == "sum_delta_views_by_date":
            d = params["date"]

            stmt = (
                select(func.sum(VideoSnapshot.delta_views_count))
                .where(VideoSnapshot.created_at.like(f"{d}%"))
            )
            return session.scalar(stmt) or 0

        # 5. Сколько видео получили новые просмотры в эту дату
        if intent == "count_videos_with_new_views_on_date":
            d = params["date"]

            stmt = (
                select(func.count())
                .select_from(VideoSnapshot)
                .where(VideoSnapshot.delta_views_count > 0)
                .where(VideoSnapshot.created_at.like(f"{d}%"))
            )
            return session.scalar(stmt)

        raise ValueError("Неизвестный intent")
