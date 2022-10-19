from flask import Blueprint, request, render_template
from flask_login import current_user

from nebula.models import Question, SubjectTag, User, Course

bp = Blueprint("search", __name__)


@bp.route("/search")
def search():
    return render_template("main/search.html")
