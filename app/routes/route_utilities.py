from flask import abort, make_response, Response
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

    model = db.session.get(model_class, model_id_int)

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


def update_model(obj, data):
    for attr, value in data.items():
        if hasattr(obj, attr):
            setattr(obj, attr, value)

    db.session.commit()
    return Response(status=204)