import os

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from nebula import db
from nebula.helpers.access_levels import ACCESS_LEVELS
from nebula.models.user import User, validate_email, validate_password
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


@bp.route("/validate/email", methods=["POST"])
def validate_email_route():
    data = request.get_json(silent=True)
    email = data.get("email")

    if email is None:
        return jsonify({"valid": False, "message": "Email is required"}), 200

    valid, message = validate_email(email)
    if not valid:
        return jsonify({"valid": False, "message": message}), 200

    return jsonify({"valid": True, "message": "Email is valid"}), 200


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
def create_user_route():
    data = request.get_json(silent=True)
    email = data.get("email")

    error_bin = {}
    if email is None:
        error_bin["email"] = "Email is required"

    if email:
        valid, message = validate_email(email)
        if not valid:
            error_bin["email"] = message

    first_name = data.get("first_name")
    if not first_name:
        error_bin["first_name"] = "First name is required"

    last_name = data.get("last_name")
    if not last_name:
        error_bin["last_name"] = "Last name is required"

    password = data.get("password")
    if not password:
        error_bin["password"] = "Password is required"

    if password:
        valid, message = validate_password(email)
        if not valid:
            error_bin["password"] = message

    password_confirmation = data.get("password_confirmation")
    if not password_confirmation:
        error_bin["password_confirmation"] = "Password confirmation is required"

    if password and password_confirmation and password != password_confirmation:
        error_bin["password"] = "Passwords do not match"

    access_level = data.get("access_level")
    if access_level is not None:
        if access_level not in ACCESS_LEVELS["ByLevel"].keys():
            return (
                jsonify(
                    {
                        "message": "Invalid access level",
                        "errors": {"access_level": "Invalid access level"},
                    }
                ),
                400,
            )

        if (
            current_user.is_authenticated
            and access_level >= current_user.access_level
            and current_user.access_level
            != ACCESS_LEVELS["ByName"]["maintainer"]["level"]
        ):
            return (
                jsonify(
                    {
                        "message": "You are not allowed to create a user with this access level",
                        "errors": {
                            "access_level": "You are not allowed to create a user with this access level"
                        },
                    }
                ),
                400,
            )
    if access_level is None:
        access_level = 0

    print(error_bin)

    if error_bin:
        return (
            jsonify(
                {
                    "message": "Some values were not entered correctly",
                    "errors": error_bin,
                }
            ),
            400,
        )

    user = User(
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
    if (
        str(current_user.uuid) != uuid
        and current_user.access_level < ACCESS_LEVELS["ByName"]["admin"]["level"]
    ):
        return jsonify({"message": "Unauthorized"}), 401

    user = User.query.filter_by(uuid=uuid).one_or_none()
    if user is None:
        return jsonify({"message": "User not found"}), 404

    if (
        user.access_level >= current_user.access_level
        and current_user.access_level != ACCESS_LEVELS["ByName"]["maintainer"]["level"]
        and current_user.uuid != user.uuid
    ):
        return jsonify({"message": "You are not allowed to update this user"}), 400

    data = request.get_json(silent=True)

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
            return (
                jsonify(
                    {
                        "message": "You cannot change the access_level to a level equal to or higher than your own"
                    }
                ),
                400,
            )

        if current_user.access_level <= user.access_level:
            return (
                jsonify(
                    {
                        "message": "You cannot change the access_level of a user equal to or higher than your own"
                    }
                ),
                400,
            )
        user.access_level = access_level

    db.session.commit()
    return jsonify(user.expose())


@bp.route("/<uuid>", methods=["DELETE"])
@login_required
def delete_user(uuid):
    if not current_user.access_level >= ACCESS_LEVELS["ByName"]["admin"]["level"]:
        return jsonify({"message": "Unauthorized"}), 401

    user = User.query.filter_by(uuid=uuid).one_or_none()
    if user is None:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted"}), 204
