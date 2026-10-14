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

class TaskRequest(BaseModel):
    goal: str
    max_steps: int = 5


@app.get("/health")
def health():
    return {"service": SERVICE_NAME, "status": "ok"}

@app.get("/admin/overview")
def overview():
    return {"project": "AURA-X 2.0 Core", "mode": "starter", "services": SERVICES,
            "note": "Connect real services only after configuring authenticated endpoints."}

@app.get("/admin/policies")
def policies():
    return {"defaults": {"require_auth": True, "audit_actions": True,
                         "allow_stealth_or_evasion": False, "paid_services_need_approval": True}}
