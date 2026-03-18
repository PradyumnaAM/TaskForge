from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, nullable = False)
    description = Column(String, nullable = False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    owner = relationship("User", back_populates = "tasks")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String, unique = True, index = True)
    hashed_password = Column(String, nullable = False)

    tasks = relationship("Task", back_populates = "owner")
