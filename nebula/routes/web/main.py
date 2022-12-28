from flask import Blueprint, render_template

from nebula.models import CourseLevel
from nebula.routes.web import bp as web_bp

bp = Blueprint("main", __name__)

web_bp.register_blueprint(bp)


@bp.route("/")
def index():
    bsc = CourseLevel.query.filter_by(study_type="Bachelor").all()
    msc = CourseLevel.query.filter_by(study_type="Master").all()
    return render_template("main/index.html", bsc_levels=bsc, msc_levels=msc)
