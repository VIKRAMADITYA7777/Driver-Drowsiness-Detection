# Backend

FastAPI backend foundation for the Intelligent Driver Drowsiness Detection system.

## Setup

Create a virtual environment and install dependencies:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
uvicorn main:app --reload
```

## Database setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python db_init.py
```

## Migrations

```powershell
cd backend
alembic upgrade head
```

## API

- `GET /health`
- `GET /api/health/status`
- `GET /api/monitoring/status`
- `POST /api/monitoring/alerts`

## Structure

- `main.py` — FastAPI entrypoint
- `app/config.py` — environment configuration
- `app/database.py` — SQLAlchemy engine and session
- `app/models.py` — ORM data models
- `app/schemas.py` — request/response schemas
- `app/crud.py` — basic database operations
- `app/routes/` — API route modules
- `app/logger.py` — structured logging
