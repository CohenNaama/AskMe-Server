from functools import wraps
from flask import request, jsonify
from jsonschema import validate


def json_validator(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                validate(request.json, schema)
            except Exception as e:
                return jsonify({"message": "Error: Invalid JSON data", "details": str(e)}), 400
            return func(*args, **kwargs)
        return wrapper
    return decorator
