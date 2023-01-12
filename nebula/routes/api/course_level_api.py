from flask import Blueprint, jsonify, request
from flask_login import current_user

from nebula import db
from nebula.models.course_level import CourseLevel
from nebula.routes.api import bp as api_bp

bp = Blueprint("course_level_api", __name__, url_prefix="/course_levels")

api_bp.register_blueprint(bp)


@bp.route("/", methods=["GET"])
def get_course_levels():
    course_levels = CourseLevel.query.all()
    return jsonify(
        [
            course_level.expose() for course_level in course_levels
        ]
    )

@bp.route("/<uuid>", methods=["GET"])
def get_course_level(uuid):
    course_level = CourseLevel.query.filter_by(uuid=uuid).one_or_none()
    if course_level is None:
        return jsonify({"message": "course level not found"}), 404

    return jsonify(course_level.expose())

@bp.route("/<uuid>", methods=["PUT"])
def update_course_level(uuid):
    if not current_user.is_authenticated or not current_user.access_level >= 3:
        return jsonify({"message": "unauthorized"}), 401

    course_level = CourseLevel.query.filter_by(uuid=uuid).one_or_none()
    if course_level is None:
        return jsonify({"message": "Course level not found"}), 404

    data = request.get_json(silent=True)

    name = data.get("name")
    if name is not None:
        course_level.name = name

    code = data.get("code")
    if code is not None:
        course_level.code = code

    study_type = data.get("study_type")
    if study_type is not None:
        course_level.study_type = study_type

    db.session.commit()
    return jsonify(course_level.expose())

@bp.route("/", methods=["POST"])
def create_course_level():
    if not current_user.is_authenticated or not current_user.access_level >= 3:
        return jsonify({"message": "unauthorized"}), 401

    data = request.get_json(silent=True)

    name = data.get("name")
    if name is None:
        return jsonify({"message": "name is required"}), 400

    code = data.get("code")
    if code is None:
        return jsonify({"message": "code is required"}), 400

    study_type = data.get("study_type")
    if study_type is None:
        return jsonify({"message": "study_type is required"}), 400

    course_level = CourseLevel(name=name, code=code, study_type=study_type)
    db.session.add(course_level)
    db.session.commit()
    return jsonify(course_level.expose())

@bp.route("/<uuid>", methods=["DELETE"])
def delete_course_level(uuid):
    return jsonify(
        {"message": "not implemented"}
    )