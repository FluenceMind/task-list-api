from flask import Blueprint, request, jsonify, Response
from .. import db
from ..models.task import Task
from .route_utils import validate_model, create_from_dict_or_400

bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@bp.post("")
def create_task():
    data = request.get_json() or {}
    task = create_from_dict_or_400(Task, data)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@bp.get("")
def get_tasks():
    sort_param = request.args.get("sort", default=None, type=str)
    
    if sort_param == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_param == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.order_by(Task.id).all()

    return jsonify([t.to_dict() for t in tasks]), 200


@bp.get("/<int:task_id>")
def get_task(task_id):
    task = validate_model(Task, task_id)
    return jsonify(task.to_dict()), 200


@bp.put("/<int:task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    data = request.get_json() or {}
    if "title" in data:
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"]
    db.session.commit()
    return Response(status=204, mimetype="application/json")


@bp.delete("/<int:task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return Response(status=204, mimetype="application/json")