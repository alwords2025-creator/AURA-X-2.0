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

class DocumentIn(BaseModel):
    title: str = Field(min_length=1, max_length=250)
    text: str = Field(min_length=1, max_length=50000)
    source: str = Field(default="user_supplied", max_length=1000)


@app.get("/health")
def health():
    return {"service": SERVICE_NAME, "status": "ok"}

@app.post("/documents")
def add_document(doc: DocumentIn):
    if not doc.text.strip():
        raise HTTPException(status_code=400, detail="text must not be empty")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO documents(title, text, source, created_at) VALUES(?,?,?,?)",
                (doc.title, doc.text, doc.source, datetime.now(timezone.utc).isoformat()))
    conn.commit()
    doc_id = cur.lastrowid
    conn.close()
    return {"id": doc_id, "stored": True, "source": doc.source}

@app.get("/search")
def search(q: str = Query(min_length=1, max_length=300), limit: int = 5):
    terms = [t.lower() for t in re.findall(r"\w+", q) if len(t) > 1]
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT id,title,text,source,created_at FROM documents ORDER BY id DESC LIMIT 1000").fetchall()
    conn.close()
    scored = []
    for row in rows:
        hay = (row[1] + " " + row[2]).lower()
        score = sum(hay.count(term) for term in terms)
        if score:
            scored.append((score, row))
    scored.sort(key=lambda x: x[0], reverse=True)
    return {"query": q, "results": [
        {"id": r[0], "title": r[1], "snippet": r[2][:700], "source": r[3],
         "created_at": r[4], "lexical_score": score} for score, r in scored[:min(max(limit,1),20)]
    ], "note": "Verify sources and facts independently; lexical score is not a truth score."}
