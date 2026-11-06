
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Paper(Base):
    __tablename__ = "papers"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    title: Mapped[str] = mapped_column(Text, nullable=False)
    abstract: Mapped[str | None] = mapped_column(Text, nullable=True)

    doi: Mapped[str | None] = mapped_column(
        String(255), unique=True, nullable=True
    )
    pmid: Mapped[str | None] = mapped_column(
        String(20), unique=True, nullable=True
    )

    journal: Mapped[str | None] = mapped_column(
        String(500), nullable=True
    )
    publication_date: Mapped[date | None] = mapped_column(
        Date, nullable=True
    )
    source_url: Mapped[str | None] = mapped_column(
        String(2048), nullable=True
    )

    source_type: Mapped[str] = mapped_column(
        String(30), nullable=False, default="manual"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
