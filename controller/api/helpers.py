"""API Helpers"""

from functools import wraps
from os import environ
import jwt
from flask import request, jsonify
from db import users_tbl

SECRET_KEY = environ.get("secret_key", "secret")
undefined = object()


def _require_token():
    token = request.headers.get("Authorization")
    if not token:
        return undefined

    token = token.split(" ")[1]  # Remove "Bearer" prefix if present
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])


def token_required(func):
    """Certain action requires authenticated tokens"""

    def wrapper(*args, **kwargs):
        try:
            decoded_data = _require_token()
            if decoded_data is undefined:
                return jsonify({"status": "error", "message": "Token is missing"}), 401
            return func(decoded_data, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

    return wrapper


def is_admin(func):
    """Is user an admin?"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            decoded_data = _require_token()
            if decoded_data is undefined:
                return jsonify({"status": "error", "message": "Token is missing"}), 401
            if decoded_data["role"] != users_tbl.select_one(
                {"username": "user"}, only="role"
            ):
                return (
                    jsonify({"status": "error", "message": "Your role is not admin"}),
                    403,
                )
            return func(decoded_data, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired", "status": "error"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token", "status": "error"}), 401

    return wrapper
