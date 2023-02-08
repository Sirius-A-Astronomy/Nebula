from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from nebula import db
from nebula.models.user import User
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

    user = User.query.filter_by(uuid=current_user.uuid).one_or_none()

    logout_user()

    if user.is_authenticated:
        user.is_authenticated = False
        db.session.commit()

    return jsonify({"message": "Successfully logged out."}), 200


@bp.route("/login", methods=["POST"])
def login():
    from flask_login import login_user

    from nebula.models.user import User

    email = request.json.get("email")
    password = request.json.get("password")

    user = User.query.filter_by(email=email).first()

    if user is None or not user.check_password(password):
        return jsonify({"message": "Invalid email or password."}), 401

    user.is_authenticated = login_user(user)
    db.session.commit()

    return jsonify({"message": "Successfully logged in.", "user": user.expose()}), 200
