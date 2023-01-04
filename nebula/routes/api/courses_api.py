from flask import Blueprint, jsonify, request
from flask_login import current_user

from nebula import csrf, db
from nebula.models.course import Course
from nebula.models.course_level import CourseLevel
from nebula.routes.api import bp as api_bp

bp = Blueprint("course_api", __name__, url_prefix="/courses")

api_bp.register_blueprint(bp)


@bp.route("/", methods=["GET"])
def get_courses():
    courses = Course.query.all()
    return jsonify([course.expose() for course in courses])


@bp.route("/<uuid>", methods=["GET"])
def get_course(uuid):
    course = Course.query.filter_by(uuid=uuid).one_or_none()
    if course is None:
        return jsonify({"message": "course not found"}), 404

    return jsonify(course.expose())


@bp.route("/<uuid>", methods=["PUT"])
def update_course(uuid):
    if not current_user.is_authenticated or not current_user.access_level >= 3:
        return jsonify({"message": "Unauthorized"}), 401

    course = Course.query.filter_by(uuid=uuid).one_or_none()
    if course is None:
        return jsonify({"message": "Course not found"}), 404

    data = request.get_json(silent=True)

    name = data.get("name")
    if name is not None:
        course.name = name

    code = data.get("code")
    if code is not None:
        course.code = code

    description = data.get("description")
    if description is not None:
        course.description = description

    course_level_id = (
        data.get("course_level").get("id")
        if data.get("course_level") is not None
        else None
    )
    if course_level_id is not None:
        if CourseLevel.query.filter_by(uuid=course_level_id).one_or_none() is None:
            return jsonify({"message": "Course level does not exist"}), 400
        course.course_level_uuid = course_level_id

    semester = data.get("semester")
    if semester is not None:
        if not semester in ["1", "1a", "1b", "2", "2a", "2b"]:
            return jsonify({"message": "Semester must be 1, 1a, 1b, 2, 2a or 2b"}), 400
        course.semester = semester

    db.session.commit()

    course = Course.query.filter_by(uuid=uuid).one_or_none()

    return jsonify(course.expose())


@bp.route("/", methods=["POST"])
def create_course():
    if not current_user.is_authenticated or not current_user.access_level >= 3:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()

    name = data.get("name")
    code = data.get("code")
    description = data.get("description")
    course_level_id = (
        data.get("course_level").get("id")
        if data.get("course_level") is not None
        else None
    )
    semester = data.get("semester")

    if not name or not code or not course_level_id or not semester:
        return jsonify({"message": "Missing required fields"}), 400

    if Course.query.filter_by(code=code).one_or_none() is not None:
        return jsonify({"message": "Course code already exists"}), 400

    if not semester in ["1", "1a", "1b", "2", "2a", "2b"]:
        return jsonify({"message": "Semester must be 1, 1a, 1b, 2, 2a or 2b"}), 400

    if CourseLevel.query.filter_by(uuid=course_level_id).one_or_none() is None:
        return jsonify({"message": "Course level does not exist"}), 400

    course = Course(
        name=name,
        code=code,
        description=description,
        course_level_uuid=course_level_id,
        semester=semester,
    )
    db.session.add(course)
    db.session.commit()

    return jsonify(course.expose()), 201


@bp.route("/<uuid>", methods=["DELETE"])
@csrf.exempt
def delete_course(uuid):
    if not current_user.is_authenticated or not current_user.access_level >= 3:
        return jsonify({"message": "Unauthorized"}), 401

    course = Course.query.filter_by(uuid=uuid).one_or_none()
    if course is None:
        return jsonify({"message": "Course not found"}), 404

    data = course.expose()
    db.session.delete(course)
    db.session.commit()

    return jsonify(data), 200