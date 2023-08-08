from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship
from task_list.models import TaskList

from core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=False)
    lists = relationship("TaskList", back_populates="user")

    def __repr__(self) -> str:
        return f"User: [{self.id}, {self.username}]"
