from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

from .config import get_settings

settings = get_settings()

# Ensure the data directory exists for SQLite persistence
db_url = settings.database_url
if db_url.startswith("sqlite:///"):
    db_path = Path(db_url.replace("sqlite:///", "", 1))
    db_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(db_url, echo=False, connect_args={"check_same_thread": False})


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

