from flask import abort, make_response
from app import db


def validate_model(model_class, model_id):
    model_name = model_class.__name__
    error_key = "details" if model_name == "Task" else "message"

    try:
        model_id_int = int(model_id)
    except ValueError:
        abort(make_response(
            {error_key: f"{model_name} {model_id} invalid"},
            400,
        ))

    model = model_class.query.get(model_id_int)

    if model is None:
        abort(make_response(
            {error_key: f"{model_name} {model_id_int} not found"},
            404,
        ))

    return model


def create_model(model_class, request_body):
    try:
        new_model = model_class.from_dict(request_body)
    except KeyError:
        abort(make_response(
            {"details": "Invalid data"},
            400,
        ))

    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201