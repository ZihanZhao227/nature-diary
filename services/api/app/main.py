import os
import json
from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import redis

from .db import Base, engine, get_db
from .models import Entry
from .schemas import EntryCreate, EntryOut

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
QUEUE_NAME = os.getenv("QUEUE_NAME", "nd:jobs")

rds = redis.Redis.from_url(REDIS_URL, decode_responses=True)

app = FastAPI(title="Nature Diary API", version="0.2.0")
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/v1/entries", response_model=EntryOut)
def create_entry(payload: EntryCreate, db: Session = Depends(get_db)):
    e = Entry(kind=payload.kind, title=payload.title, notes=payload.notes, status="PENDING")
    db.add(e)
    db.commit()
    db.refresh(e)

    # push async job (distributed skeleton)
    rds.lpush(QUEUE_NAME, str(e.id))
    return e

@app.get("/v1/entries", response_model=list[EntryOut])
def list_entries(db: Session = Depends(get_db)):
    return db.query(Entry).order_by(Entry.created_at.desc()).limit(100).all()

@app.get("/v1/entries/{entry_id}", response_model=EntryOut)
def get_entry(entry_id: UUID, db: Session = Depends(get_db)):
    cache_key = f"entry:{entry_id}"
    cached = rds.get(cache_key)
    if cached:
        return json.loads(cached)

    e = db.get(Entry, entry_id)
    if not e:
        raise HTTPException(404, "not found")

    # cache 30s
    out = EntryOut.model_validate(e).model_dump()
    rds.setex(cache_key, 30, json.dumps(out, default=str))
    return out

@app.post("/v1/entries/{entry_id}/favorite", response_model=EntryOut)
def favorite(entry_id: UUID, db: Session = Depends(get_db)):
    e = db.get(Entry, entry_id)
    if not e:
        raise HTTPException(404, "not found")
    e.is_favorite = True
    db.commit()
    db.refresh(e)
    # invalidate cache
    rds.delete(f"entry:{entry_id}")
    return e

@app.get("/v1/search", response_model=list[EntryOut])
def search(q: str, db: Session = Depends(get_db)):
    # minimal search: title ilike
    return (
        db.query(Entry)
        .filter(Entry.title.ilike(f"%{q}%"))
        .order_by(Entry.created_at.desc())
        .limit(50)
        .all()
    )
