import json
import uuid
from datetime import datetime

from langchain_core.tools import tool
from sqlalchemy import Update, delete, or_, select, update
from sqlalchemy.orm import Session

from syfu.core.db import db
from syfu.models.task import Task
from syfu.schemas.task import TaskItem, TaskPriority, TaskSchema, UpdateTaskSchema

from syfu.utils.file_handling import create_tool_log


@tool()
def get_tasks(prompt_id: str) -> str:
    """This function is used to get all the tasks.

    Returns:
        List[dict]: A list of all the tasks
    """
    print("[tool-invoke][get_tasks]")

    with Session(db) as session:
        tasks = session.scalars(select(Task))
        res =  json.dumps(
                [TaskItem.model_validate(x).model_dump(mode="json") for x in tasks]
            ) if tasks else json.dumps([])
        create_tool_log("get_tasks", "None", res, prompt_id)
        return res


@tool()
def get_tasks_by_title(title: list[str], prompt_id: str) -> str:
    """This function is used to get all the tasks matching a certain title.
    Agrs:
        title (list[str]): Titles related to the task that you want to search.

    Returns:
        list[dict]: A list of all the tasks that match the title.
    """

    print("[tool-invoke][get_tasks_by_title]")
    if not title:
        return json.dumps([])
    with Session(db) as session:
        tasks = session.scalars(
            select(Task).where(or_(*[Task.title.ilike(f"%{t}%") for t in title]))
        ).all()
        res =  json.dumps(
            [TaskItem.model_validate(x).model_dump(mode="json") for x in tasks]
        ) if tasks else json.dumps([])
        create_tool_log("get_tasks_by_title", json.dumps(title), res, prompt_id)
        return res


@tool()
def get_task_by_id(id: str, prompt_id: str) -> str:
    """This function is used to get a single task with the matching id.
    Agrs:
        id (str): UUID as string of the task that you want to search.

    Returns:
        List[dict]: A list of all the tasks that match the title.
    """
    print("[tool-invoke][get_task_by_id]")
    try:
        uid = uuid.UUID(id.strip())
    except Exception as err:
        return f"Error parsing task ID: {err}"
    with Session(db) as session:
        task = session.scalar(select(Task).where(Task.id == uid))

        res =  json.dumps(
                TaskItem.model_validate(task).model_dump(mode="json") if task else None
            ) if task else json.dumps([])
        create_tool_log("get_task_by_id", id, res, prompt_id)
        return res


@tool("create_tasks")
def create_tasks(tasks: list[TaskItem], prompt_id: str) -> str:
    """this is the function which is used to create a new task.

    args:
        tasks: [
            {
                id (optional[uuid.uuid], optional): unique identifier for the task. defaults to none.
                title (str): title of the task.
                description (optional[str], optional): detailed description of the task. defaults to none.
                assocdate (optional[datetime], optional): associated date with the task. defaults to none.
                deadline (optional[datetime], optional): last date and time to finish that task. defaults to none.
                priority (taskpriority, optional): priority of the task. defaults to taskpriority.chl.
                completed (bool): defaults to false and is the indicator of task completion.
            },
            ...
        ]

    returns:
        dict: the task that was just now created is returned
    """

    print("[tool-invoke][create_tasks]")
    with Session(db) as session:
        tasks = [Task(**d.model_dump()) for d in tasks]
        session.add_all(tasks)
        session.commit()
        for task in tasks:
            session.refresh(task)
        res = json.dumps(
            [TaskItem.model_validate(t).model_dump(mode="json") for t in tasks]
        )
        create_tool_log("create_tasks", json.dumps(tasks), res, prompt_id)
        return res
        


@tool("delete_tasks")
def delete_tasks(ids: list[str], prompt_id: str) -> str:
    """
    this function is used to delete all the entries with the given ids.
    args:
        ids (list[str]): uuids of all the entries to be deleted

    returns: str
    """

    print("[tool-invoke][delete-tasks]")

    try:
        uuids = [uuid.UUID(i.strip()) for i in ids]
    except Exception as err:
        return f"Error occured: {err}"

    with Session(db) as session:
        session.execute(delete(Task).where(Task.id.in_(uuids)))
        session.commit()
        res = f"Successfully deleted tasks with IDs {ids}"
        create_tool_log("delete_tasks", json.dumps(ids), res, prompt_id)
        return res


@tool("complete_task")
def complete_task(id: str, status: bool, prompt_id: str) -> str:
    """
    this function is used to mark a task as either completed or not completed
    args:
        ids (str): uuid of all the task in question
        status (bool): Indicator of completion, (True -> Completed, False -> Not Completed)

    returns: str
    """

    print("[tool-invoke][complete-tasks]")
    try:
        uid = uuid.UUID(id.strip())
    except Exception as err:
        return f"Error in task completion status updation: {err}"
    with Session(db) as session:
        session.execute(update(Task).where(Task.id == uid).values(completed=status))
        session.commit()
        res = f"Successfully marked task with id {id} as {'Completed' if status else 'Not Completed'}"
        create_tool_log("complete_task", json.dumps({'id': id, 'status': status}), res, prompt_id)
        return res


@tool("update_tasks")
def update_tasks(tasks: list[UpdateTaskSchema], prompt_id: str) -> str:
    """this is the function which is used to update tasks.

    args:
        tasks: [
            {
                id (uuid.uuid): unique identifier for the task.
                title (str | None): title of the task. defaults to none.
                description (str | None): detailed description of the task. defaults to none.
                assocdate (datetime | None): associated date with the task. defaults to none.
                deadline (datetime | None): last date and time to finish that task. defaults to none.
                priority (taskpriority | None): priority of the task. defaults to none.
                completed (bool | None): defaults to false and is the indicator of task completion. defaults to none.
            },
            ...
        ]

    returns: str
    """

    print("[tool-invoke][update_tasks]")
    print(tasks)
    try:
        tasks = [task.model_dump(exclude_unset=True) for task in tasks]
        tasks = [{k: v for k, v in task.items() if v is not None} for task in tasks]
    except Exception as err:
        print(f"Error occured while updation of tasks: {err}")

    with Session(db) as session:
        session.bulk_update_mappings(Task, tasks)
        session.commit()

    res = f"Successfully updated all the entries of the IDs {[x['id'] for x in tasks]}"
    create_tool_log("update_tasks", json.dumps(tasks), res, prompt_id)
    return res
