from datetime import datetime
from pgvector.sqlalchemy import Vector

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .paper import Paper

from app.database import Base

class PaperChunk(Base):
    __tablename__ = "paper_chunks"

    __table_args__ = (
        UniqueConstraint(
            "paper_id",
            "chunk_index",
            name="uq_paper_chunk_index",
        ),
    )

    id: Mapped[int] = mapped_column(
            Integer,
            primary_key=True,
            index=True,
    )

    paper_id: Mapped[int] = mapped_column(
            ForeignKey("papers.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
    )

    chunk_index: Mapped[int] = mapped_column(
            Integer,
            nullable=False,
    )

    section_name: Mapped[str | None] = mapped_column(
            String(100),
            nullable=True,
    )

    content: Mapped[str] = mapped_column(
            Text,
            nullable=False,
    )

    token_count: Mapped[int | None] = mapped_column(
            Integer,
            nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
    )

    paper: Mapped["Paper"] = relationship(
        back_populates="chunks",
    )

    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(768),
        nullable=True,
    )