import enum
import uuid
from datetime import datetime

from sqlalchemy import Uuid, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.syfu.api.models.base import Base


class TaskPriority(enum.Enum):
    IMP = "important"
    DOT = "doit"
    CHL = "chill"


class Task(Base):
    __tablename__ = "time-slot"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(
        String(40),
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(250),
    )
    assocDate: Mapped[datetime] = mapped_column(
        DateTime,
    )
    deadline: Mapped[datetime] = mapped_column(
        DateTime
    )
    priority: Mapped[TaskPriority] = mapped_column(
        nullable=False
    )


class Youtube(Base):
    __tablename__ = "youtube"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    channelName: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )


class Interest(Base):
    __tablename__ = "youtube"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    interestName: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )
