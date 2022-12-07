from flask import flash, redirect, request, url_for


def unauthorized_handler():
    """Redirects to the login page if the user is not logged in."""
    flash("Please log in to access this page.", "warning")
    return redirect(url_for("user.login_register", next=request.full_path))


ACCESS_LEVELS = [
    {"name": "Guest", "value": 0},
    {"name": "Student", "value": 1},
    {"name": "Moderator", "value": 2},
    {"name": "Admin", "value": 3},
    {"name": "Maintainer", "value": 4},
]
