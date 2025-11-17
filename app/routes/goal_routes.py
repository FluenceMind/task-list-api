from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.goal import Goal
from app.models.task import Task
from app.routes.route_utilities import validate_model, create_model

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")


@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json() or {}
    title = request_body.get("title")
    if not title:
        return make_response({"details": "Invalid data"}, 400)

    new_goal = Goal(title=title)
    db.session.add(new_goal)
    db.session.commit()

    return jsonify(new_goal.to_dict()), 201


@goal_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    response = [goal.to_dict() for goal in goals]
    return jsonify(response), 200


@goal_bp.route("/<goal_id>", methods=["GET"])
def read_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return jsonify(goal.to_dict()), 200


@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json() or {}
    title = request_body.get("title")
    if not title:
        return make_response({"details": "Invalid data"}, 400)

    goal.title = title
    db.session.commit()

    return "", 204


@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return "", 204


@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def assign_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json() or {}
    task_ids = request_body.get("task_ids")
    if not isinstance(task_ids, list):
        return make_response({"details": "Invalid data"}, 400)

    for task in goal.tasks:
        task.goal_id = None

    validated_ids = []
    for tid in task_ids:
        task = validate_model(Task, tid)
        task.goal_id = goal.id
        validated_ids.append(task.id)

    db.session.commit()

    return jsonify({"id": goal.id, "task_ids": validated_ids}), 200


@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    tasks_payload = [t.to_dict_with_goal() for t in goal.tasks]
    return jsonify({
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_payload
    }), 200