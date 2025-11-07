from datetime import datetime
from ..db import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None,
        }

    @classmethod
    def from_dict(cls, data):
        try:
            title = data["title"]
            description = data["description"]
        except KeyError as exc:
            raise KeyError(exc.args[0])

        return cls(
            title=title,
            description=description,
            completed_at=data.get("completed_at"),
        )