import json
import uuid
from datetime import datetime

from langchain_core.tools import tool
from sqlalchemy import select
from sqlalchemy.orm import Session

from syfu.core.db import db
from syfu.models.task import Task
from syfu.schemas.task import TaskPriority, TaskSchema


@tool()
def get_tasks() -> str:
    """This function is used to get all the tasks.

    Returns:
        List[dict]: A list of all the tasks
    """

    with Session(db) as session:
        tasks = session.scalars(select(Task))
        if tasks:
            return json.dumps(
                [TaskSchema.model_validate(x).model_dump(mode="json") for x in tasks]
            )
        else:
            return json.dumps([])


@tool()
def get_tasks_by_title(title: str) -> str:
    """This function is used to get all the tasks matching a certain title.
    Agrs:
        title (str): Title of the task that you want to search.

    Returns:
        List[dict]: A list of all the tasks that match the title.
    """

    with Session(db) as session:
        tasks = session.scalars(select(Task).where(Task.title.like(title)))
        if tasks:
            return json.dumps(
                [TaskSchema.model_validate(x).model_dump(mode="json") for x in tasks]
            )
        else:
            return json.dumps([])


@tool()
def get_task_by_id(id: str) -> str:
    """This function is used to get a single task with the matching id.
    Agrs:
        id (str): UUID as string of the task that you want to search.

    Returns:
        List[dict]: A list of all the tasks that match the title.
    """

    with Session(db) as session:
        task = session.scalar(select(Task).where(Task.id == id))
        if task:
            return json.dumps(
                TaskSchema.model_validate(task).model_dump(mode="json")
                if task
                else None
            )
        else:
            return json.dumps([])


@tool("create_tasks", args_schema=TaskSchema)
def create_tasks(
    id: uuid.UUID | None = None,
    title: str = "",
    description: str | None = None,
    assocDate: datetime | None = None,
    deadline: datetime | None = None,
    priority: TaskPriority = TaskPriority.CHL,
) -> str:
    """This is the function which is used to create a new task.

    Args:
        id (Optional[uuid.UUID], optional): Unique identifier for the task. Defaults to None.
        title (str): Title of the task.
        description (Optional[str], optional): Detailed description of the task. Defaults to None.
        assocDate (Optional[datetime], optional): Associated date with the task. Defaults to None.
        deadline (Optional[datetime], optional): Last date and time to finish that task. Defaults to None.
        priority (TaskPriority, optional): Priority of the task. Defaults to TaskPriority.CHL.

    Returns:
        dict: The task that was just now created is returned
    """
    with Session(db) as session:
        new_task = Task(
            title=title,
            description=description,
            assocDate=assocDate,
            deadline=deadline,
            priority=priority,
        )
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        return json.dumps(TaskSchema.model_validate(new_task).model_dump(mode="json"))
