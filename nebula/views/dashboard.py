from datetime import datetime, timedelta
from re import A

from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import func
from flask_login import login_required, current_user
from wtforms import Form, SubmitField, HiddenField
from flask_wtf import FlaskForm

from nebula.models import User, Comment, Course, CourseLevel, Question, Answer
from nebula import db

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@bp.route('/')
def index():
    if current_user.is_anonymous or current_user.access_level < 2:
        flash("You need to be a KLC or Cosmic Web Member to access this page.", 'warning')
        return redirect(url_for('main.index'))

    questions = Question.query.all()
    answers = len(Answer.query.all())
    answered_questions = len(
        Question.query.filter(Question.answers.any()).all())

    reviewed_questions = len(Question.query.filter(
        Question.reviewed != 0).all())
    users = User.query.all()

    recent_user_count = len([1 if
                             (datetime.now() - user.created_at).days <= 30 else None for user in users])

    print(recent_user_count)

    return render_template(
        'dashboard/index.html', questions=questions,
        recent_user_count=recent_user_count, reviewed_questions=reviewed_questions,
        answers=answers, answered_questions=answered_questions)


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
        db.session.commit()
        flash("Question accepted.", 'success')
        return redirect(url_for('dashboard.index'))
    if question_review_form.reject_submit_button.data:
        question.reviewed = 2
        question.reviewed_by = current_user
        db.session.commit()
        flash("Question rejected.", 'success')
        return redirect(url_for('dashboard.index'))
