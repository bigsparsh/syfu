import uuid

from pydantic import BaseModel, ConfigDict, Field

from syfu.models.project import SDLCModel


class ProjectItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID | None = Field(
        default=None, description="Unique identifier for the project."
    )
    title: str = Field(
        description="Title of the project."
    )
    description: str | None = Field(
        default=None, description="Detailed description of the project."
    )
    sdlcModel: SDLCModel = Field(
        description=(
            "SDLC model followed by the project "
            "(one of: classic-waterfall, interactive-waterfall, spiral)."
        )
    )
    aiTickets: bool = Field(
        default=True,
        description="Whether the project should automatically generate AI tickets.",
    )


class ProjectSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    projects: list[ProjectItem] = Field(
        default_factory=list, description="List of projects."
    )


class UpdateProjectSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(
        description="Unique identifier for the project."
    )
    title: str | None = Field(
        default=None, description="Title of the project."
    )
    description: str | None = Field(
        default=None, description="Detailed description of the project."
    )
    sdlcModel: SDLCModel | None = Field(
        default=None,
        description=(
            "SDLC model followed by the project "
            "(one of: classic-waterfall, interactive-waterfall, spiral)."
        ),
    )
    aiTickets: bool | None = Field(
        default=None,
        description="Whether the project should automatically generate AI tickets.",
    )