from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class KnowledgeBase(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = None
    source: Optional[str] = None
    difficulty: Optional[int] = Field(default=None, ge=0, le=2)

    @field_validator("tags")
    @classmethod
    def clean_tags(cls, tags: Optional[List[str]]):
        if tags is None:
            return None
        cleaned = [t.strip() for t in tags if t and t.strip()]
        return cleaned or None


class KnowledgeCreate(KnowledgeBase):
    pass


class KnowledgeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    source: Optional[str] = None
    difficulty: Optional[int] = Field(default=None, ge=0, le=2)

    @field_validator("tags")
    @classmethod
    def clean_tags(cls, tags: Optional[List[str]]):
        if tags is None:
            return None
        cleaned = [t.strip() for t in tags if t and t.strip()]
        return cleaned or None


class KnowledgeRead(KnowledgeBase):
    id: int
    created_at: datetime
    updated_at: datetime


class TagStat(BaseModel):
    name: str
    count: int

