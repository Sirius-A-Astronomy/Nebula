from flask import flash, redirect, request, url_for, jsonify


def unauthorized_handler():
    if (
        request.path.startswith("/api/")
        or request.headers.get("content-type") == "application/json"
    ):
        return jsonify({"message" : "Unauthorized"}), 401
    """Redirects to the login page if the user is not logged in."""
    flash("Please log in to access this page.", "warning")
    return redirect(url_for("web.user.login_register", next=request.full_path))