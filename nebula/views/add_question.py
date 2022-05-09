from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
import re

from wtforms import Form, StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Optional

from nebula import db
from nebula.models import Course, Question, Answer

bp = Blueprint("add_question", __name__)


class QuestionForm(Form):
    """Form for adding a new question."""
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Question", validators=[DataRequired()])
    answer = TextAreaField("Answer (optional)", validators=[Optional()])
    course = SelectField("Course", coerce=int)
    difficulty = SelectField("Difficulty", coerce=int, choices=[
                             (1, "Easy"), (2, "Medium"), (3, "Hard")], validators=[DataRequired()])
    submit = SubmitField("Submit")


@bp.route("/add_question", methods=['GET', 'POST'])
@login_required
def add_question(success=False, course_code=None):
    question_form = QuestionForm(request.form)
    question_form.course.choices = [
        (course.id, course.name) for course in Course.query.all()]
    course_code = request.args.get('course_code')
    if course_code is not None:
        course = Course.query.filter_by(code=course_code).first()
        course_id = course.id
        question_form.course.default = course_id
        # pylint thinks question_form.process() is not defined,
        #  but it is, 2 inheritence levels deep QuestionForm > Form > BaseForm
        # pylint: disable=E1101
        question_form.process()
    else:
        course = None

    if request.method == 'POST' and question_form.validate():
        title = question_form.title.data

        # replace $$ with \( and \) for LaTeX equations to only have inline equations in the title
        block_equations = [i for i in range(
            len(title)) if title.startswith('$$', i)]
        if len(block_equations) > 0:
            cleaned_title = ""
            for i, index in enumerate(block_equations):
                if i == 0:
                    cleaned_title += title[:index]
                if i % 2 == 0:
                    try:
                        cleaned_title += r"\(" + \
                            title[index + 2:block_equations[i + 1]] + r"\)"
                    except IndexError:
                        # if there is not another $$, just add the rest of the string
                        cleaned_title += title[index + 2:]
                else:
                    try:
                        cleaned_title += title[index +
                                               2:block_equations[i + 1]]
                    except IndexError:
                        # if there is not another $$, just add the rest of the string
                        cleaned_title += title[index + 2:]
            title = cleaned_title

        content = question_form.content.data
        answer = question_form.answer.data
        course_id = question_form.course.data
        difficulty = question_form.difficulty.data
        difficulty = "Easy" if difficulty == 1 else "Medium" if difficulty == 2 else "Hard"
        user = current_user
        course = Course.query.filter_by(id=course_id).first()

        question = Question(title=title, content=content, user=user, course=course,
                            difficulty=difficulty, approved=False)
        if answer is not None or answer != "":
            answer_obj = Answer(content=answer, user=user,
                                question=question, approved=False)
            db.session.add(answer_obj)
        db.session.add(question)

        db.session.commit()

        return render_template("main/add_question_succes.html",
                               question=question,
                               course=course,
                               course_code=course_code)
    return render_template("main/add_question.html",
                           question_form=question_form,
                           success=success,
                           course=course,
                           course_code=course_code)
