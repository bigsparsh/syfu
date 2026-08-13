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
    __tablename__ = "task"

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
        nullable=True
    )
    assocDate: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )
    deadline: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )
    priority: Mapped[TaskPriority] = mapped_column(
        nullable=False
    )

    def __repr__(self) -> str:
        return f'Task(id={self.id}, title={self.title}, description={self.description}, assocDate: {self.assocDate}, deadline: {self.deadline}, priority: {self.priority})'
    


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
    __tablename__ = "interest"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    interestName: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )
