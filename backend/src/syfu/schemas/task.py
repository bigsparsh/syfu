import uuid
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class TaskPriority(StrEnum):
    IMP = "important"
    DOT = "do_it"
    CHL = "chill"


class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID | None = Field(
        default=None, description="Unique identifier for the task."
    )
    title: str = Field(description="Title of the task.")
    description: str | None = Field(
        default=None, description="Detailed description of the task."
    )
    assocDate: datetime | None = Field(
        default=None, description="Associated date with the task."
    )
    deadline: datetime | None = Field(
        default=None, description="Last date and time to finish that task."
    )
    priority: TaskPriority = Field(
        default=TaskPriority.CHL,
        description="Priority of the task according to the importance.",
    )
