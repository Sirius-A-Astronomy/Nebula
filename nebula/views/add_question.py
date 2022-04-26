from flask import Blueprint, render_template, request
from nebula.models import Course, CourseLevel, Question, User
from nebula import db
from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from datetime import datetime

bp = Blueprint("add_question", __name__)


class QuestionForm(Form):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Question", validators=[DataRequired()])
    answer = TextAreaField("Answer", validators=[DataRequired()])
    course = SelectField("Course", coerce=int)
    difficulty = SelectField("Difficulty", coerce=int, choices=[
                             (1, "Easy"), (2, "Medium"), (3, "Hard")], validators=[DataRequired()])
    submit = SubmitField("Submit")


@bp.route("/add_question", methods=['GET', 'POST'])
def add_question():
    question_form = QuestionForm(request.form)
    question_form.course.choices = [
        (course.id, course.name) for course in Course.query.all()]

    # for now we'll hardcode the user
    user = User.query.filter_by(username="sipma").first()
    if request.method == 'POST' and question_form.validate():
        title = question_form.title.data
        content = question_form.content.data
        answer = question_form.answer.data
        course_id = question_form.course.data
        difficulty = question_form.difficulty.data
        difficulty = "Easy" if difficulty == 1 else "Medium" if difficulty == 2 else "Hard"
        course = Course.query.filter_by(id=course_id).first()

        question = Question(title=title, content=content, answer=answer, user=user, course=course,
                            difficulty=difficulty, creation_datetime=datetime.now())
        user.questions.append(question)
        print(db)
        print(question)
        db.session.add(question)
        db.session.commit()
    return render_template("main/add_question.html", question_form=question_form)
