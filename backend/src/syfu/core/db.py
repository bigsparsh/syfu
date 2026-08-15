from pathlib import Path

from sqlalchemy import create_engine

from syfu.models.base import Base

DB_PATH = Path(__file__).resolve().parents[3] / "main.db"
db = create_engine(f"sqlite:///{DB_PATH}", echo=False)


def init_db() -> None:
    from syfu import models  # noqa: F401

    Base.metadata.create_all(bind=db)
