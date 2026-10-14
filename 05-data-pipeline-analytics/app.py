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

class DataRequest(BaseModel):
    rows: list[dict[str, Any]] = Field(min_length=1, max_length=10000)


@app.get("/health")
def health():
    return {"service": SERVICE_NAME, "status": "ok"}

@app.post("/analyze")
def analyze(req: DataRequest):
    if not req.rows:
        raise HTTPException(status_code=400, detail="rows must contain at least one record")
    cols = sorted({k for row in req.rows for k in row.keys()})
    profile = {}
    for col in cols:
        vals = [row.get(col) for row in req.rows]
        nonempty = [v for v in vals if v is not None and v != ""]
        nums = []
        for v in nonempty:
            try: nums.append(float(v))
            except (ValueError, TypeError): pass
        profile[col] = {"count": len(vals), "non_empty": len(nonempty),
                        "numeric_count": len(nums),
                        "numeric_min": min(nums) if nums else None,
                        "numeric_max": max(nums) if nums else None,
                        "numeric_mean": (sum(nums)/len(nums)) if nums else None}
    return {"row_count": len(req.rows), "columns": cols, "profile": profile,
            "warning": "Statistics describe supplied data; they do not establish causation or guarantee correctness."}
