from functools import wraps
from flask import request, jsonify
from jsonschema import validate


def json_validator(schema):
    """
      Decorator to validate JSON request data against a given schema.

      Args:
          schema (dict): The JSON schema to validate against.

      Returns:
          function: The decorated function with JSON validation.

      Raises:
          Exception: If the JSON data does not conform to the schema.
      """
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
