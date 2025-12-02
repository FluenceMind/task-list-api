from flask import Blueprint, request, make_response
from app import db
from app.models.task import Task
from app.routes.route_utilities import validate_model, create_model, update_model
import os
import requests

bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

SLACK_API_URL = "https://slack.com/api/chat.postMessage"
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "task-notifications")


def send_task_completed_notification(task):
    if not SLACK_BOT_TOKEN:
        return

    message = f"Someone just completed the task: {task.title}"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    data = {
        "channel": SLACK_CHANNEL,
        "text": message,
    }
    requests.post(SLACK_API_URL, data=data, headers=headers)


@bp.post("")
def create_task():
    request_body = request.get_json() or {}
    response_body, status_code = create_model(Task, request_body)
    return response_body, status_code


@bp.get("")
def get_all_tasks():
    sort_query = request.args.get("sort")

    tasks_stmt = db.select(Task)

    if sort_query == "asc":
        tasks_stmt = tasks_stmt.order_by(Task.title.asc())
    elif sort_query == "desc":
        tasks_stmt = tasks_stmt.order_by(Task.title.desc())

    tasks = db.session.scalars(tasks_stmt).all()
    response = [task.to_dict() for task in tasks]
    return response, 200


@bp.get("/<task_id>")
def get_task(task_id):
    task = validate_model(Task, task_id)
    return task.to_dict(), 200


@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json() or {}

    title = request_body.get("title")
    description = request_body.get("description")

    if not title or not description:
        return make_response({"details": "Invalid data"}, 400)

    return update_model(task, {"title": title, "description": description})


@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response("", 204)


@bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = task.completed_at or db.func.now()
    db.session.commit()
    send_task_completed_notification(task)
    return make_response("", 204)


@bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    return make_response("", 204)