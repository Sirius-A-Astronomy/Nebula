from flask import Blueprint, render_template
from nebula.models import Course, CourseLevel
bp = Blueprint('level', __name__, url_prefix='/course_levels')


@bp.route('/<course_level_code>')
@bp.route('/<course_level_code>/courses')
def level(course_level_code):
    course_level = CourseLevel.query.filter_by(code=course_level_code).first()
    course_level_uuid = course_level.uuid
    courses = Course.query.filter_by(course_level_uuid=course_level_uuid).all()
    return render_template('main/level.html', course_level=course_level, courses=courses)
