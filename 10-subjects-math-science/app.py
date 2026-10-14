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

class ProblemIn(BaseModel):
    domain: str
    problem: str = Field(min_length=1, max_length=10000)


@app.get("/health")
def health():
    return {"service": SERVICE_NAME, "status": "ok"}

@app.post("/solve/route")
def route_problem(req: ProblemIn):
    domains = {"mathematics", "physics", "chemistry", "biology", "engineering",
               "technology", "computer_science", "general"}
    if req.domain not in domains:
        raise HTTPException(status_code=400, detail=f"domain must be one of {sorted(domains)}")
    return {"domain": req.domain, "problem": req.problem,
            "workflow": ["identify knowns and unknowns", "state assumptions and units",
                         "select a suitable method", "solve step by step",
                         "check dimensions/logic", "cite sources for current facts",
                         "state uncertainty and limitations"],
            "status": "routed_not_solved",
            "note": "This is a workflow gateway, not a connected LLM or scientific computation engine."}
