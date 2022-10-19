from datetime import datetime, timedelta
from re import A
from unicodedata import category

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from wtforms import Form, SubmitField, HiddenField
from flask_wtf import FlaskForm

from nebula.models import User, Comment, Course, CourseLevel, Question, Answer, Notification
from nebula import db

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@bp.route('/')
def index():
    if current_user.is_anonymous or current_user.access_level < 2:
        flash("You need to be a KLC or Cosmic Web Member to access this page.", 'warning')
        return redirect(url_for('main.index'))

    questions_for_review = Question.query.filter(Question.reviewed == 0).all()

    total_questions = Question.query.count()

    answers = len(Answer.query.all())
    answered_questions = len(
        Question.query.filter(Question.answers.any()).all())

    reviewed_questions = len(Question.query.filter(
        Question.reviewed != 0).all())
    approved_questions = len(Question.query.filter(
        Question.reviewed == 1).all())
    users = User.query.all()

    recent_user_count = len([1 if
                             (datetime.now() - user.created_at).days <= 30 else None for user in users])

    return render_template(
        'dashboard/index.html', questions_for_review=questions_for_review, total_questions=total_questions,
        recent_user_count=recent_user_count, reviewed_questions=reviewed_questions,
        answers=answers, answered_questions=answered_questions, approved_questions=approved_questions)


class QuestionReviewForm(FlaskForm):
    accept_submit_button = SubmitField('Accept')
    reject_submit_button = SubmitField('Reject')


@bp.route('/question/<question_uuid>', methods=['GET', 'POST'])
def question(question_uuid):
    question_review_form = QuestionReviewForm(request.form)
    question = Question.query.filter_by(uuid=question_uuid).first()
    if not question:
        flash("Question not found.", 'warning')
        return redirect(url_for('dashboard.index'))

    if request.method != 'POST':
        return render_template(
            'dashboard/question.html', question=question, question_review_form=question_review_form)

    # POST
    print(request.form)

    if current_user.is_anonymous or current_user.access_level < 2:
        flash(
            "You need to be a KLC or Cosmic Web Member to perform this action.", 'warning')
        return redirect(url_for('main.index'))

    if not question_review_form.validate():
        flash("Something went wrong with submitting your request.", 'warning')
        flash(question_review_form.errors, 'error')
        return redirect(url_for('dashboard.question', question_uuid=question_uuid))

    if question_review_form.accept_submit_button.data:
        question.reviewed = 1
        question.reviewed_by = current_user

        notification = Notification(
            content=f"Your question '{question.title}' has been approved and is now visible on the site.",
            user=question.user, category="success",
            link=url_for('question.question', question_uuid=question_uuid,
                         course_level_code=question.course.course_level.code, course_code=question.course.code),
            link_text="View Question")
        db.session.commit()
        flash("Question accepted.", 'success')
        return redirect(url_for('dashboard.index'))
    if question_review_form.reject_submit_button.data:
        question.reviewed = 2
        question.reviewed_by = current_user
        notification = Notification(
            content=f"Your question '{question.title}' has not been accepted will not be shown to other users.",
            category="info", user=question.user)
        db.session.commit()
        flash("Question rejected.", 'success')
        return redirect(url_for('dashboard.index'))


@bp.route('/users')
def users():
    if current_user.is_anonymous or current_user.access_level < 2:
        flash("You need to be a KLC or Cosmic Web Member to access this page.", 'warning')
        return redirect(url_for('main.index'))

    users = User.query.all()
    return render_template('dashboard/users.html', users=users)
