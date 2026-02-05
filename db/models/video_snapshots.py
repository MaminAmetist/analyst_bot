from datetime import datetime

from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base


class VideoSnapshot(Base):
    __tablename__ = "video_snapshots"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    video_id: Mapped[str] = mapped_column(ForeignKey("videos.id"), index=True)

    views_count: Mapped[int] = mapped_column(Integer)
    likes_count: Mapped[int] = mapped_column(Integer)
    comments_count: Mapped[int] = mapped_column(Integer)
    reports_count: Mapped[int] = mapped_column(Integer)

    delta_views_count: Mapped[int] = mapped_column(Integer)
    delta_likes_count: Mapped[int] = mapped_column(Integer)
    delta_comments_count: Mapped[int] = mapped_column(Integer)
    delta_reports_count: Mapped[int] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    video: Mapped["Video"] = relationship(back_populates="snapshots")
