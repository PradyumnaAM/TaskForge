from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List
from app.db_models import User
from app.models import UserCreate, UserResponse
from app.utils.security import hash_password
from app.utils.security import verify_password
from app.models import UserLogin    
from app.utils.security import create_access_token

router = APIRouter(prefix = "/users",tags = ["Users"])


@router.post("/", response_model = UserResponse, status_code = 201)
def create_user(
        user: UserCreate,
        db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code = 400, detail = "Username already exists")

    db_user = User(
        username = user.username,
        hashed_password = hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.get("/",response_model = List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/login")
def login_user(
    credentials : UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == credentials.username).first()

    if not user:
        raise HTTPException(status_code = 401, detail = "Invalid Credentials")
    
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code = 401, detail = "Invalid Credentials")
    
    access_token = create_access_token(data = {"sub" : user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

