from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.db_models import Base
from app.routes.tasks import router as task_router
from app.routes.users import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="TaskForge API",
    description="A secure multi-user task management REST API with JWT authentication.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(task_router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "TaskForge API is running"}
