import os
import time
import json
from uuid import UUID

import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID, JSONB
from sqlalchemy import String, Boolean, DateTime, Text
import uuid as uuidlib
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
QUEUE_NAME = os.getenv("QUEUE_NAME", "nd:jobs")

rds = redis.Redis.from_url(REDIS_URL, decode_responses=True)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

class Entry(Base):
    __tablename__ = "entries"
    id: Mapped[uuidlib.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    kind: Mapped[str] = mapped_column(String(32))
    title: Mapped[str] = mapped_column(String(200))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(32), default="PENDING")
    cv_result: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

def process(entry_id: UUID):
    # CV 占位：模拟推理耗时 + 写回结果
    time.sleep(1.2)
    return {
        "labels": ["leaf", "outdoor"],
        "confidence": 0.87
    }

def main():
    print("worker started, queue:", QUEUE_NAME)
    while True:
        item = rds.brpop(QUEUE_NAME, timeout=5)
        if not item:
            continue
        _, entry_id_str = item
        try:
            entry_id = UUID(entry_id_str)
        except Exception:
            continue

        db = SessionLocal()
        try:
            e = db.get(Entry, entry_id)
            if not e:
                continue
            e.cv_result = process(entry_id)
            e.status = "PROCESSED"
            db.commit()

            # cache invalidate
            rds.delete(f"entry:{entry_id}")
            print("processed:", entry_id)
        finally:
            db.close()

if __name__ == "__main__":
    main()
