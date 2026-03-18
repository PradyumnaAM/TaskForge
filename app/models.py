from pydantic import BaseModel

class TaskCreate(BaseModel):
    title : str
    description: str

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    model_config = {
        "from_attributes": True
    }

class UserLogin(BaseModel):
    username:str
    password:str