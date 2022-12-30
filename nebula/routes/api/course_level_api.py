from flask import Blueprint, jsonify

from nebula.models.course_level import CourseLevel
from nebula.routes.api import bp as api_bp

bp = Blueprint("course_level_api", __name__, url_prefix="/course_levels")

api_bp.register_blueprint(bp)


@bp.route("/", methods=["GET"])
def get_course_levels():
    course_levels = CourseLevel.query.all()
    return jsonify(
        [
            {
                "id": course_level.uuid,
                "name": course_level.name,
                "code": course_level.code,
                "study_type": course_level.study_type,
            }
            for course_level in course_levels
        ]
    )
