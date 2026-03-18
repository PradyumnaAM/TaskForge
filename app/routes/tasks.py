from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_models import Task
from app.models import TaskCreate, TaskResponse
from typing import List
from app.utils.dependencies import get_current_user
from app.db_models import User



router = APIRouter()


@router.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_task = Task(
        title=task.title,
        description=task.description,
        user_id = current_user.id
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task

@router.get("/tasks", response_model = List[TaskResponse])
def get_all_tasks(
    db: Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
    ):
    return db.query(Task).filter(Task.user_id == current_user.id).all()

@router.get("/tasks/{task_id}", response_model = TaskResponse)
def get_task(
    task_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()

    if not task:
        raise HTTPException(status_code = 404, detail = "Task not found")
    
    return task

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    updated_task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = updated_task.title
    task.description = updated_task.description

    db.commit()
    db.refresh(task)

    return task

@router.delete("/tasks/{task_id}", status_code = 204)
def delete_task(
    task_id : int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()

    if not task:
        raise HTTPException(status_code = 404, detail= "Task not found")
    
    db.delete(task)
    db.commit()

