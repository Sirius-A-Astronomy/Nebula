from flask import Blueprint, render_template, url_for, request
from sqlalchemy import and_
from nebula.models import Course, CourseLevel, Question


# Does a course need to be a sublevel of courseLevel?
# level dependent blueprint:
bp = Blueprint('course', __name__, url_prefix='/q/<course_level_code>')

# level independent blueprint
# bp = Blueprint('course', __name__, url_prefix='/courses')


@bp.route('/<course_code>')
def course(course_code, course_level_code):
    course = Course.query.filter_by(code=course_code).first()
    course_level = CourseLevel.query.filter_by(code=course_level_code).first()
    questions = Question.query.filter(
        and_(Question.reviewed == 1, Question.course_uuid == course.uuid)).all()

    return render_template('main/course.html', course=course, course_level=course_level, questions=questions)
