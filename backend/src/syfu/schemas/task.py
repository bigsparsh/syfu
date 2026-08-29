import uuid
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class TaskPriority(StrEnum):
    IMP = "important"
    DOT = "do_it"
    CHL = "chill"


class TaskItem(BaseModel):
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
    completed: bool = Field(
        default=False,
        description="Defaults to False and is the indicator of task completion.",
    )


class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tasks: list[TaskItem] = Field(default_factory=list, description="List of tasks.")


class UpdateTaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(default=None, description="Unique identifier for the task.")
    title: str | None = Field(description="Title of the task.")
    description: str | None = Field(
        default=None, description="Detailed description of the task."
    )
    assocDate: datetime | None = Field(
        default=None, description="Associated date with the task."
    )
    deadline: datetime | None = Field(
        default=None, description="Last date and time to finish that task."
    )
    priority: TaskPriority | None = Field(
        default=None,
        description="Priority of the task according to the importance.",
    )
    completed: bool | None = Field(
        default=None,
        description="Defaults to False and is the indicator of task completion.",
    )
