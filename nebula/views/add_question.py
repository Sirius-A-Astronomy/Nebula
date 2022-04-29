from flask import Blueprint, render_template, request
from wtforms import Form, StringField, SubmitField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Optional
from flask_jwt_extended import jwt_required

from nebula import db, jwt
from nebula.models import Course, Question, User

bp = Blueprint("add_question", __name__)


class QuestionForm(Form):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Question", validators=[DataRequired()])
    answer = TextAreaField("Answer (optional)", validators=[Optional()])
    course = SelectField("Course", coerce=int)
    difficulty = SelectField("Difficulty", coerce=int, choices=[
                             (1, "Easy"), (2, "Medium"), (3, "Hard")], validators=[DataRequired()])
    course_code = HiddenField("Course Code")
    submit = SubmitField("Submit")


@bp.route("/add_question", methods=['GET', 'POST'])
# @jwt_required()
def add_question(success=False, course_code=None):
    question_form = QuestionForm(request.form)
    question_form.course.choices = [
        (course.id, course.name) for course in Course.query.all()]
    course_code = request.args.get('course_code')
    if(course_code is not None):
        course = Course.query.filter_by(code=course_code).first()
        course_id = course.id
        question_form.course.default = course_id
        question_form.process()
    else:
        course = None

    # for now we'll hardcode the user as there is no login system
    user = User.query.filter_by(username="sipma").first()
    if request.method == 'POST' and question_form.validate():
        title = question_form.title.data
        content = question_form.content.data
        answer = question_form.answer.data
        if answer is None or answer == "":
            answer = "No answer provided yet."
        course_id = question_form.course.data
        difficulty = question_form.difficulty.data
        difficulty = "Easy" if difficulty == 1 else "Medium" if difficulty == 2 else "Hard"
        course = Course.query.filter_by(id=course_id).first()

        question = Question(title=title, content=content, answer=answer, user=user, course=course,
                            difficulty=difficulty, approved=False)
        user.questions.append(question)
        # Pass along the course code to the succes page to have back navigation
        if course.code == question_form.course_code.data:
            course_code = question_form.course_code.data
        else:
            course_code = None
        db.session.add(question)
        db.session.commit()

        return render_template("main/add_question_succes.html", question=question, course=course, course_code=course_code)
    return render_template("main/add_question.html", question_form=question_form, success=success, course=course, course_code=course_code)
