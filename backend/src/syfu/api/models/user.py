import uuid

from sqlalchemy import Uuid, String
from sqlalchemy.orm import Mapped, mapped_column

from src.syfu.api.models.base import Base


class User(Base):
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

