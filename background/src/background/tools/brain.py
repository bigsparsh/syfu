import subprocess
from pathlib import Path
from uuid import uuid4
from langchain_core.tools import tool
from platformdirs import user_cache_path
from pydantic import Field

from src.background.utils.cache import ensure_cache_structure

ensure_cache_structure()
cache_path = user_cache_path("syfu")

BRAIN_DIR= cache_path / "brain"

@tool()
def get_index() -> str:
    """
    Gets the brain index where each index is an markdown file name which is present in different folders inside the brain dir.
    """
    print("[tool-invoke][get-index]")
    with open(BRAIN_DIR/"index.md", "r") as f:
        return f.read()

@tool()
def update_index(data: str) -> str:
    """
    Updates the current index with the new files or folders that have been created or deleted.
    Note: This replaces the previous index and overwrites the date give, so be sure to include the previous data as well as the new one.
    """

    print("[tool-invoke][update-index]")
    with open(BRAIN_DIR/"index.md", "w") as f:
        f.write(data)

@tool()
def list_brain(folder: str="") -> str:
    """
    Just performs a `ls` command in the brain directory to get all the folders and files inside it.
    Agrs:
        folder (str): This is the path of the folder inside the brain directory that needs to be checked
    Output:
        str: All all elements inside the brain folder
    """
    print("[tool-invoke][list-brain]")
    return subprocess.run(['ls', '-la'], cwd=BRAIN_DIR/folder, capture_output=True, text=True)

@tool()
def update_brain_file(file_path: str, data: str):
    """
    Update any particular file inside the brain. 
    Note: The file will be overwritten by using this function. So, keep the older content along with the newer content in order to update properly.
    Agrs:
        file_path (str): The path of file inside the brain folder that needs to be updated.
        data (str): The data that needs to be updated inside the file.
    """

    print("[tool-invoke][update-brain-file]")
    with open(BRAIN_DIR/file_path, "w") as f:
        f.write(data)


@tool()
def create_brain_folder(path: str):
    """
    Creates a new folder in brain folder.
    Agrs:
        path (str): Name of the new folder to be created.
    """
    print("[tool-invoke][create-brain-folder]")
    folder = Path(BRAIN_DIR/path)
    folder.mkdir(parents=True, exist_ok=True)

@tool()
def create_brain_file(path: str = Field( description="The exact filename only, e.g., 'tasks.md'. Do NOT include any folder names or directory paths."), header: str="---\n---"):
    """
    Create a new markdown file in the brain folder or any top level folder inside the brain folder.
    NOTE: The base path is already in the brain folder. So, if a file needs to be present in the base brain folder then DO NOT add the folder name.
    Agrs:
        path (str): Path of the folder and the name of the file to create inside the brain folder.
        header (str): Header of the markdown file that describes the information that is to be stored in here.
    """
    
    print("[tool-invoke][create-brain-file]")
    with open(BRAIN_DIR/path, "w") as f: f.write(header)

@tool()
def get_uuid():
    """
    Returns a new and unique UUIDv4.
    Output:
        str : A unique UUID
    """
    return uuid4()