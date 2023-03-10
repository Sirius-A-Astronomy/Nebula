from flask import flash, jsonify, redirect, request, url_for


def unauthorized_handler():
    if (
        request.path.startswith("/api/")
        or request.headers.get("content-type") == "application/json"
    ):
        return jsonify({"message": "Unauthorized"}), 401
    """Redirects to the login page if the user is not logged in."""
    flash("Please log in to access this page.", "warning")
    return redirect("/login")
