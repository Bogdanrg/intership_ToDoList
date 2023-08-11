from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from core.database import Base
from task_list.models import TaskList  # noqa F401


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=False)
    lists = relationship("TaskList", back_populates="user")

    def __repr__(self) -> str:
        return f"User: [{self.id}, {self.username}]"
