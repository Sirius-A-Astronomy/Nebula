from flask import Blueprint, jsonify, request

from nebula import csrf
from nebula.models import Course
from nebula.routes.api import bp as api_bp

bp = Blueprint("course_api", __name__, url_prefix="/courses")

api_bp.register_blueprint(bp)


@bp.route("/", methods=["GET"])
def get_courses():
    courses = Course.query.all()
    return jsonify(
        [
            {
                "id": course.uuid,
                "name": course.name,
                "code": course.code,
                "course_level": {
                    "id": course.course_level.uuid,
                    "name": course.course_level.name,
                    "code": course.course_level.code,
                    "study_type": course.course_level.study_type,
                },
                "description": course.description,
            }
            for course in courses
        ]
    )


@bp.route("/", methods=["POST"])
def create_course():
    data = request.get_json()
    return jsonify({"POST:": data})


@bp.route("/", methods=["PUT"])
@csrf.exempt
def update_course():
    data = request.get_json()
    return jsonify({"PUT:": data})


@bp.route("/", methods=["DELETE"])
@csrf.exempt
def delete_course():
    data = request.get_json()
    return jsonify({"DELETE:": data})


@bp.route("/ping", methods=["post", "GET"])
def ping():
    return jsonify({"message": "pong"})
