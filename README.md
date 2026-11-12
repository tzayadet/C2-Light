# C2-Lite Lab

An experimental client/server lab for studying agent registration, task queues and process communication in an isolated environment. The public page is an architecture overview only; it does not connect to an agent or execute tasks.

<p align="center">
  <a href="https://tzayadet.github.io/C2-Light/"><img src="https://img.shields.io/badge/ARCHITECTURE_SHOWCASE-OPEN-00a86b?style=flat-square" alt="Architecture showcase"></a>
  <a href="https://github.com/tzayadet/C2-Light"><img src="https://img.shields.io/badge/SOURCE-GITHUB-161b22?style=flat-square&logo=github" alt="Source"></a>
</p>

[![Python CI](https://github.com/tzayadet/C2-Light/actions/workflows/python-syntax.yml/badge.svg)](https://github.com/tzayadet/C2-Light/actions/workflows/python-syntax.yml) · [![Container build](https://github.com/tzayadet/C2-Light/actions/workflows/container-build.yml/badge.svg)](https://github.com/tzayadet/C2-Light/actions/workflows/container-build.yml) · [![Pages](https://github.com/tzayadet/C2-Light/actions/workflows/pages.yml/badge.svg)](https://github.com/tzayadet/C2-Light/actions/workflows/pages.yml)

## Components

| Path | Purpose |
|---|---|
| `server.py` | FastAPI server and in-memory storage |
| `agent.py` | Experimental check-in and polling client |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Server container image |
| `docs/` | Static architecture showcase |

## Run locally

**Requirements:** Python 3.11 or later.

```bash
python -m pip install -r requirements.txt
```

Review the source before execution. The server's default bind configuration must be kept inside an isolated lab network.

## Status and security limitations

**Experimental. Not suitable for production or public networks.**

The prototype includes a flow where the server can deliver commands for execution by the agent through a shell. It does not implement robust agent authentication, task-level authorisation, process isolation or a complete secure channel. Initialisation of cryptographic objects does not mean the task flow is protected end to end; the shared key is delivered during registration to unauthenticated clients and is not a trustworthy identity mechanism.

Use only in a disposable virtual machine and isolated lab network. Do not expose the service to the Internet or run it on systems belonging to others.

## Showcase and deployment

The static showcase explains the architecture. It does not connect to the agent, issue tasks or provide a live command interface. GitHub Pages deployment uses `.github/workflows/pages.yml`; Pages must be enabled with GitHub Actions and the `ENABLE_PAGES=true` Actions variable configured.

## License

See [LICENSE](LICENSE) for the repository's licensing terms.
