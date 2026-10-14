import os, sys, time, json, uuid, sqlite3, re, platform
from datetime import datetime, timezone
from typing import Any
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

SERVICE_NAME = os.getenv("SERVICE_NAME", "AURA-X service")
START_TIME = time.time()
DB_PATH = os.getenv("DB_PATH", "aura_x_local.sqlite3")
EVENT_LOG = os.getenv("EVENT_LOG", "events.jsonl")
SERVICES = {
  "admin": os.getenv("ADMIN_SERVICE_URL", "not_configured"),
  "orchestrator": os.getenv("ORCHESTRATOR_URL", "not_configured"),
  "knowledge": os.getenv("KNOWLEDGE_URL", "not_configured")
}
app = FastAPI(title=SERVICE_NAME, version="0.1.0",
              description="AURA-X 2.0 Core starter service. Secure it before internet exposure.")

class QueueIn(BaseModel):
    payload: dict[str, Any]


@app.get("/health")
def health():
    return {"service": SERVICE_NAME, "status": "ok"}

@app.post("/queue")
def enqueue(item: QueueIn):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO queue(task_id,payload,status,created_at) VALUES(?,?,?,?)",
                (str(uuid.uuid4()), json.dumps(item.payload), "queued", datetime.now(timezone.utc).isoformat()))
    conn.commit()
    task_id = cur.lastrowid
    conn.close()
    return {"queue_id": task_id, "status": "queued", "sync_status": "not_configured"}

@app.get("/queue")
def get_queue():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT id,payload,status,created_at FROM queue ORDER BY id DESC LIMIT 100").fetchall()
    conn.close()
    return {"items": [{"id": r[0], "payload": json.loads(r[1]), "status": r[2], "created_at": r[3]} for r in rows],
            "note": "Configure authenticated sync and conflict resolution before connecting cloud services."}
