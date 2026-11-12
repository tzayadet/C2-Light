<p align="center">
  <img src="https://img.shields.io/badge/SECURITY_LAB-C2_LITE_SIMULATOR-101010?style=for-the-badge&labelColor=050805&color=00FF41" alt="C2-Lite simulator"/>
  <img src="https://img.shields.io/badge/PYTHON-FASTAPI-101010?style=for-the-badge&logo=python&logoColor=00FF41" alt="Python and FastAPI"/>
</p>

# C2-Lite · Client/Server Simulation

A deliberately limited Python client/server lab for studying agent registration, authenticated polling, task queues and result reporting. The agent supports one fixed demonstration task and **does not execute shell commands or run arbitrary code**.

<p align="center">
  <a href="https://github.com/tzayadet/C2-Light/blob/main/docs/index.html"><strong>SHOWCASE SOURCE</strong></a> ·
  <a href="https://github.com/tzayadet/C2-Light"><strong>SOURCE CODE</strong></a> · <sub>PAGES ACTIVATION PENDING</sub>
</p>

[![Python checks](https://github.com/tzayadet/C2-Light/actions/workflows/python-syntax.yml/badge.svg)](https://github.com/tzayadet/C2-Light/actions/workflows/python-syntax.yml)

## Features

- Agent registration with a per-session random token.
- Token validation for polling and result submission.
- In-memory task queue and result collection.
- Fixed `report_status` demonstration task.
- Loopback-only server binding and client URL validation.
- Automated tests for task restrictions and URL validation.

## Run locally

**Requirements:** Python 3.11+.

```bash
python -m pip install -r requirements.txt
python server.py
```

In a second terminal:

```bash
python agent.py
```

The server listens on `127.0.0.1:8000`. The agent accepts only a loopback HTTP URL and rejects remote hosts. Stop the agent with Ctrl+C.

## Project structure

| Path | Purpose |
|---|---|
| `server.py` | FastAPI registration, task queue and result API |
| `agent.py` | Restricted demonstration client |
| `tests/test_agent.py` | Safety and behaviour tests |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Local server container |
| `docs/` | Static architecture showcase |
| `.github/workflows/` | Syntax and unit-test workflow |

## Tests

```bash
python -m unittest discover -s tests -v
python -m compileall -q .
```

## Security model and limitations

This version is a **simulation**, not a remote administration tool or production C2 framework.

- No arbitrary command execution, shell invocation, persistence or file transfer.
- Only the fixed `report_status` task is accepted.
- The server binds to loopback; the client rejects non-loopback destinations.
- Session tokens provide a basic local demonstration, not production-grade identity or transport security.
- State is held in memory and is lost when the server stops.
- The API has no production administrator role, durable audit log, rate limiting or deployment hardening.

Do not change the loopback restrictions or expose the service to a network. The project demonstrates API and queue mechanics, not operational command-and-control.

## Showcase and deployment

The static architecture overview is available in [docs/index.html](docs/index.html). It does not connect to the server or run an agent. The Pages workflow is present, but publication is pending repository-level Pages activation. The backend runs locally and is not deployed to Pages.

## License

See [LICENSE](LICENSE).
