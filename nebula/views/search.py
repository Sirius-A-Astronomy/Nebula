from flask import Blueprint, render_template, request
from flask_login import current_user

from nebula.models import Course, Question, SubjectTag, User

bp = Blueprint("search", __name__)


@bp.route("/search")
def search():
    return render_template("main/search.html")
