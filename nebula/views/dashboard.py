from datetime import datetime, timedelta
from re import A

from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import func
from flask_login import login_required, current_user

from nebula.models import User, Comment, Course, CourseLevel, Question
from nebula import db

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@bp.route('/')
def index():
    if current_user.is_anonymous and current_user.access_level < 2:
        flash("You need to be a KLC or Cosmic Web Member to access this page.", 'danger')
        return redirect(url_for('main.index'))

    questions = Question.query.all()
    users = User.query.all()

    recent_user_count = len([1 if
                             (datetime.now() - user.created_at).days <= 30 else None for user in users])

    print(recent_user_count)

    return render_template('dashboard/index.html', questions=questions, recent_user_count=recent_user_count)
