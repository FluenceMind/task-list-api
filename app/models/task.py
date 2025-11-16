from app import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }

    def to_dict_with_goal(self):
        d = self.to_dict()
        d["goal_id"] = self.goal_id
        return d

    @classmethod
    def from_dict(cls, data):
        if "title" not in data:
            raise KeyError("title")
        if "description" not in data:
            raise KeyError("description")

        return cls(
            title=data["title"],
            description=data["description"]
        )