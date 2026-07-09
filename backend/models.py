from extensions import BaseSQL
from sqlalchemy import String, Uuid, DateTime, Time, Boolean
from datetime import datetime, time
import uuid, enum
from sqlalchemy.orm import mapped_column, Mapped

class User(BaseSQL):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    def __repr__(self) -> str:
        return f'User(id={self.id}, email={self.email}, password={self.password})'

class ApiServices(enum.Enum):
    GEMINI = 'gemini'
    GROQ = 'groq'
    OPENAI = 'openai'


class ApiKey(BaseSQL):
    __tablename__ = "api-key"
    
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    service: Mapped[ApiServices] = mapped_column(
        nullable=False
    )
    key: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )
    def __repr__(self) -> str:
        return f'User(id={self.id}, service={self.service}, key={self.key})'

class TimeTable(BaseSQL):
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

class TimeSlot(BaseSQL):
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

class TaskPriority(enum.Enum):
    IMP = "important"
    DOT = "doit"
    CHL = "chill"

class Task(BaseSQL):
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

class Youtube(BaseSQL):
    __tablename__ = "youtube"
    
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    channelName: Mapped[str] =  mapped_column(
        String(30),
        nullable=False
    )

class Interest(BaseSQL):
    __tablename__ = "youtube"
    
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    interestName: Mapped[str] =  mapped_column(
        String(30),
        nullable=False
    )

class SDLCModel(enum.Enum):
    CWTR = 'classic-waterfall'
    IWTR = 'interative-waterfall'
    SPRL = 'spiral'

class Project(BaseSQL):
    __tablename__ = "youtube"
    
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
    sdlcModel: Mapped[SDLCModel] = mapped_column()
    # TODO: Add ideapoints and techstack for the project
    aiTickets: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )