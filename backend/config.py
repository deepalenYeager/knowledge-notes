from functools import lru_cache
from typing import List

from pydantic import BaseModel


class Settings(BaseModel):
    database_url: str = "sqlite:///data/knowledge.db"
    allowed_origins: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


@lru_cache
def get_settings() -> Settings:
    return Settings()

