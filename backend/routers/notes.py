from datetime import datetime
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlmodel import Session

from ..database import get_session
from ..models import KnowledgeItem
from ..schemas import KnowledgeCreate, KnowledgeRead, KnowledgeUpdate, TagStat

router = APIRouter(prefix="/api", tags=["notes"])


def _deserialize_tags(tag_str: Optional[str]) -> Optional[List[str]]:
    if not tag_str:
        return None
    tags = [t.strip() for t in tag_str.split(",") if t and t.strip()]
    return tags or None


def _serialize_tags(tags: Optional[List[str]]) -> Optional[str]:
    if not tags:
        return None
    cleaned = [t.strip() for t in tags if t and t.strip()]
    return ",".join(cleaned) if cleaned else None


def _to_schema(item: KnowledgeItem) -> KnowledgeRead:
    return KnowledgeRead(
        id=item.id,
        title=item.title,
        content=item.content,
        tags=_deserialize_tags(item.tags),
        source=item.source,
        difficulty=item.difficulty,
        created_at=item.created_at,
        updated_at=item.updated_at,
    )


@router.get("/notes", response_model=List[KnowledgeRead])
def list_notes(
    q: Optional[str] = None,
    tag: Optional[str] = None,
    session: Session = Depends(get_session),
):
    query = select(KnowledgeItem)

    if q:
        pattern = f"%{q.lower()}%"
        query = query.where(
            func.lower(KnowledgeItem.title).like(pattern)
            | func.lower(KnowledgeItem.content).like(pattern)
        )

    if tag:
        pattern = f"%{tag.lower()}%"
        query = query.where(func.lower(KnowledgeItem.tags).like(pattern))

    query = query.order_by(KnowledgeItem.updated_at.desc())
    items = session.exec(query).all()
    return [_to_schema(item) for item in items]


@router.get("/notes/{item_id}", response_model=KnowledgeRead)
def get_note(item_id: int, session: Session = Depends(get_session)):
    item = session.get(KnowledgeItem, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return _to_schema(item)


@router.post("/notes", response_model=KnowledgeRead, status_code=status.HTTP_201_CREATED)
def create_note(payload: KnowledgeCreate, session: Session = Depends(get_session)):
    now = datetime.utcnow()
    db_item = KnowledgeItem(
        title=payload.title,
        content=payload.content,
        tags=_serialize_tags(payload.tags),
        source=payload.source,
        difficulty=payload.difficulty,
        created_at=now,
        updated_at=now,
    )
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return _to_schema(db_item)


@router.put("/notes/{item_id}", response_model=KnowledgeRead)
def update_note(
    item_id: int,
    payload: KnowledgeUpdate,
    session: Session = Depends(get_session),
):
    item = session.get(KnowledgeItem, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    if payload.title is not None:
        item.title = payload.title
    if payload.content is not None:
        item.content = payload.content
    if payload.tags is not None:
        item.tags = _serialize_tags(payload.tags)
    if payload.source is not None:
        item.source = payload.source
    if payload.difficulty is not None:
        item.difficulty = payload.difficulty

    item.updated_at = datetime.utcnow()
    session.add(item)
    session.commit()
    session.refresh(item)
    return _to_schema(item)


@router.delete("/notes/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(item_id: int, session: Session = Depends(get_session)):
    item = session.get(KnowledgeItem, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    session.delete(item)
    session.commit()
    return None


@router.get("/tags", response_model=List[TagStat])
def list_tags(session: Session = Depends(get_session)):
    tags_column = session.exec(select(KnowledgeItem.tags)).all()
    counter: Dict[str, int] = {}
    for tag_str in tags_column:
        for tag in _deserialize_tags(tag_str) or []:
            counter[tag] = counter.get(tag, 0) + 1
    stats = [TagStat(name=name, count=count) for name, count in sorted(counter.items(), key=lambda kv: kv[0].lower())]
    return stats


@router.get("/export", response_model=List[KnowledgeRead])
def export_notes(session: Session = Depends(get_session)):
    items = session.exec(select(KnowledgeItem)).all()
    return [_to_schema(item) for item in items]

