from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.database import Base
from task.models import Task


class TaskList(Base):
    __tablename__ = "task_lists"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    active_date = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="lists")
    tasks = relationship("Task", backref="list")
