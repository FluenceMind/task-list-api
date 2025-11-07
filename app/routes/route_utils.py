from flask import abort, jsonify, make_response
from .. import db


def validate_model(cls, model_id):
    instance = db.session.get(cls, model_id)
    if instance is None:
        abort(
            make_response(
                jsonify({"details": f"{cls.__name__} {model_id} not found"}), 404
            )
        )
    return instance


def create_from_dict_or_400(model_cls, data):
    try:
        return model_cls.from_dict(data)
    except Exception:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))