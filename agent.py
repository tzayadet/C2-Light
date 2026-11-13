from __future__ import annotations

import os
import time
from urllib.parse import urlparse

import requests

SERVER = os.getenv("C2_SERVER", "http://127.0.0.1:8000").rstrip("/")
AGENT_ID = os.getenv("AGENT_ID", "")


def validate_server_url(url: str) -> str:
    if not isinstance(url, str) or not url or len(url) > 2048:
        raise ValueError("A valid loopback server URL is required.")
    if any(char.isspace() or ord(char) < 32 or ord(char) == 127 for char in url):
        raise ValueError("Server URL must not contain whitespace or control characters.")
    try:
        parsed = urlparse(url)
        port = parsed.port
    except ValueError as exc:
        raise ValueError("Server URL is malformed.") from exc
    if (
        parsed.scheme != "http"
        or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
        or parsed.path not in {"", "/"}
    ):
        raise ValueError("C2-Lite is restricted to a plain HTTP loopback URL.")
    if port not in {None, 8000}:
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
    # Ignore proxy environment variables and never follow a server redirect.
    session.trust_env = False

    def request(method: str, path: str, **kwargs):
        response = session.request(
            method,
            f"{server}{path}",
            timeout=5,
            allow_redirects=False,
            **kwargs,
        )
        if 300 <= response.status_code < 400:
            raise RuntimeError("Redirects are disabled in the loopback-only simulation.")
        response.raise_for_status()
        return response

    response = request("POST", "/checkin", json={"id": AGENT_ID})
    registration = response.json()
    agent_id = registration["id"]
    token = registration["token"]
    headers = {"X-Agent-Token": token}

    print(f"[+] Simulation agent {agent_id} registered against loopback.")
    try:
        while True:
            response = request("GET", f"/tasks/{agent_id}", headers=headers)
            for task in response.json():
                output = run_task(task)
                request(
                    "POST",
                    f"/result/{agent_id}",
                    json={"task": task, "output": output},
                    headers=headers,
                )
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n[+] Agent stopped.")


if __name__ == "__main__":
    main()
