from typing import List

from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.database import Base
from task_list.models import TaskList  # noqa F401


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=False)
    lists: Mapped[List["TaskList"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User: [{self.id}, {self.username}]"
