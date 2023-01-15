from flask import Blueprint, render_template

from nebula.models.course_level import CourseLevel
from nebula.routes.web import bp as web_bp

bp = Blueprint("main", __name__)

web_bp.register_blueprint(bp)


@bp.route("/", defaults={"path": ""})
@bp.route("/<path:path>")
def index(path = None):
    return render_template("main/index.html")
