from __future__ import annotations

import secrets
import time
import uuid
from typing import Literal

import uvicorn
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="C2-Lite Lab", version="2.0.0")

TaskName = Literal["report_status"]
agents: dict[str, dict] = {}


class CheckIn(BaseModel):
    id: str = Field(default="", max_length=80)


class Task(BaseModel):
    task: TaskName


class Result(BaseModel):
    task: TaskName
    output: str = Field(max_length=500)


def _agent(aid: str, token: str) -> dict:
    record = agents.get(aid)
    if not record or not secrets.compare_digest(record["token"], token):
        raise HTTPException(status_code=401, detail="Invalid agent credentials")
    return record


@app.post("/checkin")
def checkin(payload: CheckIn):
    aid = payload.id or str(uuid.uuid4())
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
    record["tasks"].append(task.task)
    return {"status": "queued", "task": task.task}


@app.post("/result/{aid}")
def result(aid: str, payload: Result, x_agent_token: str = Header(default="")):
    record = _agent(aid, x_agent_token)
    record["last_seen"] = time.time()
    record["results"].append({"task": payload.task, "output": payload.output, "received_at": time.time()})
    return {"logged": True}


if __name__ == "__main__":
    # Loopback-only by design. Do not expose this prototype to a network.
    uvicorn.run(app, host="127.0.0.1", port=8000)
