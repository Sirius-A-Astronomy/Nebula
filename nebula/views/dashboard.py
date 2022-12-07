from datetime import datetime, timedelta
from re import A
from unicodedata import category

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import Form, HiddenField, SubmitField

from nebula import db
from nebula.models import (
    Answer,
    Comment,
    Course,
    CourseLevel,
    Notification,
    Question,
    User,
)
from nebula.utilities import ACCESS_LEVELS

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@bp.route("/")
def index():
    if current_user.is_anonymous or current_user.access_level < 2:
        flash(
            "You need to be a KLC or Cosmic Web Member to access this page.", "warning"
        )
        return redirect(url_for("main.index"))

    questions_for_review = Question.query.filter(Question.reviewed == 0).all()

    total_questions = Question.query.count()

    answers = len(Answer.query.all())
    answered_questions = len(Question.query.filter(Question.answers.any()).all())

    reviewed_questions = len(Question.query.filter(Question.reviewed != 0).all())
    approved_questions = len(Question.query.filter(Question.reviewed == 1).all())
    users = User.query.all()

    recent_user_count = len(
        [1 if (datetime.now() - user.created_at).days <= 30 else None for user in users]
    )

    return render_template(
        "dashboard/index.html",
        questions_for_review=questions_for_review,
        total_questions=total_questions,
        recent_user_count=recent_user_count,
        reviewed_questions=reviewed_questions,
        answers=answers,
        answered_questions=answered_questions,
        approved_questions=approved_questions,
    )


class QuestionReviewForm(FlaskForm):
    accept_submit_button = SubmitField("Accept")
    reject_submit_button = SubmitField("Reject")


@bp.route("/question/<question_uuid>", methods=["GET", "POST"])
def question(question_uuid):
    question_review_form = QuestionReviewForm(request.form)
    question = Question.query.filter_by(uuid=question_uuid).first()
    if not question:
        flash("Question not found.", "warning")
        return redirect(url_for("dashboard.index"))

    if request.method != "POST":
        return render_template(
            "dashboard/question.html",
            question=question,
            question_review_form=question_review_form,
        )

    # POST
    print(request.form)

    if current_user.is_anonymous or current_user.access_level < 2:
        flash(
            "You need to be a KLC or Cosmic Web Member to perform this action.",
            "warning",
        )
        return redirect(url_for("main.index"))

    if not question_review_form.validate():
        flash("Something went wrong with submitting your request.", "warning")
        flash(question_review_form.errors, "error")
        return redirect(url_for("dashboard.question", question_uuid=question_uuid))

    if question_review_form.accept_submit_button.data:
        question.reviewed = 1
        question.reviewed_by = current_user

        notification = Notification(
            content=f"Your question '{question.title}' has been approved and is now visible on the site.",
            user=question.user,
            category="success",
            link=url_for(
                "question.question",
                question_uuid=question_uuid,
                course_level_code=question.course.course_level.code,
                course_code=question.course.code,
            ),
            link_text="View Question",
        )
        db.session.commit()
        flash("Question accepted.", "success")
        return redirect(url_for("dashboard.index"))
    if question_review_form.reject_submit_button.data:
        question.reviewed = 2
        question.reviewed_by = current_user
        notification = Notification(
            content=f"Your question '{question.title}' has not been accepted will not be shown to other users.",
            category="info",
            user=question.user,
        )
        db.session.commit()
        flash("Question rejected.", "success")
        return redirect(url_for("dashboard.index"))


@bp.route("/users", methods=["GET"])
def users():
    if current_user.is_anonymous or current_user.access_level < 2:
        flash(
            "You need to be a KLC or Cosmic Web Member to access this page.", "warning"
        )
        return redirect(url_for("main.index"))

    users = User.query.all()

    return render_template(
        "dashboard/users.html", users=users, access_levels=ACCESS_LEVELS
    )


@bp.route("/user/<user_uuid>/access_level", methods=["POST"])
def user_access_level(user_uuid):
    if current_user.is_anonymous or current_user.access_level < 3:
        flash("You need to be a Cosmic Web Member to perform this action.", "warning")
        return redirect(url_for("main.index"))

    user = User.query.filter_by(uuid=user_uuid).first()
    if not user:
        flash("User not found.", "warning")
        return redirect(url_for("dashboard.users"))

    if request.method != "POST":
        flash("Invalid request method.", "warning")
        return redirect(url_for("dashboard.users"))

    if not request.form.get("access_level"):
        flash("No access level provided.", "warning")
        return redirect(url_for("dashboard.index"))

    access_level = int(request.form.get("access_level"))

    if access_level not in [0, 1, 2, 3, 4]:
        flash("Invalid access level provided.", "warning")
        return redirect(url_for("dashboard.index"))

    if access_level >= current_user.access_level and current_user.access_level != 4:
        flash(
            "You cannot set a user's access level to be equal to or higher than your own.",
            "warning",
        )
        return redirect(url_for("dashboard.users"))

    if (
        user.access_level >= current_user.access_level
        and current_user.access_level != 4
    ):
        flash(
            "You cannot change a user's access level with an access level equal to or higher than your own.",
            "warning",
        )
        return redirect(url_for("dashboard.users"))

    old_access_level = user.access_level
    user.access_level = access_level
    db.session.commit()
    flash(
        f"Changed {user.first_name} {user.last_name}'s access level from {ACCESS_LEVELS[old_access_level]['name']} to {ACCESS_LEVELS[access_level]['name']}.",
        "success",
    )
    return redirect(url_for("dashboard.users"))
