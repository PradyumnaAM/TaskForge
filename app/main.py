from fastapi import FastAPI
from app.routes.tasks import router as task_router
from app.database import engine
from app.db_models import Base
from app.routes.users import router as user_router

app = FastAPI(title = "TaskForge API")

Base.metadata.create_all(bind=engine)


app.include_router(task_router)
app.include_router(user_router)

@app.get("/")
def home():
    return{"message": "TaskForge is running successfully"}

