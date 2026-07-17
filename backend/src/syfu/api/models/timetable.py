import uuid
from datetime import datetime, time

from sqlalchemy import Uuid, DateTime, Time, String
from sqlalchemy.orm import mapped_column, Mapped

from src.syfu.api.models.base import Base


class TimeTable(Base):
    __tablename__ = "time-table"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    dayStartTime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    dayEndTime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )


# TODO: Add the working days in the timetable

class TimeSlot(Base):
    __tablename__ = "time-slot"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    timeFrom: Mapped[time] = mapped_column(
        Time,
        nullable=False
    )
    timeTo: Mapped[time] = mapped_column(
        Time,
        nullable=False
    )
    title: Mapped[str] = mapped_column(
        String(40),
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(250),
    )
