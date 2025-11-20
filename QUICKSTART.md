# Flask Task Manager API - Quick Start Guide

## Installation

1. Install uv:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. Clone and setup:
```powershell
git clone <your-repo-url>
cd flask-task-manager-api
uv venv
.venv\Scripts\activate
uv pip install -e .
```

3. Configure environment:
```powershell
Copy-Item .env.example .env
```

4. Initialize database:
```powershell
uv run python init_db.py seed
```

5. Run the app:
```powershell
uv run python -m app.main
```

Visit: http://localhost:5000

## Quick Commands

- `uv run python -m app.main` - Run app
- `uv run pytest` - Run tests
- `uv run python init_db.py seed` - Reset database

## API Endpoints

- GET `/` - API info
- GET `/health` - Health check
- POST `/api/users` - Create user
- GET `/api/tasks` - Get tasks
- POST `/api/tasks` - Create task
- GET `/api/stats` - Statistics

See README.md for full documentation.
