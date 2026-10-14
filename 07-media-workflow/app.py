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

class MediaRequest(BaseModel):
    kind: str
    brief: str = Field(min_length=1, max_length=5000)
    resolution: str = "1080p"


@app.get("/health")
def health():
    return {"service": SERVICE_NAME, "status": "ok"}

@app.post("/media/jobs")
def create_job(req: MediaRequest):
    if req.kind not in {"video", "image", "audio"}:
        raise HTTPException(status_code=400, detail="kind must be video, image, or audio")
    if req.resolution not in {"720p", "1080p", "1440p", "2160p", "source"}:
        raise HTTPException(status_code=400, detail="unsupported resolution label")
    return {"job_id": str(uuid.uuid4()), "kind": req.kind, "brief": req.brief,
            "resolution_target": req.resolution, "status": "planned",
            "checks": ["confirm source rights", "confirm codec and dimensions", "verify audio sync",
                       "check duration and file integrity"],
            "note": "No media is rendered by this planning-only starter endpoint."}
