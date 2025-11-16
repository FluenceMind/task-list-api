from flask import Blueprint, jsonify, request, make_response
from app import db
from app.models.goal import Goal
from app.routes.route_utils import validate_model, create_from_dict_or_400


goal_bp = Blueprint("goals", __name__, url_prefix="/goals")


@goal_bp.route("", methods=["POST"])
def create_goal():
    data = request.get_json() or {}
    goal = create_from_dict_or_400(Goal, data)

    db.session.add(goal)
    db.session.commit()

    return jsonify(goal.to_dict()), 201


@goal_bp.route("", methods=["GET"])
def list_goals():
    goals = Goal.query.all()
    return jsonify([goal.to_dict() for goal in goals]), 200


@goal_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return jsonify(goal.to_dict()), 200


@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    data = request.get_json() or {}

    if "title" in data:
        goal.title = data["title"]

    db.session.commit()

    return make_response(jsonify(goal.to_dict()), 204)


@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify(goal.to_dict()), 204)
