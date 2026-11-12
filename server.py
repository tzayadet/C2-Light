from __future__ import annotations

import re
import secrets
import time
import uuid
from typing import Literal

import uvicorn
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="C2-Lite Lab", version="2.0.0")

TaskName = Literal["report_status"]
MAX_AGENTS = 100
MAX_TASKS_PER_AGENT = 20
MAX_RESULTS_PER_AGENT = 100
AGENT_TTL_SECONDS = 1800
agents: dict[str, dict] = {}


def _purge_expired(now: float | None = None) -> None:
    current = time.time() if now is None else now
    expired = [
        aid for aid, record in agents.items()
        if current - record["last_seen"] > AGENT_TTL_SECONDS
    ]
    for aid in expired:
        agents.pop(aid, None)


class CheckIn(BaseModel):
    id: str = Field(default="", max_length=80)


class Task(BaseModel):
    task: TaskName


class Result(BaseModel):
    task: TaskName
    output: str = Field(max_length=500)


def _agent(aid: str, token: str) -> dict:
    _purge_expired()
    record = agents.get(aid)
    if not record or not secrets.compare_digest(record["token"], token):
        raise HTTPException(status_code=401, detail="Invalid agent credentials")
    return record


@app.post("/checkin")
def checkin(payload: CheckIn):
    _purge_expired()
    aid = payload.id or str(uuid.uuid4())
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,80}", aid):
        raise HTTPException(status_code=400, detail="Invalid agent identifier")
    if aid in agents:
        raise HTTPException(status_code=409, detail="Agent identifier is already registered")
    if len(agents) >= MAX_AGENTS:
        raise HTTPException(status_code=503, detail="Agent capacity reached")
    token = secrets.token_urlsafe(32)
    agents[aid] = {
        "last_seen": time.time(),
        "token": token,
        "tasks": ["report_status"],
        "results": [],
    }
    return {"id": aid, "token": token}


@app.get("/tasks/{aid}")
def get_tasks(aid: str, x_agent_token: str = Header(default="")):
    record = _agent(aid, x_agent_token)
    record["last_seen"] = time.time()
    tasks = record["tasks"]
    record["tasks"] = []
    return tasks


@app.post("/tasks/{aid}")
def enqueue_status_task(aid: str, task: Task, x_agent_token: str = Header(default="")):
    record = _agent(aid, x_agent_token)
    if len(record["tasks"]) >= MAX_TASKS_PER_AGENT:
        raise HTTPException(status_code=429, detail="Task queue is full")
    record["tasks"].append(task.task)
    return {"status": "queued", "task": task.task}


@app.post("/result/{aid}")
def result(aid: str, payload: Result, x_agent_token: str = Header(default="")):
    record = _agent(aid, x_agent_token)
    record["last_seen"] = time.time()
    record["results"].append({"task": payload.task, "output": payload.output, "received_at": time.time()})
    if len(record["results"]) > MAX_RESULTS_PER_AGENT:
        del record["results"][:-MAX_RESULTS_PER_AGENT]
    return {"logged": True}


if __name__ == "__main__":
    # Loopback-only by design. Do not expose this prototype to a network.
    uvicorn.run(app, host="127.0.0.1", port=8000)
