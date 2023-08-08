from sqlalchemy import Column, Integer, String, ForeignKey, Text
from core.database import Base
from sqlalchemy_utils.types import ChoiceType


class Task(Base):
    __tablename__ = "tasks"

    TASK_STATUSES = (
        ('done', 'done'),
        ('in-progress', 'in-progress')
    )

    id = Column(Integer, primary_key=True)
    name = Column(String)
    content = Column(Text)
    status = Column(ChoiceType(choices=TASK_STATUSES), default="in-progress")
    list_id = Column(Integer, ForeignKey("task_lists.id"))
