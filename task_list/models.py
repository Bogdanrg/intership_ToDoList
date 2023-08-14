import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.database import Base
from task.models import Task  # noqa: F401


class TaskList(Base):
    __tablename__ = "task_lists"

    id = Column(Integer, primary_key=True)
    name = Column(String, default="ToDo list")
    active_date = Column(DateTime, default=datetime.datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="lists")
    tasks = relationship("Task", backref="list")
