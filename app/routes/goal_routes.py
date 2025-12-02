from flask import Blueprint, request, make_response, Response
from app import db
from app.models.goal import Goal
from app.models.task import Task
from app.routes.route_utilities import validate_model, create_model, update_model

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")


@bp.post("")
def create_goal():
    request_body = request.get_json() or {}
    response_body, status_code = create_model(Goal, request_body)
    return response_body, status_code


@bp.get("")
def get_goals():
    goals_stmt = db.select(Goal)
    goals = db.session.scalars(goals_stmt).all()
    response = [goal.to_dict() for goal in goals]
    return response, 200


@bp.get("/<goal_id>")
def read_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict(), 200


@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json() or {}
    title = request_body.get("title")
    if not title:
        return make_response({"details": "Invalid data"}, 400)

    return update_model(goal, {"title": title})


@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return Response(status=204)


@bp.post("/<goal_id>/tasks")
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

    return {"id": goal.id, "task_ids": validated_ids}, 200


@bp.get("/<goal_id>/tasks")
def get_tasks_of_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict(with_tasks=True), 200