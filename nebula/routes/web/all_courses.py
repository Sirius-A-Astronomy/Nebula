from flask import Blueprint, render_template

from nebula.models import Course, CourseLevel
from nebula.routes.web import bp as web_bp

bp = Blueprint("courses", __name__)

web_bp.register_blueprint(bp)


@bp.route("/courses")
def all_courses():
    course_levels = CourseLevel.query.all()
    courses = [
        Course.query.filter_by(course_level_uuid=course_level.uuid).all()
        for course_level in course_levels
    ]
    return render_template(
        "main/all_courses.html", course_levels=course_levels, courses=courses
    )
