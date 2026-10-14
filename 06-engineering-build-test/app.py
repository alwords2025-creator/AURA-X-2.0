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

class BuildRequest(BaseModel):
    project_name: str = Field(min_length=1, max_length=200)
    acceptance_criteria: list[str] = Field(default_factory=list, max_length=100)


@app.get("/health")
def health():
    return {"service": SERVICE_NAME, "status": "ok"}

@app.post("/engineering/checklist")
def checklist(req: BuildRequest):
    if not req.project_name.strip():
        raise HTTPException(status_code=400, detail="project_name must not be empty")
    return {"project_name": req.project_name, "acceptance_criteria": req.acceptance_criteria,
            "checklist": ["review requirements", "inspect dependencies", "build in an isolated environment",
                          "run tests", "review logs", "verify deliverables", "document limitations"],
            "execution_status": "not_executed",
            "note": "This endpoint plans checks; it does not claim to build or test a project."}
