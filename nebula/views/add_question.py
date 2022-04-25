from flask import Blueprint, render_template
from nebula.models import Course, CourseLevel, Question, User
from nebula import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from datetime import datetime

bp = Blueprint("add_question", __name__)


class QuestionForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Question", validators=[DataRequired()])
    answer = TextAreaField("Answer", validators=[DataRequired()])
    course = SelectField("Course", validators=[DataRequired()])
    difficulty = SelectField("Difficulty", coerce=int, choices=[
                             (1, "Easy"), (2, "Medium"), (3, "Hard")], validators=[DataRequired()])
    submit = SubmitField("Submit")


@bp.route("/add_question/", methods=["GET", "POST"])
def add_question():
    question_form = QuestionForm()
    question_form.course.choices = [
        (course.id, course.name) for course in Course.query.all()]

    # for now we'll hardcode the user
    user = User.query.filter_by(username="sipma").first()

    if question_form.validate_on_submit():
        title = question_form.title.data
        content = question_form.question.data
        answer = question_form.answer.data
        course_id = question_form.course.data
        difficulty = question_form.difficulty.data
        difficulty = "Easy" if difficulty == 1 else "Medium" if difficulty == 2 else "Hard"
        course = Course.query.filter_by(id=course_id).first()

        question = Question(question=question, answer=answer, user=user, course=course,
                            difficulty=difficulty, creation_datetime=datetime.now())
        # user.questions.append(question)
        db.session.add(question)
        db.session.commit()
        return render_template("add_question.html", question_form=question_form)
    return render_template("main/add_question.html", question_form=question_form)
