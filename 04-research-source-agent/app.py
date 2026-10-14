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

class SourceIn(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    url: str = Field(min_length=8, max_length=2000)
    publisher: str = Field(default="unknown", max_length=300)
    published_date: str | None = None
    notes: str = Field(default="", max_length=5000)


@app.get("/health")
def health():
    return {"service": SERVICE_NAME, "status": "ok"}

@app.post("/research/record")
def record_source(src: SourceIn):
    if not src.url.startswith(("https://", "http://")):
        raise HTTPException(status_code=400, detail="url must use http or https")
    return {"accepted": True, "source": src.model_dump(),
            "checks": ["URL scheme checked", "review publication date", "verify publisher",
                       "cross-check important claims", "respect terms and permissions"]}
