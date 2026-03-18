# TaskForge API

A production-ready multi-user task management REST API built with FastAPI, SQLAlchemy, and JWT authentication.

## Features
- JWT authentication with bcrypt password hashing
- Per-user task isolation — users can only see their own tasks
- Full CRUD on tasks with status tracking (pending, in_progress, done)
- Pagination and status filtering on task listing
- Auto-generated interactive API docs at `/docs`
- Docker + Railway deployment ready

## Quick Start (Local)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment
cp .env.example .env
# Edit .env and set a strong SECRET_KEY

# 3. Run
uvicorn main:app --reload
```

Open http://localhost:8000/docs for the interactive API explorer.

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/users/` | No | Register a new user |
| POST | `/users/login` | No | Login, get JWT token |
| POST | `/tasks/` | Yes | Create a task |
| GET | `/tasks/` | Yes | List your tasks (paginated) |
| GET | `/tasks/{id}` | Yes | Get a single task |
| PUT | `/tasks/{id}` | Yes | Update a task |
| DELETE | `/tasks/{id}` | Yes | Delete a task |

## Deploy to Railway

1. Push to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Set environment variables in Railway Variables tab:
   ```
   SECRET_KEY = your-long-random-secret
   ```
4. Add a Volume at `/app/data` and set:
   ```
   DATABASE_URL = sqlite:////app/data/taskforge.db
   ```
5. Generate Domain in Settings → Networking
