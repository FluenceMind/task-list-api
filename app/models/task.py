from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db


class Task(db.Model):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(db.String, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(db.DateTime, nullable=True)

    goal_id: Mapped[Optional[int]] = mapped_column(
        db.Integer,
        db.ForeignKey("goal.id"),
        nullable=True,
    )
    goal: Mapped["Goal"] = relationship(back_populates="tasks")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at),
            **({"goal_id": self.goal_id} if self.goal_id is not None else {})
        }

    @classmethod
    def from_dict(cls, data):
        if "title" not in data:
            raise KeyError("title")
        if "description" not in data:
            raise KeyError("description")

        return cls(
            title=data["title"],
            description=data["description"],
        )