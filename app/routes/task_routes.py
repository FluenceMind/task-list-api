from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.task import Task
from app.routes.route_utilities import validate_model, create_model

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json() or {}

    response_body, status_code = create_model(Task, request_body)

    return response_body, status_code


@bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    response = [task.to_dict() for task in tasks]
    return jsonify(response), 200


@bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = validate_model(Task, task_id)
    task_dict = task.to_dict()

    if task.goal_id is not None:
        task_dict["goal_id"] = task.goal_id

    return task_dict, 200


@bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json() or {}

    title = request_body.get("title")
    description = request_body.get("description")

    if not title or not description:
        return make_response({"details": "Invalid data"}, 400)

    task.title = title
    task.description = description

    db.session.commit()

    return "", 204


@bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return "", 204


@bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = task.completed_at or db.func.now()
    db.session.commit()

    return "", 204


@bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()

    return "", 204