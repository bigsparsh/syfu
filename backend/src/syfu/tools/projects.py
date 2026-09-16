import json
import uuid

from langchain_core.tools import tool
from sqlalchemy import delete, or_, select, update
from sqlalchemy.orm import Session

from syfu.core.db import db
from syfu.models.project import Project
from syfu.schemas.project import ProjectItem, UpdateProjectSchema

from syfu.utils.file_handling import create_tool_log


@tool()
def get_projects(prompt_id: str) -> str:
    """This function is used to get all the projects.

    Returns:
        List[dict]: A list of all the projects
    """
    print("[tool-invoke][get_projects]")

    with Session(db) as session:
        projects = session.scalars(select(Project)).all()
        res = (
            json.dumps(
                [
                    ProjectItem.model_validate(x).model_dump(mode="json")
                    for x in projects
                ]
            )
            if projects
            else json.dumps([])
        )
        create_tool_log("get_projects", "None", res, prompt_id)
        return res


@tool()
def get_projects_by_title(title: list[str], prompt_id: str) -> str:
    """This function is used to get all the projects matching a certain title.
    Agrs:
        title (list[str]): Titles related to the project that you want to search.

    Returns:
        list[dict]: A list of all the projects that match the title.
    """

    print("[tool-invoke][get_projects_by_title]")
    if not title:
        return json.dumps([])
    with Session(db) as session:
        projects = session.scalars(
            select(Project).where(or_(*[Project.title.ilike(f"%{t}%") for t in title]))
        ).all()
        res = (
            json.dumps(
                [
                    ProjectItem.model_validate(x).model_dump(mode="json")
                    for x in projects
                ]
            )
            if projects
            else json.dumps([])
        )
        create_tool_log("get_projects_by_title", json.dumps(title), res, prompt_id)
        return res


@tool()
def get_project_by_id(id: str, prompt_id: str) -> str:
    """This function is used to get a single project with the matching id.
    Agrs:
        id (str): UUID as string of the project that you want to search.

    Returns:
        dict: The project that matches the given id.
    """
    print("[tool-invoke][get_project_by_id]")
    try:
        uid = uuid.UUID(id.strip())
    except Exception as err:
        return f"Error parsing project ID: {err}"
    with Session(db) as session:
        project = session.scalar(select(Project).where(Project.id == uid))

        res = (
            json.dumps(
                ProjectItem.model_validate(project).model_dump(mode="json")
                if project
                else None
            )
            if project
            else json.dumps([])
        )
        create_tool_log("get_project_by_id", id, res, prompt_id)
        return res


@tool("create_projects")
def create_projects(projects: list[ProjectItem], prompt_id: str) -> str:
    """this is the function which is used to create new projects.

    args:
        projects: [
            {
                id (optional[uuid.UUID], optional): unique identifier for the project. defaults to none.
                title (str): title of the project.
                description (optional[str], optional): detailed description of the project. defaults to none.
                sdlcModel (sdlcmodel): SDLC model followed by the project (classic-waterfall, interactive-waterfall, spiral).
                aiTickets (bool): whether the project should automatically generate AI tickets. defaults to true.
            },
            ...
        ]

    returns:
        dict: the projects that were just now created are returned
    """

    print("[tool-invoke][create_projects]")
    input_log = json.dumps([p.model_dump(mode="json") for p in projects])
    with Session(db) as session:
        projects = [Project(**d.model_dump()) for d in projects]
        session.add_all(projects)
        session.commit()
        for project in projects:
            session.refresh(project)
        res = json.dumps(
            [
                ProjectItem.model_validate(p).model_dump(mode="json")
                for p in projects
            ]
        )
        create_tool_log("create_projects", input_log, res, prompt_id)
        return res


@tool("delete_projects")
def delete_projects(ids: list[str], prompt_id: str) -> str:
    """
    this function is used to delete all the projects with the given ids.
    args:
        ids (list[str]): uuids of all the entries to be deleted

    returns: str
    """

    print("[tool-invoke][delete_projects]")

    try:
        uuids = [uuid.UUID(i.strip()) for i in ids]
    except Exception as err:
        return f"Error occured: {err}"

    with Session(db) as session:
        session.execute(delete(Project).where(Project.id.in_(uuids)))
        session.commit()
        res = f"Successfully deleted projects with IDs {ids}"
        create_tool_log("delete_projects", json.dumps(ids), res, prompt_id)
        return res


@tool("update_projects")
def update_projects(projects: list[UpdateProjectSchema], prompt_id: str) -> str:
    """this is the function which is used to update projects.

    args:
        projects: [
            {
                id (uuid.UUID): unique identifier for the project.
                title (str | None): title of the project. defaults to none.
                description (str | None): detailed description of the project. defaults to none.
                sdlcModel (sdlcmodel | None): SDLC model followed by the project (classic-waterfall, interactive-waterfall, spiral). defaults to none.
                aiTickets (bool | None): whether the project should automatically generate AI tickets. defaults to none.
            },
            ...
        ]

    returns: str
    """

    print("[tool-invoke][update_projects]")
    print(projects)
    try:
        projects = [p.model_dump(exclude_unset=True) for p in projects]
        projects = [{k: v for k, v in p.items() if v is not None} for p in projects]
    except Exception as err:
        print(f"Error occured while updating projects: {err}")

    with Session(db) as session:
        session.bulk_update_mappings(Project, projects)
        session.commit()

    res = f"Successfully updated all the entries of the IDs {[x['id'] for x in projects]}"
    create_tool_log("update_projects", json.dumps(projects, default=str), res, prompt_id)
    return res