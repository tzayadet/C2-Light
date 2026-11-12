from __future__ import annotations

import os
import time
from urllib.parse import urlparse

import requests

SERVER = os.getenv("C2_SERVER", "http://127.0.0.1:8000").rstrip("/")
AGENT_ID = os.getenv("AGENT_ID", "")


def validate_server_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("C2-Lite is restricted to an HTTP loopback server.")
    if parsed.port not in {None, 8000}:
        raise ValueError("C2-Lite uses the local port 8000.")
    return url.rstrip("/")


def run_task(task: str) -> str:
    """Return a fixed demonstration result. No shell or OS commands are executed."""
    if task != "report_status":
        raise ValueError(f"Unsupported demonstration task: {task}")
    return "simulation: agent online; no host commands executed"


def main() -> None:
    server = validate_server_url(SERVER)
    session = requests.Session()
    response = session.post(f"{server}/checkin", json={"id": AGENT_ID}, timeout=5)
    response.raise_for_status()
    registration = response.json()
    agent_id = registration["id"]
    token = registration["token"]
    headers = {"X-Agent-Token": token}

    print(f"[+] Simulation agent {agent_id} registered against loopback.")
    try:
        while True:
            response = session.get(f"{server}/tasks/{agent_id}", headers=headers, timeout=5)
            response.raise_for_status()
            for task in response.json():
                output = run_task(task)
                result = session.post(
                    f"{server}/result/{agent_id}",
                    json={"task": task, "output": output},
                    headers=headers,
                    timeout=5,
                )
                result.raise_for_status()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n[+] Agent stopped.")


if __name__ == "__main__":
    main()
