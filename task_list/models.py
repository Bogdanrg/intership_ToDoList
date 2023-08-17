import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from task.models import Task  # noqa: F401


class TaskList(Base):
    __tablename__ = "task_lists"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(default="ToDo list")
    active_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="lists")
    tasks: Mapped[List["Task"]] = relationship(backref="list")
