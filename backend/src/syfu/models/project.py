import enum
import uuid

from sqlalchemy import Boolean, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from syfu.models.base import Base


class SDLCModel(enum.Enum):
    CWTR = 'classic-waterfall'
    IWTR = 'interactive-waterfall'
    SPRL = 'spiral'


class Project(Base):
    __tablename__ = "project"

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
    sdlcModel: Mapped[SDLCModel] = mapped_column()
    # TODO: Add ideapoints and techstack for the project
    aiTickets: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    def __repr__(self) -> str:
        return f'Project(id={self.id}, title={self.title}, description={self.description}, sdlcModel={self.sdlcModel}, aiTickets={self.aiTickets})'
