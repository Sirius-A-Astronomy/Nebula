from flask import Blueprint, render_template, request
from flask_login import current_user

from nebula.models import Course, Question, SubjectTag, User
from nebula.routes.web import bp as web_bp

bp = Blueprint("search", __name__)

web_bp.register_blueprint(bp)


@bp.route("/search")
def search():
    return render_template("main/search.html")
