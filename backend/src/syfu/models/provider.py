import enum
import uuid

from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from syfu.models.base import Base


class Providers(enum.Enum):
    GEMINI = 'gemini'
    GROQ = 'groq'
    OPENAI = 'openai'


class ProviderApiKey(Base):
    __tablename__ = "provider-api-key"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    service: Mapped[Providers] = mapped_column(
        nullable=False
    )
    key: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )

    def __repr__(self) -> str:
        return f'ProviderApiKey(id={self.id}, service={self.service}, key={self.key})'
