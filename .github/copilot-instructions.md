# PawsNPlay Copilot Instructions

## Project Overview
**PawsNPlay** is a FastAPI-based backend service with a microservices architecture. The project uses Python 3.13, UV for package management, and Docker Compose for local development with PostgreSQL, Qdrant (vector DB), Redis, and Ollama (LLM).

## Architecture & Components

### Core Structure
- **`app/app.py`**: FastAPI application entrypoint - start here for route definitions and middleware
- **`main.py`**: Entry point for local execution
- **`auth/`**: Authentication module (currently empty, planned for auth logic)
- **`dbstruct/`**: Database structure/models (currently empty, planned for ORM models)

### External Services (Docker Compose)
- **PostgreSQL** (`postgres:15`): Primary database at `postgres:5432`
- **Qdrant**: Vector database for embeddings at port `6333`
- **Redis**: Caching layer at port `6379`
- **Ollama**: Local LLM inference at port `11434`

All services are configured to communicate via service names (not localhost) within the Docker network.

## Development Workflow

### Setup & Running
```bash
# Initialize the project (first time)
uv init

# Run locally
python main.py

# Run with FastAPI dev server
uvicorn app.app:app --reload

# Start full stack (Docker)
docker-compose up -d
```

### Key Commands
- **Dependencies**: Managed via `pyproject.toml` with UV. Add with `uv add <package>`
- **Environment**: Python 3.13 (see `.python-version`). UV handles venv automatically
- **Docker**: Python 3.11 in container (note: differs from local 3.13 - update Dockerfile if needed)

## Important Patterns & Conventions

### Environment Configuration
- Services communicate via Docker Compose service names, not localhost
- Environment variables are injected in `docker-compose.yaml` (see `environment:` section)
- Local development may need manual .env setup for external services

### Dependencies
- **FastAPI** (>=0.123.5): Web framework - all routes go in `app/app.py`
- **No ORM yet**: `dbstruct/` is empty - design with SQLAlchemy or similar in mind
- **UV over pip**: Always use `uv add/remove`, not pip directly

### API Design
- Start with simple route handlers in `app.app.py`
- Expected to grow: plan for router organization as endpoints multiply
- Integration with Qdrant and Ollama for LLM features is likely

## Critical Notes for Agents

1. **Python Version Mismatch**: Local uses 3.13 (`.python-version`), but Docker uses 3.11 (Dockerfile). Align before deployment.
2. **Empty Modules**: `auth/` and `dbstruct/` are placeholders - design these as core features develop.
3. **Service Communication**: When adding features, remember Docker Compose service names differ from localhost URLs.
4. **No Tests Yet**: No test framework configured - establish testing conventions early if adding test files.

## File Reference
- `pyproject.toml`: Dependency and project metadata
- `docker-compose.yaml`: Full stack orchestration with all service configs
- `Dockerfile`: Container image for backend service
- `.python-version`: Local development Python version (3.13)
