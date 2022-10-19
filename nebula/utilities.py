from flask import redirect, url_for, request, flash


def unauthorized_handler():
    """Redirects to the login page if the user is not logged in."""
    flash("Please log in to access this page.", "warning")
    return redirect(url_for('user.login_register', next=request.full_path))
