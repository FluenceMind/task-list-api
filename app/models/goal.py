from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db


class Goal(db.Model):
    __tablename__ = "goal"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String, nullable=False)
    tasks: Mapped[List["Task"]] = relationship(back_populates="goal")

    def to_dict(self, with_tasks: bool = False):
        goal_dict = {
            "id": self.id,
            "title": self.title,
        }

        if with_tasks:
            goal_dict["tasks"] = [task.to_dict() for task in self.tasks]

        return goal_dict

    @classmethod
    def from_dict(cls, data):
        title = data.get("title")
        if not title:
            raise KeyError("title is required")
        return cls(title=title)
