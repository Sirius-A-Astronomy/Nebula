from flask import Blueprint, render_template, url_for, request
from nebula.models import Course, Question

bp = Blueprint('question', __name__, url_prefix='/course/<course_code>/question')

@bp.route('/<question_id>')
def question(course_code, question_id):
    question = Question.query.filter_by(id = question_id).first()
    course = Course.query.filter_by(code = course_code).first()
    return render_template('main/question.html', course = course, question = question)