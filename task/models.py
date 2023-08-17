from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils.types import ChoiceType

from core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    TASK_STATUSES = (("done", "done"), ("in-progress", "in-progress"))

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    content: Mapped[str]
    status: Mapped[str] = mapped_column(
        ChoiceType(choices=TASK_STATUSES), default="in-progress"
    )
    list_id: Mapped[int] = mapped_column(ForeignKey("task_lists.id"))
