import json

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional

from nebula import db
from nebula.models.answer import Answer
from nebula.models.course import Course
from nebula.models.question import Question
from nebula.models.subject_tag import SubjectTag
from nebula.routes.web import bp as web_bp

bp = Blueprint("add_question", __name__)


class QuestionForm(FlaskForm):
    """Form for adding a new question."""

    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Question", validators=[DataRequired()])
    answers = HiddenField("Answers", validators=[Optional()])
    course = SelectField("Course", coerce=int)
    subject_tags = HiddenField("Subject Tags (optional)", validators=[Optional()])
    difficulty = SelectField(
        "Difficulty",
        coerce=int,
        choices=[(1, "Easy"), (2, "Medium"), (3, "Hard")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit")


@bp.route("/add_question", methods=["GET", "POST"])
def add_question(success=False, course_code=None):

    # Only admins or moderators can add questions
    if not current_user.is_authenticated or current_user.access_level < 2:
        flash("Only KLC or Cosmic Web members can create questions.", "warning")
        return redirect(url_for("web.main.index"))

    # Add courses to the form
    question_form = QuestionForm(request.form)
    question_form.course.choices = [
        (course.id, course.name) for course in Course.query.all()
    ]
    course_code = request.args.get("course_code")

    # Set the default course if a course code is provided
    if course_code:
        course = Course.query.filter_by(code=course_code).first()
        course_id = course.id
        question_form.course.default = course_id
        # pylint thinks question_form.process() is not defined,
        #  but it is, 2 inheritence levels deep QuestionForm > Form > BaseForm
        # pylint: disable=E1101
        question_form.process()
    else:
        course = None

    # If this is not a POST request, show the page
    if request.method != "POST":
        return render_template(
            "main/add_question.html",
            question_form=question_form,
            success=success,
            course=course,
            course_code=course_code,
        )

    # POST

    if not question_form.validate():
        return render_template(
            "main/add_question.html",
            question_form=question_form,
            success=success,
            course=course,
            course_code=course_code,
        )
    title = question_form.title.data.strip()

    # replace $$ with $ for LaTeX equations to only have inline equations in the title
    block_equations = [i for i in range(len(title)) if title.startswith("$$", i)]
    if len(block_equations) > 0:
        cleaned_title = ""
        for i, index in enumerate(block_equations):
            if i == 0:
                cleaned_title += title[:index]
            if i % 2 == 0:
                try:
                    cleaned_title += (
                        r"$" + title[index + 2 : block_equations[i + 1]] + r"$"
                    )
                except IndexError:
                    # if there is not another $$, just add the rest of the string
                    cleaned_title += title[index + 2 :]
            else:
                try:
                    cleaned_title += title[index + 2 : block_equations[i + 1]]
                except IndexError:
                    # if there is not another $$, just add the rest of the string
                    cleaned_title += title[index + 2 :]
        title = cleaned_title

    subject_tags = []
    if question_form.subject_tags.data != "":
        for tag in json.loads(question_form.subject_tags.data):
            tag = tag.strip()
            if not tag:
                continue
            if (
                SubjectTag.query.filter(SubjectTag.name.ilike(tag)).one_or_none()
                is None
            ):
                subject_tags.append(SubjectTag(name=tag))
                print("Added not existing tag: " + tag)
                continue
            subject_tags.append(
                SubjectTag.query.filter(SubjectTag.name.ilike(tag)).one()
            )

    content = question_form.content.data.strip()
    course_id = question_form.course.data
    difficulty = question_form.difficulty.data
    difficulty = "Easy" if difficulty == 1 else "Medium" if difficulty == 2 else "Hard"
    user = current_user
    course = Course.query.filter_by(id=course_id).first()
    question = Question(
        title=title,
        content=content,
        user=user,
        course=course,
        difficulty=difficulty,
        subject_tags=subject_tags,
    )
    if question_form.answers.data:
        for answer in json.loads(question_form.answers.data):
            if not answer:
                continue
            content = answer["content"].strip()
            title = answer["title"].strip()
            question.answers.append(
                Answer(
                    content=content, title=title, user=current_user, question=question
                )
            )

    db.session.add(question)

    db.session.commit()

    flash("Your question has been added!", "success")
    return render_template(
        "main/add_question_succes.html",
        question=question,
        course=course,
        course_code=course_code,
    )
