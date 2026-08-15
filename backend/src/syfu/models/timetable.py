import uuid
from datetime import datetime, time

from sqlalchemy import DateTime, String, Time, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from syfu.models.base import Base


class TimeTable(Base):
    __tablename__ = "time-table"
    __table_args__ = {"extend_existing": True}

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

    def __repr__(self) -> str:
        return f'TimeTable(id={self.id}, dayStartTime={self.dayStartTime}, dayEndTime={self.dayEndTime})'


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
        nullable=True
    )

    def __repr__(self) -> str:
        return f'TimeSlot(id={self.id}, title={self.title}, description={self.description}, timeTo={self.timeTo}, timeFrom={self.timeFrom})'
