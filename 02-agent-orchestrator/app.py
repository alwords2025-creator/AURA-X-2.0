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
    goal: str = Field(min_length=1, max_length=3000)
    max_steps: int = 5


@app.get("/health")
def health():
    return {"service": SERVICE_NAME, "status": "ok"}

@app.post("/tasks/plan")
def plan(req: TaskRequest):
    if not req.goal.strip():
        raise HTTPException(status_code=400, detail="goal must not be empty")
    steps = [
        {"agent": "planner", "action": "clarify goal and acceptance criteria"},
        {"agent": "research", "action": "collect authorized evidence if needed"},
        {"agent": "specialist", "action": "perform the bounded task"},
        {"agent": "verifier", "action": "check output against acceptance criteria"},
        {"agent": "reporter", "action": "return result, evidence, limitations"}
    ]
    return {"task_id": str(uuid.uuid4()), "goal": req.goal, "status": "planned",
            "max_steps": min(max(req.max_steps, 1), 10), "plan": steps,
            "requires_admin_approval_for_external_actions": True}
