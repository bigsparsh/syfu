import uuid
from datetime import datetime, time

from pydantic import BaseModel, ConfigDict, Field


class TimeTableItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID | None = Field(
        default=None, description="Unique identifier for the timetable entry."
    )
    dayStartTime: datetime = Field(
        description="Start datetime (ISO 8601) of the working day."
    )
    dayEndTime: datetime = Field(
        description="End datetime (ISO 8601) of the working day."
    )


class TimeTableSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    timetables: list[TimeTableItem] = Field(
        default_factory=list, description="List of timetable entries."
    )


class UpdateTimeTableSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(
        description="Unique identifier for the timetable entry."
    )
    dayStartTime: datetime | None = Field(
        default=None, description="Start datetime (ISO 8601) of the working day."
    )
    dayEndTime: datetime | None = Field(
        default=None, description="End datetime (ISO 8601) of the working day."
    )


class TimeSlotItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID | None = Field(
        default=None, description="Unique identifier for the time slot."
    )
    timeFrom: time = Field(
        description="Start time (HH:MM:SS) of the time slot."
    )
    timeTo: time = Field(
        description="End time (HH:MM:SS) of the time slot."
    )
    title: str = Field(
        description="Title of the time slot."
    )
    description: str | None = Field(
        default=None, description="Detailed description of the time slot."
    )


class TimeSlotSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    timeSlots: list[TimeSlotItem] = Field(
        default_factory=list, description="List of time slots."
    )


class UpdateTimeSlotSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(
        description="Unique identifier for the time slot."
    )
    timeFrom: time | None = Field(
        default=None, description="Start time (HH:MM:SS) of the time slot."
    )
    timeTo: time | None = Field(
        default=None, description="End time (HH:MM:SS) of the time slot."
    )
    title: str | None = Field(
        default=None, description="Title of the time slot."
    )
    description: str | None = Field(
        default=None, description="Detailed description of the time slot."
    )