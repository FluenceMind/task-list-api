from flask import abort, make_response


def validate_model(model_cls, model_id):
    try:
        model_id_int = int(model_id)
    except ValueError:
        name = model_cls.__name__
        abort(make_response({"message": f"{name} {model_id} invalid"}, 400))

    model = model_cls.query.get(model_id_int)

    if model is None:
        name = model_cls.__name__

        if name == "Task":
            body = {"details": f"{name} {model_id_int} not found"}
        else:
            body = {"message": f"{name} {model_id_int} not found"}

        abort(make_response(body, 404))

    return model


def create_from_dict_or_400(model_cls, data: dict):
    try:
        model = model_cls.from_dict(data)
    except (KeyError, TypeError):
        abort(make_response({"details": "Invalid data"}, 400))

    return model