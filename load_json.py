import requests
import ijson
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dateutil.parser import isoparse

from models.videos import Video
from models.video_snapshots import VideoSnapshot


DRIVE_LINK = os.getenv("DRIVE_LINK")


def load_json_from_drive(db_url: str):
    engine = create_engine(db_url)
    with requests.get(DRIVE_LINK, stream=True) as response:
        response.raise_for_status()

        objects = ijson.items(response.raw, "videos.item")

        with Session(engine) as session:
            count = 0

            for v in objects:
                video = Video(
                    id=v["id"],
                    creator_id=v["creator_id"],
                    video_created_at=isoparse(v["video_created_at"]),
                    views_count=v["views_count"],
                    likes_count=v["likes_count"],
                    comments_count=v["comments_count"],
                    reports_count=v["reports_count"],
                    created_at=isoparse(v["created_at"]),
                    updated_at=isoparse(v["updated_at"]),
                )
                session.add(video)

                for s in v["snapshots"]:
                    snap = VideoSnapshot(
                        id=s["id"],
                        video_id=s["video_id"],
                        views_count=s["views_count"],
                        likes_count=s["likes_count"],
                        comments_count=s["comments_count"],
                        reports_count=s["reports_count"],
                        delta_views_count=s["delta_views_count"],
                        delta_likes_count=s["delta_likes_count"],
                        delta_comments_count=s["delta_comments_count"],
                        delta_reports_count=s["delta_reports_count"],
                        created_at=isoparse(s["created_at"]),
                        updated_at=isoparse(s["updated_at"]),
                    )
                    session.add(snap)

                count += 1

                if count % 500 == 0:
                    session.commit()

            session.commit()
