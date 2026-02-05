from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    creator_id: Mapped[str] = mapped_column(String, index=True)

    video_created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    views_count: Mapped[int] = mapped_column(Integer)
    likes_count: Mapped[int] = mapped_column(Integer)
    comments_count: Mapped[int] = mapped_column(Integer)
    reports_count: Mapped[int] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    snapshots: Mapped[List["VideoSnapshot"]] = relationship(
        back_populates="video",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
