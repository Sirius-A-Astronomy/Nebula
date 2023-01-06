from flask import Blueprint, jsonify
from flask_login import current_user, login_required

from nebula.routes.api import bp


@login_required
@bp.route("/me", methods=["GET"])
def me():
    if current_user.is_anonymous:
        return jsonify(None), 401

    user = current_user

    return jsonify(user.expose()), 200
