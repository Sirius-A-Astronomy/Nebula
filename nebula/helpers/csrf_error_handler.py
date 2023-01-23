from flask import flash, jsonify, redirect, request, url_for


def csrf_error_handler(e):
    if (
        request.path.startswith("/api/")
        or request.headers.get("content-type") == "application/json"
    ):
        return jsonify({"message": "CSRF error"}), 419
    """Redirects to the login page if the user is not logged in."""
    flash("Session expired. Please try again.", "warning")
    return redirect(request.referrer if request.referrer else url_for("web.main.index"))
