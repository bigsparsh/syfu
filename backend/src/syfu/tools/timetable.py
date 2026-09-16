import json
import uuid

from langchain_core.tools import tool
from sqlalchemy import delete, or_, select, update
from sqlalchemy.orm import Session

from syfu.core.db import db
from syfu.models.timetable import TimeSlot, TimeTable
from syfu.schemas.timetable import (
    TimeSlotItem,
    TimeTableItem,
    UpdateTimeSlotSchema,
    UpdateTimeTableSchema,
)

from syfu.utils.file_handling import create_tool_log


# ---------------------------------------------------------------------------
# TimeTable CRUD
# ---------------------------------------------------------------------------


@tool()
def get_timetables(prompt_id: str) -> str:
    """This function is used to get all the timetable entries.

    Returns:
        List[dict]: A list of all the timetable entries.
    """
    print("[tool-invoke][get_timetables]")

    with Session(db) as session:
        timetables = session.scalars(select(TimeTable)).all()
        res = (
            json.dumps(
                [
                    TimeTableItem.model_validate(x).model_dump(mode="json")
                    for x in timetables
                ]
            )
            if timetables
            else json.dumps([])
        )
        create_tool_log("get_timetables", "None", res, prompt_id)
        return res


@tool()
def get_timetable_by_id(id: str, prompt_id: str) -> str:
    """This function is used to get a single timetable entry with the matching id.

    Agrs:
        id (str): UUID as string of the timetable entry that you want to search.

    Returns:
        dict: The timetable entry that matches the given id.
    """
    print("[tool-invoke][get_timetable_by_id]")
    try:
        uid = uuid.UUID(id.strip())
    except Exception as err:
        return f"Error parsing timetable ID: {err}"
    with Session(db) as session:
        timetable = session.scalar(select(TimeTable).where(TimeTable.id == uid))

        res = (
            json.dumps(
                TimeTableItem.model_validate(timetable).model_dump(mode="json")
                if timetable
                else None
            )
            if timetable
            else json.dumps([])
        )
        create_tool_log("get_timetable_by_id", id, res, prompt_id)
        return res


@tool("create_timetables")
def create_timetables(timetables: list[TimeTableItem], prompt_id: str) -> str:
    """this is the function which is used to create new timetable entries.

    args:
        timetables: [
            {
                id (optional[uuid.UUID], optional): unique identifier for the timetable entry. defaults to none.
                dayStartTime (datetime): start datetime (ISO 8601) of the working day.
                dayEndTime (datetime): end datetime (ISO 8601) of the working day.
            },
            ...
        ]

    returns:
        dict: the timetable entries that were just now created are returned
    """

    print("[tool-invoke][create_timetables]")
    input_log = json.dumps([t.model_dump(mode="json") for t in timetables])
    with Session(db) as session:
        timetables = [TimeTable(**d.model_dump()) for d in timetables]
        session.add_all(timetables)
        session.commit()
        for timetable in timetables:
            session.refresh(timetable)
        res = json.dumps(
            [
                TimeTableItem.model_validate(t).model_dump(mode="json")
                for t in timetables
            ]
        )
        create_tool_log("create_timetables", input_log, res, prompt_id)
        return res


@tool("delete_timetables")
def delete_timetables(ids: list[str], prompt_id: str) -> str:
    """
    this function is used to delete all the timetable entries with the given ids.
    args:
        ids (list[str]): uuids of all the entries to be deleted

    returns: str
    """

    print("[tool-invoke][delete_timetables]")

    try:
        uuids = [uuid.UUID(i.strip()) for i in ids]
    except Exception as err:
        return f"Error occured: {err}"

    with Session(db) as session:
        session.execute(delete(TimeTable).where(TimeTable.id.in_(uuids)))
        session.commit()
        res = f"Successfully deleted timetable entries with IDs {ids}"
        create_tool_log("delete_timetables", json.dumps(ids), res, prompt_id)
        return res


@tool("update_timetables")
def update_timetables(timetables: list[UpdateTimeTableSchema], prompt_id: str) -> str:
    """this is the function which is used to update timetable entries.

    args:
        timetables: [
            {
                id (uuid.UUID): unique identifier for the timetable entry.
                dayStartTime (datetime | None): start datetime (ISO 8601) of the working day. defaults to none.
                dayEndTime (datetime | None): end datetime (ISO 8601) of the working day. defaults to none.
            },
            ...
        ]

    returns: str
    """

    print("[tool-invoke][update_timetables]")
    print(timetables)
    try:
        timetables = [t.model_dump(exclude_unset=True) for t in timetables]
        timetables = [
            {k: v for k, v in t.items() if v is not None} for t in timetables
        ]
    except Exception as err:
        print(f"Error occured while updating timetable entries: {err}")

    with Session(db) as session:
        session.bulk_update_mappings(TimeTable, timetables)
        session.commit()

    res = f"Successfully updated all the entries of the IDs {[x['id'] for x in timetables]}"
    create_tool_log("update_timetables", json.dumps(timetables, default=str), res, prompt_id)
    return res


# ---------------------------------------------------------------------------
# TimeSlot CRUD
# ---------------------------------------------------------------------------


@tool()
def get_time_slots(prompt_id: str) -> str:
    """This function is used to get all the time slots.

    Returns:
        List[dict]: A list of all the time slots.
    """
    print("[tool-invoke][get_time_slots]")

    with Session(db) as session:
        slots = session.scalars(select(TimeSlot)).all()
        res = (
            json.dumps(
                [TimeSlotItem.model_validate(x).model_dump(mode="json") for x in slots]
            )
            if slots
            else json.dumps([])
        )
        create_tool_log("get_time_slots", "None", res, prompt_id)
        return res


@tool()
def get_time_slots_by_title(title: list[str], prompt_id: str) -> str:
    """This function is used to get all the time slots matching a certain title.
    Agrs:
        title (list[str]): Titles related to the time slots that you want to search.

    Returns:
        list[dict]: A list of all the time slots that match the title.
    """

    print("[tool-invoke][get_time_slots_by_title]")
    if not title:
        return json.dumps([])
    with Session(db) as session:
        slots = session.scalars(
            select(TimeSlot).where(or_(*[TimeSlot.title.ilike(f"%{t}%") for t in title]))
        ).all()
        res = (
            json.dumps(
                [TimeSlotItem.model_validate(x).model_dump(mode="json") for x in slots]
            )
            if slots
            else json.dumps([])
        )
        create_tool_log("get_time_slots_by_title", json.dumps(title), res, prompt_id)
        return res


@tool()
def get_time_slot_by_id(id: str, prompt_id: str) -> str:
    """This function is used to get a single time slot with the matching id.
    Agrs:
        id (str): UUID as string of the time slot that you want to search.

    Returns:
        dict: The time slot that matches the given id.
    """
    print("[tool-invoke][get_time_slot_by_id]")
    try:
        uid = uuid.UUID(id.strip())
    except Exception as err:
        return f"Error parsing time slot ID: {err}"
    with Session(db) as session:
        slot = session.scalar(select(TimeSlot).where(TimeSlot.id == uid))

        res = (
            json.dumps(
                TimeSlotItem.model_validate(slot).model_dump(mode="json")
                if slot
                else None
            )
            if slot
            else json.dumps([])
        )
        create_tool_log("get_time_slot_by_id", id, res, prompt_id)
        return res


@tool("create_time_slots")
def create_time_slots(timeSlots: list[TimeSlotItem], prompt_id: str) -> str:
    """this is the function which is used to create new time slots.

    args:
        timeSlots: [
            {
                id (optional[uuid.UUID], optional): unique identifier for the time slot. defaults to none.
                timeFrom (time): start time (HH:MM:SS) of the time slot.
                timeTo (time): end time (HH:MM:SS) of the time slot.
                title (str): title of the time slot.
                description (optional[str], optional): detailed description of the time slot. defaults to none.
            },
            ...
        ]

    returns:
        dict: the time slots that were just now created are returned
    """

    print("[tool-invoke][create_time_slots]")
    input_log = json.dumps([s.model_dump(mode="json") for s in timeSlots])
    with Session(db) as session:
        slots = [TimeSlot(**d.model_dump()) for d in timeSlots]
        session.add_all(slots)
        session.commit()
        for slot in slots:
            session.refresh(slot)
        res = json.dumps(
            [TimeSlotItem.model_validate(s).model_dump(mode="json") for s in slots]
        )
        create_tool_log("create_time_slots", input_log, res, prompt_id)
        return res


@tool("delete_time_slots")
def delete_time_slots(ids: list[str], prompt_id: str) -> str:
    """
    this function is used to delete all the time slots with the given ids.
    args:
        ids (list[str]): uuids of all the entries to be deleted

    returns: str
    """

    print("[tool-invoke][delete_time_slots]")

    try:
        uuids = [uuid.UUID(i.strip()) for i in ids]
    except Exception as err:
        return f"Error occured: {err}"

    with Session(db) as session:
        session.execute(delete(TimeSlot).where(TimeSlot.id.in_(uuids)))
        session.commit()
        res = f"Successfully deleted time slots with IDs {ids}"
        create_tool_log("delete_time_slots", json.dumps(ids), res, prompt_id)
        return res


@tool("update_time_slots")
def update_time_slots(timeSlots: list[UpdateTimeSlotSchema], prompt_id: str) -> str:
    """this is the function which is used to update time slots.

    args:
        timeSlots: [
            {
                id (uuid.UUID): unique identifier for the time slot.
                timeFrom (time | None): start time (HH:MM:SS) of the time slot. defaults to none.
                timeTo (time | None): end time (HH:MM:SS) of the time slot. defaults to none.
                title (str | None): title of the time slot. defaults to none.
                description (str | None): detailed description of the time slot. defaults to none.
            },
            ...
        ]

    returns: str
    """

    print("[tool-invoke][update_time_slots]")
    print(timeSlots)
    try:
        slots = [s.model_dump(exclude_unset=True) for s in timeSlots]
        slots = [{k: v for k, v in s.items() if v is not None} for s in slots]
    except Exception as err:
        print(f"Error occured while updating time slots: {err}")

    with Session(db) as session:
        session.bulk_update_mappings(TimeSlot, slots)
        session.commit()

    res = f"Successfully updated all the entries of the IDs {[x['id'] for x in slots]}"
    create_tool_log("update_time_slots", json.dumps(slots, default=str), res, prompt_id)
    return res