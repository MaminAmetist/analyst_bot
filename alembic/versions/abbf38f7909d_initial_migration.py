"""Initial migration

Revision ID: abbf38f7909d
Revises:
Create Date: 2026-02-04 20:44:29.711926
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "abbf38f7909d"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "videos",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("creator_id", sa.String(), nullable=False),
        sa.Column("video_created_at", sa.DateTime(timezone=True), nullable=False),

        sa.Column("views_count", sa.Integer(), nullable=False),
        sa.Column("likes_count", sa.Integer(), nullable=False),
        sa.Column("comments_count", sa.Integer(), nullable=False),
        sa.Column("reports_count", sa.Integer(), nullable=False),

        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_index(
        "ix_videos_creator_id",
        "videos",
        ["creator_id"],
    )

    op.create_table(
        "video_snapshots",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column(
            "video_id",
            sa.String(),
            sa.ForeignKey("videos.id", ondelete="CASCADE"),
            nullable=False,
        ),

        sa.Column("views_count", sa.Integer(), nullable=False),
        sa.Column("likes_count", sa.Integer(), nullable=False),
        sa.Column("comments_count", sa.Integer(), nullable=False),
        sa.Column("reports_count", sa.Integer(), nullable=False),

        sa.Column("delta_views_count", sa.Integer(), nullable=False),
        sa.Column("delta_likes_count", sa.Integer(), nullable=False),
        sa.Column("delta_comments_count", sa.Integer(), nullable=False),
        sa.Column("delta_reports_count", sa.Integer(), nullable=False),

        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_index(
        "ix_video_snapshots_video_id",
        "video_snapshots",
        ["video_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_video_snapshots_video_id", table_name="video_snapshots")
    op.drop_table("video_snapshots")

    op.drop_index("ix_videos_creator_id", table_name="videos")
    op.drop_table("videos")
