from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class KnowledgeItem(SQLModel, table=True):
    __tablename__ = "knowledge_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    tags: Optional[str] = Field(default=None, description="Comma separated tags")
    source: Optional[str] = None
    difficulty: Optional[int] = Field(default=None, ge=0, le=2)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

