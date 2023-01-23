from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from nebula.routes.api import bp


@login_required
@bp.route("/me", methods=["GET"])
def me():
    if current_user.is_anonymous:
        return jsonify(None), 401

    user = current_user

    return jsonify(user.expose()), 200


@bp.route("/logout", methods=["POST"])
def logout():
    from flask_login import logout_user

    logout_user()

    return jsonify({"message": "Successfully logged out."}), 200


@bp.route("/login", methods=["POST"])
def login():
    from flask_login import login_user

    from nebula.models.user import User

    username = request.json.get("username")
    password = request.json.get("password")

    user = User.query.filter_by(username=username).first()

    if user is None or not user.check_password(password):
        return jsonify({"message": "Invalid username or password."}), 401

    login_user(user)

    return jsonify({"message": "Successfully logged in.", "user": user.expose()}), 200
