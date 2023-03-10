from flask import Blueprint, render_template

from nebula.models.course import Course
from nebula.models.course_level import CourseLevel
from nebula.models.question import Question
from nebula.routes.web import bp as web_bp

# Does a course need to be a sublevel of courseLevel?
# level dependent blueprint:
bp = Blueprint("course", __name__, url_prefix="/q/<course_level_code>")


@bp.route("/<course_code>")
def course(course_code, course_level_code):
    course = Course.query.filter_by(code=course_code).first()
    course_level = CourseLevel.query.filter_by(code=course_level_code).first()
    questions = Question.query.filter_by(course_uuid=course.uuid).all()

    return render_template(
        "main/course.html",
        course=course,
        course_level=course_level,
        questions=questions,
    )
