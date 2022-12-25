from flask import flash, redirect, request, url_for


def unauthorized_handler():
    if (request.path.startswith("/api/") or request.headers.get("content-type") == "application/json"):
        return "Unauthorized", 401
    """Redirects to the login page if the user is not logged in."""
    flash("Please log in to access this page.", "warning")
    return redirect(url_for("user.login_register", next=request.full_path))


ACCESS_LEVELS_PROTO = {
    "guest": {"level": 0, "name": "Guest"},
    "student": {"level": 1, "name": "Student"},
    "moderator": {"level": 2, "name": "Moderator"},
    "admin": {"level": 3, "name": "Admin"},
    "maintainer": {"level": 4, "name": "Maintainer"},
}

ACCESS_LEVELS = {
    "ByLevel": {},
    "ByName": {},
}

for access_level in ACCESS_LEVELS_PROTO.values():
    ACCESS_LEVELS["ByLevel"][access_level["level"]] = access_level
    ACCESS_LEVELS["ByName"][access_level["name"].lower()] = access_level
