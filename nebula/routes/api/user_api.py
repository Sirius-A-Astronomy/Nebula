from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import os

from nebula.helpers.access_levels import ACCESS_LEVELS

from nebula import db

from nebula.models.user import User, validate_email, validate_username

from nebula.routes.api import bp as api_bp

bp = Blueprint("user_api", __name__, url_prefix="/users")

api_bp.register_blueprint(bp)

@bp.route("/", methods=["GET"])
@login_required
def get_users():
    if not current_user.access_level >= ACCESS_LEVELS["ByName"]["admin"]["level"]:
        return jsonify({"message": "Unauthorized"}), 401

    users = User.query.all()
    return jsonify([user.expose() for user in users])

@bp.route("/<uuid>", methods=["GET"])
@login_required
def get_user(uuid):
    if not current_user.access_level >= ACCESS_LEVELS["ByName"]["admin"]["level"]:
        return jsonify({"message": "Unauthorized"}), 401

    user = User.query.filter_by(uuid=uuid).one_or_none()
    if user is None:
        return jsonify({"message": "User not found"}), 404

    return jsonify(user.expose())

@bp.route("/", methods=["POST"])
@login_required
def create_user_route():
    if not current_user.access_level >= ACCESS_LEVELS["ByName"]["admin"]["level"]:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json(silent=True)

    username = data.get("username")
    if username is None:
        return jsonify({"message": "Username is required"}), 400

    email = data.get("email")
    if email is None:
        return jsonify({"message": "Email is required"}), 400

    first_name = data.get("first_name")
    if first_name is None:
        return jsonify({"message": "First name is required"}), 400

    last_name = data.get("last_name")
    if last_name is None:
        return jsonify({"message": "Last name is required"}), 400

    password = data.get("password")
    if password is None:
        return jsonify({"message": "Password is required"}), 400

    password_confirmation = data.get("password_confirmation")
    if password_confirmation is None:
        return jsonify({"message": "Password confirmation is required"}), 400

    if password != password_confirmation:
        return jsonify({"message": "Passwords do not match"}), 400

    access_level = data.get("access_level")
    if access_level is None:
        return jsonify({"message": "Access level is required"}), 400

    if access_level not in ACCESS_LEVELS["ByLevel"].keys():
        return jsonify({"message": "Invalid access level"}), 400

    if access_level >= current_user.access_level and current_user.access_level != ACCESS_LEVELS["ByName"]["maintainer"]["level"]:
        return jsonify({"message": "You are not allowed to create a user with this access level"}), 400

    user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        access_level=access_level,
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify(user.expose()), 201

@bp.route("/reset_password", methods=["POST"])
@login_required
def reset_password():
    if not current_user.access_level >= ACCESS_LEVELS["ByName"]["admin"]["level"]:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json(silent=True)

    uuid = data.get("uuid")
    if uuid is None:
        return jsonify({"message": "UUID is required"}), 400

    user = User.query.filter_by(uuid=uuid).one_or_none()
    if user is None:
        return jsonify({"message": "User not found"}), 404

    random_password = os.urandom(16).hex()

    user.set_password(random_password)

    db.session.commit()

    return jsonify({"password": random_password}), 200

@bp.route("/<uuid>", methods=["PUT"])
@login_required
def update_user(uuid):
    if current_user.uuid != uuid and not current_user.access_level >= ACCESS_LEVELS["ByName"]["admin"]["level"]:
        return jsonify({"message": "Unauthorized"}), 401


    user = User.query.filter_by(uuid=uuid).one_or_none()
    if user is None:
        return jsonify({"message": "User not found"}), 404

    if user.access_level >= current_user.access_level and current_user.access_level != ACCESS_LEVELS["ByName"]["maintainer"]["level"]:
        return jsonify({"message": "You are not allowed to update this user"}), 400

    data = request.get_json(silent=True)

    username = data.get("username")
    if username is not None and username != user.username:
        (valid, message) = validate_username(username, user=user)
        if not valid:
            return jsonify({"message": message}), 400
        user.username = username

    email = data.get("email")
    if email is not None:
        (valid, message) = validate_email(email, user=user)
        if not valid:
            return jsonify({"message": message}), 400
        user.email = email

    first_name = data.get("first_name")
    if first_name is not None and first_name != user.first_name:
        user.first_name = first_name

    last_name = data.get("last_name")
    if last_name is not None and last_name != user.last_name:
        user.last_name = last_name

    access_level = data.get("access_level")
    if access_level is not None and access_level != user.access_level:
        if access_level not in ACCESS_LEVELS["ByLevel"].keys():
            return jsonify({"message": "Invalid access level"}), 400

        if current_user.uuid == uuid:
            return jsonify({"message": "You cannot change your own access_level"}), 400

        if current_user.access_level <= access_level:
            return jsonify({"message": "You cannot change the access_level to a level equal to or higher than your own"}), 400

        if current_user.access_level <= user.access_level:
            return jsonify({"message": "You cannot change the access_level of a user equal to or higher than your own"}), 400
        user.access_level = access_level

    db.session.commit()
    return jsonify(user.expose())

@bp.route("/<uuid>", methods=["DELETE"])
def delete_user(uuid):
    if not current_user.access_level >= ACCESS_LEVELS["ByName"]["admin"]["level"]:
        return jsonify({"message": "Unauthorized"}), 401

    user = User.query.filter_by(uuid=uuid).one_or_none()
    if user is None:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted"}), 200