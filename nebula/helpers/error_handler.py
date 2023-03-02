import json

from flask import flash, jsonify, redirect, request, url_for
from sqlalchemy.exc import StatementError
from werkzeug.exceptions import HTTPException


def csrf_error_handler(e):
    if (
        request.path.startswith("/api/")
        or request.headers.get("content-type") == "application/json"
    ):
        return jsonify({"message": "CSRF error"}), 419
    """Redirects to the login page if the user is not logged in."""
    flash("Session expired. Please try again.", "warning")
    return redirect(request.referrer if request.referrer else url_for("nebula.web.main.index"))


def generic_error_handler(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    if isinstance(e, HTTPException):
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps(
            {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }
        )
        response.content_type = "application/json"
        return response

    # hacky way to check if the error is a badly formed UUID string
    # This way we don't have to error handle every single route
    if isinstance(e, StatementError) and "badly formed hexadecimal UUID string" in str(
        e
    ):
        return jsonify({"message": "Given id is not a valid UUID string"}), 400

    return jsonify({"message": f"Internal server error: {str(e)}"}), 500
