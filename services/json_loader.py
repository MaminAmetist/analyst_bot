from __future__ import annotations

import aiohttp
import ijson
from datetime import datetime
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from models.videos import Video
from models.video_snapshots import VideoSnapshot


class DriveJSONLoader:
    """
    Сервис потоковой загрузки JSON-данных в БД.
    """

    def __init__(self, drive_url: str, batch_size: int = 500) -> None:
        self._drive_url = drive_url
        self._batch_size = batch_size

    async def load(self, session: AsyncSession) -> int:
        """
        Загружает данные в БД.

        :param session: AsyncSession
        :return: количество загруженных видео
        """
        count = 0

        async with aiohttp.ClientSession() as http:
            async with http.get(self._drive_url) as response:
                response.raise_for_status()

                async for video_data in self._iter_videos(response):
                    session.add(self._build_video(video_data))

                    for snap in video_data["snapshots"]:
                        session.add(self._build_snapshot(snap))

                    count += 1

                    if count % self._batch_size == 0:
                        await session.flush()

                await session.commit()

        return count

    async def _iter_videos(self, response) -> AsyncIterator[dict]:
        """
        Потоковое чтение videos.item из JSON.
        """
        async for item in ijson.items_async(response.content, "videos.item"):
            yield item

    @staticmethod
    def _build_video(data: dict) -> Video:
        return Video(
            id=data["id"],
            creator_id=data["creator_id"],
            video_created_at=datetime.fromisoformat(data["video_created_at"]),
            views_count=data["views_count"],
            likes_count=data["likes_count"],
            comments_count=data["comments_count"],
            reports_count=data["reports_count"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )

    @staticmethod
    def _build_snapshot(data: dict) -> VideoSnapshot:
        return VideoSnapshot(
            id=data["id"],
            video_id=data["video_id"],
            views_count=data["views_count"],
            likes_count=data["likes_count"],
            comments_count=data["comments_count"],
            reports_count=data["reports_count"],
            delta_views_count=data["delta_views_count"],
            delta_likes_count=data["delta_likes_count"],
            delta_comments_count=data["delta_comments_count"],
            delta_reports_count=data["delta_reports_count"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )
