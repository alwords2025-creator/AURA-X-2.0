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

class EventIn(BaseModel):
    source: str = Field(min_length=1, max_length=100)
    severity: str = "info"
    message: str = Field(min_length=1, max_length=2000)


@app.get("/health")
def health():
    return {"service": SERVICE_NAME, "status": "ok"}

@app.get("/metrics/basic")
def basic_metrics():
    return {"process_id": os.getpid(), "python": sys.version.split()[0],
            "platform": platform.platform(), "uptime_seconds": round(time.time()-START_TIME, 2),
            "note": "This is basic process metadata, not full host RAM/CPU telemetry."}

@app.post("/events")
def event(ev: EventIn):
    # Starter keeps events in a local JSONL file; secure the host filesystem in real deployments.
    record = {"timestamp": datetime.now(timezone.utc).isoformat(), **ev.model_dump()}
    with open(EVENT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return {"recorded": True, "audience": "authorized_admin_dashboard",
            "event_id": str(uuid.uuid4()), "severity": ev.severity}
