import json

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

from syfu.schemas.task import TaskSchema, UpdateTaskSchema
from syfu.tools.tasks import (
    complete_task,
    create_tasks,
    delete_tasks,
    get_task_by_id,
    get_tasks,
    get_tasks_by_title,
    update_tasks,
)

tasks_router = APIRouter(prefix="/tasks", tags=["tasks"])


class DeleteTasksRequest(BaseModel):
    """Request body for deleting one or more tasks."""

    ids: list[str] = Field(description="UUIDs of all the tasks to be deleted.")


class CompleteTaskRequest(BaseModel):
    """Request body for marking a task as completed / not completed."""

    completed: bool = Field(
        default=True,
        description="Indicator of completion (True -> Completed, False -> Not Completed).",
    )


class TaskMessage(BaseModel):
    """Structured response for mutations performed through the task tools."""

    message: str


def _loads(payload: str):
    """Safely parse a tool's JSON-string return value."""
    try:
        return json.loads(payload)
    except (json.JSONDecodeError, TypeError):
        return payload


@tasks_router.get("")
def list_tasks():
    """Get all tasks (delegates to the `get_tasks` tool)."""
    return _loads(get_tasks.func())


@tasks_router.get("/search")
def search_tasks(title: list[str] = Query(...)):
    """Search tasks by title (delegates to the `get_tasks_by_title` tool)."""
    return _loads(get_tasks_by_title.func(title))


@tasks_router.get("/{task_id}")
def get_task(task_id: str):
    """Get a single task by ID (delegates to the `get_task_by_id` tool)."""
    result = _loads(get_task_by_id.func(task_id))
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    return result


@tasks_router.post("", status_code=status.HTTP_201_CREATED)
def create_new_tasks(payload: TaskSchema):
    """Create new tasks (delegates to the `create_tasks` tool)."""
    return _loads(create_tasks.func(payload.tasks))


@tasks_router.delete("")
def delete_tasks_by_ids(payload: DeleteTasksRequest):
    """Delete tasks by IDs (delegates to the `delete_tasks` tool)."""
    return TaskMessage(message=_loads(delete_tasks.func(payload.ids)))


@tasks_router.patch("/{task_id}/complete")
def set_task_completion(task_id: str, payload: CompleteTaskRequest):
    """Mark a task as completed or not completed (delegates to the `complete_task` tool)."""
    return TaskMessage(message=_loads(complete_task.func(task_id, payload.completed)))


@tasks_router.patch("")
def update_existing_tasks(payload: list[UpdateTaskSchema]):
    """Update existing tasks (delegates to the `update_tasks` tool)."""
    return TaskMessage(message=_loads(update_tasks.func(payload)))